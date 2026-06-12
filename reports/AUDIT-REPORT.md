# Timbersite Security & Quality Audit

**Auditor:** 🦓 Zebra (built-in `secrets` + `quality` scanners)
**Date:** 2026-06-13
**Scope:** two repositories
- `timbersite` — full monorepo (backend + infra + bundled frontend) → branch `dev`
- `timbersite-frontend` — standalone frontend repo → branch `dev`

> This is the human-readable summary. The complete, line-by-line findings live in the
> raw Zebra reports:
> - [raw/timbersite-zebra-report.md](raw/timbersite-zebra-report.md)
> - [raw/timbersite-frontend-zebra-report.md](raw/timbersite-frontend-zebra-report.md)

---

## 1. Headline numbers

| Repo | Total | 🔴 Critical | 🟠 High | 🟡 Medium | ⚪ Low | ℹ️ Info |
|---|---|---|---|---|---|---|
| timbersite (full) | 1,017 | 1 | 26 | 15 | 265 | 710 |
| timbersite-frontend | 664 | 1 | 16 | 2 | 47 | 598 |

The two repos overlap: `timbersite` bundles a copy of the frontend, so most
frontend findings appear in both reports. Treat `timbersite-frontend` as the
authoritative source for frontend issues and the `backend\…` paths in the
`timbersite` report as backend-only.

### Scanner coverage

Only the two zero-dependency built-in scanners ran. The dependency/CVE and deep
SAST engines were **not installed**, so the following were skipped on both repos:
`bandit`, `pip-audit`, `dependencies` (npm/trivy/osv), `ruff`, `semgrep`, `gitleaks`.

**Implication:** there is currently *no* dependency-CVE coverage despite
`package.json` / `package-lock.json` being present. Installing `semgrep` + a
dependency auditor before the next run is the highest-value improvement.

---

## 2. Must-fix (act now)

### 🔴 Committed private key — CRITICAL
- `tests\hooks\api\functions\storage.test.js:26` (present in both repos)
- A private-key block is committed in source. Even in a test file this is a
  disclosure risk. **Rotate the key**, remove it from the working tree, and purge
  it from git history (`git filter-repo` / BFG) since it is already in past commits.

### 🟠 Database credentials in a shell script — HIGH (backend)
- `backend\backup-restore-northstar2dev.sh:5` and `:7`
- Connection strings with inline passwords. Move to environment variables / a
  secrets manager and rotate the exposed password.

### 🟠 TLS verification disabled in production config — HIGH (backend)
- `backend\kube\values-prod-33.0.0.yaml` lines 521, 538, 564, 581, 987, 988
- Certificate verification is turned off in prod values, exposing traffic to
  man-in-the-middle. Confirm whether these are intentional (e.g. internal
  self-signed endpoints) and, if not, re-enable verification with proper CAs.

### 🟠 Dynamic code execution — HIGH (backend)
- `backend\src\services\mcp\mcpKeyService.js:13` — use of `exec()` on dynamic
  input. Replace with explicit logic; never execute strings derived from input.

### 🟡 DOM XSS via innerHTML — MEDIUM (frontend)
- `src\components\logs\Editor.jsx:78` — assigning untrusted data to `innerHTML`.
  Sanitize (e.g. DOMPurify) or use safe DOM APIs / framework binding.

### 🟡 Hard-coded credentials — MEDIUM
- One real-config hit worth checking: `backend\kube\base\config.yaml:14`.
- The remaining ~13 are in test fixtures (`mcp-server\test\unit\*`,
  `UserUpsert.validation.test.js`, `artillery-config.yml`, `get-mcp-token.sh`).
  Likely placeholders — confirm none are live secrets, then suppress/ignore.

---

## 3. Known false positives (discount these)

- **"Possible SQL injection" — 17 high in timbersite / 16 high in frontend.**
  Every one is in `src\apollo\generated\graphql.ts`, an **auto-generated**
  GraphQL types file. No SQL is executed there; these are pattern false
  positives. Do not spend effort on them — instead, exclude generated files from
  future scans.

This single false-positive cluster accounts for the bulk of the "high" count in
both repos. Excluding generated code drops the frontend high count from 16 to ~0.

---

## 4. Cleanup backlog (low / info — non-blocking)

| Theme | Count (approx) | Where | Action |
|---|---|---|---|
| Leftover `console.log` debug statements | ~220 (timbersite) / ~14 (frontend) | backend resolvers/services, a few frontend components | Strip before release; consider a lint rule (`no-console`) |
| `TODO` / `FIXME` markers | ~700 info | concentrated in `backend\src\graphql\todo\*` (ironically) and infra YAML | Triage; convert to tracked issues |
| `SELECT *` queries | 42 (timbersite) / 33 (frontend) | QuickBooks integration (`thirdparty\quickbooks\*`, `services\quickbooks\*`) | Select only needed columns to cut I/O |
| Very long lines | a handful | generated `graphql.ts` / `gql.ts`, `env-helper.js` | Cosmetic; ignore generated files |

The debug-statement and TODO volume is high but each item is individually trivial.
Best handled by a lint gate rather than manual cleanup.

---

## 5. Recommended next steps

1. **Rotate + purge** the committed private key and the DB password (history rewrite).
2. **Review** the prod TLS-disable flags and the `exec()` usage.
3. **Exclude generated code** (`**/generated/**`) from scans to kill the SQL-injection noise.
4. **Install the heavier engines and re-scan** for real coverage:
   ```bash
   pip install semgrep bandit pip-audit ruff   # SAST + Python + dependency CVEs
   ```
   This adds dependency-CVE matching (currently zero) and multi-language SAST.
5. **Add a CI gate**: `zebra scan . --fail-on high` per-PR, plus a `no-console`
   lint rule to stop new debug statements landing.

---

*Generated by Zebra. Raw machine-readable detail in [`raw/`](raw/).*
