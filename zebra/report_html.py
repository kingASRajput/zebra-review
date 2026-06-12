"""Rich graphical HTML report (also the source for PDF export).

Produces a self-contained HTML document — no external CSS/JS/fonts — so it
renders identically offline and converts cleanly to PDF via a headless browser.
Findings are grouped by category and then by rule, and each rule group carries
its remediation guidance (what / why it matters / how to fix) from
``zebra.remediation`` followed by a table of every location it was found.
"""
from __future__ import annotations

import html
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from .remediation import lookup
from .report import CAT_LABEL, CAT_ORDER, _all_findings, severity_counts
from .util import Finding, ScanResult, SEVERITIES

# Palette — severity -> (text/badge colour, soft background)
SEV_STYLE = {
    "critical": ("#b91c1c", "#fee2e2"),
    "high":     ("#c2410c", "#ffedd5"),
    "medium":   ("#a16207", "#fef9c3"),
    "low":      ("#1d4ed8", "#dbeafe"),
    "info":     ("#475569", "#e2e8f0"),
}
CAT_ACCENT = {
    "vulnerability": "#dc2626",
    "flaw":          "#d97706",
    "optimisation":  "#059669",
}


def _esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def _badge(sev: str) -> str:
    fg, bg = SEV_STYLE.get(sev, ("#475569", "#e2e8f0"))
    return (f'<span class="badge" style="color:{fg};background:{bg}">'
            f'{_esc(sev)}</span>')


def _summary_cards(counts: Counter, total: int) -> str:
    cards = [f'<div class="card total"><div class="num">{total}</div>'
             f'<div class="lbl">total findings</div></div>']
    for s in SEVERITIES:
        n = counts.get(s, 0)
        fg, bg = SEV_STYLE[s]
        cards.append(
            f'<div class="card" style="background:{bg}">'
            f'<div class="num" style="color:{fg}">{n}</div>'
            f'<div class="lbl" style="color:{fg}">{s}</div></div>')
    return f'<div class="cards">{"".join(cards)}</div>'


def _severity_bar(counts: Counter, total: int) -> str:
    if not total:
        return ""
    segs = []
    for s in SEVERITIES:
        n = counts.get(s, 0)
        if not n:
            continue
        pct = n / total * 100
        fg, _ = SEV_STYLE[s]
        segs.append(f'<div class="seg" style="width:{pct:.2f}%;background:{fg}" '
                    f'title="{s}: {n}"></div>')
    legend = "  ".join(
        f'<span class="lg"><i style="background:{SEV_STYLE[s][0]}"></i>'
        f'{s} ({counts.get(s,0)})</span>'
        for s in SEVERITIES if counts.get(s))
    return (f'<div class="bar">{"".join(segs)}</div>'
            f'<div class="legend">{legend}</div>')


def _scanner_table(results: List[ScanResult]) -> str:
    rows = []
    for r in sorted(results, key=lambda x: x.scanner):
        if r.available and not r.error:
            status, cls = "ran", "ok"
        elif r.error:
            status, cls = f"error — {_esc(r.error)}", "err"
        else:
            status, cls = f"skipped — {_esc(r.skipped_reason)}", "skip"
        rows.append(f'<tr><td><code>{_esc(r.scanner)}</code></td>'
                    f'<td class="{cls}">{status}</td>'
                    f'<td class="n">{len(r.findings)}</td></tr>')
    return ('<table class="scanners"><thead><tr><th>Scanner</th><th>Status</th>'
            f'<th>Findings</th></tr></thead><tbody>{"".join(rows)}</tbody></table>')


def _rule_group(title: str, sev: str, group: List[Finding]) -> str:
    rem = lookup(group[0].rule, title)
    refs = ""
    if rem.get("refs"):
        links = " · ".join(f'<a href="{_esc(u)}">{_esc(u)}</a>'
                           for u in rem["refs"])
        refs = f'<div class="refs">Further reading: {links}</div>'
    locs = "".join(
        f'<tr><td class="loc"><code>{_esc(f.location())}</code></td>'
        f'<td class="src">{_esc(f.source)}</td>'
        f'<td>{_esc(f.detail or "")}</td></tr>'
        for f in group)
    return f"""
    <div class="rule">
      <div class="rule-head">
        {_badge(sev)}
        <h3>{_esc(title)}</h3>
        <span class="count">{len(group)} occurrence{'s' if len(group) != 1 else ''}</span>
      </div>
      <div class="remedy">
        <p><b>What it is.</b> {_esc(rem.get('what',''))}</p>
        <p><b>Why it matters.</b> {_esc(rem.get('risk',''))}</p>
        <p class="fix"><b>How to fix.</b> {_esc(rem.get('fix',''))}</p>
        {refs}
      </div>
      <table class="locs"><thead><tr><th>Location</th><th>Source</th><th>Detail</th></tr></thead>
      <tbody>{locs}</tbody></table>
    </div>"""


