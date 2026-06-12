"""Dependency vulnerability scanning.

Prefers real vulnerability databases via external tools when present:
  - pip-audit / osv-scanner  -> Python & lockfiles
  - npm audit                -> Node
  - trivy fs                 -> multi-ecosystem
Falls back to a built-in check that simply *detects* and lists manifests so the
user knows what to audit, plus flags unpinned dependencies (a real flaw).
"""
from __future__ import annotations

import json
import os
import re
from typing import List

from ..util import (CAT_FLAW, CAT_VULN, Finding, ScanResult, have, read_text,
                    rel, run, walk_files)

_MANIFESTS = {
    "requirements.txt", "Pipfile", "Pipfile.lock", "poetry.lock",
    "pyproject.toml", "package.json", "package-lock.json", "yarn.lock",
    "pnpm-lock.yaml", "go.mod", "go.sum", "Gemfile", "Gemfile.lock",
    "Cargo.toml", "Cargo.lock", "composer.json", "pom.xml", "build.gradle",
}


def _find_manifests(root: str, ignore) -> List[str]:
    found = []
    for path in walk_files(root, ignore, only_source=False):
        if os.path.basename(path) in _MANIFESTS:
            found.append(path)
    return found


def _pip_audit(root: str, res: ScanResult) -> bool:
    if not have("pip-audit"):
        return False
    try:
        cp = run(["pip-audit", "-f", "json", "--progress-spinner", "off"], cwd=root, timeout=300)
        data = json.loads(cp.stdout or "{}")
    except Exception as e:  # noqa: BLE001
        res.error = f"pip-audit failed: {e}"
        return True
    deps = data.get("dependencies", data) if isinstance(data, dict) else data
    for dep in (deps or []):
        for v in dep.get("vulns", []):
            res.findings.append(Finding(
                category=CAT_VULN, severity="high",
                title=f"Vulnerable dependency: {dep.get('name')} {dep.get('version')}",
                detail=f"{v.get('id')}: {(v.get('description') or '')[:200]}",
                rule=v.get("id"), source="pip-audit"))
    return True


def _npm_audit(root: str, res: ScanResult) -> bool:
    if not (have("npm") and os.path.exists(os.path.join(root, "package.json"))):
        return False
    try:
        cp = run(["npm", "audit", "--json"], cwd=root, timeout=300)
        data = json.loads(cp.stdout or "{}")
    except Exception:  # noqa: BLE001
        return False
    for name, v in (data.get("vulnerabilities") or {}).items():
        sev = v.get("severity", "medium")
        sev = sev if sev in ("critical", "high", "medium", "low") else "medium"
        res.findings.append(Finding(
            category=CAT_VULN, severity=sev,
            title=f"Vulnerable npm package: {name}",
            detail=f"npm audit reports {v.get('severity')} severity issue(s).",
            rule="npm-audit", source="npm-audit"))
    return True


def _trivy(root: str, res: ScanResult) -> bool:
    if not have("trivy"):
        return False
    try:
        cp = run(["trivy", "fs", "--quiet", "--scanners", "vuln", "-f", "json", root], timeout=420)
        data = json.loads(cp.stdout or "{}")
    except Exception:  # noqa: BLE001
        return False
    for r in (data.get("Results") or []):
        for v in (r.get("Vulnerabilities") or []):
            sev = (v.get("Severity") or "MEDIUM").lower()
            sev = sev if sev in ("critical", "high", "medium", "low") else "medium"
            res.findings.append(Finding(
                category=CAT_VULN, severity=sev,
                title=f"{v.get('PkgName')} {v.get('InstalledVersion')} — {v.get('VulnerabilityID')}",
                detail=(v.get("Title") or "")[:200],
                file=rel(r.get("Target"), root), rule=v.get("VulnerabilityID"),
                source="trivy"))
    return True


def _unpinned_python(root: str, res: ScanResult, ignore) -> None:
    """Built-in flaw check: unpinned requirements (reproducibility/security)."""
    req = os.path.join(root, "requirements.txt")
    text = read_text(req)
    if not text:
        return
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("-"):
            continue
        if not re.search(r"[=<>~!]=|@", s):
            res.findings.append(Finding(
                category=CAT_FLAW, severity="low",
                title=f"Unpinned dependency: {s}",
                detail="No version constraint; builds are non-reproducible and may "
                       "silently pull a vulnerable release.",
                file="requirements.txt", line=i, rule="unpinned", source="dependencies"))


def scan(root: str, opts) -> ScanResult:
    res = ScanResult(scanner="dependencies")
    ran_real = False
    ran_real |= _pip_audit(root, res)
    ran_real |= _npm_audit(root, res)
    ran_real |= _trivy(root, res)

    manifests = _find_manifests(root, opts.ignore)
    _unpinned_python(root, res, opts.ignore)

    if not ran_real:
        res.available = False
        names = ", ".join(sorted({os.path.basename(m) for m in manifests})) or "none found"
        res.skipped_reason = (
            "No dependency-audit tool installed (pip-audit / npm / trivy / osv-scanner). "
            f"Manifests present: {names}. Install one to get CVE matches — "
            "e.g. `pip install pip-audit` or `brew install trivy`."
        )
    return res
