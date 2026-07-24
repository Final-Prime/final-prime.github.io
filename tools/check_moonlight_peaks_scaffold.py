#!/usr/bin/env python3
"""Validate the score-locked Moonlight Peaks living-review scaffold."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "/reviews/moonlight-peaks/"
CANONICAL = f"https://final-prime.github.io{ROUTE}"
PAGE = ROOT / "reviews" / "moonlight-peaks" / "index.html"
CSS = ROOT / "assets" / "moonlight-peaks-dossier.css"
PROTOCOL = ROOT / "docs" / "moonlight-peaks-review-protocol.md"
INTAKE = ROOT / "docs" / "moonlight-peaks-session-intake-template.md"


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"{label} missing required token: {token}")


def main() -> int:
    errors: list[str] = []
    required_files = (PAGE, CSS, PROTOCOL, INTAKE)
    for path in required_files:
        if not path.is_file():
            errors.append(f"Missing Moonlight Peaks file: {path.relative_to(ROOT)}")

    if errors:
        print("Moonlight Peaks scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    page = PAGE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    intake = INTAKE.read_text(encoding="utf-8")

    page_tokens = (
        f'<link rel="canonical" href="{CANONICAL}">',
        'data-review-id="FP-REV-0002"',
        "SCORE LOCKED",
        "Public score",
        "Canonical status",
        "Sketch",
        "MOONLIT",
        "Fantasy vs routine",
        'id="capture"',
        'id="chronicle"',
        'id="completion"',
        'id="capability"',
        'id="questions"',
        'id="roadmap"',
        'id="limits"',
        "Moonlight Peaks and related",
        "/legal/",
        "Daniel Kenessy",
        "All rights reserved.",
    )
    for token in page_tokens:
        require(page, token, "Moonlight page", errors)

    for forbidden in (
        r'data-review-score="\d+"',
        r'data-axis-score="\d+"',
        r'itemprop="ratingValue"',
        r'itemscope\s+itemtype="https://schema.org/Review"',
        r'<strong class="score">\d+',
        r'\b(?:Buy now|Buy on sale|Avoid for now)\b',
    ):
        if re.search(forbidden, page, flags=re.IGNORECASE):
            errors.append(f"Premature public verdict detected: {forbidden}")

    if page.count("<h1") != 1:
        errors.append("Moonlight page must contain exactly one h1")
    if page.count('class="mp-axis"') != 8:
        errors.append("Moonlight page must expose seven MOONLIT axes plus one PLATER bridge")
    if page.count('class="mp-question"') != 12:
        errors.append("Moonlight page must expose twelve initial questions")
    if page.count('class="mp-capability"') != 9:
        errors.append("Moonlight page must expose nine capability cards")

    for token in (
        ".mp-hero",
        ".mp-score-lock",
        ".mp-axis-grid",
        ".mp-capability-grid",
        "@media (max-width: 760px)",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ):
        require(css, token, "Moonlight CSS", errors)

    for token in (
        "FP-REV-0002",
        "MOONLIT",
        "MP-Sxx",
        "MP-CLM-xxx",
        "MP-ISS-xxx",
        "MP-SHOT-xxx",
        "Gate 1",
        "Gate 4",
        "append-only",
        "Narration protocol",
        "Adversarial checks",
    ):
        require(protocol, token, "Moonlight protocol", errors)

    for token in (
        "#[MP-Sxx]",
        "MP-SHOT-xxx",
        "MP-ISS-xxx",
        "MP-ACH-xxx",
        "Do not infer unreported events",
    ):
        require(intake, token, "Moonlight intake", errors)

    registry_checks = {
        ROOT / "reviews" / "index.html": (
            "FP-REV-0002",
            ROUTE,
            "Published dossiers</dt><dd>01",
        ),
        ROOT / "sitemap.xml": (f"<loc>{CANONICAL}</loc>",),
        ROOT / "llms.txt": (CANONICAL, "score-locked evidence dossier"),
    }
    for path, tokens in registry_checks.items():
        if not path.is_file():
            errors.append(f"Missing registry file: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            require(text, token, path.relative_to(ROOT).as_posix(), errors)

    if errors:
        print("Moonlight Peaks scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Moonlight Peaks scaffold validation passed.")
    print("State: FP-REV-0002 / Sketch / score locked")
    print("Public score and buyer action: withheld")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
