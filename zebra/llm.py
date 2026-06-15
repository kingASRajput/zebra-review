"""LLM-powered code review via Claude (the semantic half of the hybrid review).

Uses the official `anthropic` SDK, imported lazily so Zebra's core stays
dependency-free. If the SDK or an API key is missing, the caller falls back to
the deterministic scanners alone.

Defaults to claude-opus-4-8 with adaptive thinking and structured outputs.
Following Anthropic's 4.8 code-review guidance, the model is told to report
*every* finding with a confidence + severity so we can filter downstream rather
than have the model silently drop low-confidence bugs.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

DEFAULT_MODEL = "claude-opus-4-8"

SYSTEM_PROMPT = """\
You are a senior software engineer doing a focused **code review** of a pull \
request diff. This is a code review, not a security audit — comment the way a \
thoughtful human reviewer would on GitHub.

Focus on the changed (added) lines. Look for:
- Correctness bugs, logic errors, edge cases, off-by-one, null/undefined misuse
- API/contract mismatches (e.g. a docstring/JSDoc that disagrees with the code, \
wrong argument shapes, stale comments)
- Unused variables/imports, dead code, obvious lint violations
- Naming, readability, and small structural improvements that genuinely help
- Missing error handling or resource leaks
- Reuse opportunities and needless complexity

Do NOT:
- Re-explain what the code does
- Praise the code or add filler
- Flag pure style that a formatter would handle, unless it harms readability
- Comment on lines that were not changed unless a change clearly breaks them

Report EVERY issue you find, including low-confidence or low-severity ones — a \
downstream filter ranks them. For each finding give a confidence and severity so \
it can be ranked. Anchor each finding to the exact new-file line number shown in \
the diff. Write each comment in clear, specific prose (1-3 sentences), naming the \
symbol involved, like the best GitHub review comments.

Also produce a short PR overview: one or two sentences on what the PR does, then \
a one-line description per changed file."""

# JSON schema for structured output.
_SCHEMA = {
    "type": "object",
    "properties": {
        "overview": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "files": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["path", "description"],
                        "additionalProperties": False,
                    },
                },
            },
            "required": ["summary", "files"],
            "additionalProperties": False,
        },
        "comments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "path": {"type": "string"},
                    "line": {"type": "integer"},
                    "severity": {"type": "string",
                                 "enum": ["critical", "high", "medium", "low", "info"]},
                    "confidence": {"type": "string",
                                   "enum": ["high", "medium", "low"]},
                    "category": {"type": "string",
                                 "enum": ["bug", "correctness", "api-mismatch",
                                          "unused", "error-handling", "readability",
                                          "naming", "simplification", "other"]},
                    "comment": {"type": "string"},
                },
                "required": ["path", "line", "severity", "confidence",
                             "category", "comment"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["overview", "comments"],
    "additionalProperties": False,
}


@dataclass
class LLMReview:
    summary: str
    file_descriptions: List[Tuple[str, str]]   # (path, description)
    comments: List[dict]                        # raw comment dicts (schema above)
    available: bool = True
    skipped_reason: str = ""
    model: str = DEFAULT_MODEL


def available() -> Tuple[bool, str]:
    """(usable, reason-if-not)."""
    try:
        import anthropic  # noqa: F401
    except Exception:  # noqa: BLE001
        return False, ("anthropic SDK not installed — `pip install anthropic` "
                       "for the LLM review pass.")
    if not (os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")):
        return False, ("no ANTHROPIC_API_KEY set — export one to enable the LLM "
                       "review pass.")
    return True, ""


def _build_user_prompt(diff_text: str) -> str:
    return ("Here is the pull-request diff. Review the added lines and return your "
            "findings.\n\n```diff\n" + diff_text + "\n```")


def review_diff(diff_text: str, model: str = DEFAULT_MODEL,
                max_chars: int = 180_000) -> LLMReview:
    ok, reason = available()
    if not ok:
        return LLMReview("", [], [], available=False, skipped_reason=reason, model=model)

    import anthropic

    if len(diff_text) > max_chars:
        diff_text = diff_text[:max_chars] + "\n... (diff truncated for length) ...\n"

    client = anthropic.Anthropic()
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            output_config={
                "effort": "high",
                "format": {"type": "json_schema", "schema": _SCHEMA},
            },
            system=[{"type": "text", "text": SYSTEM_PROMPT,
                     "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": _build_user_prompt(diff_text)}],
        )
    except Exception as exc:  # noqa: BLE001
        return LLMReview("", [], [], available=False,
                         skipped_reason=f"Claude API error: {exc}", model=model)

    text = next((b.text for b in resp.content if b.type == "text"), "")
    try:
        data = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return LLMReview("", [], [], available=False,
                         skipped_reason="Could not parse model output as JSON.",
                         model=model)

    overview = data.get("overview", {}) or {}
    files = [(f.get("path", ""), f.get("description", ""))
             for f in overview.get("files", []) or []]
    return LLMReview(
        summary=overview.get("summary", ""),
        file_descriptions=files,
        comments=data.get("comments", []) or [],
        model=model,
    )
