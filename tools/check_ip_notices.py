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
    ROOT / "assets" / "fonts" / "inter-v4.1" / "LICENSE.txt",
    ROOT / "assets" / "fonts" / "inter-v4.1" / "SOURCE.md",
]
PUBLIC_HTML = [
    ROOT / "index.html",
    ROOT / "systems" / "index.html",
    ROOT / "systems" / "async" / "index.html",
    ROOT / "works" / "index.html",
    ROOT / "works" / "realops-01" / "index.html",
    ROOT / "thought" / "index.html",
    ROOT / "reviews" / "index.html",
    ROOT / "reviews" / "metro-2033-redux" / "index.html",
    ROOT / "reviews" / "moonlight-peaks" / "index.html",
    ROOT / "index" / "index.html",
    ROOT / "contact" / "index.html",
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
        for required in (OWNER, "All rights reserved.", "/legal/"):
            if required not in text:
                errors.append(f"Missing static legal notice {required!r} in {path.relative_to(ROOT)}")

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
        for forbidden in ("ensureLegalNotice", "data.legalMark", "data.legalLink", 'document.createElement("meta")'):
            if forbidden in app:
                errors.append(f"assets/app.js must not repair static legal notices at runtime: {forbidden}")

    notice_path = ROOT / "NOTICE"
    if notice_path.is_file():
        notice = notice_path.read_text(encoding="utf-8")
        for phrase in ("Inter v4.1", "The Inter Project Authors", "SIL Open Font License, Version 1.1"):
            if phrase not in notice:
                errors.append(f"NOTICE missing Inter attribution: {phrase}")

    inter_license_path = ROOT / "assets" / "fonts" / "inter-v4.1" / "LICENSE.txt"
    if inter_license_path.is_file():
        inter_license = inter_license_path.read_text(encoding="utf-8")
        for phrase in ("SIL OPEN FONT LICENSE Version 1.1", "Copyright (c) 2016 The Inter Project Authors"):
            if phrase not in inter_license:
                errors.append(f"Inter license missing required phrase: {phrase}")

    inter_source_path = ROOT / "assets" / "fonts" / "inter-v4.1" / "SOURCE.md"
    if inter_source_path.is_file():
        inter_source = inter_source_path.read_text(encoding="utf-8")
        for phrase in (
            "https://github.com/rsms/inter/releases/tag/v4.1",
            "693B77D4F32EE9B8BFC995589B5FAD5E99ADF2832738661F5402F9978429A8E3",
            "copied without modification",
        ):
            if phrase not in inter_source:
                errors.append(f"Inter source record missing provenance: {phrase}")

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
