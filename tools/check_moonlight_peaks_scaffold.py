#!/usr/bin/env python3
"""Validate the score-locked Moonlight Peaks living-review dossier."""

from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "/reviews/moonlight-peaks/"
CANONICAL = f"https://final-prime.github.io{ROUTE}"
PAGE = ROOT / "reviews" / "moonlight-peaks" / "index.html"
CSS = ROOT / "assets" / "moonlight-peaks-dossier.css"
JS = ROOT / "assets" / "moonlight-peaks-dossier.js"
PROTOCOL = ROOT / "docs" / "moonlight-peaks-review-protocol.md"
INTAKE = ROOT / "docs" / "moonlight-peaks-session-intake-template.md"
MANIFEST = ROOT / "docs" / "moonlight-peaks-asset-manifest.md"
EVIDENCE = ROOT / "docs" / "moonlight-peaks-evidence-board.md"
SYNC_RECEIPT = ROOT / "docs" / "moonlight-peaks-sync-v003.md"
CURATED = ROOT / "assets" / "reviews" / "moonlight-peaks" / "curated"
SOCIAL = (
    ROOT
    / "assets"
    / "reviews"
    / "moonlight-peaks"
    / "social"
    / "moonlight-peaks-first-contact-og.png"
)
CAPTURES = tuple(
    ROOT / "docs" / "moonlight-peaks-captures" / name
    for name in (
        "MP-S01-CAPTURE-02.md",
        "MP-S01-CAPTURE-03-AMENDMENT.md",
        "MP-S01-CAPTURE-04.md",
        "MP-S01-CAPTURE-05.md",
        "MP-S01-CAPTURE-06.md",
        "MP-S01-CAPTURE-07.md",
    )
)


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"{label} missing required token: {token}")


def png_contract(path: Path, expected_size: tuple[int, int] | None = None) -> list[str]:
    """Return contract errors for a deliberately minimal public PNG."""
    errors: list[str] = []
    if not path.is_file():
        return [f"Missing public PNG: {path.relative_to(ROOT)}"]
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return [f"Invalid PNG signature: {path.relative_to(ROOT)}"]

    chunks: list[bytes] = []
    width = height = 0
    cursor = 8
    try:
        while cursor < len(data):
            length = struct.unpack(">I", data[cursor : cursor + 4])[0]
            chunk = data[cursor + 4 : cursor + 8]
            payload = data[cursor + 8 : cursor + 8 + length]
            chunks.append(chunk)
            if chunk == b"IHDR":
                width, height = struct.unpack(">II", payload[:8])
            cursor += 12 + length
            if chunk == b"IEND":
                break
    except (struct.error, ValueError):
        return [f"Malformed PNG structure: {path.relative_to(ROOT)}"]

    forbidden = sorted({chunk for chunk in chunks if chunk not in {b"IHDR", b"IDAT", b"IEND"}})
    if forbidden:
        names = ", ".join(chunk.decode("ascii", errors="replace") for chunk in forbidden)
        errors.append(f"Unexpected PNG chunks in {path.relative_to(ROOT)}: {names}")
    if not chunks or chunks[0] != b"IHDR" or chunks[-1] != b"IEND" or b"IDAT" not in chunks:
        errors.append(f"Incomplete PNG chunk sequence: {path.relative_to(ROOT)}")
    if expected_size and (width, height) != expected_size:
        errors.append(
            f"Wrong PNG dimensions for {path.relative_to(ROOT)}: "
            f"{width}x{height}, expected {expected_size[0]}x{expected_size[1]}"
        )
    return errors


def main() -> int:
    errors: list[str] = []
    required_files = (
        PAGE,
        CSS,
        JS,
        PROTOCOL,
        INTAKE,
        MANIFEST,
        EVIDENCE,
        SYNC_RECEIPT,
        *CAPTURES,
    )
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
    js = JS.read_text(encoding="utf-8")
    protocol = PROTOCOL.read_text(encoding="utf-8")
    intake = INTAKE.read_text(encoding="utf-8")
    manifest = MANIFEST.read_text(encoding="utf-8")
    evidence = EVIDENCE.read_text(encoding="utf-8")
    receipt = SYNC_RECEIPT.read_text(encoding="utf-8")

    page_tokens = (
        f'<link rel="canonical" href="{CANONICAL}">',
        'data-review-id="FP-REV-0002"',
        "SCORE LOCKED",
        "Public score",
        "Current record state",
        "NEW MOON",
        "Sketch",
        "MP-S01 open",
        "MOONLIT",
        "Fantasy vs routine",
        'id="now"',
        'id="first-contact"',
        'id="method"',
        'id="moonlit"',
        'id="evidence"',
        'id="field-log"',
        'id="completion"',
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
    if page.count('class="mp-axis"') != 7:
        errors.append("Moonlight page must expose exactly seven MOONLIT axes")
    question_clusters = re.findall(
        r'<section class="mp-question-cluster[^>]*>(.*?)</section>', page, flags=re.DOTALL
    )
    if len(question_clusters) != 3 or sum(cluster.count("<li>") for cluster in question_clusters) != 12:
        errors.append("Moonlight page must expose three question clusters and twelve routed questions")
    if page.count('class="mp-claim-card"') != 15:
        errors.append("Moonlight page must expose fifteen bounded evidence claims")

    for shot in range(1, 18):
        token = f"MP-SHOT-{shot:03d}"
        require(page, token, "Moonlight page", errors)
        require(manifest, token, "Moonlight asset manifest", errors)
    require(evidence, "State: `Sketch / score locked`", "Moonlight evidence board", errors)
    for token in ("Sketch / New Moon", "MP-S01", "score, grade and buyer action remain locked"):
        require(receipt, token, "Moonlight v003 sync receipt", errors)

    for token in (
        ".mp-hero",
        ".mp-score-lock",
        ".mp-axis-grid",
        ".mp-evidence-gallery",
        ".mp-claim-grid",
        ".mp-question-clusters",
        "@media (max-width: 760px)",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ):
        require(css, token, "Moonlight CSS", errors)

    for token in ("[data-section-nav]", "[data-track-section]", "aria-current"):
        require(js, token, "Moonlight JS", errors)

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

    curated = sorted(CURATED.glob("MP-SHOT-???__*__web.png")) if CURATED.is_dir() else []
    if len(curated) != 17:
        errors.append(f"Expected 17 curated Moonlight PNGs, found {len(curated)}")
    for shot, path in enumerate(curated, start=1):
        expected_prefix = f"MP-SHOT-{shot:03d}__"
        if not path.name.startswith(expected_prefix):
            errors.append(f"Curated PNG sequence mismatch: {path.name} expected {expected_prefix}*")
        if path.stat().st_size > 1024 * 1024:
            errors.append(f"Public PNG exceeds 1 MiB: {path.relative_to(ROOT)}")
        errors.extend(png_contract(path))
    errors.extend(png_contract(SOCIAL, expected_size=(1200, 630)))

    if errors:
        print("Moonlight Peaks scaffold validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Moonlight Peaks dossier validation passed through Capture 07.")
    print("State: FP-REV-0002 / Sketch / New Moon / MP-S01 open")
    print("Public evidence: MP-SHOT-001..017 / metadata-stripped PNGs")
    print("Public score and buyer action: withheld")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
