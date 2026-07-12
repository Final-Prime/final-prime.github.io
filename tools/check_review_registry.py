#!/usr/bin/env python3
"""Verify the published Final Prime review registry and Metro 2033 Redux dossier."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "/reviews/metro-2033-redux/"
CANONICAL = f"https://final-prime.github.io{ROUTE}"
SOURCE_COMMIT = "e8e77e9d628027106bfe741563df2fc9aadf65d2"

REVIEW_PAGE = ROOT / "reviews" / "metro-2033-redux" / "index.html"
OG_ASSET = ROOT / "assets" / "reviews" / "metro-2033-redux-og.svg"
DOSSIER_CSS = ROOT / "assets" / "review-dossier.css"
POLISH_CSS = ROOT / "assets" / "review-dossier-polish.css"
DOSSIER_JS = ROOT / "assets" / "review-dossier.js"
RELEASE_CSS = ROOT / "assets" / "review-release.css"
PROVENANCE = ROOT / "docs" / "metro-2033-redux-import-audit.md"

REGISTRY_FILES = {
    "homepage": ROOT / "index.html",
    "thought": ROOT / "thought" / "index.html",
    "reviews": ROOT / "reviews" / "index.html",
    "public index": ROOT / "index" / "index.html",
    "sitemap": ROOT / "sitemap.xml",
}

OBSOLETE_PHRASES = (
    "The first dossier is in research.",
    "First game review in preparation.",
    "No published review yet.",
    "Research / experience",
)


def read(path: Path, errors: list[str]) -> str:
    if not path.is_file():
        errors.append(f"Missing required review file: {path.relative_to(ROOT)}")
        return ""
    return path.read_text(encoding="utf-8")


def require(text: str, token: str, label: str, errors: list[str]) -> None:
    if token not in text:
        errors.append(f"{label} missing required token: {token}")


def attribute(text: str, name: str) -> int | None:
    match = re.search(rf'\b{name}="(-?\d+)"', text)
    return int(match.group(1)) if match else None


def main() -> int:
    errors: list[str] = []

    review = read(REVIEW_PAGE, errors)
    read(OG_ASSET, errors)
    read(DOSSIER_CSS, errors)
    polish_css = read(POLISH_CSS, errors)
    dossier_js = read(DOSSIER_JS, errors)
    read(RELEASE_CSS, errors)
    provenance = read(PROVENANCE, errors)

    for label, path in REGISTRY_FILES.items():
        text = read(path, errors)
        require(text, ROUTE, label, errors)
        for phrase in OBSOLETE_PHRASES:
            if phrase in text:
                errors.append(f"{label} still contains obsolete review state: {phrase}")

    if review:
        require(review, f'<link rel="canonical" href="{CANONICAL}">', "review page", errors)
        require(review, 'data-review-id="FP-REV-0001"', "review page", errors)
        require(review, "/assets/reviews/metro-2033-redux-og.svg", "review page", errors)
        require(review, "/assets/review-dossier.css", "review page", errors)
        require(review, "/assets/review-dossier-polish.css", "review page", errors)
        require(review, "/assets/review-dossier.js", "review page", errors)
        require(review, "/assets/review-release.css", "review page", errors)
        require(review, "/legal/", "review page", errors)
        require(review, "Metro 2033 Redux and related", "review page", errors)
        require(review, "Ending reconstructed", "review page", errors)
        require(review, 'itemscope itemtype="https://schema.org/Review"', "review page", errors)
        require(review, 'itemprop="reviewRating"', "review page", errors)
        require(review, 'data-dossier-nav', "review page", errors)
        require(review, 'data-evidence-toolbar', "review page", errors)
        require(review, 'data-evidence-list', "review page", errors)
        require(review, 'twitter:image:alt', "review page", errors)
        require(review, 'article:modified_time', "review page", errors)
        require(review, "Published 12 Jul 2026", "review page", errors)

        raw = attribute(review, "data-review-raw")
        correction = attribute(review, "data-review-correction")
        score = attribute(review, "data-review-score")
        if (raw, correction, score) != (90, -4, 86):
            errors.append(f"Review score receipt mismatch: raw={raw}, correction={correction}, score={score}")
        elif raw + correction != score:
            errors.append("Review score arithmetic does not balance")

        axis_scores = [int(value) for value in re.findall(r'data-axis-score="(\d+)"', review)]
        if axis_scores != [20, 17, 17, 17, 19]:
            errors.append(f"Unexpected axis score sequence: {axis_scores}")
        if sum(axis_scores) != 90:
            errors.append(f"Axis scores total {sum(axis_scores)}, expected 90")

        expected_counts = {
            "evidence arcs": (review.count('class="evidence-arc"'), 9),
            "audit cards": (review.count('class="audit-card"'), 8),
            "friction rows": (review.count('class="friction-row"'), 4),
            "taste cards": (review.count('class="taste-card"'), 7),
            "fit gates": (review.count('class="fit-gate '), 3),
        }
        for label, (actual, expected) in expected_counts.items():
            if actual != expected:
                errors.append(f"Review page has {actual} {label}, expected {expected}")

        spoiler_counts = {level: review.count(f'data-spoiler="{level}"') for level in ("light", "medium", "heavy")}
        if spoiler_counts != {"light": 6, "medium": 2, "heavy": 1}:
            errors.append(f"Unexpected spoiler distribution: {spoiler_counts}")

        if re.search(r'<(?:img|script|link)[^>]+(?:src|href)="https?://', review, re.IGNORECASE):
            allowed = (
                'href="https://github.com/Kenessy/Kenessy/blob/',
                'href="https://final-prime.github.io/',
            )
            external_tags = re.findall(r'<(?:img|script|link)[^>]+(?:src|href)="https?://[^"]+"[^>]*>', review, re.IGNORECASE)
            for tag in external_tags:
                if not any(prefix in tag for prefix in allowed):
                    errors.append(f"Unexpected remote dependency in review page: {tag[:140]}")

    if polish_css:
        for token in ("scroll-margin-top", ".evidence-toolbar", 'a[aria-current="location"]', "--dossier-progress"):
            require(polish_css, token, "review polish CSS", errors)

    if dossier_js:
        for token in ("data-evidence-open-light", "data-evidence-collapse", "aria-current", "--dossier-progress"):
            require(dossier_js, token, "review dossier JavaScript", errors)

    if provenance:
        require(provenance, SOURCE_COMMIT, "provenance record", errors)
        require(provenance, "089e6df0ee52260f19eaa2325e9c5344084e977c", "provenance record", errors)
        require(provenance, "1c601b1680539c58f5e7326bb2cbc023143cd1a2", "provenance record", errors)
        require(provenance, "No third-party artwork", "provenance record", errors)

    if errors:
        print("Review registry check failed.")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Review registry check passed.")
    print("Object: FP-REV-0001")
    print("Route: /reviews/metro-2033-redux/")
    print("Score: 90 - 4 = 86 / A")
    print("Evidence arcs: 9")
    print("Audit checks: 8")
    print("Friction rows: 4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
