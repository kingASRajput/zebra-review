# 🦓 Zebra — Usage Guide

Zebra audits any codebase for **security vulnerabilities**, **code flaws**, and
**optimisation opportunities**, and renders the result in whatever format you
need — including a polished, graphical **PDF/HTML** report with remediation
guidance for every finding.

It runs out of the box with **zero dependencies**. Heavier engines
(`semgrep`, `bandit`, `pip-audit`, `ruff`, `trivy`, `gitleaks`, `osv-scanner`)
are auto-detected and orchestrated when present.

---

## 1. Install

```bash
# Run straight from source (needs Python 3.8+; PDF/HTML need nothing extra):
python zebra.py scan .

# Or install the `zebra` command:
pip install -e .
pip install -e '.[all]'      # + markitdown and the optional scan engines
```

> **PDF export** needs a Chromium-based browser (Chrome, Edge, Chromium, or
> Brave) — Zebra finds it automatically. No browser? `pip install weasyprint`
> or `pip install xhtml2pdf` and Zebra will fall back to those.

Check what's available on your machine:

```bash
python zebra.py tools
```

---

## 2. The three lenses

| Lens | Examples of what it finds |
| --- | --- |
| 🔴 **Vulnerabilities** | committed private keys, AWS/GitHub/Stripe tokens, `eval`/`exec`, unsafe `pickle`, SQL/shell injection, disabled TLS, weak hashes, DOM XSS |
| 🟡 **Flaws** | bare/empty `except`, swallowed exceptions, mutable default args, over-long functions, too many params, leftover debug/TODO |
| 🟢 **Optimisations** | triple-nested loops (O(n³)), string-build in loops (O(n²)), `SELECT *` |

Every finding has a **severity**: `critical · high · medium · low · info`.

---

## 3. Scanning

```bash
zebra scan PATH                 # audit a directory (default: current dir)
```

### Output formats

```bash
zebra scan .                                   # colourised terminal (default)
zebra scan . --format md   -o report.md        # Markdown
zebra scan . --format json -o report.json      # machine-readable
zebra scan . --format sarif -o report.sarif    # GitHub code-scanning / CI
zebra scan . --format html -o report.html      # graphical, self-contained HTML
zebra scan . --format pdf  -o report.pdf       # graphical PDF (browser-rendered)
```

`html` and `pdf` are the **rich** formats. They include, for each finding type:

- a **What it is** description,
- a **Why it matters** risk explanation,
- a **How to fix** remediation, and
- a table of every location it occurs, plus summary cards and a severity chart.

If you omit `-o` with `--format pdf`, Zebra writes `zebra-report.pdf`. Parent
directories are created automatically.

### Selecting / limiting scanners

```bash
zebra scan . --builtin-only            # skip all external tools
zebra scan . --only secrets quality    # run just these scanners
zebra scan . --ignore "**/generated/**" dist   # extra ignore patterns
```

> **Tip — false positives.** Auto-generated files (e.g. GraphQL/ORM type files
> under `**/generated/**`) can trip the SQL-injection pattern. Exclude them with
> `--ignore "**/generated/**"` for a cleaner report.

### CI gate

```bash
zebra scan . --fail-on high            # exit code 2 if any high+ finding exists
```

```yaml
# .github/workflows/zebra.yml
- run: pip install -e '.[security]'
- run: zebra scan . --fail-on high --format sarif -o zebra.sarif
- uses: github/codeql-action/upload-sarif@v3
  with: { sarif_file: zebra.sarif }
```

---

## 4. Watch mode

Continuously re-audit while you work:

```bash
zebra watch .                  # re-scan every 15s, shows the delta each pass
zebra watch . --interval 30
```

---

## 5. Document → Markdown

```bash
zebra md report.pdf notes.docx -o ./markdown/   # convert docs to Markdown
zebra md page.html                              # print Markdown to stdout
```

Full document support (PDF/DOCX/PPTX/XLSX/images/audio) uses **markitdown** and
needs Python 3.10+. On 3.9 Zebra falls back to txt/md/html.

---

## 6. Generating a PDF — end to end

```bash
# 1. (optional) install deeper engines for real CVE + SAST coverage
pip install semgrep bandit pip-audit ruff

# 2. produce the graphical PDF
zebra scan ./my-project --format pdf -o reports/my-project-audit.pdf
```

Behind the scenes Zebra renders the HTML report and prints it to PDF with a
headless browser. Point it at a specific browser with:

```bash
ZEBRA_BROWSER="/path/to/chrome" zebra scan . --format pdf -o out.pdf
```

---

## 7. How it works

```
zebra/
├── cli.py              # argparse front-end: scan / watch / md / tools
├── util.py             # Finding model, file walking, tool detection
├── report.py           # terminal / markdown / json / sarif renderers
├── report_html.py      # graphical HTML + PDF renderer (browser print-to-pdf)
├── remediation.py      # rule → {what, why, fix} knowledge base
├── docs.py             # markitdown document → Markdown (with fallback)
└── scanners/
    ├── secrets.py      # regex + entropy secret detection
    ├── quality.py      # line rules + Python AST analysis
    ├── dependencies.py # pip-audit / npm audit / trivy + unpinned-dep check
    └── sast.py         # wrappers: semgrep, bandit, gitleaks, ruff
```

Each scanner returns a `ScanResult`. Missing tools are **skipped with an install
hint**, never fatal — so the report always renders.

---

## 8. Extending the remediation guidance

The advice in the HTML/PDF report comes from `zebra/remediation.py`, a dict
keyed by rule id (or finding title). To add or refine guidance for a rule:

```python
# zebra/remediation.py
REMEDIATION["my-rule-id"] = {
    "what": "One sentence on what the finding means.",
    "risk": "Why it matters / the impact.",
    "fix":  "Concrete steps to resolve it.",
    "refs": ["https://owasp.org/..."],   # optional
}
```

Anything without an entry falls back to a generic message, so the report never
shows a blank cell. Rule ids come from the scanners — secret rules use ids like
`private-key`, while the language-agnostic line rules use the finding title
(e.g. `"Possible SQL injection"`).

---

## 9. Command reference

| Command | Purpose |
| --- | --- |
| `zebra scan PATH` | one-shot audit |
| `zebra watch PATH` | continuous re-audit on an interval |
| `zebra md FILES…` | convert documents to Markdown |
| `zebra tools` | list installed/optional scanners |

| `scan` flag | Default | Meaning |
| --- | --- | --- |
| `--format` | `terminal` | `terminal · md · json · sarif · html · pdf` |
| `-o, --output` | — | write report to a file (dirs auto-created) |
| `--fail-on` | `never` | exit 2 if a finding at/above this severity exists |
| `--builtin-only` | off | skip external tools |
| `--only` | all | run only the named scanners |
| `--ignore` | — | extra glob/dir patterns to ignore |
| `--max-rows` | 25 | max findings per category in terminal output |

| Env var | Effect |
| --- | --- |
| `ZEBRA_BROWSER` | path to the browser used for PDF export |
| `NO_COLOR` | disable terminal colour |
