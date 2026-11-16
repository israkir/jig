"""Fail when a committed store has a plaintext value or an age private key is in the tree.

This check does not decrypt. It reads files. A value that is not SOPS ciphertext is a failure.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

SKIP = {
    ".git",
    ".venv",
    ".next",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "node_modules",
    "runtime",
}
LEAF = re.compile(r"^\s*(?P<key>[A-Za-z0-9_.-]+):\s+(?P<value>\S.*)$")
PRIVATE_KEY = "AGE-SECRET-" + "KEY-1"
MAX_BYTES = 1_000_000


def is_store(path: Path) -> bool:
    return path.name.endswith(".enc.yaml") or path.name.endswith(".enc.yml")


def read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > MAX_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None


def plaintext_keys(text: str) -> list[str]:
    """Key names whose values are not SOPS ciphertext. Empty when the store is encrypted."""
    if "\nsops:" not in text:
        return ["<missing sops metadata>"]
    body = text.split("\nsops:", 1)[0]
    found = [
        match["key"]
        for line in body.splitlines()
        if (match := LEAF.match(line)) and not match["value"].startswith("ENC[")
    ]
    if "ENC[" not in body:
        found.append("<no encrypted values>")
    return found


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP]
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            yield path


def scan(root: Path) -> list[str]:
    failures: list[str] = []
    for path in iter_files(root):
        text = read_text(path)
        if text is None:
            continue
        relative = path.relative_to(root)
        if PRIVATE_KEY in text:
            failures.append(f"{relative}: age private key")
        if is_store(path):
            keys = plaintext_keys(text)
            if keys:
                failures.append(f"{relative}: plaintext values for {', '.join(keys)}")
    return failures


def main() -> int:
    failures = scan(Path.cwd())
    if failures:
        sys.stderr.write("\n".join(failures) + "\n")
        return 1
    sys.stdout.write("ok\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
