"""Wrappers around best-in-class external SAST / secret tools.

Each returns a ScanResult; when the tool is absent the result is marked
unavailable with an install hint rather than failing the whole run.
"""
from __future__ import annotations

import json
from typing import List

from ..util import (CAT_FLAW, CAT_VULN, Finding, ScanResult, have, rel, run)


def _semgrep(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="semgrep")
    if not have("semgrep"):
        res.available = False
        res.skipped_reason = "semgrep not installed — `pip install semgrep` (deep multi-language SAST)."
        return res
    try:
        cp = run(["semgrep", "--config", "auto", "--json", "--quiet", root], timeout=600)
        data = json.loads(cp.stdout or "{}")
    except Exception as e:  # noqa: BLE001
        res.error = f"semgrep failed: {e}"
        return res
    sev_map = {"ERROR": "high", "WARNING": "medium", "INFO": "low"}
    for r in data.get("results", []):
        extra = r.get("extra", {})
        sev = sev_map.get(extra.get("severity", "WARNING"), "medium")
        res.findings.append(Finding(
            category=CAT_VULN, severity=sev,
            title=r.get("check_id", "semgrep finding").split(".")[-1],
            detail=(extra.get("message") or "")[:240],
            file=rel(r.get("path"), root),
            line=(r.get("start") or {}).get("line"),
            rule=r.get("check_id"), source="semgrep"))
    return res


def _bandit(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="bandit")
    if not have("bandit"):
        res.available = False
        res.skipped_reason = "bandit not installed — `pip install bandit` (Python security linter)."
        return res
    try:
        cp = run(["bandit", "-r", "-f", "json", "-q", root], timeout=300)
        data = json.loads(cp.stdout or "{}")
    except Exception as e:  # noqa: BLE001
        res.error = f"bandit failed: {e}"
        return res
    sev_map = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
    for r in data.get("results", []):
        res.findings.append(Finding(
            category=CAT_VULN,
            severity=sev_map.get(r.get("issue_severity", "LOW"), "low"),
            title=r.get("test_name", "bandit issue"),
            detail=(r.get("issue_text") or "")[:240],
            file=rel(r.get("filename"), root), line=r.get("line_number"),
            rule=r.get("test_id"), source="bandit"))
    return res


def _gitleaks(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="gitleaks")
    if not have("gitleaks"):
        res.available = False
        res.skipped_reason = "gitleaks not installed — `brew install gitleaks` (git-history secret scan)."
        return res
    try:
        cp = run(["gitleaks", "detect", "--no-banner", "--report-format", "json",
                  "--report-path", "/dev/stdout", "-s", root], timeout=300)
        data = json.loads(cp.stdout or "[]")
    except Exception as e:  # noqa: BLE001
        res.error = f"gitleaks failed: {e}"
        return res
    for r in (data or []):
        res.findings.append(Finding(
            category=CAT_VULN, severity="high",
            title=f"Secret leaked: {r.get('RuleID')}",
            detail=(r.get("Description") or "")[:200],
            file=rel(r.get("File"), root), line=r.get("StartLine"),
            rule=r.get("RuleID"), source="gitleaks"))
    return res


def _ruff(root: str, opts) -> ScanResult:
    """Ruff surfaces correctness flaws + perf lints (the optimisation angle)."""
    res = ScanResult(scanner="ruff")
    if not have("ruff"):
        res.available = False
        res.skipped_reason = "ruff not installed — `pip install ruff` (fast Python linter, incl. perf rules)."
        return res
    try:
        cp = run(["ruff", "check", "--output-format", "json", root], timeout=200)
        data = json.loads(cp.stdout or "[]")
    except Exception as e:  # noqa: BLE001
        res.error = f"ruff failed: {e}"
        return res
    for r in (data or []):
        code = r.get("code") or ""
        cat = CAT_VULN if code.startswith("S") else CAT_FLAW
        res.findings.append(Finding(
            category=cat, severity="low",
            title=f"{code}: {(r.get('message') or '')[:80]}",
            detail=r.get("message", ""),
            file=rel(r.get("filename"), root),
            line=(r.get("location") or {}).get("row"),
            rule=code, source="ruff"))
    return res


def scan_all(root: str, opts) -> List[ScanResult]:
    return [_semgrep(root, opts), _bandit(root, opts),
            _gitleaks(root, opts), _ruff(root, opts)]
