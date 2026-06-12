"""Remediation knowledge base.

Maps each Zebra rule (or finding title, for the language-agnostic line rules
whose ``rule`` *is* their title) to a structured explanation:

    what  — plain-English description of what the finding means
    risk  — why it matters / what an attacker or maintainer should worry about
    fix   — concrete steps to resolve it
    refs  — optional further-reading links

The rich HTML/PDF report uses this to turn a bare table row into something a
developer can actually act on. Anything without an entry falls back to a
sensible generic message so the report never shows a blank cell.
"""
from __future__ import annotations

from typing import Dict, List, Optional, TypedDict


class Remedy(TypedDict, total=False):
    what: str
    risk: str
    fix: str
    refs: List[str]


# Keyed by rule id. Line-rule findings set ``rule == title`` so both the rule id
# and the human title are registered where they differ.
REMEDIATION: Dict[str, Remedy] = {
    # ------------------------------------------------------------------ secrets
    "private-key": {
        "what": "A PEM private-key block (RSA/EC/OpenSSH/PGP) is committed in source.",
        "risk": "Anyone with repo access — including its full git history — can "
                "impersonate the key's owner, decrypt traffic, or sign artefacts.",
        "fix": "Rotate the key immediately. Remove it from the working tree and "
               "purge it from history with `git filter-repo` or BFG, then force-push. "
               "Store secrets in a vault (AWS Secrets Manager, HashiCorp Vault) and "
               "inject at runtime via env vars.",
        "refs": ["https://docs.github.com/code-security/secret-scanning"],
    },
    "aws-access-key": {
        "what": "An AWS access key id (AKIA…) is hard-coded in source.",
        "risk": "Paired with a secret it grants programmatic access to your AWS "
                "account — data exfiltration, resource spin-up, and billing abuse.",
        "fix": "Deactivate and delete the key in IAM, rotate it, and purge from git "
               "history. Use IAM roles / instance profiles or short-lived STS "
               "credentials instead of long-lived keys.",
    },
    "aws-secret-key": {
        "what": "An AWS secret access key appears in source.",
        "risk": "Full programmatic control of the associated AWS identity.",
        "fix": "Rotate in IAM, purge from history, and move to a secrets manager. "
               "Enable AWS GuardDuty + key-exposure alerts.",
    },
    "github-token": {
        "what": "A GitHub personal/OAuth/app token is committed.",
        "risk": "Repo, package, and workflow access under the token's scopes — "
                "potential supply-chain compromise.",
        "fix": "Revoke the token in GitHub settings, rotate, and purge from history. "
               "Prefer fine-grained tokens or GitHub Actions OIDC.",
    },
    "slack-token": {
        "what": "A Slack API token (xox…) is committed.",
        "risk": "Read/post access to workspace messages and files.",
        "fix": "Revoke in the Slack app config, rotate, and purge from history.",
    },
    "google-api-key": {
        "what": "A Google API key (AIza…) is committed.",
        "risk": "Quota abuse and, if unrestricted, access to enabled Google APIs.",
        "fix": "Regenerate the key, apply application + API restrictions, and purge "
               "from history.",
    },
    "stripe-key": {
        "what": "A live Stripe secret key (sk_live/rk_live) is committed.",
        "risk": "Direct access to charge customers, issue refunds, and read PII.",
        "fix": "Roll the key in the Stripe dashboard immediately, purge from history, "
               "and load from env/secret store.",
    },
    "jwt": {
        "what": "A hard-coded JSON Web Token is present.",
        "risk": "If still valid it grants whatever the token authorises; it also "
                "leaks the signing structure.",
        "fix": "Treat as a live credential: invalidate the session/secret, and never "
               "commit tokens — mint them at runtime.",
    },
    "generic-secret": {
        "what": "A high-entropy value assigned to an api-key/secret/password/token "
                "variable is committed.",
        "risk": "Likely a live credential granting access to some system.",
        "fix": "Confirm whether it is real; if so rotate and purge from history. Move "
               "to environment variables or a secrets manager. If it is a test "
               "placeholder, replace with an obvious dummy (e.g. 'changeme').",
    },
    "connection-string": {
        "what": "A database/redis connection string embeds an inline password.",
        "risk": "Anyone reading the repo gains direct database access — full data "
                "read/write and possible lateral movement.",
        "fix": "Rotate the database password. Move the connection string to an env "
               "var / secret store and reference it (e.g. `process.env.DATABASE_URL`).",
    },
    # ------------------------------------------------------------- vuln (quality)
    "Use of eval()": {
        "what": "`eval()` executes a string as code at runtime.",
        "risk": "If any part of the input is attacker-influenced this is remote code "
                "execution.",
        "fix": "Remove `eval`. Parse data with `JSON.parse`/`ast.literal_eval`, or "
               "dispatch via an explicit lookup table instead of evaluating code.",
        "refs": ["https://owasp.org/www-community/attacks/Code_Injection"],
    },
    "eval": {  # AST rule id
        "what": "`eval()` executes a string as code at runtime.",
        "risk": "Attacker-influenced input becomes remote code execution.",
        "fix": "Replace with explicit parsing or a dispatch table.",
    },
    "Use of exec()": {
        "what": "`exec()` runs dynamically constructed code.",
        "risk": "Dynamic code execution is a classic RCE sink and defeats static "
                "analysis of what the program actually does.",
        "fix": "Refactor to explicit branching/functions. If you must template "
               "behaviour, use a constrained registry of allowed operations.",
    },
    "exec": {  # AST rule id
        "what": "`exec()` runs dynamically constructed code.",
        "risk": "A remote-code-execution sink.",
        "fix": "Replace with explicit logic or a vetted operation registry.",
    },
    "Shell injection risk": {
        "what": "A shell is invoked with `shell=True` / `os.system` and possibly "
                "untrusted arguments.",
        "risk": "Command injection — an attacker can append `; rm -rf` style payloads.",
        "fix": "Pass arguments as a list without a shell (`subprocess.run([...], "
               "shell=False)`), and never interpolate user input into the command "
               "string. Validate/escape if a shell is unavoidable.",
        "refs": ["https://owasp.org/www-community/attacks/Command_Injection"],
    },
    "Unsafe deserialization": {
        "what": "`pickle.load(s)` deserialises data that may be untrusted.",
        "risk": "Pickle can construct arbitrary objects on load — remote code "
                "execution from a malicious payload.",
        "fix": "Never unpickle untrusted data. Use a safe format (JSON, MessagePack) "
               "or sign+verify the payload before loading.",
    },
    "TLS verification disabled": {
        "what": "Certificate verification is turned off (`verify=False`, "
                "`rejectUnauthorized:false`, `InsecureSkipVerify`).",
        "risk": "The connection is open to man-in-the-middle interception and "
                "credential/data theft, even though it 'looks' encrypted.",
        "fix": "Re-enable verification. For internal/self-signed endpoints, install "
               "the CA cert and trust it explicitly rather than disabling checks. "
               "Scope any exception to a single client, never globally.",
        "refs": ["https://owasp.org/www-community/vulnerabilities/"
                 "Insecure_Transport_Layer_Protection"],
    },
    "Weak hash algorithm": {
        "what": "MD5 or SHA-1 is used.",
        "risk": "Both are broken against collision/preimage attacks and are unfit for "
                "passwords, signatures, or integrity in a security context.",
        "fix": "Use SHA-256+ for integrity, and a slow KDF (bcrypt, scrypt, argon2) "
               "for passwords. MD5/SHA-1 are acceptable only for non-security "
               "checksums.",
    },
    "Possible DOM XSS": {
        "what": "Untrusted data is assigned to `.innerHTML`.",
        "risk": "Injected markup executes as script in the victim's browser — session "
                "theft, defacement, keylogging.",
        "fix": "Use `.textContent` for text, or sanitise HTML with DOMPurify before "
               "insertion. In frameworks, rely on safe binding and avoid "
               "`dangerouslySetInnerHTML`.",
        "refs": ["https://owasp.org/www-community/attacks/xss/"],
    },
    "Possible SQL injection": {
        "what": "A SQL string is built by concatenating or interpolating variables.",
        "risk": "If a value is attacker-controlled they can rewrite the query — data "
                "exfiltration, auth bypass, or destruction.",
        "fix": "Use parameterised queries / prepared statements (bound parameters), "
               "or an ORM that parameterises for you. Never build SQL with string "
               "concatenation of input. NOTE: matches inside generated GraphQL/ORM "
               "type files are usually false positives — exclude `**/generated/**`.",
        "refs": ["https://owasp.org/www-community/attacks/SQL_Injection"],
    },
    # -------------------------------------------------------------------- flaws
    "Outstanding TODO/FIXME": {
        "what": "A TODO/FIXME/HACK/XXX marker is left in the code.",
        "risk": "Tracks unfinished or fragile work that is invisible outside the "
                "source; easy to ship and forget.",
        "fix": "Convert each marker into a tracked issue with an owner, or resolve "
               "and delete it. Add a lint/CI check to keep the count bounded.",
    },
    "Debug statement": {
        "what": "A leftover `console.log` / debug `print` / `debugger` statement.",
        "risk": "Noisy logs, potential leakage of sensitive values, and a `debugger` "
                "can pause execution in production.",
        "fix": "Remove it or route through a proper logger with levels. Enforce with "
               "an ESLint `no-console`/`no-debugger` rule or a pre-commit hook.",
    },
    "Swallowed exception": {
        "what": "An empty `catch {}` / `except: pass` discards the error.",
        "risk": "Failures vanish silently, producing corrupt state and "
                "near-impossible debugging.",
        "fix": "Handle the error meaningfully, or at minimum log it with context and "
               "re-raise. Catch the narrowest exception type you expect.",
    },
    "Very long line": {
        "what": "A source line exceeds 200 characters.",
        "risk": "Hurts readability and code review; often hides multiple statements.",
        "fix": "Wrap or refactor. Configure a formatter (Prettier/Black) and a max "
               "line-length lint rule. Generated files can be excluded from scans.",
    },
    "long-line": {
        "what": "A source line exceeds 200 characters.",
        "risk": "Readability and review friction.",
        "fix": "Run a formatter; exclude generated files.",
    },
    "Overly long function": {
        "what": "A function spans more than ~80 lines.",
        "risk": "Long functions are hard to test, reason about, and reuse; they tend "
                "to accumulate bugs.",
        "fix": "Extract cohesive blocks into well-named helper functions; aim for a "
               "single responsibility per function.",
    },
    "long-function": {
        "what": "A function spans more than ~80 lines.",
        "risk": "Hard to test and maintain.",
        "fix": "Split into smaller, single-purpose functions.",
    },
    "Too many parameters": {
        "what": "A function takes more than 6 parameters.",
        "risk": "Long argument lists are error-prone (easy to mis-order) and signal a "
                "function doing too much.",
        "fix": "Group related parameters into a config/options object or dataclass; "
               "consider splitting the function.",
    },
    "many-params": {
        "what": "A function takes more than 6 parameters.",
        "risk": "Error-prone call sites.",
        "fix": "Pass an options object / dataclass.",
    },
    "Mutable default argument": {
        "what": "A function default value is a mutable list/dict/set.",
        "risk": "The default is shared across all calls, so state leaks between "
                "invocations — a notorious Python bug.",
        "fix": "Default to `None` and create the mutable inside the function body.",
    },
    "mutable-default": {
        "what": "A mutable default argument is shared across calls.",
        "risk": "State leaks between invocations.",
        "fix": "Default to None; allocate inside the function.",
    },
    "Bare except": {
        "what": "A bare `except:` catches everything, including "
                "`KeyboardInterrupt`/`SystemExit`.",
        "risk": "Masks unrelated failures and can make a program un-interruptible.",
        "fix": "Catch the specific exception type(s) you expect; let the rest "
               "propagate.",
    },
    "bare-except": {
        "what": "A bare `except:` catches everything.",
        "risk": "Masks failures; blocks interrupts.",
        "fix": "Catch specific exception types.",
    },
    # ------------------------------------------------------------ optimisations
    "SELECT * query": {
        "what": "A query fetches all columns with `SELECT *`.",
        "risk": "Wastes I/O and memory, breaks on schema changes, and can pull "
                "sensitive columns you did not intend to expose.",
        "fix": "Select only the columns you actually use. For GraphQL/ORM calls, "
               "request a specific field set.",
    },
    "Triple-nested loop": {
        "what": "Three levels of nested loops — O(n³) behaviour.",
        "risk": "Scales poorly; a likely performance cliff as data grows.",
        "fix": "Reduce complexity with hashing/indexing, precomputation, or a better "
               "algorithm; cache repeated work.",
    },
    "nested-loop": {
        "what": "Three levels of nested loops (O(n³)).",
        "risk": "Poor scaling.",
        "fix": "Use hashing/indexing or a better algorithm.",
    },
    "String/list build in loop": {
        "what": "A value is accumulated with `+=` inside a loop.",
        "risk": "Repeated string concatenation is O(n²) in many languages.",
        "fix": "Collect into a list and `''.join()` once, or use a buffer/StringIO.",
    },
    "concat-in-loop": {
        "what": "Accumulating with `+=` in a loop.",
        "risk": "Potentially O(n²).",
        "fix": "Build a list and join once.",
    },
}

_GENERIC: Remedy = {
    "what": "See the finding detail.",
    "risk": "Review in context to assess impact.",
    "fix": "Address per the detail, or suppress if it is a confirmed false positive.",
}


def lookup(rule: Optional[str], title: str) -> Remedy:
    """Best-effort remedy for a finding, keyed by rule id then title."""
    if rule and rule in REMEDIATION:
        return REMEDIATION[rule]
    if title in REMEDIATION:
        return REMEDIATION[title]
    return _GENERIC
