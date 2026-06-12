# 🦓 Zebra audit report

**Target:** `D:\WORK\SkillRev\timbersite`  
**Generated:** 2026-06-13T04:34:20  
**Total findings:** 1017

## Summary

| Severity | Count |
| --- | --- |
| critical | 1 |
| high | 26 |
| medium | 15 |
| low | 265 |
| info | 710 |

### Scanner status

| Scanner | Status | Findings |
| --- | --- | --- |
| bandit | ⏭️ skipped — bandit not installed — `pip install bandit` (Python security linter). | 0 |
| dependencies | ⏭️ skipped — No dependency-audit tool installed (pip-audit / npm / trivy / osv-scanner). Manifests present: package-lock.json, package.json. Install one to get CVE matches — e.g. `pip install pip-audit` or `brew install trivy`. | 0 |
| gitleaks | ⏭️ skipped — gitleaks not installed — `brew install gitleaks` (git-history secret scan). | 0 |
| quality | ✅ ran | 1000 |
| ruff | ⏭️ skipped — ruff not installed — `pip install ruff` (fast Python linter, incl. perf rules). | 0 |
| secrets | ✅ ran | 17 |
| semgrep | ⏭️ skipped — semgrep not installed — `pip install semgrep` (deep multi-language SAST). | 0 |

## Security vulnerabilities (42)

