"""Zebra command-line interface.

Subcommands:
  scan    one-shot audit of a codebase (vulns + flaws + optimisations)
  watch   keep auditing on an interval / on file change
  md      convert documents to Markdown (via markitdown)
  tools   show which optional scanners are installed + install hints
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from types import SimpleNamespace
from typing import List

from . import __version__
from .util import C, ScanResult, have
from .scanners import secrets, quality, dependencies, sast
from . import report, docs

# Optional external tools Zebra knows how to drive, with install hints.
OPTIONAL_TOOLS = {
    "semgrep": "pip install semgrep",
    "bandit": "pip install bandit",
    "pip-audit": "pip install pip-audit",
    "ruff": "pip install ruff",
    "trivy": "brew install trivy",
    "gitleaks": "brew install gitleaks",
    "osv-scanner": "brew install osv-scanner",
    "npm": "ships with Node.js",
}


# --------------------------------------------------------------------------- #
def _run_scan(root: str, opts) -> List[ScanResult]:
    results: List[ScanResult] = []
    selected = opts.only
    def want(name): return (not selected) or name in selected

    if want("secrets"):
        results.append(secrets.scan(root, opts))
    if want("quality"):
        results.append(quality.scan(root, opts))
    if want("dependencies"):
        results.append(dependencies.scan(root, opts))
    if not opts.builtin_only:
        for r in sast.scan_all(root, opts):
            if want(r.scanner):
                results.append(r)
    return results


def _emit(root: str, results: List[ScanResult], opts) -> None:
    fmt = opts.format
    if fmt == "terminal":
        report.render_terminal(root, results, opts.max_rows)
        return
    text = {"md": report.render_markdown,
            "markdown": report.render_markdown,
            "json": report.render_json,
            "sarif": report.render_sarif}[fmt](root, results)
    if opts.output:
        with open(opts.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(C.green(f"Report written to {opts.output}"))
    else:
        print(text)


def _exit_code(results: List[ScanResult], fail_on: str) -> int:
    from .util import SEV_RANK
    if fail_on == "never":
        return 0
    threshold = SEV_RANK[fail_on]
    for r in results:
        for f in r.findings:
            if SEV_RANK.get(f.severity, 99) <= threshold:
                return 2
    return 0


# --------------------------------------------------------------------------- #
def cmd_scan(opts) -> int:
    root = os.path.abspath(opts.path)
    if not os.path.isdir(root):
        print(C.red(f"Not a directory: {root}"))
        return 1
    results = _run_scan(root, opts)
    _emit(root, results, opts)
    return _exit_code(results, opts.fail_on)


def cmd_watch(opts) -> int:
    root = os.path.abspath(opts.path)
    if not os.path.isdir(root):
        print(C.red(f"Not a directory: {root}"))
        return 1
    print(C.bold(f"🦓 Watching {root} every {opts.interval}s — Ctrl-C to stop"))
    prev_total = None
    try:
        while True:
            results = _run_scan(root, opts)
            total = sum(len(r.findings) for r in results)
            os.system("clear" if os.name != "nt" else "cls")
            report.render_terminal(root, results, opts.max_rows)
            if prev_total is not None and total != prev_total:
                delta = total - prev_total
                arrow = C.red(f"▲ +{delta}") if delta > 0 else C.green(f"▼ {delta}")
                print(C.bold(f"   Change since last scan: {arrow}"))
            prev_total = total
            time.sleep(opts.interval)
    except KeyboardInterrupt:
        print("\nStopped.")
        return 0


def cmd_md(opts) -> int:
    n = docs.convert(opts.files, opts.output_dir)
    print(C.green(f"\nConverted {n} file(s) to Markdown."))
    return 0 if n else 1


def cmd_tools(opts) -> int:
    print(C.bold("\nOptional scanners Zebra can use:\n"))
    for tool, hint in OPTIONAL_TOOLS.items():
        if have(tool):
            print(f"   {C.green('✓ installed'):>20}  {tool}")
        else:
            print(f"   {C.dim('– missing'):>20}  {tool:<14} {C.dim(hint)}")
    try:
        import markitdown  # noqa: F401
        print(f"   {C.green('✓ installed'):>20}  markitdown")
    except Exception:  # noqa: BLE001
        print(f"   {C.dim('– missing'):>20}  {'markitdown':<14} "
              f"{C.dim('pip install markitdown[all]')}")
    print(C.dim("\nZebra's built-in scanners (secrets, quality, dependency-flaws) "
                "always run with no install needed.\n"))
    return 0


# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="zebra",
        description="🦓 Monitor any codebase for vulnerabilities, flaws and optimisations.")
    p.add_argument("--version", action="version", version=f"zebra {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_scan_opts(sp):
        sp.add_argument("path", nargs="?", default=".", help="codebase root (default: .)")
        sp.add_argument("--only", nargs="*", default=[],
                        help="run only these scanners (secrets quality dependencies "
                             "semgrep bandit gitleaks ruff)")
        sp.add_argument("--builtin-only", action="store_true",
                        help="skip external tools; use Zebra's built-ins only")
        sp.add_argument("--ignore", nargs="*", default=[],
                        help="extra glob/dir patterns to ignore")
        sp.add_argument("--max-rows", type=int, default=25,
                        help="max findings shown per category in terminal output")

    sp = sub.add_parser("scan", help="one-shot audit")
    add_scan_opts(sp)
    sp.add_argument("--format", choices=["terminal", "md", "markdown", "json", "sarif"],
                    default="terminal")
    sp.add_argument("-o", "--output", help="write report to a file")
    sp.add_argument("--fail-on", choices=["never", "critical", "high", "medium", "low", "info"],
                    default="never", help="exit non-zero if a finding at/above this severity exists")
    sp.set_defaults(func=cmd_scan)

    sp = sub.add_parser("watch", help="continuously re-audit on an interval")
    add_scan_opts(sp)
    sp.add_argument("--interval", type=int, default=15, help="seconds between scans")
    sp.set_defaults(func=cmd_watch, format="terminal", output=None, fail_on="never")

    sp = sub.add_parser("md", help="convert documents to Markdown (markitdown)")
    sp.add_argument("files", nargs="+", help="files to convert (pdf, docx, pptx, xlsx, html, …)")
    sp.add_argument("-o", "--output-dir", help="write .md files here (default: print to stdout)")
    sp.set_defaults(func=cmd_md)

    sp = sub.add_parser("tools", help="show installed/optional scanners")
    sp.set_defaults(func=cmd_tools)
    return p


def main(argv=None) -> int:
    parser = build_parser()
    opts = parser.parse_args(argv)
    # ensure attrs exist for scanners regardless of subcommand
    for attr, default in (("only", []), ("ignore", []), ("builtin_only", False),
                          ("max_rows", 25)):
        if not hasattr(opts, attr):
            setattr(opts, attr, default)
    try:
        return opts.func(opts)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
