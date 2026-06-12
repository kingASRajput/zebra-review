"""Built-in code-quality scanner: dangerous-pattern flaws + optimisation hints.

Language-agnostic line heuristics plus a Python AST pass. Designed for high
signal: every rule here flags something a reviewer would genuinely comment on.
"""
from __future__ import annotations

import ast
import os
import re
from typing import List

from ..util import (CAT_FLAW, CAT_OPT, CAT_VULN, Finding, ScanResult,
                    read_text, rel, walk_files)

# --- language-agnostic dangerous patterns (regex, severity, category, title) --
_LINE_RULES = [
    (re.compile(r"\beval\s*\("), "high", CAT_VULN, "Use of eval()",
     "Dynamic eval can execute arbitrary code; avoid or sanitise input."),
    (re.compile(r"\bexec\s*\("), "high", CAT_VULN, "Use of exec()",
     "Executing dynamic code is dangerous; prefer explicit logic."),
    (re.compile(r"(?i)\bos\.system\s*\(|\bsubprocess\.[a-z]+\([^)]*shell\s*=\s*True"),
     "high", CAT_VULN, "Shell injection risk",
     "Shell=True / os.system with untrusted input enables command injection."),
    (re.compile(r"\bpickle\.loads?\s*\("), "high", CAT_VULN, "Unsafe deserialization",
     "pickle on untrusted data allows remote code execution."),
    (re.compile(r"(?i)verify\s*=\s*False|rejectUnauthorized\s*:\s*false|InsecureSkipVerify"),
     "high", CAT_VULN, "TLS verification disabled",
     "Disabling certificate verification exposes traffic to MITM."),
    (re.compile(r"(?i)\b(md5|sha1)\s*\("), "medium", CAT_VULN, "Weak hash algorithm",
     "MD5/SHA1 are broken for security use; prefer SHA-256+ / bcrypt / argon2."),
    (re.compile(r"\.innerHTML\s*="), "medium", CAT_VULN, "Possible DOM XSS",
     "Assigning to innerHTML with untrusted data can inject scripts."),
    (re.compile(r"(?i)(select|insert|update|delete)\b.*\+\s*\w+|f['\"].*(select|insert|update|delete).*\{"),
     "high", CAT_VULN, "Possible SQL injection",
     "String-built SQL; use parameterised queries instead."),
    (re.compile(r"(?i)\b(TODO|FIXME|HACK|XXX)\b"), "info", CAT_FLAW, "Outstanding TODO/FIXME",
     "Unfinished work marker left in the code."),
    (re.compile(r"(?i)\bconsole\.log\s*\(|\bprint\s*\(.*debug|\bdebugger\b"),
     "low", CAT_FLAW, "Debug statement",
     "Leftover debug output; remove before release."),
    (re.compile(r"\bcatch\s*\([^)]*\)\s*\{\s*\}|except\s*:\s*pass"),
     "medium", CAT_FLAW, "Swallowed exception",
     "Empty catch/except hides errors and complicates debugging."),
]

_OPT_LINE_RULES = [
    (re.compile(r"(?i)select\s+\*\s+from"), "low", CAT_OPT, "SELECT * query",
     "Fetching all columns wastes I/O; select only what you need."),
]


def _line_pass(path: str, text: str, root: str, out: List[Finding]) -> None:
    in_block_comment = False
    for i, line in enumerate(text.splitlines(), 1):
        for rx, sev, cat, title, detail in _LINE_RULES + _OPT_LINE_RULES:
            if rx.search(line):
                out.append(Finding(category=cat, severity=sev, title=title,
                                   detail=detail, file=rel(path, root), line=i,
                                   rule=title, source="quality"))
        # long-line readability flaw (skip data files)
        if len(line) > 200 and path.endswith((".py", ".js", ".ts", ".go", ".java")):
            out.append(Finding(category=CAT_FLAW, severity="info",
                               title="Very long line",
                               detail=f"Line is {len(line)} chars; consider wrapping.",
                               file=rel(path, root), line=i, rule="long-line",
                               source="quality"))


# --------------------------- Python AST analysis ---------------------------
class _PyVisitor(ast.NodeVisitor):
    def __init__(self, path: str, root: str):
        self.path = rel(path, root)
        self.out: List[Finding] = []

    def _add(self, node, sev, cat, title, detail, rule):
        self.out.append(Finding(category=cat, severity=sev, title=title,
                                detail=detail, file=self.path,
                                line=getattr(node, "lineno", None),
                                rule=rule, source="quality-ast"))

    def visit_FunctionDef(self, node):
        # length / complexity heuristics -> flaws & optimisation
        length = (max((getattr(n, "lineno", node.lineno) for n in ast.walk(node)),
                      default=node.lineno) - node.lineno)
        if length > 80:
            self._add(node, "medium", CAT_FLAW, "Overly long function",
                      f"'{node.name}' spans ~{length} lines; consider splitting.",
                      "long-function")
        args = node.args
        n_args = len(args.args) + len(args.kwonlyargs)
        if n_args > 6:
            self._add(node, "low", CAT_FLAW, "Too many parameters",
                      f"'{node.name}' takes {n_args} params; consider a config object.",
                      "many-params")
        # nested-loop optimisation hint
        self._check_nested_loops(node)
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def _check_nested_loops(self, func):
        for n in ast.walk(func):
            if isinstance(n, (ast.For, ast.While)):
                for child in ast.walk(n):
                    if child is not n and isinstance(child, (ast.For, ast.While)):
                        for gc in ast.walk(child):
                            if gc is not child and isinstance(gc, (ast.For, ast.While)):
                                self._add(n, "low", CAT_OPT, "Triple-nested loop",
                                          "O(n^3) loop nesting; review for a better "
                                          "algorithm or caching.", "nested-loop")
                                return

    def visit_Call(self, node):
        f = node.func
        # mutable default args, dangerous builtins
        if isinstance(f, ast.Name) and f.id in ("eval", "exec"):
            self._add(node, "high", CAT_VULN, f"Use of {f.id}()",
                      f"{f.id}() executes dynamic code.", f.id)
        self.generic_visit(node)

    def visit_arguments(self, node):
        for default in node.defaults:
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self._add(default, "medium", CAT_FLAW, "Mutable default argument",
                          "Mutable default args are shared across calls; use None.",
                          "mutable-default")
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.type is None:
            self._add(node, "low", CAT_FLAW, "Bare except",
                      "Bare 'except:' catches everything incl. KeyboardInterrupt.",
                      "bare-except")
        self.generic_visit(node)

    def visit_Compare(self, node):
        # string concat in loop is hard to catch statically; flag '+ ' on str in For handled elsewhere
        self.generic_visit(node)


def _python_pass(path: str, text: str, root: str, out: List[Finding]) -> None:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return
    v = _PyVisitor(path, root)
    v.visit(tree)
    out.extend(v.out)
    # string concatenation inside loops -> optimisation
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While)):
            for child in ast.walk(node):
                if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                    if isinstance(child.target, ast.Name):
                        out.append(Finding(
                            category=CAT_OPT, severity="info",
                            title="String/list build in loop",
                            detail="Accumulating with += in a loop can be O(n^2) for "
                                   "strings; consider ''.join() or a list.",
                            file=rel(path, root), line=child.lineno,
                            rule="concat-in-loop", source="quality-ast"))
                        break


def scan(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="quality")
    for path in walk_files(root, opts.ignore):
        text = read_text(path)
        if text is None:
            continue
        _line_pass(path, text, root, res.findings)
        if path.endswith(".py"):
            _python_pass(path, text, root, res.findings)
    return res
