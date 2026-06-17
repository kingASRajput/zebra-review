# 🦓 Zebra

**Monitor any codebase for vulnerabilities, flaws and optimisations — and convert documents to Markdown.**

📖 **Full handbook:** [`docs/DOCUMENTATION.md`](docs/DOCUMENTATION.md) (benefits, workflows, every feature) · **Cheat-sheet:** [`docs/USAGE.md`](docs/USAGE.md)

Zebra runs out-of-the-box with **zero dependencies**. Its built-in scanners
(secrets, code-quality, dependency-flaws) always work. When heavier tools
(`semgrep`, `bandit`, `pip-audit`, `ruff`, `trivy`, `gitleaks`) are installed,
Zebra automatically detects and orchestrates them — one report, three lenses:

| Lens | What it finds |
| --- | --- |
| 🔴 **Vulnerabilities** | hard-coded secrets, AWS/GitHub/Stripe keys, `eval`/`exec`, unsafe `pickle`, SQL/shell injection, disabled TLS, weak hashes, CVEs in dependencies |
| 🟡 **Flaws** | bare/empty `except`, mutable default args, swallowed exceptions, over-long functions, too many params, leftover debug/TODO, unpinned deps |
| 🟢 **Optimisations** | triple-nested loops (O(n³)), string-build in loops (O(n²)), `SELECT *`, ruff perf lints |

---

## Install

```bash
# Core only (no dependencies):
python3 zebra.py scan .

# Or install as a command + optional engines:
pip install -e .                 # gives you the `zebra` command
pip install -e '.[all]'          # + markitdown, semgrep, bandit, pip-audit, ruff
```

> **markitdown note:** full document conversion (PDF/DOCX/PPTX/XLSX/images/audio)
> needs **Python 3.10+**. On 3.9 Zebra uses a built-in fallback for txt/md/html.

---

## Usage

```bash
zebra scan PATH                  # one-shot audit (defaults to current dir)
zebra scan . --format md -o report.md      # Markdown report
zebra scan . --format json -o out.json     # machine-readable
zebra scan . --format sarif -o out.sarif   # for GitHub code-scanning / CI
zebra scan . --format html -o report.html  # graphical report + fix guidance
zebra scan . --format pdf -o report.pdf    # graphical PDF (browser-rendered)
zebra scan . --fail-on high      # exit code 2 if any high+ finding (CI gate)
zebra scan . --builtin-only      # skip external tools
zebra scan . --only secrets quality        # run specific scanners

zebra watch .                    # continuously re-audit (default every 15s)
zebra watch . --interval 30

zebra md report.pdf notes.docx -o ./markdown/   # docs -> Markdown
zebra md page.html               # print Markdown to stdout

zebra tools                      # show which optional scanners are installed
```

### Code review (not audit)

`zebra review` is a **PR code review** — scoped to the diff, not the whole repo.
It is a *hybrid* of deterministic scanners (run on the changed lines only) and an
LLM pass (Claude) that catches the semantic stuff linters miss (API/docstring
mismatches, unused args, logic bugs). Output is Copilot-style:

- a **verdict** up front — `✅ Approve` / `🔧 Changes requested` / `💬 Comment`
  with a direct message telling you whether the changes are good to merge or what
  to fix and in which file;
