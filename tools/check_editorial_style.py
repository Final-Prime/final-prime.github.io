#!/usr/bin/env python3
"""Reject long dashes in public Final Prime website copy."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN = {"\u2013": "U+2013 EN DASH", "\u2014": "U+2014 EM DASH"}
PUBLIC_FILES = [
    ROOT / "index.html",
    ROOT / "404.html",
    ROOT / "site.webmanifest",
    ROOT / "sitemap.xml",
]
PUBLIC_DIRS = [
    ROOT / "assets",
    ROOT / "reviews",
    ROOT / "works",
    ROOT / "index",
    ROOT / ".well-known",
]
TEXT_SUFFIXES = {".html", ".js", ".json", ".xml", ".svg", ".txt"}


def iter_public_files():
    for path in PUBLIC_FILES:
        if path.is_file():
            yield path
    for directory in PUBLIC_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def main() -> int:
    violations = []
    for path in sorted(set(iter_public_files())):
        text = path.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for character, label in FORBIDDEN.items():
                if character in line:
                    violations.append((path.relative_to(ROOT), line_number, label, line.strip()))

    if violations:
        print("Editorial style check failed. Long dashes are forbidden in public copy.")
        for path, line_number, label, line in violations:
            print(f"{path}:{line_number}: {label}: {line}")
        return 1

    print("Editorial style check passed. No U+2013 or U+2014 characters found in public copy.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