| Severity | Title | Location | Source | Detail |
| --- | --- | --- | --- | --- |
| critical | Private key block | `timbersite-frontend\tests\hooks\api\functions\storage.test.js:26` | secrets | Potential private key block committed in source. |
| high | Connection string with inline password | `backend\backup-restore-northstar2dev.sh:5` | secrets | Potential connection string with inline password committed in source. |
| high | Connection string with inline password | `backend\backup-restore-northstar2dev.sh:7` | secrets | Potential connection string with inline password committed in source. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:521` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:538` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:564` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:581` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:987` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | TLS verification disabled | `backend\kube\values-prod-33.0.0.yaml:988` | quality | Disabling certificate verification exposes traffic to MITM. |
| high | Possible SQL injection | `backend\src\env-helper.js:1` | quality | String-built SQL; use parameterised queries instead. |
| high | Use of exec() | `backend\src\services\mcp\mcpKeyService.js:13` | quality | Executing dynamic code is dangerous; prefer explicit logic. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:3983` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:3991` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:4031` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:4038` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:4515` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5113` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5129` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5136` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5230` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5232` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5233` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5279` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5342` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5343` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5345` | quality | String-built SQL; use parameterised queries instead. |
| high | Possible SQL injection | `timbersite-frontend\src\apollo\generated\graphql.ts:5346` | quality | String-built SQL; use parameterised queries instead. |
| medium | Hard-coded credential | `backend\kube\base\config.yaml:14` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `get-mcp-token.sh:54` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\config.test.js:6` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\config.test.js:64` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\request-context.test.js:24` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\request-context.test.js:25` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:14` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:32` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:49` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:97` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:132` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `mcp-server\test\unit\user-token-service.test.js:163` | secrets | Potential hard-coded credential committed in source. |
| medium | Possible DOM XSS | `timbersite-frontend\src\components\logs\Editor.jsx:78` | quality | Assigning to innerHTML with untrusted data can inject scripts. |
| medium | Hard-coded credential | `timbersite-frontend\tests\components\users\UserUpsert.validation.test.js:71` | secrets | Potential hard-coded credential committed in source. |
| medium | Hard-coded credential | `utils\performance\artillery-config.yml:17` | secrets | Potential hard-coded credential committed in source. |

## Code flaws (933)

| Severity | Title | Location | Source | Detail |
| --- | --- | --- | --- | --- |
| low | Debug statement | `backend\scripts\create-mcp-key.js:72` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:65` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:84` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:100` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:120` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:130` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:163` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:170` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:171` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:182` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:206` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:259` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:276` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:348` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:377` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:382` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:394` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:413` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:430` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:454` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:509` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:549` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:613` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\changeOrder\resolvers.js:617` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\choices\resolvers.js:77` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:366` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:377` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:395` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:414` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:430` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:567` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:570` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:593` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:601` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\estimate\resolvers.js:639` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:7` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:14` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:24` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:37` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:42` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:43` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:44` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:45` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:86` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\file\resolvers.js:105` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\lineItem\resolvers.js:17` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\mcp\resolvers.js:70` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\mcp\resolvers.js:116` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\project\resolvers.js:65` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2269` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2270` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2644` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2649` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2650` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2651` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2652` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2653` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2654` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2655` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2658` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2659` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2661` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2663` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\reports\resolvers.js:2674` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\selection\resolvers.js:18` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\selection\resolvers.js:35` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\selection\resolvers.js:152` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:152` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:247` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:248` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:284` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:285` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:286` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:287` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:306` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\timeEntry\resolvers.js:307` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:185` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:186` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:200` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:208` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:250` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\resolvers.js:271` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\typedefs.js:181` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\typedefs.js:209` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\graphql\user\typedefs.js:226` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\index.js:287` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:10` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:29` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:41` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:57` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:65` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:75` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:84` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\apikey.js:109` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:14` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:22` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:46` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:72` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:94` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:115` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\middleware\jwt.js:168` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\migrations\rollback-unify-line-items.js:12` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\migrations\unify-line-items.js:30` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\api.js:19` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:105` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:139` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:196` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:198` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:229` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:239` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:345` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:457` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:470` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:520` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\atlas.js:592` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:299` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:300` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:304` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:330` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:353` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:354` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:355` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:356` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:357` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:358` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:434` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:435` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:436` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:437` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\emailService.js:438` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\excel\hourly.js:225` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\excel\hourly.js:238` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\excel\invoice.js:261` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:186` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:190` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:198` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:213` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:220` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:222` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\fileGeneration.js:225` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\keycloak\keycloakAdmin.js:113` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:108` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:116` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:127` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:136` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:147` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:149` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:158` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:161` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:185` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:193` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:205` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:214` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:225` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:227` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:251` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:275` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:294` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.changeorder.js:297` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.common.js:82` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.common.js:139` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.config.js:27` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.config.js:53` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.config.js:111` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\pdf\pdf.selection.js:195` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\preview-link.js:15` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\preview-link.js:59` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\quickbooks\qb-oauth.js:576` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\quickbooks\qb-oauth.js:618` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\quickbooks\tokenRefreshJob.js:88` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\quickbooks\tokenRefreshJob.js:98` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\quickbooks\tokenRefreshJob.js:203` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:30` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:35` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:89` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:115` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:133` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:134` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:137` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:141` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:263` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:317` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\services\users\users.js:338` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:17` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:70` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:131` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:185` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:225` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\formatters.js:233` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\graphql.js:18` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\graphql.js:53` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\graphql.js:196` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\graphql.js:234` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\mongo.js:50` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `backend\src\util\quill.js:16` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `key.sh:12` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `key.sh:13` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `key.sh:14` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\ChangeOrder\ChangeOrderUpsertV2\LineItem.jsx:113` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\navigation\NextBreadcrumbs.js:74` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\navigation\NextBreadcrumbs.js:89` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\navigation\NextBreadcrumbs.js:105` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\navigation\NextBreadcrumbs.js:159` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\navigation\NextBreadcrumbs.js:164` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\common\selects\StdDynamicSelect.js:36` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\estimate\EstimateUpsert\LineItem.tsx:145` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:236` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:237` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:239` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:242` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:272` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `timbersite-frontend\src\components\users\UserUpsert.jsx:932` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\ci\gen-firebase-rewrites.js:56` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\ci\gen-firebase-rewrites.js:66` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\csv-transform\buildertrend-customers-to-firebase.js:24` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\csv-transform\buildertrend-estimates-to-firebase.js:54` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\csv-transform\buildertrend-estimates-to-firebase.js:93` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\csv-transform\buildertrend-users-to-firebase.js:33` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\merge-json\merge-json.js:14` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\merge-json\merge-json.js:16` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\merge-json\merge-json.js:17` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\merge-json\merge-json.js:19` | quality | Leftover debug output; remove before release. |
| low | Debug statement | `utils\performance\processor.js:10` | quality | Leftover debug output; remove before release. |
| info | Outstanding TODO/FIXME | `.github\workflows\push-on-merge-dev.yml:79` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `.github\workflows\push-on-merge.yml:78` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\kube\le-storageclass.yaml:10` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\kube\values-prod-33.0.0.yaml:80` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\kube\values-prod-33.0.0.yaml:462` | quality | Unfinished work marker left in the code. |
| info | Very long line | `backend\src\env-helper.js:1` | quality | Line is 4452 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\file\typedefs.js:34` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\mutationFields.js:24` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\project\resolvers.js:6` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\project\resolvers.js:1089` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\project\resolvers.js:1096` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\project\resolvers.js:1106` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\queryFields.js:24` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\reports\resolvers.js:2688` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\mutations.js:8` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\mutations.js:19` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\mutations.js:33` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\queries.js:17` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\queries.js:19` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\queries.js:25` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:1` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:13` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:24` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:27` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:29` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:33` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:36` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:37` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:51` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:53` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:54` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:70` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:72` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:77` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:80` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:81` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:93` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\resolvers.js:95` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\typedefs.js:30` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\typedefs.js:35` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\typedefs.js:63` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\graphql\todo\typedefs.js:79` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\index.js:138` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\index.js:145` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\index.js:148` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\middleware\backend.js:2` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\middleware\jwt.js:135` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\middleware\jwt.js:222` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\CompanyDetails.js:181` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\Customer.js:47` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\Customer.js:48` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\File.js:33` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\File.js:34` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\File.js:35` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\File.js:36` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\File.js:43` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\Todo.js:41` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\Todo.js:55` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\mongo\models\quickbooks\Quickbooks.js:34` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\atlas.js:166` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\pdf\pdf.config.js:37` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\preview-link.js:3` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\users\users.js:32` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\users\users.js:105` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\services\users\users.js:112` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\util\formatters.js:10` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\util\formatters.js:140` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\util\formatters.js:199` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `backend\src\util\formatters.js:204` | quality | Unfinished work marker left in the code. |
| info | Very long line | `backend\test\integration\artifacts\random-key.js:3` | quality | Line is 852 chars; consider wrapping. |
| info | Very long line | `backend\test\unit\preview-link.test.js:15` | quality | Line is 263 chars; consider wrapping. |
| info | Very long line | `backend\test\unit\preview-link.test.js:32` | quality | Line is 263 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\admin-and-reports.js:6` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\admin-and-reports.js:254` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\admin-and-reports.js:267` | quality | Unfinished work marker left in the code. |
| info | Very long line | `mcp-server\src\tools\admin-and-reports.js:423` | quality | Line is 201 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\change-orders.js:223` | quality | Line is 278 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\change-orders.js:310` | quality | Line is 354 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\change-orders.js:366` | quality | Line is 208 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\customers.js:271` | quality | Line is 291 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\estimates-write.js:190` | quality | Line is 268 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\estimates-write.js:218` | quality | Line is 202 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:6` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:14` | quality | Unfinished work marker left in the code. |
| info | Very long line | `mcp-server\src\tools\operations.js:319` | quality | Line is 207 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\operations.js:375` | quality | Line is 201 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:646` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:700` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:702` | quality | Unfinished work marker left in the code. |
| info | Very long line | `mcp-server\src\tools\operations.js:702` | quality | Line is 201 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:707` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:712` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:715` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:718` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:768` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:770` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:775` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:776` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:782` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:820` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:822` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\operations.js:827` | quality | Unfinished work marker left in the code. |
| info | Very long line | `mcp-server\src\tools\ops-write.js:328` | quality | Line is 230 chars; consider wrapping. |
| info | Very long line | `mcp-server\src\tools\projects-write.js:103` | quality | Line is 214 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\projects.js:4` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\src\tools\projects.js:14` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\test\unit\phase3-tools.test.js:164` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\test\unit\phase3-tools.test.js:173` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `mcp-server\test\unit\phase3-tools.test.js:177` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\.github\workflows\push-on-merge-dev.yml:73` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\.github\workflows\push-on-merge.yml:73` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\fragment-masking.ts:60` | quality | Line is 207 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:17` | quality | Line is 3205 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:18` | quality | Line is 5045 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:19` | quality | Line is 1744 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:20` | quality | Line is 1025 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:21` | quality | Line is 1880 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:22` | quality | Line is 897 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:23` | quality | Line is 735 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:24` | quality | Line is 1423 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:25` | quality | Line is 1064 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:26` | quality | Line is 1214 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:27` | quality | Line is 1094 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:28` | quality | Line is 1747 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:29` | quality | Line is 1790 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:30` | quality | Line is 2184 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:31` | quality | Line is 566 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:32` | quality | Line is 299 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:33` | quality | Line is 5594 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:34` | quality | Line is 8272 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:35` | quality | Line is 1052 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:36` | quality | Line is 1286 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:37` | quality | Line is 1400 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:38` | quality | Line is 2304 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:39` | quality | Line is 985 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:40` | quality | Line is 1729 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:41` | quality | Line is 982 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:42` | quality | Line is 1257 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:43` | quality | Line is 836 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:44` | quality | Line is 1387 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:45` | quality | Line is 337 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:46` | quality | Line is 528 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:47` | quality | Line is 1159 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:48` | quality | Line is 1609 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:49` | quality | Line is 3227 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:50` | quality | Line is 307 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:51` | quality | Line is 288 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:52` | quality | Line is 3605 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:53` | quality | Line is 740 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:54` | quality | Line is 3277 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:55` | quality | Line is 1551 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:56` | quality | Line is 1781 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:57` | quality | Line is 2337 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:58` | quality | Line is 3898 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:59` | quality | Line is 594 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\gql.ts:60` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:60` | quality | Line is 850 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:61` | quality | Line is 548 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:62` | quality | Line is 1871 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:63` | quality | Line is 2603 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:64` | quality | Line is 889 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:65` | quality | Line is 1372 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:68` | quality | Line is 3198 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:69` | quality | Line is 5038 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:70` | quality | Line is 1737 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:71` | quality | Line is 1018 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:72` | quality | Line is 1873 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:73` | quality | Line is 890 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:74` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:75` | quality | Line is 1416 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:76` | quality | Line is 1057 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:77` | quality | Line is 1207 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:78` | quality | Line is 1087 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:79` | quality | Line is 1740 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:80` | quality | Line is 1783 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:81` | quality | Line is 2177 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:82` | quality | Line is 559 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:83` | quality | Line is 292 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:84` | quality | Line is 5587 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:85` | quality | Line is 8265 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:86` | quality | Line is 1045 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:87` | quality | Line is 1279 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:88` | quality | Line is 1393 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:89` | quality | Line is 2297 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:90` | quality | Line is 978 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:91` | quality | Line is 1722 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:92` | quality | Line is 975 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:93` | quality | Line is 1250 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:94` | quality | Line is 829 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:95` | quality | Line is 1380 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:96` | quality | Line is 330 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:97` | quality | Line is 521 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:98` | quality | Line is 1152 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:99` | quality | Line is 1602 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:100` | quality | Line is 3220 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:101` | quality | Line is 300 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:102` | quality | Line is 281 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:103` | quality | Line is 3598 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:104` | quality | Line is 733 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:105` | quality | Line is 3270 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:106` | quality | Line is 1544 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:107` | quality | Line is 1774 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:108` | quality | Line is 2330 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:109` | quality | Line is 3891 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:110` | quality | Line is 587 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\gql.ts:111` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:111` | quality | Line is 843 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:112` | quality | Line is 541 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:113` | quality | Line is 1864 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:114` | quality | Line is 2596 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:115` | quality | Line is 882 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:116` | quality | Line is 1365 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:136` | quality | Line is 6376 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:140` | quality | Line is 10060 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:144` | quality | Line is 3464 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:148` | quality | Line is 2030 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:152` | quality | Line is 3720 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:156` | quality | Line is 1760 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:160` | quality | Line is 1442 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:164` | quality | Line is 2822 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:168` | quality | Line is 2092 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:172` | quality | Line is 2396 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:176` | quality | Line is 2160 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:180` | quality | Line is 3470 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:184` | quality | Line is 3552 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:188` | quality | Line is 4344 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:192` | quality | Line is 1090 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:196` | quality | Line is 562 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:200` | quality | Line is 11160 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:204` | quality | Line is 16520 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:208` | quality | Line is 2060 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:212` | quality | Line is 2532 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:216` | quality | Line is 2774 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:220` | quality | Line is 4586 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:224` | quality | Line is 1950 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:228` | quality | Line is 3442 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:232` | quality | Line is 1938 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:236` | quality | Line is 2492 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:240` | quality | Line is 1644 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:244` | quality | Line is 2750 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:248` | quality | Line is 648 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:252` | quality | Line is 1026 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:256` | quality | Line is 2292 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:260` | quality | Line is 3192 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:264` | quality | Line is 6432 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:268` | quality | Line is 586 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:272` | quality | Line is 554 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:276` | quality | Line is 7162 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:280` | quality | Line is 1444 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:284` | quality | Line is 6522 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:288` | quality | Line is 3072 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:292` | quality | Line is 3536 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:296` | quality | Line is 4644 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:300` | quality | Line is 7768 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:304` | quality | Line is 1168 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\gql.ts:308` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:308` | quality | Line is 1684 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:312` | quality | Line is 1080 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:316` | quality | Line is 3722 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:320` | quality | Line is 5190 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:324` | quality | Line is 1754 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\gql.ts:328` | quality | Line is 2724 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:19` | quality | Line is 244 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:641` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:1609` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:1610` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:1651` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:1715` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:1716` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:2160` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:2484` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:2485` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:2957` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:3483` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:3484` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:3504` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:3826` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:3983` | quality | Line is 1722 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:3991` | quality | Line is 1955 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4006` | quality | Line is 303 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4022` | quality | Line is 438 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4031` | quality | Line is 2842 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4038` | quality | Line is 2639 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4047` | quality | Line is 264 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4061` | quality | Line is 1697 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4069` | quality | Line is 827 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4078` | quality | Line is 830 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4086` | quality | Line is 809 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4093` | quality | Line is 742 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4101` | quality | Line is 741 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4115` | quality | Line is 1541 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4122` | quality | Line is 1541 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4127` | quality | Line is 1526 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4134` | quality | Line is 235 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4142` | quality | Line is 693 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4158` | quality | Line is 793 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4165` | quality | Line is 690 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4174` | quality | Line is 255 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4188` | quality | Line is 766 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4196` | quality | Line is 774 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4212` | quality | Line is 866 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4219` | quality | Line is 759 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4233` | quality | Line is 718 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4241` | quality | Line is 939 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4257` | quality | Line is 1107 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4264` | quality | Line is 1004 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4273` | quality | Line is 243 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4287` | quality | Line is 1290 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4295` | quality | Line is 1286 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4311` | quality | Line is 1534 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4318` | quality | Line is 1431 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4332` | quality | Line is 364 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4340` | quality | Line is 372 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4347` | quality | Line is 417 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4354` | quality | Line is 3290 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4362` | quality | Line is 2895 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4376` | quality | Line is 1443 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4384` | quality | Line is 270 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4400` | quality | Line is 418 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4409` | quality | Line is 4078 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4416` | quality | Line is 4658 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4425` | quality | Line is 251 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4439` | quality | Line is 3377 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4446` | quality | Line is 710 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4454` | quality | Line is 718 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4470` | quality | Line is 874 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4477` | quality | Line is 763 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4491` | quality | Line is 817 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4499` | quality | Line is 1245 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4515` | quality | Line is 1854 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4522` | quality | Line is 1381 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4536` | quality | Line is 462 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4544` | quality | Line is 470 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4558` | quality | Line is 533 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4567` | quality | Line is 681 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4574` | quality | Line is 582 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4581` | quality | Line is 592 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4595` | quality | Line is 706 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4602` | quality | Line is 616 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4610` | quality | Line is 651 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4626` | quality | Line is 825 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4633` | quality | Line is 723 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4647` | quality | Line is 554 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4655` | quality | Line is 562 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4671` | quality | Line is 734 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4678` | quality | Line is 631 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4687` | quality | Line is 337 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4720` | quality | Line is 340 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4728` | quality | Line is 321 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4744` | quality | Line is 650 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4751` | quality | Line is 546 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4760` | quality | Line is 263 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4774` | quality | Line is 1064 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4782` | quality | Line is 1297 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4798` | quality | Line is 1661 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4805` | quality | Line is 1559 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4814` | quality | Line is 507 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4828` | quality | Line is 837 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4836` | quality | Line is 371 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4841` | quality | Line is 470 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4850` | quality | Line is 623 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4859` | quality | Line is 1211 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4866` | quality | Line is 1461 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4873` | quality | Line is 879 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4880` | quality | Line is 1069 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4887` | quality | Line is 465 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4895` | quality | Line is 473 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4911` | quality | Line is 2277 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4918` | quality | Line is 2170 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4933` | quality | Line is 392 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4940` | quality | Line is 1209 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4948` | quality | Line is 1217 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4964` | quality | Line is 1339 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4971` | quality | Line is 1235 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4985` | quality | Line is 1546 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:4993` | quality | Line is 2248 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5009` | quality | Line is 2895 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5016` | quality | Line is 2725 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:5037` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5037` | quality | Line is 394 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:5045` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5045` | quality | Line is 348 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:5061` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5061` | quality | Line is 561 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:5068` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5068` | quality | Line is 462 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5084` | quality | Line is 350 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5091` | quality | Line is 251 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5105` | quality | Line is 1326 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5113` | quality | Line is 1732 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5129` | quality | Line is 1796 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5136` | quality | Line is 1697 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5145` | quality | Line is 315 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5159` | quality | Line is 395 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5167` | quality | Line is 823 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5183` | quality | Line is 861 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5190` | quality | Line is 565 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5199` | quality | Line is 243 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5209` | quality | Line is 4426 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5210` | quality | Line is 5256 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5211` | quality | Line is 743 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5212` | quality | Line is 1548 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5213` | quality | Line is 826 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5214` | quality | Line is 2240 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5215` | quality | Line is 7590 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5216` | quality | Line is 6518 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5217` | quality | Line is 1766 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5218` | quality | Line is 853 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5219` | quality | Line is 4410 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5220` | quality | Line is 2722 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5221` | quality | Line is 3054 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5222` | quality | Line is 2671 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5223` | quality | Line is 2208 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5224` | quality | Line is 2532 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5225` | quality | Line is 748 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5226` | quality | Line is 3744 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5227` | quality | Line is 3744 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5228` | quality | Line is 3336 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5229` | quality | Line is 1104 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5230` | quality | Line is 2399 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5231` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5232` | quality | Line is 2928 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5233` | quality | Line is 2088 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5234` | quality | Line is 1751 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5235` | quality | Line is 835 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5236` | quality | Line is 2177 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5237` | quality | Line is 2488 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5238` | quality | Line is 748 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5239` | quality | Line is 2964 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5240` | quality | Line is 2120 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5241` | quality | Line is 859 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5242` | quality | Line is 2181 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5243` | quality | Line is 2958 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5244` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5245` | quality | Line is 3660 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5246` | quality | Line is 2820 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5247` | quality | Line is 1747 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5248` | quality | Line is 835 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5249` | quality | Line is 3445 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5250` | quality | Line is 3703 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5251` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5252` | quality | Line is 4629 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5253` | quality | Line is 3789 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5254` | quality | Line is 835 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5255` | quality | Line is 1366 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5256` | quality | Line is 1677 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5257` | quality | Line is 1491 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5258` | quality | Line is 7935 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5259` | quality | Line is 7359 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5260` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5261` | quality | Line is 3751 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5262` | quality | Line is 1484 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5263` | quality | Line is 762 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5264` | quality | Line is 2214 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5265` | quality | Line is 10346 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5266` | quality | Line is 11079 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5267` | quality | Line is 1747 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5268` | quality | Line is 835 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5269` | quality | Line is 8076 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5270` | quality | Line is 2230 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5271` | quality | Line is 2541 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5272` | quality | Line is 768 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5273` | quality | Line is 3190 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5274` | quality | Line is 2342 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5275` | quality | Line is 883 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5276` | quality | Line is 2711 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5277` | quality | Line is 3996 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5278` | quality | Line is 723 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5279` | quality | Line is 5709 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5280` | quality | Line is 4022 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5281` | quality | Line is 829 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5282` | quality | Line is 1530 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5283` | quality | Line is 1841 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5284` | quality | Line is 708 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5285` | quality | Line is 1698 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5286` | quality | Line is 2622 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5287` | quality | Line is 1786 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5288` | quality | Line is 1818 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5289` | quality | Line is 811 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5290` | quality | Line is 2055 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5291` | quality | Line is 1942 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5292` | quality | Line is 2313 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5293` | quality | Line is 723 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5294` | quality | Line is 3022 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5295` | quality | Line is 2183 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5296` | quality | Line is 829 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5297` | quality | Line is 1868 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5298` | quality | Line is 2179 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5299` | quality | Line is 728 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5300` | quality | Line is 2833 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5301` | quality | Line is 1993 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5302` | quality | Line is 1973 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5303` | quality | Line is 835 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5304` | quality | Line is 644 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5305` | quality | Line is 1019 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5306` | quality | Line is 733 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5307` | quality | Line is 1316 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5308` | quality | Line is 1567 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5309` | quality | Line is 733 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5310` | quality | Line is 2608 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5311` | quality | Line is 1767 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5312` | quality | Line is 1753 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5313` | quality | Line is 841 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5314` | quality | Line is 3022 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5315` | quality | Line is 3852 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5316` | quality | Line is 723 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5317` | quality | Line is 4906 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5318` | quality | Line is 4067 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5319` | quality | Line is 2240 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5320` | quality | Line is 829 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5321` | quality | Line is 2398 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5322` | quality | Line is 1662 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5323` | quality | Line is 1234 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5324` | quality | Line is 2604 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5325` | quality | Line is 3802 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5326` | quality | Line is 3633 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5327` | quality | Line is 2410 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5328` | quality | Line is 2837 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5329` | quality | Line is 1646 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5330` | quality | Line is 1957 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5331` | quality | Line is 748 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5332` | quality | Line is 6290 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5333` | quality | Line is 5446 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5334` | quality | Line is 859 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5335` | quality | Line is 1799 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5336` | quality | Line is 3215 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5337` | quality | Line is 3526 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5338` | quality | Line is 733 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5339` | quality | Line is 4109 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5340` | quality | Line is 3268 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5341` | quality | Line is 841 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5342` | quality | Line is 4198 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5343` | quality | Line is 6129 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5344` | quality | Line is 733 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5345` | quality | Line is 8052 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5346` | quality | Line is 7039 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5347` | quality | Line is 909 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5348` | quality | Line is 846 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5349` | quality | Line is 1529 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5350` | quality | Line is 1720 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5351` | quality | Line is 708 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5352` | quality | Line is 2496 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\apollo\generated\graphql.ts:5353` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5353` | quality | Line is 1660 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5354` | quality | Line is 811 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5355` | quality | Line is 1907 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5356` | quality | Line is 1071 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5357` | quality | Line is 811 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5358` | quality | Line is 3479 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5359` | quality | Line is 4709 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5360` | quality | Line is 708 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5361` | quality | Line is 5126 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5362` | quality | Line is 4290 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5363` | quality | Line is 1900 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5364` | quality | Line is 811 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5365` | quality | Line is 1531 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5366` | quality | Line is 2816 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5367` | quality | Line is 718 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5368` | quality | Line is 3172 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5369` | quality | Line is 1879 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5370` | quality | Line is 1735 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\apollo\generated\graphql.ts:5371` | quality | Line is 823 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\components\Files\FilesTreeView.helpers.js:265` | quality | Line is 300 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\components\Files\NoImage.js:17` | quality | Line is 251 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\Files\ResponsiveImage.js:49` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\Files\ResponsiveStorageImage.jsx:120` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\components\StdErrorFallback.js:12` | quality | Line is 247 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\StdErrorFallback.js:13` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\common\UseDnD.js:62` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\common\selects\ScheduleColors.js:12` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\common\selects\StdDynamicSelect.js:14` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\common\selects\StdDynamicSelect.js:45` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\estimate\EstimateEditActions.js:7` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\global-drawer\GlobalDrawer.jsx:14` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\global-drawer\todos\AssignedTodos.jsx:26` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\global-drawer\todos\AssignedTodos.jsx:33` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\BasicTabs.js:9` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\BasicTabs.js:143` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\Files.jsx:130` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:23` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:30` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:115` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:168` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:170` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:173` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:174` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:176` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:234` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\Manage\ToDo.jsx:255` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\project\ProjectDetails\ProjectOverview.tsx:27` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\timetracking\reports\TimeTrackingReports.jsx:151` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:9` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:10` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:13` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:18` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:20` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:23` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:39` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\AddSubTodo.jsx:97` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:9` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:10` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:13` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:14` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:17` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\NewTodoForm.jsx:117` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\SubTodoTable.jsx:5` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoBreadcrumbs.jsx:5` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoBreadcrumbs.jsx:10` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoBreadcrumbs.jsx:24` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoBreadcrumbs.jsx:25` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:28` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:54` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:68` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:81` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:119` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:148` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:150` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:154` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoCellComponents.jsx:186` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:48` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:53` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:55` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:60` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:90` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:92` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:142` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:160` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:206` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:221` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:246` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:312` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:315` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoDrawer.jsx:351` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRow.jsx:14` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRow.jsx:20` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:31` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:34` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:35` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:37` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:41` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoRowGroup.jsx:42` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:263` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:265` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:309` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:323` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:335` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:347` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:359` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:392` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.helpers.js:406` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.jsx:7` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.jsx:11` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoTable.jsx:15` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:23` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:78` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:81` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:90` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:98` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\TodoUpsert.jsx:193` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\todos\todoValidationSchema.js:4` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\users\tabs\UsersTab.jsx:71` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:46` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:53` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:121` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:164` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:166` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:169` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:170` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\AssignedTodos.jsx:172` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:114` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:157` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:159` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:162` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:163` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\components\widgets\CreatedTodos.jsx:165` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\Selections\index.js:3` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\hooks\api\changeorders.js:2` | quality | Line is 204 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\hooks\api\customFilters.js:1` | quality | Line is 210 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\hooks\api\estimateTemplates.js:1` | quality | Line is 234 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\api\functions\storage.js:26` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\hooks\api\helpers.js:123` | quality | Line is 246 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\hooks\api\scheduleItems.js:1` | quality | Line is 210 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\createQbSyncAdapter.js:258` | quality | Line is 221 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\quickbooksApi.js:9` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEstimate.js:112` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\firebaseApi.js:150` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\hooks\thirdparty\OneDrive\useOdClient.js:18` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\layout\Header\AnnouncementsMenu.js:22` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\layout\Navigator\Navigator.js:70` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\layout\theme.js:61` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\layout\theme.ts:104` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\src\pages\_error.js:91` | quality | Line is 233 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\pages\_error.js:109` | quality | Line is 223 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\pages\_error.js:113` | quality | Line is 205 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\src\pages\_error.js:130` | quality | Line is 201 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\store\common\snackbarSlice.ts:57` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\store\common\snackbarSlice.ts:69` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\stories\decorators\ThemeProvider.jsx:5` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\util\client.js:97` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\util\client.js:102` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\util\helpers.js:206` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\src\util\helpers.js:399` | quality | Unfinished work marker left in the code. |
| info | Very long line | `timbersite-frontend\stories\components\common\StdSnackbar.stories.js:37` | quality | Line is 307 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\stories\components\estimate\EstimateSummary.stories.js:141` | quality | Line is 922 chars; consider wrapping. |
| info | Very long line | `timbersite-frontend\tests\hooks\api\functions\storage.test.js:59` | quality | Line is 847 chars; consider wrapping. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\tests\hooks\hooks-util.test.js:136` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `timbersite-frontend\tests\util\helpers.test.js:84` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `utils\proposal-import\0_login.js:7` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `utils\proposal-import\0_login.js:8` | quality | Unfinished work marker left in the code. |
| info | Outstanding TODO/FIXME | `utils\proposal-import\0_login.js:14` | quality | Unfinished work marker left in the code. |