- a short **Pull request overview** + **per-file summary**;
- **inline comments** anchored to changed lines, each with a severity; and
- **one-click autofix suggestions** (GitHub ` ```suggestion ` blocks) when a fix
  is mechanical.

```bash
zebra review                     # review working tree vs merge-base with main
zebra review --base origin/main --head HEAD
zebra review --no-llm            # deterministic scanners only (no API key needed)
zebra review --format md -o review.md
zebra review --post --repo owner/name --pr 42   # post as a GitHub PR review
zebra review --dry-run --pr 42   # preview what would be posted
zebra review --min-confidence medium --min-severity low   # filter the LLM findings
```

The LLM pass uses **`claude-opus-4-8`** (override with `--model`) with adaptive
thinking and structured outputs. It needs `pip install anthropic` and an
`ANTHROPIC_API_KEY`; without either, Zebra prints a hint and falls back to the
deterministic pass. (`zebra pr-comment` still posts the full *audit* summary —
use `zebra review` for a code review.)

### Output formats
`terminal` (default, colourised) · `md` · `json` · `sarif` · `html` · `pdf`

The **`html`** and **`pdf`** formats produce a graphical report: summary cards, a
severity distribution chart, and — for every finding type — a **What it is /
Why it matters / How to fix** block plus a table of all locations. PDF export
renders via an auto-detected Chromium browser (Chrome/Edge/Chromium/Brave) with
no extra install; `weasyprint`/`xhtml2pdf` are used as fallbacks if present.
See [`docs/USAGE.md`](docs/USAGE.md) for the full guide.

---

## How it works

```
zebra/
├── cli.py              # argparse front-end: scan / watch / md / tools
├── util.py             # Finding model, file walking, tool detection
├── report.py           # terminal / markdown / json / sarif renderers
├── report_html.py      # graphical HTML + PDF renderer (browser print-to-pdf)
├── report_review.py    # code-review renderer (terminal + GitHub markdown)
├── remediation.py      # rule → {what, why, fix} knowledge base
├── diff.py             # git diff acquisition + parsing (changed-line index)
├── llm.py              # Claude-powered review pass (anthropic SDK, lazy)
├── review.py           # hybrid PR review: scanners-on-diff + LLM
├── github.py           # PR comment + PR review posting (urllib)
├── docs.py             # markitdown document → Markdown (with fallback)
└── scanners/
    ├── secrets.py      # built-in regex + entropy secret detection
    ├── quality.py      # built-in line rules + Python AST analysis
    ├── dependencies.py # pip-audit / npm audit / trivy + unpinned-dep check
    └── sast.py         # wrappers: semgrep, bandit, gitleaks, ruff
```

Each scanner returns a `ScanResult`. Missing tools are *skipped with an install
hint*, never fatal — so the report always renders.

---

## CI gate example

```yaml
# .github/workflows/zebra.yml
- run: pip install -e '.[security]'
- run: zebra scan . --fail-on high --format sarif -o zebra.sarif
- uses: github/codeql-action/upload-sarif@v3
  with: { sarif_file: zebra.sarif }
```

---

## Other ways to achieve this (recommendations)

Zebra is a lightweight orchestration layer. Depending on your needs, you may
also reach for:

**Hosted / all-in-one platforms**
- **Snyk** / **GitHub Advanced Security (CodeQL)** / **Semgrep Cloud** — managed
  SAST + dependency scanning with PR comments and dashboards.
- **SonarQube / SonarCloud** — code quality + security + maintainability with
  trend tracking and quality gates.

**Best-of-breed single-purpose tools** (all auto-used by Zebra if installed)
- Secrets: **gitleaks**, **trufflehog**
- Dependencies/CVEs: **trivy**, **osv-scanner**, **pip-audit**, **npm audit**, **Dependabot/Renovate**
- SAST: **semgrep**, **bandit** (Python), **gosec** (Go), **brakeman** (Rails)
- Quality/perf lint: **ruff**, **eslint**, **pylint**, **golangci-lint**

**Continuous / automated**
- **pre-commit** hooks — run Zebra (or gitleaks/ruff) before every commit.
- `zebra watch` — live local monitoring while you code.
- Schedule `zebra scan --fail-on high` in CI nightly or per-PR.

**For document conversion** (the `zebra md` use case)
- **markitdown** (Microsoft) — broadest format support, what Zebra wraps.
- **pandoc** — the universal document converter (great for DOCX/LaTeX/EPUB).
- **pymupdf4llm** / **unstructured** / **docling** — PDF→Markdown tuned for LLM
  ingestion, with layout and table preservation.

A pragmatic stack: **pre-commit (gitleaks + ruff)** locally → **Zebra `--fail-on
high` in CI** → **Snyk/Dependabot** for ongoing dependency alerts.
```
