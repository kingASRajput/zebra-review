"""Hybrid PR code review: deterministic scanners (scoped to the diff) + an LLM pass.

Output is a code review — a short overview, a per-file summary table, and inline
comments anchored to changed lines — not Zebra's full vuln/flaw/optimisation
audit. See `zebra review` in the CLI.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from . import diff as gitdiff
from . import llm
from .scanners import secrets, quality, sast
from .util import SEV_RANK, rel


@dataclass
class ReviewComment:
    path: str
    line: int
    severity: str
    body: str
    source: str               # "claude" | "ruff" | "quality" | ...
    category: str = ""
    confidence: str = ""
    suggestion: str = ""      # one-line replacement for an autofix block

    def sort_key(self):
        return (self.path, self.line, SEV_RANK.get(self.severity, 99))


@dataclass
class Review:
    root: str
    overview_summary: str = ""
    file_descriptions: List[Tuple[str, str]] = field(default_factory=list)
    comments: List[ReviewComment] = field(default_factory=list)
    changed_files: List[gitdiff.FileDiff] = field(default_factory=list)
    verdict_decision: str = "comment"   # approve | request_changes | comment
    verdict_message: str = ""
    llm_status: str = ""          # "" means ran; otherwise the skip reason
    model: str = ""

    def by_file(self) -> Dict[str, List[ReviewComment]]:
        out: Dict[str, List[ReviewComment]] = {}
        for c in sorted(self.comments, key=lambda x: x.sort_key()):
            out.setdefault(c.path, []).append(c)
        return out


# --------------------------------------------------------------------------- #
# Deterministic pass — run the lint-y scanners, keep only changed lines
# --------------------------------------------------------------------------- #
_REVIEW_SOURCES = {"ruff", "quality", "quality-ast", "secrets", "bandit", "semgrep"}


def _deterministic_comments(root: str, opts,
                            changed: Dict[str, Set[int]]) -> List[ReviewComment]:
    results = [secrets.scan(root, opts), quality.scan(root, opts)]
    if not getattr(opts, "builtin_only", False):
        for r in sast.scan_all(root, opts):
            if r.scanner in ("ruff", "bandit", "semgrep"):
                results.append(r)

    out: List[ReviewComment] = []
    for res in results:
        for f in res.findings:
            if not f.file or f.line is None:
                continue
            allowed = changed.get(f.file)
            if allowed is None or f.line not in allowed:
                continue   # only comment on lines this PR actually touched
            body = f.detail or f.title
            out.append(ReviewComment(
                path=f.file, line=f.line, severity=f.severity,
                body=f"{f.title} — {body}" if f.detail else f.title,
                source=f.source, category=f.rule or "", confidence="high"))
    return out


def _dedupe(comments: List[ReviewComment]) -> List[ReviewComment]:
    """Drop near-duplicate comments on the same (path, line)."""
    seen: Set[Tuple[str, int, str]] = set()
    out: List[ReviewComment] = []
    for c in sorted(comments, key=lambda x: (x.sort_key(), 0 if x.source == "claude" else 1)):
        key = (c.path, c.line, c.category[:24] or c.body[:40].lower())
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
    return out


# --------------------------------------------------------------------------- #
def run_review(root: str, opts) -> Review:
    review = Review(root=root)
    if not gitdiff.is_git_repo(root):
        review.llm_status = "not a git repository — cannot compute a diff."
        return review

    diff_text = gitdiff.get_diff(root, getattr(opts, "base", None),
                                 getattr(opts, "head", None))
    files = gitdiff.parse_diff(diff_text)
    review.changed_files = files
    if not files:
        review.llm_status = "no changes to review."
        return review

    changed = gitdiff.changed_line_index(files)

    # 1. deterministic, scoped to the diff
    comments = _deterministic_comments(root, opts, changed)

    # 2. LLM pass (hybrid) unless disabled
    if not getattr(opts, "no_llm", False):
        model = getattr(opts, "model", llm.DEFAULT_MODEL) or llm.DEFAULT_MODEL
        result = llm.review_diff(diff_text, model=model)
        review.model = result.model
        if not result.available:
            review.llm_status = result.skipped_reason
        else:
            review.overview_summary = result.summary
            review.file_descriptions = result.file_descriptions
            review.verdict_decision = result.verdict_decision
            review.verdict_message = result.verdict_message
            min_conf = getattr(opts, "min_confidence", "low")
            conf_rank = {"high": 0, "medium": 1, "low": 2}
            thr = conf_rank.get(min_conf, 2)
            for c in result.comments:
                if conf_rank.get(c.get("confidence", "low"), 2) > thr:
                    continue
                path = c.get("path", "")
                line = c.get("line")
                if line is None or not path:
                    continue
                comments.append(ReviewComment(
                    path=path, line=int(line),
                    severity=c.get("severity", "low"),
                    body=c.get("comment", ""), source="claude",
                    category=c.get("category", ""),
                    confidence=c.get("confidence", ""),
                    suggestion=(c.get("suggestion") or "").rstrip("\n")))

    # severity floor
    floor = getattr(opts, "min_severity", "info")
    fthr = SEV_RANK.get(floor, 99)
    comments = [c for c in comments if SEV_RANK.get(c.severity, 99) <= fthr]

    review.comments = _dedupe(comments)

    # If the LLM didn't supply a verdict (skipped or disabled), derive one.
    if review.llm_status or not review.verdict_message:
        review.verdict_decision, review.verdict_message = _fallback_verdict(review.comments)
    return review


def _fallback_verdict(comments: List[ReviewComment]) -> Tuple[str, str]:
    """Deterministic verdict from comment severities when no LLM message exists."""
    if not comments:
        return "approve", "No issues found in the changed lines — looks good to merge."
    worst = min((SEV_RANK.get(c.severity, 99) for c in comments), default=99)
    n = len(comments)
    if worst <= SEV_RANK["high"]:
        return ("request_changes",
                f"{n} issue(s) found, including high-severity ones — please address "
                f"the flagged lines before merging.")
    if worst <= SEV_RANK["medium"]:
        return ("comment",
                f"{n} issue(s) worth reviewing before merge; none are blocking.")
    return ("approve",
            f"Only minor ({n}) low/info notes — fine to merge after a quick look.")
