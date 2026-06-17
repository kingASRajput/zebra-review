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


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent:
        os.makedirs(parent, exist_ok=True)


def _emit(root: str, results: List[ScanResult], opts) -> None:
    fmt = opts.format
    if fmt == "terminal":
        report.render_terminal(root, results, opts.max_rows)
        return
    if opts.output:
        _ensure_parent(opts.output)
    if fmt == "pdf":
        from . import report_html
        out = opts.output or "zebra-report.pdf"
        _ensure_parent(out)
        try:
            engine = report_html.render_pdf(root, results, out)
        except Exception as exc:  # noqa: BLE001
            print(C.red(f"PDF export failed: {exc}"))
            return
        print(C.green(f"PDF report written to {out}  ({engine})"))
        return
    if fmt == "html":
        from . import report_html
        text = report_html.render_html(root, results)
    else:
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


def cmd_pr_comment(opts) -> int:
    from . import github as gh
    root = os.path.abspath(opts.path)
    if not os.path.isdir(root):
        print(C.red(f"Not a directory: {root}"))
        return 1
    repo = gh.resolve_repo(opts.repo)
    token = gh.resolve_token(opts.token)
    pr = gh.resolve_pr(opts.pr)
    sha = gh.resolve_sha(opts.sha)

    results = _run_scan(root, opts)
    body = gh.render_pr_comment(root, results, repo=repo, sha=sha,
                                max_findings=opts.max_findings,
                                comment_threshold=opts.comment_threshold)

    if opts.dry_run:
        print(body)
    else:
        missing = [n for n, v in (("--repo/GITHUB_REPOSITORY", repo),
                                  ("--pr/GITHUB_REF", pr),
                                  ("--token/GITHUB_TOKEN", token)) if not v]
        if missing:
            print(C.red(f"Cannot post: missing {', '.join(missing)}. "
                        f"Use --dry-run to preview."))
            return 1
        try:
            result = gh.post_or_update_comment(repo, pr, token, body)
        except Exception as exc:  # noqa: BLE001
            print(C.red(f"Failed to post PR comment: {exc}"))
            return 1
        print(C.green(f"PR #{pr}: {result}"))
    return _exit_code(results, opts.fail_on)


