"""Shared helpers: findings model, file walking, tool detection, colours."""
from __future__ import annotations

import fnmatch
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

# ---------------------------------------------------------------------------
# Severity / category vocabulary
# ---------------------------------------------------------------------------
SEVERITIES = ["critical", "high", "medium", "low", "info"]
SEV_RANK = {s: i for i, s in enumerate(SEVERITIES)}

# Categories let us split the final report into the three things the user asked
# for: security vulnerabilities, code flaws, and optimisation opportunities.
CAT_VULN = "vulnerability"
CAT_FLAW = "flaw"
CAT_OPT = "optimisation"


@dataclass
class Finding:
    category: str            # one of CAT_*
    severity: str            # one of SEVERITIES
    title: str
    detail: str
    file: Optional[str] = None
    line: Optional[int] = None
    rule: Optional[str] = None
    source: str = "zebra"    # which scanner produced it

    def location(self) -> str:
        if not self.file:
            return "-"
        return f"{self.file}:{self.line}" if self.line else self.file

    def sort_key(self):
        return (SEV_RANK.get(self.severity, 99), self.category, self.file or "", self.line or 0)


@dataclass
class ScanResult:
    scanner: str
    available: bool = True          # was the underlying tool present?
    skipped_reason: str = ""
    findings: List[Finding] = field(default_factory=list)
    error: str = ""


# ---------------------------------------------------------------------------
# Terminal colour (auto-disabled when not a TTY)
# ---------------------------------------------------------------------------
class C:
    enabled = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None

    @classmethod
    def _w(cls, code: str, s: str) -> str:
        return f"\033[{code}m{s}\033[0m" if cls.enabled else s

    @classmethod
    def bold(cls, s):   return cls._w("1", s)
    @classmethod
    def dim(cls, s):    return cls._w("2", s)
    @classmethod
    def red(cls, s):    return cls._w("31", s)
    @classmethod
    def green(cls, s):  return cls._w("32", s)
    @classmethod
    def yellow(cls, s): return cls._w("33", s)
    @classmethod
    def blue(cls, s):   return cls._w("34", s)
    @classmethod
    def cyan(cls, s):   return cls._w("36", s)


SEV_COLOR = {
    "critical": C.red,
    "high": C.red,
    "medium": C.yellow,
    "low": C.blue,
    "info": C.dim,
}


# ---------------------------------------------------------------------------
# File walking
# ---------------------------------------------------------------------------
DEFAULT_IGNORES = [
    ".git", ".hg", ".svn", "node_modules", "venv", ".venv", "env",
    "__pycache__", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "dist", "build", ".next", ".nuxt", "target", "vendor", "coverage",
    ".idea", ".vscode", ".DS_Store", "*.min.js", "*.lock",
]

# Extensions Zebra's built-in scanners understand for line-level analysis.
SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".rb", ".php", ".java",
    ".c", ".cc", ".cpp", ".h", ".hpp", ".rs", ".sh", ".bash", ".sql",
    ".yaml", ".yml", ".json", ".tf", ".env", ".cfg", ".ini", ".toml",
}


def _ignored(path: str, root: str, patterns: Iterable[str]) -> bool:
    rel = os.path.relpath(path, root)
    name = os.path.basename(path)
    for pat in patterns:
        if fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(rel, pat):
            return True
        # match directory components
        if pat in rel.split(os.sep):
            return True
    return False


def walk_files(root: str, extra_ignores: Optional[List[str]] = None,
               only_source: bool = True, max_bytes: int = 2_000_000) -> Iterable[str]:
    patterns = list(DEFAULT_IGNORES) + list(extra_ignores or [])
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored dirs in place for speed
        dirnames[:] = [d for d in dirnames
                       if not _ignored(os.path.join(dirpath, d), root, patterns)]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if _ignored(full, root, patterns):
                continue
            if only_source and os.path.splitext(fn)[1].lower() not in SOURCE_EXTS:
                continue
            try:
                if os.path.getsize(full) > max_bytes:
                    continue
            except OSError:
                continue
            yield full


def read_text(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except (OSError, UnicodeError):
        return None


# ---------------------------------------------------------------------------
# External tool helpers
# ---------------------------------------------------------------------------
def have(tool: str) -> bool:
    return shutil.which(tool) is not None


def run(cmd: List[str], cwd: Optional[str] = None, timeout: int = 600) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
    )


def rel(path: Optional[str], root: str) -> Optional[str]:
    if not path:
        return path
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return path
