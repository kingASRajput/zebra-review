"""Render scan results to terminal, Markdown, JSON or SARIF."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime
from typing import List

from .util import (CAT_FLAW, CAT_OPT, CAT_VULN, C, Finding, SEV_COLOR,
                   SEV_RANK, SEVERITIES, ScanResult)

CAT_LABEL = {CAT_VULN: "Security vulnerabilities",
             CAT_FLAW: "Code flaws",
             CAT_OPT: "Optimisations"}
CAT_ORDER = [CAT_VULN, CAT_FLAW, CAT_OPT]


def _all_findings(results: List[ScanResult]) -> List[Finding]:
    out: List[Finding] = []
    for r in results:
        out.extend(r.findings)
    out.sort(key=lambda f: f.sort_key())
    return out


def severity_counts(findings: List[Finding]) -> Counter:
    return Counter(f.severity for f in findings)


# --------------------------------------------------------------------------- #
def render_terminal(root: str, results: List[ScanResult], max_rows: int) -> None:
    findings = _all_findings(results)
    print(C.bold(f"\n🦓  Zebra audit — {root}"))
    print(C.dim(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"))

    # scanner status line
    for r in sorted(results, key=lambda x: x.scanner):
        if r.available and not r.error:
            tag = C.green("ok")
            print(f"   {tag:>14}  {r.scanner:<14} {len(r.findings)} finding(s)")
        elif r.error:
            print(f"   {C.red('error'):>14}  {r.scanner:<14} {C.dim(r.error)}")
        else:
            print(f"   {C.dim('skipped'):>14}  {r.scanner:<14} {C.dim(r.skipped_reason)}")

    counts = severity_counts(findings)
    summary = "  ".join(
        SEV_COLOR[s](f"{s}:{counts.get(s, 0)}") for s in SEVERITIES if counts.get(s)
    ) or C.green("no issues found")
    print(C.bold(f"\n   Summary: {summary}   (total {len(findings)})\n"))

    by_cat = defaultdict(list)
    for f in findings:
        by_cat[f.category].append(f)

    for cat in CAT_ORDER:
        group = by_cat.get(cat, [])
        if not group:
            continue
        print(C.bold(C.cyan(f"\n▌ {CAT_LABEL[cat]}  ({len(group)})")))
        for f in group[:max_rows]:
            sev = SEV_COLOR[f.severity](f"{f.severity:<8}")
            loc = C.dim(f.location())
            print(f"   {sev} {f.title}")
            print(f"            {loc}  {C.dim('[' + f.source + ']')}")
            if f.detail:
                print(f"            {C.dim(f.detail)}")
        if len(group) > max_rows:
            print(C.dim(f"   … and {len(group) - max_rows} more "
                        f"(use --format md -o report.md for the full list)"))
    print()


# --------------------------------------------------------------------------- #
def render_markdown(root: str, results: List[ScanResult]) -> str:
    findings = _all_findings(results)
    counts = severity_counts(findings)
    lines = [f"# 🦓 Zebra audit report",
             "",
             f"**Target:** `{root}`  ",
             f"**Generated:** {datetime.now().isoformat(timespec='seconds')}  ",
             f"**Total findings:** {len(findings)}",
             "",
             "## Summary",
             "",
             "| Severity | Count |",
             "| --- | --- |"]
    for s in SEVERITIES:
        if counts.get(s):
            lines.append(f"| {s} | {counts[s]} |")
    lines += ["", "### Scanner status", "",
              "| Scanner | Status | Findings |", "| --- | --- | --- |"]
    for r in sorted(results, key=lambda x: x.scanner):
        status = "✅ ran" if (r.available and not r.error) else (
            f"⚠️ {r.error}" if r.error else f"⏭️ skipped — {r.skipped_reason}")
        lines.append(f"| {r.scanner} | {status} | {len(r.findings)} |")

    by_cat = defaultdict(list)
    for f in findings:
        by_cat[f.category].append(f)
    for cat in CAT_ORDER:
        group = by_cat.get(cat, [])
        if not group:
            continue
        lines += ["", f"## {CAT_LABEL[cat]} ({len(group)})", "",
                  "| Severity | Title | Location | Source | Detail |",
                  "| --- | --- | --- | --- | --- |"]
        for f in group:
            detail = (f.detail or "").replace("|", "\\|")
            lines.append(f"| {f.severity} | {f.title} | `{f.location()}` | "
                         f"{f.source} | {detail} |")
    lines.append("")
    return "\n".join(lines)


def render_json(root: str, results: List[ScanResult]) -> str:
    findings = _all_findings(results)
    payload = {
        "target": root,
        "generated": datetime.now().isoformat(timespec="seconds"),
        "summary": dict(severity_counts(findings)),
        "scanners": [{"name": r.scanner, "available": r.available,
                      "skipped_reason": r.skipped_reason, "error": r.error,
                      "count": len(r.findings)} for r in results],
        "findings": [vars(f) for f in findings],
    }
    return json.dumps(payload, indent=2)


def render_sarif(root: str, results: List[ScanResult]) -> str:
    """Minimal SARIF 2.1.0 so CI / GitHub code-scanning can ingest results."""
    findings = _all_findings(results)
    sev_to_level = {"critical": "error", "high": "error", "medium": "warning",
                    "low": "note", "info": "note"}
    sarif_results = []
    rules = {}
    for f in findings:
        rid = f.rule or f.title
        rules.setdefault(rid, {"id": rid, "name": f.title,
                               "shortDescription": {"text": f.title}})
        res = {"ruleId": rid, "level": sev_to_level.get(f.severity, "warning"),
               "message": {"text": f.detail or f.title}}
        if f.file:
            res["locations"] = [{"physicalLocation": {
                "artifactLocation": {"uri": f.file},
                "region": {"startLine": f.line or 1}}}]
        sarif_results.append(res)
    sarif = {"version": "2.1.0",
             "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
             "runs": [{"tool": {"driver": {"name": "Zebra", "version": "0.1.0",
                                           "rules": list(rules.values())}},
                       "results": sarif_results}]}
    return json.dumps(sarif, indent=2)