def cmd_review(opts) -> int:
    from . import review as rv
    from . import report_review as rr
    root = os.path.abspath(opts.path)
    if not os.path.isdir(root):
        print(C.red(f"Not a directory: {root}"))
        return 1

    result = rv.run_review(root, opts)

    # local output
    if opts.format == "md":
        text = rr.render_markdown(result)
        if opts.output:
            _ensure_parent(opts.output)
            with open(opts.output, "w", encoding="utf-8") as fh:
                fh.write(text)
            print(C.green(f"Review written to {opts.output}"))
        else:
            print(text)
    else:
        rr.render_terminal(result)

    # optional: post to a GitHub PR as a code review
    if opts.post or opts.dry_run:
        from . import github as gh
        # Body has the verdict + overview; suggestions live on the inline comments
        # (so GitHub renders the one-click "apply suggestion" autofix).
        body = rr.render_markdown(result, inline_suggestions=False)

        def _inline_body(c):
            txt = (f"{rr.SEV_EMOJI.get(c.severity, '')} **{c.severity}** "
                   f"({c.source}): {c.body}")
            if c.suggestion:
                txt += "\n\n```suggestion\n" + c.suggestion + "\n```"
            return txt

        inline = [{"path": c.path, "line": c.line, "body": _inline_body(c)}
                  for c in result.comments]
        if opts.dry_run:
            print(C.dim("\n--- would post this review body ---\n"))
            print(body)
            print(C.dim(f"\n(+ {len(inline)} inline comments)"))
        else:
            repo = gh.resolve_repo(opts.repo)
            pr = gh.resolve_pr(opts.pr)
            token = gh.resolve_token(opts.token)
            missing = [n for n, v in (("--repo", repo), ("--pr", pr),
                                      ("--token/GITHUB_TOKEN", token)) if not v]
            if missing:
                print(C.red(f"Cannot post: missing {', '.join(missing)}."))
                return 1
            try:
                msg = gh.post_review(repo, pr, token, body, inline)
            except Exception as exc:  # noqa: BLE001
                print(C.red(f"Failed to post review: {exc}"))
                return 1
            print(C.green(f"PR #{pr}: {msg}"))

    # exit code gate
    from .util import SEV_RANK
    if opts.fail_on != "never":
        thr = SEV_RANK[opts.fail_on]
        if any(SEV_RANK.get(c.severity, 99) <= thr for c in result.comments):
            return 2
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
    sp.add_argument("--format",
                    choices=["terminal", "md", "markdown", "json", "sarif",
                             "html", "pdf"],
                    default="terminal")
    sp.add_argument("-o", "--output", help="write report to a file")
    sp.add_argument("--fail-on", choices=["never", "critical", "high", "medium", "low", "info"],
                    default="never", help="exit non-zero if a finding at/above this severity exists")
    sp.set_defaults(func=cmd_scan)

    sp = sub.add_parser("watch", help="continuously re-audit on an interval")
    add_scan_opts(sp)
    sp.add_argument("--interval", type=int, default=15, help="seconds between scans")
    sp.set_defaults(func=cmd_watch, format="terminal", output=None, fail_on="never")

    sp = sub.add_parser("pr-comment",
                        help="scan and post a summary comment on a GitHub PR")
    add_scan_opts(sp)
    sp.add_argument("--repo", help="owner/name (default: $GITHUB_REPOSITORY)")
    sp.add_argument("--pr", type=int,
                    help="PR number (default: inferred from $GITHUB_REF / event)")
    sp.add_argument("--token", help="GitHub token (default: $GITHUB_TOKEN)")
    sp.add_argument("--sha", help="commit sha for file links (default: $GITHUB_SHA)")
    sp.add_argument("--comment-threshold",
                    choices=["critical", "high", "medium", "low", "info"],
                    default="info",
                    help="minimum severity to list in the comment (default: info)")
    sp.add_argument("--max-findings", type=int, default=30,
                    help="max findings listed in the comment (default: 30)")
    sp.add_argument("--fail-on",
                    choices=["never", "critical", "high", "medium", "low", "info"],
                    default="never",
                    help="exit non-zero if a finding at/above this severity exists")
    sp.add_argument("--dry-run", action="store_true",
                    help="print the comment instead of posting it")
    sp.set_defaults(func=cmd_pr_comment)

    sp = sub.add_parser("review",
                        help="code-review the current diff (hybrid: scanners + Claude)")
    sp.add_argument("path", nargs="?", default=".", help="repo root (default: .)")
    sp.add_argument("--base", help="base ref to diff against (default: merge-base with main)")
    sp.add_argument("--head", help="head ref (default: working tree)")
    sp.add_argument("--model", default="claude-opus-4-8",
                    help="Claude model for the LLM pass (default: claude-opus-4-8)")
    sp.add_argument("--no-llm", action="store_true",
                    help="deterministic scanners only; skip the Claude pass")
    sp.add_argument("--builtin-only", action="store_true",
                    help="skip external scanners (ruff/bandit/semgrep) in the deterministic pass")
    sp.add_argument("--min-severity", choices=["critical", "high", "medium", "low", "info"],
                    default="info", help="drop comments below this severity")
    sp.add_argument("--min-confidence", choices=["high", "medium", "low"],
                    default="low", help="drop LLM comments below this confidence")
    sp.add_argument("--format", choices=["terminal", "md"], default="terminal")
    sp.add_argument("-o", "--output", help="write the markdown review to a file")
    sp.add_argument("--post", action="store_true", help="post as a GitHub PR review")
    sp.add_argument("--dry-run", action="store_true", help="print what would be posted")
    sp.add_argument("--repo", help="owner/name (default: $GITHUB_REPOSITORY)")
    sp.add_argument("--pr", type=int, help="PR number (default: inferred from env)")
    sp.add_argument("--token", help="GitHub token (default: $GITHUB_TOKEN)")
    sp.add_argument("--fail-on", choices=["never", "critical", "high", "medium", "low", "info"],
                    default="never", help="exit 2 if a comment at/above this severity exists")
    sp.set_defaults(func=cmd_review)

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