def _category_section(cat: str, findings: List[Finding]) -> str:
    by_rule: Dict[str, List[Finding]] = defaultdict(list)
    for f in findings:
        by_rule[f.title].append(f)
    # order rule groups by worst severity, then by count desc
    from .util import SEV_RANK
    ordered = sorted(by_rule.items(),
                     key=lambda kv: (min(SEV_RANK.get(f.severity, 99) for f in kv[1]),
                                     -len(kv[1])))
    blocks = "".join(_rule_group(title, grp[0].severity, grp)
                     for title, grp in ordered)
    accent = CAT_ACCENT.get(cat, "#334155")
    return f"""
    <section class="cat" style="--accent:{accent}">
      <h2>{_esc(CAT_LABEL[cat])} <span class="cat-n">{len(findings)}</span></h2>
      {blocks}
    </section>"""


CSS = """
* { box-sizing: border-box; }
body { font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #0f172a; margin: 0; line-height: 1.5; background: #f8fafc; }
.wrap { max-width: 960px; margin: 0 auto; padding: 32px 28px 64px; }
header.top { border-bottom: 3px solid #0f172a; padding-bottom: 16px; margin-bottom: 24px; }
header.top h1 { margin: 0 0 4px; font-size: 28px; }
header.top .meta { color: #475569; font-size: 13px; }
header.top .meta code { background: #e2e8f0; padding: 1px 6px; border-radius: 4px; }
h2 { font-size: 20px; margin: 36px 0 12px; padding-left: 12px;
  border-left: 5px solid var(--accent, #0f172a); }
.cat-n, .count { color: #64748b; font-weight: 500; font-size: 14px; }
.cards { display: flex; gap: 10px; flex-wrap: wrap; margin: 18px 0; }
.card { flex: 1 1 0; min-width: 92px; background: #fff; border: 1px solid #e2e8f0;
  border-radius: 10px; padding: 14px 10px; text-align: center; }
.card.total { background: #0f172a; }
.card.total .num, .card.total .lbl { color: #fff; }
.card .num { font-size: 26px; font-weight: 700; }
.card .lbl { font-size: 11px; text-transform: uppercase; letter-spacing: .04em; }
.bar { display: flex; height: 16px; border-radius: 8px; overflow: hidden; margin: 14px 0 8px; }
.bar .seg { height: 100%; }
.legend { font-size: 12px; color: #475569; }
.legend .lg { margin-right: 14px; white-space: nowrap; }
.legend i { display: inline-block; width: 10px; height: 10px; border-radius: 2px;
  margin-right: 4px; vertical-align: middle; }
.badge { display: inline-block; font-size: 11px; font-weight: 700; text-transform: uppercase;
  letter-spacing: .03em; padding: 2px 8px; border-radius: 20px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td { text-align: left; padding: 7px 9px; border-bottom: 1px solid #e2e8f0;
  vertical-align: top; }
th { background: #f1f5f9; font-size: 11px; text-transform: uppercase; letter-spacing: .04em;
  color: #475569; }
code { font-family: "SF Mono", "Cascadia Code", Consolas, monospace; font-size: 12px; }
.scanners td.ok { color: #047857; } .scanners td.skip { color: #64748b; }
.scanners td.err { color: #b91c1c; } .scanners td.n, td.n { text-align: right; }
.rule { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
  padding: 16px 18px; margin: 14px 0; page-break-inside: avoid; }
.rule-head { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.rule-head h3 { margin: 0; font-size: 16px; flex: 1; }
.remedy { font-size: 13.5px; background: #f8fafc; border: 1px solid #eef2f7;
  border-radius: 8px; padding: 10px 14px; margin-bottom: 10px; }
.remedy p { margin: 4px 0; }
.remedy .fix { color: #065f46; }
.remedy b { color: #0f172a; }
.refs { font-size: 12px; margin-top: 6px; }
.refs a { color: #2563eb; word-break: break-all; }
.locs td.loc { width: 48%; } .locs td.src { color: #64748b; white-space: nowrap; }
.note { background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
  padding: 10px 14px; font-size: 13px; margin: 16px 0; }
footer { margin-top: 40px; padding-top: 14px; border-top: 1px solid #e2e8f0;
  color: #94a3b8; font-size: 12px; }
@page { size: A4; margin: 14mm; }
@media print { body { background: #fff; } .wrap { max-width: none; padding: 0; }
  .rule, .card { box-shadow: none; } }
"""


