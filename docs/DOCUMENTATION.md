# 🦓 Zebra — Complete Documentation

> **Monitor any codebase for security vulnerabilities, code flaws, and
> optimisation opportunities — and turn the results into a report anyone can
> act on, from a terminal summary to a graphical PDF or an automated comment on
> a pull request.**

This is the full handbook: what Zebra is, why it exists, how it helps a team,
and how to use every part of it. For a quick command cheat-sheet see
[`USAGE.md`](USAGE.md).

---

## Table of contents

1. [What is Zebra](#1-what-is-zebra)
2. [Why Zebra — the benefits](#2-why-zebra--the-benefits)
3. [How it helps us — real workflows](#3-how-it-helps-us--real-workflows)
4. [What Zebra finds (the three lenses)](#4-what-zebra-finds-the-three-lenses)
5. [Installation](#5-installation)
6. [Core usage](#6-core-usage)
7. [Reports & output formats](#7-reports--output-formats)
8. [Remediation guidance](#8-remediation-guidance)
9. [GitHub pull-request feedback](#9-github-pull-request-feedback)
10. [CI/CD integration](#10-cicd-integration)
11. [Configuration reference](#11-configuration-reference)
12. [Architecture — how it works](#12-architecture--how-it-works)
13. [Extending Zebra](#13-extending-zebra)
14. [FAQ & troubleshooting](#14-faq--troubleshooting)
15. [How Zebra compares](#15-how-zebra-compares)

---

## 1. What is Zebra

Zebra is a lightweight **code-auditing and orchestration tool**. It scans a
directory and reports three kinds of issue side by side:

- 🔴 **Vulnerabilities** — things an attacker could exploit.
- 🟡 **Flaws** — things that make the code fragile or hard to maintain.
- 🟢 **Optimisations** — things that waste time, memory, or I/O.

It ships with **built-in scanners that need no installation** (secrets,
code-quality, dependency hygiene). When heavier industry tools are present
(`semgrep`, `bandit`, `pip-audit`, `ruff`, `trivy`, `gitleaks`, `osv-scanner`),
Zebra **detects and drives them automatically**, merging everything into one
report. Missing tools are skipped with an install hint — never fatal.

The same scan can be rendered as a colour terminal summary, Markdown, JSON,
SARIF (for GitHub code-scanning), a **graphical HTML page**, a **PDF**, or an
**automated pull-request comment**.

---

## 2. Why Zebra — the benefits

| Benefit | What it means in practice |
| --- | --- |
| **Zero-setup baseline** | `python zebra.py scan .` works on any machine with Python — no install, no config, no network. You always get *something* useful. |
| **One report, three lenses** | Security, maintainability, and performance issues in a single pass instead of three separate tools and three mental models. |
| **Orchestrates, doesn't reinvent** | When `semgrep`/`bandit`/`trivy` etc. are installed it uses them — so you get best-of-breed depth without wiring each one up yourself. |
| **Actionable, not just a list** | The HTML/PDF reports explain *what* each finding is, *why* it matters, and *how to fix* it — with reference links. A junior dev can act on it. |
| **Meets people where they are** | Terminal for devs, PDF for stakeholders/audits, SARIF for security dashboards, PR comments for reviewers. |
| **Private-repo friendly** | PR comments use the standard `GITHUB_TOKEN` — no paid GitHub Advanced Security licence required. |
| **CI-ready gating** | `--fail-on high` turns the audit into a quality gate that can block risky merges. |
| **Low false-positive design** | Built-in secret detection uses entropy + safe-placeholder filters; noisy patterns (e.g. generated files) can be excluded with one flag. |
| **Extensible** | Remediation advice and ignore rules are plain Python/data you can edit. |

---

## 3. How it helps us — real workflows

**While coding (inner loop).**
Run `zebra watch .` in a terminal. Every few seconds it re-audits and shows the
*delta* — so you see immediately if a change introduced a new secret, a debug
statement, or a risky pattern, before it ever reaches review.

**At review time (pull request).**
The PR workflow posts a summary comment listing new findings, updated in place
on each push. Reviewers see "this PR adds 2 high-severity issues" without
leaving GitHub, and can decide whether to block.

**As a merge gate (CI).**
`zebra scan . --fail-on high` exits non-zero when a critical/high finding
exists, failing the build. Combined with SARIF upload, findings also surface as
inline annotations (on repos with code-scanning enabled).

**For audits & stakeholders.**
`zebra scan . --format pdf -o audit.pdf` produces a polished, graphical report
— summary cards, a severity chart, and per-issue remediation — suitable for a
security review, a client deliverable, or a compliance record.

**For onboarding / tech-debt triage.**
Point Zebra at a legacy repo to get a prioritised map of where the risk and
debt concentrate (which files, which categories), so you know where to start.

---

## 4. What Zebra finds (the three lenses)

Severities: `critical · high · medium · low · info`.

### 🔴 Vulnerabilities
| Finding | Detected by |
| --- | --- |
| Committed private key (RSA/EC/OpenSSH/PGP) | secrets |
| AWS access key / secret, GitHub / Slack / Google / Stripe tokens | secrets |
| Hard-coded credentials & JWTs (entropy-filtered) | secrets |
| DB/redis connection string with inline password | secrets |
| `eval()` / `exec()` / dynamic code execution | quality (+ AST) |
| Shell injection (`shell=True`, `os.system`) | quality |
| Unsafe deserialization (`pickle`) | quality |
| TLS verification disabled (`verify=False`, `rejectUnauthorized:false`) | quality |
| Weak hashes (MD5/SHA-1) | quality |
| DOM XSS (`innerHTML =`) | quality |
| SQL injection (string-built queries) | quality |

### 🟡 Flaws
| Finding | Detected by |
| --- | --- |
| Swallowed/empty exception (`catch {}`, `except: pass`) | quality |
| Bare `except:` | quality (AST) |
| Mutable default argument | quality (AST) |
| Overly long function (>80 lines) | quality (AST) |
| Too many parameters (>6) | quality (AST) |
| Very long line (>200 chars) | quality |
| Leftover debug (`console.log`, `debugger`, debug `print`) | quality |
| Outstanding `TODO`/`FIXME`/`HACK`/`XXX` | quality |
| Unpinned dependencies / CVEs | dependencies (+ pip-audit/npm/trivy) |

### 🟢 Optimisations
| Finding | Detected by |
| --- | --- |
| `SELECT *` queries | quality |
| Triple-nested loops (O(n³)) | quality (AST) |
| String/list build with `+=` in a loop (O(n²)) | quality (AST) |
| Performance lints | ruff (when installed) |

Plus anything reported by the external engines Zebra orchestrates
(`semgrep`, `bandit`, `gitleaks`, `ruff`, `trivy`, `osv-scanner`).

---

## 5. Installation

```bash
# Run from source — needs only Python 3.8+
python zebra.py scan .

# Install the `zebra` command
pip install -e .

# Add the deeper engines + document conversion
pip install -e ".[security]"   # semgrep, bandit, pip-audit, ruff
pip install -e ".[all]"        # the above + markitdown
```

**Optional extras**
- **PDF export** needs a Chromium browser (Chrome / Edge / Chromium / Brave) —
  auto-detected, nothing to install. Or `pip install -e ".[pdf]"` (weasyprint).
- **Document conversion** (`zebra md`) needs `markitdown`; full format support
  needs Python 3.10+.
- **brew-only tools** (`trivy`, `gitleaks`, `osv-scanner`) are auto-used if on PATH.

Check your machine:

```bash
zebra tools
```

---

## 6. Core usage

```bash
zebra scan PATH         # one-shot audit (default path: .)
zebra watch PATH        # continuous re-audit, shows the delta each pass
zebra pr-comment PATH   # scan + post a summary comment on a GitHub PR
zebra md FILES…         # convert documents to Markdown
zebra tools             # list installed/optional scanners
```

**Common scan options**

```bash
zebra scan . --builtin-only             # skip external tools
zebra scan . --only secrets quality     # run just these scanners
zebra scan . --ignore "**/generated/**" dist   # extra ignore patterns
zebra scan . --fail-on high             # exit 2 if any high+ finding (CI gate)
zebra scan . --max-rows 50              # more rows per category in the terminal
```

**Watch mode**

```bash
zebra watch . --interval 30   # re-scan every 30s
```

---

## 7. Reports & output formats

| Format | Flag | Best for |
| --- | --- | --- |
| Terminal | *(default)* | quick local check |
| Markdown | `--format md` | sharing in issues/wikis/PRs |
| JSON | `--format json` | scripting, dashboards |
| SARIF | `--format sarif` | GitHub code-scanning / security tools |
| **HTML** | `--format html` | a rich, shareable, self-contained page |
| **PDF** | `--format pdf` | audits, stakeholders, deliverables |

```bash
zebra scan . --format md   -o report.md
zebra scan . --format json -o report.json
zebra scan . --format sarif -o report.sarif
zebra scan . --format html -o report.html
zebra scan . --format pdf  -o report.pdf
```

The **HTML** and **PDF** formats are the "rich" ones. For every finding *type*
they show:

- **What it is** — a plain-English description,
- **Why it matters** — the risk / impact,
- **How to fix** — concrete remediation (with reference links),

followed by a table of every location it occurs, plus summary cards and a
severity-distribution chart at the top.

PDF export renders the HTML with a headless browser (auto-detected). Output
directories are created automatically; if you omit `-o` for PDF it writes
`zebra-report.pdf`.

---

## 8. Remediation guidance

What turns a Zebra report from a list into something actionable is the
**remediation knowledge base** ([`zebra/remediation.py`](../zebra/remediation.py)).
It maps each rule (or finding title) to `{what, why, fix, refs}`. The HTML/PDF
reports and (compactly) the PR comments use it.

You can refine or add guidance — see [§13 Extending Zebra](#13-extending-zebra).

---

## 9. GitHub pull-request feedback

Zebra can post its findings as a **single summary comment** on a PR and
**update that same comment** on every push (it tags the comment with a hidden
marker, so PRs never fill up with duplicates).

- Uses the GitHub REST API directly — **no extra dependencies**.
- Works on **private repos** with the built-in `GITHUB_TOKEN` — **no GitHub
  Advanced Security required**.
- File locations link to the exact lines at the PR's head commit.

**Set it up:** copy [`examples/zebra-pr.yml`](../examples/zebra-pr.yml) to
`.github/workflows/zebra-pr.yml` in the target repo. That's it — on every PR it
scans and comments.

**Preview locally before enabling:**

```bash
zebra pr-comment . --dry-run --comment-threshold high
```

**Post manually to a PR:**

```bash
zebra pr-comment . --repo owner/name --pr 42 --token "$GH_TOKEN" \
      --sha "$(git rev-parse HEAD)" --comment-threshold medium
```

Useful flags: `--comment-threshold` (min severity listed), `--max-findings`
(row cap), `--fail-on` (block the PR), `--ignore` (drop false positives like
`**/generated/**`), `--dry-run` (print instead of post). In Actions, repo / PR /
token / sha are read from the environment automatically.

> **Next step if you want line-anchored comments:** the scan + render work is
> already done; only diff-to-line mapping would need adding on top of this.

---

## 10. CI/CD integration

**As a merge gate**

```yaml
# .github/workflows/zebra.yml
- run: pip install -e '.[security]'
- run: zebra scan . --fail-on high --format sarif -o zebra.sarif
- uses: github/codeql-action/upload-sarif@v3   # optional: inline annotations
  with: { sarif_file: zebra.sarif }
```

`--fail-on high` makes the job exit non-zero (code 2) when any critical/high
finding exists, blocking the merge.

**As PR feedback** — use [`examples/zebra-pr.yml`](../examples/zebra-pr.yml)
(see §9). The two can run together: the comment for humans, the gate for policy.

**Nightly / scheduled** — run a full `zebra scan --format pdf` on a cron and
archive the PDF for a historical audit trail.

---

## 11. Configuration reference

**Commands**

| Command | Purpose |
| --- | --- |
| `zebra scan PATH` | one-shot audit |
| `zebra watch PATH` | continuous re-audit on an interval |
| `zebra pr-comment PATH` | scan and post a summary comment on a GitHub PR |
| `zebra md FILES…` | convert documents to Markdown |
| `zebra tools` | list installed/optional scanners |

**`scan` / `watch` flags**

| Flag | Default | Meaning |
| --- | --- | --- |
| `--format` | `terminal` | `terminal · md · json · sarif · html · pdf` |
| `-o, --output` | — | write report to a file (parent dirs auto-created) |
| `--fail-on` | `never` | exit 2 if a finding at/above this severity exists |
| `--builtin-only` | off | skip external tools, use built-ins only |
| `--only` | all | run only the named scanners |
| `--ignore` | — | extra glob/dir patterns to ignore |
| `--max-rows` | 25 | max findings per category in terminal output |
| `--interval` | 15 | (watch) seconds between scans |

**`pr-comment` flags** (plus all scan flags)

| Flag | Default | Meaning |
| --- | --- | --- |
| `--repo` | `$GITHUB_REPOSITORY` | `owner/name` |
| `--pr` | inferred | PR number (from `$GITHUB_REF`/event) |
| `--token` | `$GITHUB_TOKEN` | GitHub token |
| `--sha` | `$GITHUB_SHA` | commit sha for file links |
| `--comment-threshold` | `info` | min severity listed in the comment |
| `--max-findings` | 30 | max rows in the comment |
| `--dry-run` | off | print the comment instead of posting |

**Environment variables**

| Var | Effect |
| --- | --- |
| `ZEBRA_BROWSER` | path to the browser used for PDF export |
| `NO_COLOR` | disable terminal colour |
| `GITHUB_TOKEN` / `GH_TOKEN` | auth for `pr-comment` |
| `GITHUB_REPOSITORY` / `GITHUB_REF` / `GITHUB_SHA` / `GITHUB_EVENT_PATH` | auto-read in Actions |

---

## 12. Architecture — how it works

```
zebra/
├── cli.py              # argparse front-end: scan / watch / pr-comment / md / tools
├── util.py             # Finding model, file walking, tool detection, colours
├── report.py           # terminal / markdown / json / sarif renderers
├── report_html.py      # graphical HTML + PDF renderer (browser print-to-pdf)
├── remediation.py      # rule → {what, why, fix, refs} knowledge base
├── github.py           # post/update a findings summary on a GitHub PR
├── docs.py             # markitdown document → Markdown (with fallback)
└── scanners/
    ├── secrets.py      # regex + entropy secret detection
    ├── quality.py      # language-agnostic line rules + Python AST analysis
    ├── dependencies.py # pip-audit / npm audit / trivy + unpinned-dep check
    └── sast.py         # wrappers: semgrep, bandit, gitleaks, ruff
```

**Flow.** `scan` walks the tree (skipping `node_modules`, `.git`, build dirs,
minified/lock files, oversized files), runs each scanner, and collects
`Finding` objects (category, severity, title, detail, file, line, rule,
source). A renderer turns the merged, sorted findings into the chosen format.
Each scanner returns a `ScanResult`; if its underlying tool is missing it
reports `skipped` with an install hint rather than failing.

---

## 13. Extending Zebra

**Add remediation advice for a rule** — edit
[`zebra/remediation.py`](../zebra/remediation.py):

```python
REMEDIATION["my-rule-id"] = {
    "what": "One sentence on what the finding means.",
    "risk": "Why it matters / the impact.",
    "fix":  "Concrete steps to resolve it.",
    "refs": ["https://owasp.org/..."],   # optional
}
```

Rule ids come from the scanners: secret rules use ids like `private-key`; the
language-agnostic line rules use the finding title (e.g. `"Possible SQL
injection"`). Anything without an entry falls back to a generic message, so the
report never shows a blank cell.

**Add a detection rule** — add a `(regex, severity, category, title, detail)`
tuple to `_LINE_RULES` (or `_OPT_LINE_RULES`) in
[`zebra/scanners/quality.py`](../zebra/scanners/quality.py), or a new secret
pattern to `_PATTERNS` in
[`zebra/scanners/secrets.py`](../zebra/scanners/secrets.py).

**Add an output format** — write a `render_*` function and wire it into
`_emit` in [`zebra/cli.py`](../zebra/cli.py).

---

## 14. FAQ & troubleshooting

**"It says scanners were skipped."** That's expected — the deeper engines are
optional. Run `zebra tools` to see what's installed, then
`pip install -e ".[security]"` to add `semgrep`/`bandit`/`pip-audit`/`ruff`.
The built-in scanners always run regardless.

**Why so many "Possible SQL injection" highs in one file?** Auto-generated
GraphQL/ORM type files trip the string-built-SQL pattern. They're false
positives — exclude them: `--ignore "**/generated/**"`.

**PDF export fails.** Zebra needs a Chromium browser for PDF. Install Chrome /
Edge / Chromium / Brave (auto-detected), point at one with
`ZEBRA_BROWSER=/path/to/chrome`, or `pip install weasyprint` as a fallback.

**The PR comment isn't posted.** Ensure the workflow has
`permissions: pull-requests: write`, that `GITHUB_TOKEN` is passed in `env`,
and that it's running on a `pull_request` event. Use `--dry-run` to verify the
content renders.

**Unicode/emoji errors in the Windows terminal.** Set `PYTHONUTF8=1` (or
`PYTHONIOENCODING=utf-8`) so the console can render the report glyphs.

**Hard-coded credential findings in test files.** Often placeholders. Confirm
they aren't real; if they are test fixtures, replace with obvious dummies
(`changeme`) so the scanner's safe-placeholder filter skips them.

---

## 15. How Zebra compares

Zebra is an **orchestration layer**, not a replacement for deep platforms.
Depending on your needs you might also use:

**Hosted / all-in-one** — Snyk, GitHub Advanced Security (CodeQL),
Semgrep Cloud, SonarQube/SonarCloud (managed SAST + dependency scanning with
dashboards and trends).

**Best-of-breed single-purpose** (all auto-used by Zebra if installed)
- Secrets: gitleaks, trufflehog
- Dependencies/CVEs: trivy, osv-scanner, pip-audit, npm audit, Dependabot/Renovate
- SAST: semgrep, bandit (Python), gosec (Go), brakeman (Rails)
- Quality/perf lint: ruff, eslint, pylint, golangci-lint

**A pragmatic stack:** pre-commit (gitleaks + ruff) locally → **Zebra
`--fail-on high` + PR comments in CI** → Snyk/Dependabot for ongoing dependency
alerts.

**When to reach for Zebra specifically:** you want one tool that runs anywhere
with zero setup, gives a unified security + quality + performance view, produces
human-friendly PDF/HTML *and* machine-friendly SARIF/JSON, and comments on PRs
in private repos without a paid security licence.

---

*🦓 Zebra · remediation guidance is advisory — review each finding in context.
For the quick cheat-sheet see [`USAGE.md`](USAGE.md).*
