"""Git diff acquisition and parsing for code review.

Produces a list of FileDiff objects, each carrying the unified-diff hunks plus
the set of *added* line numbers (new-file side) so we can (a) scope findings to
changed lines and (b) anchor inline review comments.
"""
from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")


@dataclass
class FileDiff:
    path: str                       # new-file path (b/...)
    old_path: Optional[str] = None
    status: str = "modified"        # added | modified | deleted | renamed
    hunks: str = ""                 # the raw unified-diff text for this file
    added_lines: Dict[int, str] = field(default_factory=dict)  # new lineno -> text
    is_binary: bool = False

    def added_line_set(self) -> Set[int]:
        return set(self.added_lines)


def _run_git(args: List[str], cwd: str) -> str:
    cp = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    if cp.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {cp.stderr.strip()}")
    return cp.stdout


def is_git_repo(root: str) -> bool:
    try:
        _run_git(["rev-parse", "--is-inside-work-tree"], root)
        return True
    except Exception:  # noqa: BLE001
        return False


def default_base(root: str) -> str:
    """Best-effort base ref: merge-base against main/master, else HEAD~1."""
    for branch in ("origin/main", "origin/master", "main", "master"):
        try:
            mb = _run_git(["merge-base", "HEAD", branch], root).strip()
            if mb:
                return mb
        except Exception:  # noqa: BLE001
            continue
    return "HEAD~1"


def get_diff(root: str, base: Optional[str], head: Optional[str]) -> str:
    """Return unified diff text. If head is None, diff base..working-tree."""
    base = base or default_base(root)
    if head:
        return _run_git(["diff", "--no-color", "-U3", f"{base}...{head}"], root)
    # base vs working tree (staged + unstaged)
    return _run_git(["diff", "--no-color", "-U3", base], root)


def parse_diff(diff_text: str) -> List[FileDiff]:
    files: List[FileDiff] = []
    cur: Optional[FileDiff] = None
    new_lineno = 0
    lines = diff_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("diff --git"):
            if cur:
                files.append(cur)
            cur = FileDiff(path="?")
            cur.hunks = line + "\n"
            i += 1
            continue
        if cur is None:
            i += 1
            continue
        cur.hunks += line + "\n"
        if line.startswith("Binary files"):
            cur.is_binary = True
        elif line.startswith("rename from "):
            cur.old_path = line[len("rename from "):].strip()
            cur.status = "renamed"
        elif line.startswith("rename to "):
            cur.path = line[len("rename to "):].strip()
        elif line.startswith("new file"):
            cur.status = "added"
        elif line.startswith("deleted file"):
            cur.status = "deleted"
        elif line.startswith("--- "):
            op = line[4:].strip()
            cur.old_path = None if op == "/dev/null" else op[2:] if op.startswith("a/") else op
        elif line.startswith("+++ "):
            np = line[4:].strip()
            if np != "/dev/null":
                cur.path = np[2:] if np.startswith("b/") else np
        else:
            m = _HUNK_RE.match(line)
            if m:
                new_lineno = int(m.group(1))
            elif line.startswith("+") and not line.startswith("+++"):
                cur.added_lines[new_lineno] = line[1:]
                new_lineno += 1
            elif line.startswith("-") and not line.startswith("---"):
                pass  # removed line: new-file counter unchanged
            elif line.startswith("\\"):
                pass  # "\ No newline at end of file"
            else:
                new_lineno += 1  # context line advances new-file counter
        i += 1
    if cur:
        files.append(cur)
    return [f for f in files if f.path != "?" and not f.is_binary]


def changed_line_index(files: List[FileDiff]) -> Dict[str, Set[int]]:
    """Map relative path -> set of added line numbers, for scoping findings."""
    out: Dict[str, Set[int]] = {}
    for f in files:
        if f.status != "deleted":
            out[f.path] = f.added_line_set()
    return out