## Optimisations (42)

| Severity | Title | Location | Source | Detail |
| --- | --- | --- | --- | --- |
| low | SELECT * query | `backend\src\services\quickbooks\attachments.js:152` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\classes.js:12` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\customers.js:9` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\employees.js:9` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\estimates.js:9` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\estimates.js:57` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\projects.js:8` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\projects.js:49` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `backend\src\services\quickbooks\timeActivities.js:20` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\organization-settings\tabs\SalesTax.jsx:67` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\organization-settings\tabs\SalesTax.jsx:72` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbConfigSettings.jsx:7` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:78` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:83` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:95` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:96` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:137` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:138` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbCostCodes.jsx:431` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbEmployees.jsx:57` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbEmployees.jsx:70` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbExpenses.jsx:33` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbExpenses.jsx:39` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbExpenses.jsx:97` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbVendors.jsx:26` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbVendors.jsx:124` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbVendors.jsx:154` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QbVendors.jsx:411` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QuickbooksUpsert.js:603` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QuickbooksUpsert.js:608` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\components\thirdparty\quickbooks\QuickbooksUpsert.js:620` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbChangeOrder.js:148` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbCustomer.js:32` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbCustomer.js:73` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEmployee.js:31` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEmployee.js:41` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEstimate.js:97` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEstimate.js:201` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbEstimate.js:246` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbProject.js:35` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbProject.js:81` | quality | Fetching all columns wastes I/O; select only what you need. |
| low | SELECT * query | `timbersite-frontend\src\hooks\api\thirdparty\quickbooks\useSyncQbTimeActivity.js:33` | quality | Fetching all columns wastes I/O; select only what you need. |
