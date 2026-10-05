"""Programming-language detection from code and/or filename.

Pure module: no I/O. Total and deterministic (requirement 1.2, test 6.2):
never raises, always returns a value from ``KNOWN_LANGUAGES``.
"""

from __future__ import annotations

# Canonical language name -> file extension used for the vault tree.
EXTENSIONS: dict[str, str] = {
    "python": "py",
    "java": "java",
    "cpp": "cpp",
    "c": "c",
    "javascript": "js",
    "typescript": "ts",
    "go": "go",
    "rust": "rs",
    "unknown": "txt",
}

KNOWN_LANGUAGES = frozenset(EXTENSIONS)

_EXT_TO_LANG: dict[str, str] = {
    "py": "python",
    "java": "java",
    "cpp": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "c": "c",
    "js": "javascript",
    "mjs": "javascript",
    "ts": "typescript",
    "go": "go",
    "rs": "rust",
}


def extension_for(language: str) -> str:
    """Return the file extension for a canonical language name."""
    return EXTENSIONS.get(language, EXTENSIONS["unknown"])


def _from_filename(filename: str | None) -> str | None:
    if not filename or "." not in filename:
        return None
    ext = filename.rsplit(".", 1)[-1].strip().lower()
    return _EXT_TO_LANG.get(ext)


def _from_code(code: str) -> str | None:
    """Heuristic signals scanned over the raw source text (no execution)."""
    text = code
    # Order matters: more specific signals first.
    if "#include" in text or "std::" in text or "using namespace std" in text:
        return "cpp" if ("std::" in text or "cout" in text or "::" in text) else "c"
    if "public static void main" in text or "System.out.print" in text:
        return "java"
    if "func " in text and "package " in text:
        return "go"
    if "fn " in text and ("let mut" in text or "println!" in text):
        return "rust"
    if ": " in text and ("interface " in text or ": number" in text or ": string" in text):
        return "typescript"
    if "console.log" in text or "function " in text or "=>" in text or "const " in text:
        return "javascript"
    if "def " in text or "import " in text or "print(" in text or "class " in text:
        return "python"
    return None


def detect_language(code: str, filename: str | None = None) -> str:
    """Detect the language from a filename extension, then the code body.

    Falls back to ``"unknown"`` when no signal is found. Always returns a
    member of :data:`KNOWN_LANGUAGES` and never raises.
    """
    from_name = _from_filename(filename)
    if from_name is not None:
        return from_name
    from_body = _from_code(code or "")
    if from_body is not None:
        return from_body
    return "unknown"
