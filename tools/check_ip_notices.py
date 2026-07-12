#!/usr/bin/env python3
"""Verify Final Prime copyright, trademark, and legal notice boundaries."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Daniel Kenessy"
REQUIRED_FILES = [
    ROOT / "LICENSE",
    ROOT / "NOTICE",
    ROOT / "TRADEMARKS.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    ROOT / "docs" / "ip-policy.md",
    ROOT / "docs" / "ip-register.md",
    ROOT / "legal" / "index.html",
]
PUBLIC_HTML = [
    ROOT / "index.html",
    ROOT / "systems" / "index.html",
    ROOT / "works" / "index.html",
    ROOT / "thought" / "index.html",
    ROOT / "reviews" / "index.html",
    ROOT / "reviews" / "metro-2033-redux" / "index.html",
    ROOT / "index" / "index.html",
    ROOT / "legal" / "index.html",
    ROOT / "404.html",
]
CLAIMED_MARKS = [
    "Final Prime",
    "FINAL / PRIME",
    "A/SYNC",
    "Prime Compression",
    "VRAXION",
    "AlphaSync",
    "INSTNCT",
]


def main() -> int:
    errors: list[str] = []

    for path in REQUIRED_FILES:
        if not path.is_file():
            errors.append(f"Missing required IP file: {path.relative_to(ROOT)}")

    for path in PUBLIC_HTML:
        if not path.is_file():
            errors.append(f"Missing public HTML file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        if "®" in text:
            errors.append(f"Registered trademark symbol is not allowed before registration: {path.relative_to(ROOT)}")
        if path.name != "404.html" and path.parent.name != "legal":
            if "/legal/" not in text and "/assets/app.js" not in text:
                errors.append(f"Missing legal route or shared legal injector in {path.relative_to(ROOT)}")

    license_path = ROOT / "LICENSE"
    if license_path.is_file():
        license_text = license_path.read_text(encoding="utf-8")
        for phrase in ("All rights reserved.", "No license or permission is granted", OWNER):
            if phrase not in license_text:
                errors.append(f"LICENSE missing required phrase: {phrase}")

    marks_path = ROOT / "TRADEMARKS.md"
    if marks_path.is_file():
        mark_text = marks_path.read_text(encoding="utf-8")
        if OWNER not in mark_text:
            errors.append("TRADEMARKS.md does not name the current owner")
        for mark in CLAIMED_MARKS:
            if mark not in mark_text:
                errors.append(f"TRADEMARKS.md missing claimed mark: {mark}")
        if "registered trademark symbol must not be used" not in mark_text:
            errors.append("TRADEMARKS.md missing pre-registration symbol rule")

    sitemap_path = ROOT / "sitemap.xml"
    if sitemap_path.is_file() and "https://final-prime.github.io/legal/" not in sitemap_path.read_text(encoding="utf-8"):
        errors.append("sitemap.xml does not include /legal/")

    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        for required in ("LICENSE", "TRADEMARKS.md", OWNER, "/legal/"):
            if required not in readme:
                errors.append(f"README.md missing IP reference: {required}")

    app_path = ROOT / "assets" / "app.js"
    if app_path.is_file():
        app = app_path.read_text(encoding="utf-8")
        for required in (OWNER, "/legal/", "All rights reserved."):
            if required not in app:
                errors.append(f"assets/app.js missing site-wide legal notice component: {required}")

    if errors:
        print("IP notice check failed.")
        for error in errors:
            print(f"- {error}")
        return 1

    print("IP notice check passed.")
    print(f"Rights holder: {OWNER}")
    print(f"Public HTML checked: {len(PUBLIC_HTML)}")
    print(f"Claimed marks checked: {len(CLAIMED_MARKS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
