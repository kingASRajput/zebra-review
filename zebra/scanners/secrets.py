"""Built-in secret / credential scanner (no external dependencies).

Catches the high-value, low-false-positive leaks: cloud keys, private keys,
tokens and hard-coded passwords. For deep coverage Zebra will also shell out to
gitleaks / trufflehog when they are installed (see scanners/sast.py).
"""
from __future__ import annotations

import math
import re
from collections import Counter
from typing import List

from ..util import CAT_VULN, Finding, ScanResult, read_text, rel, walk_files

# (rule id, severity, compiled regex, human title)
_PATTERNS = [
    ("aws-access-key", "critical", re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
     "AWS access key id"),
    ("aws-secret-key", "critical",
     re.compile(r"(?i)aws.{0,20}?(secret|private).{0,20}?['\"][0-9a-zA-Z/+]{40}['\"]"),
     "AWS secret access key"),
    ("private-key", "critical",
     re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----"),
     "Private key block"),
    ("github-token", "high", re.compile(r"\b(ghp|gho|ghu|ghs|ghr)_[0-9A-Za-z]{36}\b"),
     "GitHub token"),
    ("slack-token", "high", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,}\b"),
     "Slack token"),
    ("google-api-key", "high", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b"),
     "Google API key"),
    ("stripe-key", "critical", re.compile(r"\b(sk|rk)_live_[0-9A-Za-z]{20,}\b"),
     "Stripe live secret key"),
    ("jwt", "medium", re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{6,}\b"),
     "Hard-coded JWT"),
    ("generic-secret", "medium",
     re.compile(r"(?i)(api[_-]?key|secret|passwd|password|token|access[_-]?key)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
     "Hard-coded credential"),
    ("connection-string", "high",
     re.compile(r"(?i)(postgres|postgresql|mysql|mongodb(\+srv)?|redis)://[^\s'\"]*:[^\s'\"@]+@"),
     "Connection string with inline password"),
]

# Lines containing these markers are almost always safe placeholders.
_SAFE = re.compile(r"(?i)(example|sample|dummy|placeholder|your[_-]?|xxx+|changeme|<.*>|\$\{|process\.env|os\.environ|getenv)")


def _shannon(s: str) -> float:
    if not s:
        return 0.0
    counts = Counter(s)
    n = len(s)
    return -sum((c / n) * math.log2(c / n) for c in counts.values())


def scan(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="secrets")
    for path in walk_files(root, opts.ignore):
        text = read_text(path)
        if text is None:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if len(line) > 1000:
                continue
            for rule, sev, rx, title in _PATTERNS:
                m = rx.search(line)
                if not m:
                    continue
                if rule == "generic-secret" and _SAFE.search(line):
                    continue
                # high-entropy guard for the noisy generic rule
                if rule == "generic-secret":
                    val = line.split("=")[-1].split(":")[-1].strip(" '\";")
                    if _shannon(val) < 3.0:
                        continue
                res.findings.append(Finding(
                    category=CAT_VULN, severity=sev, title=title,
                    detail=f"Potential {title.lower()} committed in source.",
                    file=rel(path, root), line=i, rule=rule, source="secrets",
                ))
    return res
