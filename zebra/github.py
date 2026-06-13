"""Post Zebra findings as a summary comment on a GitHub pull request.

Zero-dependency: talks to the GitHub REST API with urllib. Designed to run
inside GitHub Actions (reading repo / PR / token from the environment) but works
locally too when given --repo/--pr/--token.

Strategy: render one markdown summary comment and *upsert* it — the comment
carries a hidden marker so subsequent pushes update the same comment instead of
piling up duplicates.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import datetime
from typing import List, Optional, Tuple

from .report import CAT_LABEL, CAT_ORDER, _all_findings, severity_counts
from .util import Finding, ScanResult, SEVERITIES, SEV_RANK

MARKER = "<!-- zebra-pr-report -->"
API = "https://api.github.com"

SEV_EMOJI = {"critical": "🔴", "high": "🟠", "medium": "🟡",
             "low": "⚪", "info": "ℹ️"}


# --------------------------------------------------------------------------- #
# Environment resolution
# --------------------------------------------------------------------------- #
def resolve_repo(explicit: Optional[str]) -> Optional[str]:
    return explicit or os.environ.get("GITHUB_REPOSITORY")


def resolve_token(explicit: Optional[str]) -> Optional[str]:
    return (explicit or os.environ.get("GITHUB_TOKEN")
            or os.environ.get("GH_TOKEN"))


def resolve_pr(explicit: Optional[int]) -> Optional[int]:
    if explicit:
        return explicit
    # refs/pull/<n>/merge
    ref = os.environ.get("GITHUB_REF", "")
    parts = ref.split("/")
    if len(parts) >= 3 and parts[1] == "pull":
        try:
            return int(parts[2])
        except ValueError:
            pass
    # fall back to the event payload
    path = os.environ.get("GITHUB_EVENT_PATH")
    if path and os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as fh:
                evt = json.load(fh)
            for key in ("number",):
                if key in evt:
                    return int(evt[key])
            pr = evt.get("pull_request") or {}
            if "number" in pr:
                return int(pr["number"])
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    return None


def resolve_sha(explicit: Optional[str]) -> Optional[str]:
    return explicit or os.environ.get("GITHUB_SHA")


# --------------------------------------------------------------------------- #
# Comment rendering
# --------------------------------------------------------------------------- #
def _loc_link(f: Finding, repo: Optional[str], sha: Optional[str]) -> str:
    loc = f.location()
    if f.file and repo and sha:
        path = f.file.replace("\\", "/")  # URLs always use forward slashes
        anchor = f"#L{f.line}" if f.line else ""
        url = f"https://github.com/{repo}/blob/{sha}/{path}{anchor}"
        return f"[`{loc}`]({url})"
    return f"`{loc}`"


def _verdict(counts) -> str:
    if counts.get("critical") or counts.get("high"):
        return "🔴 **Action required** — critical/high findings present."
    if counts.get("medium"):
        return "🟡 **Review suggested** — medium findings present."
    if sum(counts.values()):
        return "🟢 **Looks OK** — only low/info findings."
    return "✅ **Clean** — no findings."


def render_pr_comment(root: str, results: List[ScanResult],
                      repo: Optional[str] = None, sha: Optional[str] = None,
                      max_findings: int = 30,
                      comment_threshold: str = "info") -> str:
    findings = _all_findings(results)
    counts = severity_counts(findings)
    total = len(findings)
    thr = SEV_RANK.get(comment_threshold, 99)
    shown = [f for f in findings if SEV_RANK.get(f.severity, 99) <= thr]

    lines = [MARKER,
             "## 🦓 Zebra audit",
             "",
             _verdict(counts),
             ""]

    # summary table
    lines += ["| Severity | Count |", "| --- | --- |"]
    for s in SEVERITIES:
        if counts.get(s):
            lines.append(f"| {SEV_EMOJI[s]} {s} | {counts[s]} |")
    lines.append(f"| **total** | **{total}** |")
    lines.append("")

    # scanner coverage (compact)
    ran = [r.scanner for r in results if r.available and not r.error]
    skipped = [r.scanner for r in results
               if not (r.available and not r.error)]
    cov = f"**Scanners:** ran `{', '.join(sorted(ran)) or 'none'}`"
    if skipped:
        cov += f" · skipped `{', '.join(sorted(skipped))}`"
    lines += [cov, ""]

    if not shown:
        lines += [f"_No findings at or above **{comment_threshold}**._", ""]
    else:
        by_cat = defaultdict(list)
        for f in shown:
            by_cat[f.category].append(f)
        budget = max_findings
        for cat in CAT_ORDER:
            grp = by_cat.get(cat, [])
            if not grp or budget <= 0:
                continue
            lines += [f"### {CAT_LABEL[cat]} ({len(grp)})", "",
                      "| Severity | Finding | Location |",
                      "| --- | --- | --- |"]
            for f in grp[:budget]:
                detail = (f.detail or "").replace("|", "\\|")
                lines.append(f"| {SEV_EMOJI.get(f.severity,'')} {f.severity} "
                             f"| {f.title} | {_loc_link(f, repo, sha)} |")
            remaining = len(grp) - min(len(grp), budget)
            if remaining > 0:
                lines.append(f"| | _…and {remaining} more_ | |")
            budget -= len(grp)
            lines.append("")

    when = datetime.now().strftime("%Y-%m-%d %H:%M UTC")
    lines += ["<sub>🦓 Generated by Zebra · "
              f"updates in place on each push · {when}</sub>"]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# REST helpers
# --------------------------------------------------------------------------- #
def _request(method: str, url: str, token: str,
             payload: Optional[dict] = None) -> Tuple[int, dict | list]:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("X-GitHub-Api-Version", "2022-11-28")
    req.add_header("User-Agent", "zebra-audit")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode()
            return resp.status, (json.loads(body) if body else {})
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        raise RuntimeError(f"GitHub API {method} {url} -> {e.code}: {body[:300]}")


def _find_existing(repo: str, pr: int, token: str) -> Optional[int]:
    page = 1
    while True:
        url = (f"{API}/repos/{repo}/issues/{pr}/comments"
               f"?per_page=100&page={page}")
        _, data = _request("GET", url, token)
        if not isinstance(data, list) or not data:
            return None
        for c in data:
            if MARKER in (c.get("body") or ""):
                return c.get("id")
        if len(data) < 100:
            return None
        page += 1


def post_or_update_comment(repo: str, pr: int, token: str, body: str,
                           dry_run: bool = False) -> str:
    """Upsert the Zebra comment. Returns a human-readable result string."""
    if dry_run:
        return "dry-run (not posted)"
    existing = _find_existing(repo, pr, token)
    if existing is not None:
        url = f"{API}/repos/{repo}/issues/comments/{existing}"
        _, res = _request("PATCH", url, token, {"body": body})
        return f"updated comment {res.get('html_url', existing)}"
    url = f"{API}/repos/{repo}/issues/{pr}/comments"
    _, res = _request("POST", url, token, {"body": body})
    return f"created comment {res.get('html_url', '')}"
