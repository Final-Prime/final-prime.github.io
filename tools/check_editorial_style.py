#!/usr/bin/env python3
"""Reject long dashes in Final Prime repository text."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {"\u2013": "U+2013 EN DASH", "\u2014": "U+2014 EM DASH"}
TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".md",
    ".py",
    ".svg",
    ".txt",
    ".xml",
    ".yml",
    ".yaml",
}
SKIP_PARTS = {".git", "__pycache__", "node_modules"}


def iter_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name in {"LICENSE", "NOTICE"} or path.suffix.lower() in TEXT_SUFFIXES:
            yield path


def main() -> int:
    violations = []
    for path in sorted(iter_text_files()):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for character, label in FORBIDDEN.items():
                if character in line:
                    violations.append((path.relative_to(ROOT), line_number, label, line.strip()))

    if violations:
        print("Editorial style check failed. Long dashes are forbidden.")
        for path, line_number, label, line in violations:
            print(f"{path}:{line_number}: {label}: {line}")
        return 1

    print("Editorial style check passed. No U+2013 or U+2014 characters found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
