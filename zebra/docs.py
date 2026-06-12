"""Document -> Markdown conversion (the `zebra md` command).

Primary engine is Microsoft's `markitdown`, which converts PDF, DOCX, PPTX,
XLSX, HTML, images (with OCR), audio (transcription) and more into clean
Markdown. We import it lazily so the rest of Zebra works without it installed.
"""
from __future__ import annotations

import os
from typing import List, Optional


def _markitdown_convert(src: str) -> str:
    from markitdown import MarkItDown  # lazy import
    md = MarkItDown()
    return md.convert(src).text_content


def _fallback_convert(src: str) -> Optional[str]:
    """Best-effort conversion for plain/text-ish files without markitdown."""
    ext = os.path.splitext(src)[1].lower()
    if ext in (".md", ".markdown", ".txt", ".rst"):
        with open(src, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    if ext in (".html", ".htm"):
        try:
            import re
            with open(src, "r", encoding="utf-8", errors="replace") as fh:
                html = fh.read()
            text = re.sub(r"<(script|style)[\s\S]*?</\1>", "", html, flags=re.I)
            text = re.sub(r"<[^>]+>", "", text)
            return re.sub(r"\n{3,}", "\n\n", text).strip()
        except Exception:  # noqa: BLE001
            return None
    return None


def _markitdown_ready() -> bool:
    """True only if a *functional* markitdown (>=0.0.1a2, Python 3.10+) is present.

    The 0.0.1a1 placeholder published for Python 3.9 ships no `MarkItDown`
    class, so we feature-detect rather than trust the bare import.
    """
    try:
        from markitdown import MarkItDown  # noqa: F401
        return True
    except Exception:  # noqa: BLE001
        return False


def convert(sources: List[str], out_dir: Optional[str]) -> int:
    """Convert each source file to Markdown. Returns count converted."""
    have_mid = _markitdown_ready()

    if not have_mid:
        print("\033[33m[zebra md]\033[0m full markitdown not available — using "
              "built-in fallback (txt/md/html only).")
        print("           For PDF/DOCX/PPTX/XLSX/image/audio support, install on "
              "Python 3.10+:  pip install 'markitdown[all]'\n")

    done = 0
    for src in sources:
        if not os.path.isfile(src):
            print(f"  skip (not a file): {src}")
            continue
        try:
            content = _markitdown_convert(src) if have_mid else _fallback_convert(src)
        except Exception as e:  # noqa: BLE001
            print(f"  error converting {src}: {e}")
            continue
        if content is None:
            print(f"  unsupported without markitdown: {src}  (pip install 'markitdown[all]')")
            continue

        base = os.path.splitext(os.path.basename(src))[0] + ".md"
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)
            dest = os.path.join(out_dir, base)
            with open(dest, "w", encoding="utf-8") as fh:
                fh.write(content)
            print(f"  \033[32m✓\033[0m {src} -> {dest}")
        else:
            # print to stdout, separated by file headers
            print(f"\n<!-- ===== {src} ===== -->\n")
            print(content)
        done += 1
    return done