def render_html(root: str, results: List[ScanResult]) -> str:
    findings = _all_findings(results)
    counts = severity_counts(findings)
    total = len(findings)
    by_cat: Dict[str, List[Finding]] = defaultdict(list)
    for f in findings:
        by_cat[f.category].append(f)

    sections = "".join(_category_section(cat, by_cat[cat])
                       for cat in CAT_ORDER if by_cat.get(cat))
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")

    empty = '<div class="note">No findings — clean scan. 🎉</div>' if not total else ""

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Zebra audit — {_esc(root)}</title>
<style>{CSS}</style></head>
<body><div class="wrap">
  <header class="top">
    <h1>🦓 Zebra Audit Report</h1>
    <div class="meta">Target <code>{_esc(root)}</code> &nbsp;·&nbsp; Generated {generated}
      &nbsp;·&nbsp; {total} findings</div>
  </header>

  <h2 style="--accent:#0f172a">Summary</h2>
  {_summary_cards(counts, total)}
  {_severity_bar(counts, total)}

  <h2 style="--accent:#0f172a">Scanner coverage</h2>
  {_scanner_table(results)}

  {empty}
  {sections}

  <footer>Generated by 🦓 Zebra · remediation guidance is advisory — review each
  finding in context. Auto-generated files (e.g. <code>**/generated/**</code>) may
  produce pattern false positives.</footer>
</div></body></html>"""


# --------------------------------------------------------------------------- #
# PDF export — render the HTML above with a headless browser (zero pip deps).
# Falls back to weasyprint / xhtml2pdf if a browser is not found.
# --------------------------------------------------------------------------- #
def _find_browser() -> Optional[str]:
    # explicit override wins
    env = os.environ.get("ZEBRA_BROWSER")
    if env and os.path.exists(env):
        return env
    names = ["chrome", "chromium", "chromium-browser", "google-chrome",
             "google-chrome-stable", "msedge", "microsoft-edge", "brave",
             "brave-browser"]
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    # common install paths by platform
    candidates: List[str] = []
    if sys.platform.startswith("win"):
        pf = os.environ.get("ProgramFiles", r"C:\Program Files")
        pfx86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local = os.environ.get("LOCALAPPDATA", "")
        for base in (pf, pfx86, local):
            if not base:
                continue
            candidates += [
                os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"),
                os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"),
                os.path.join(base, "BraveSoftware", "Brave-Browser",
                             "Application", "brave.exe"),
            ]
    elif sys.platform == "darwin":
        candidates += [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
    else:
        candidates += ["/usr/bin/google-chrome", "/usr/bin/chromium",
                       "/usr/bin/chromium-browser", "/usr/bin/microsoft-edge",
                       "/snap/bin/chromium"]
    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def _browser_to_pdf(browser: str, html_str: str, out_path: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "report.html")
        with open(src, "w", encoding="utf-8") as fh:
            fh.write(html_str)
        out_abs = os.path.abspath(out_path)
        uri = "file:///" + os.path.abspath(src).replace(os.sep, "/").lstrip("/")
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--no-pdf-header-footer",
               f"--user-data-dir={os.path.join(tmp, 'profile')}",
               f"--print-to-pdf={out_abs}", uri]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not os.path.exists(out_abs) or os.path.getsize(out_abs) == 0:
            # older Chrome/Edge: retry with legacy headless + header flag
            cmd[1] = "--headless"
            cmd[4] = "--print-to-pdf-no-header"
            subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if not os.path.exists(out_abs) or os.path.getsize(out_abs) == 0:
            raise RuntimeError(
                f"headless browser produced no PDF (exit {proc.returncode}): "
                f"{proc.stderr.strip()[:300]}")


def render_pdf(root: str, results: List[ScanResult], out_path: str) -> str:
    """Write a PDF report to *out_path*. Returns the engine used."""
    html_str = render_html(root, results)
    browser = _find_browser()
    if browser:
        _browser_to_pdf(browser, html_str, out_path)
        return f"headless browser ({os.path.basename(browser)})"
    # fallbacks (optional installs)
    try:
        from weasyprint import HTML  # type: ignore
        HTML(string=html_str).write_pdf(out_path)
        return "weasyprint"
    except Exception:  # noqa: BLE001
        pass
    try:
        from xhtml2pdf import pisa  # type: ignore
        with open(out_path, "wb") as fh:
            pisa.CreatePDF(html_str, dest=fh)
        return "xhtml2pdf"
    except Exception:  # noqa: BLE001
        pass
    raise RuntimeError(
        "No PDF engine available. Install Chrome/Edge/Chromium (auto-detected), "
        "or `pip install weasyprint` / `pip install xhtml2pdf`. "
        "Tip: set ZEBRA_BROWSER=/path/to/chrome to point Zebra at a browser.")
