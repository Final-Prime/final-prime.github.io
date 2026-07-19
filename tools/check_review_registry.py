#!/usr/bin/env python3
"""Verify the published Final Prime review registry and Metro 2033 Redux dossier."""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROUTE = "/reviews/metro-2033-redux/"
CANONICAL = f"https://final-prime.github.io{ROUTE}"
SOURCE_COMMIT = "e8e77e9d628027106bfe741563df2fc9aadf65d2"

REVIEW_PAGE = ROOT / "reviews" / "metro-2033-redux" / "index.html"
OG_ASSET = ROOT / "assets" / "reviews" / "metro-2033-redux-og.png"
DOSSIER_CSS = ROOT / "assets" / "review-dossier.css"
DOSSIER_JS = ROOT / "assets" / "review-dossier.js"
INDEX_CSS = ROOT / "assets" / "reviews.css"
PROVENANCE = ROOT / "docs" / "metro-2033-redux-import-audit.md"

REGISTRY_FILES = {
    "homepage": ROOT / "index.html",
    "works": ROOT / "works" / "index.html",
    "reviews": ROOT / "reviews" / "index.html",
    "public index": ROOT / "index" / "index.html",
    "sitemap": ROOT / "sitemap.xml",
}

OBSOLETE_PHRASES = (
    "The first dossier is in research.",
    "First game review in preparation.",
    "No published review yet.",
    "Research / experience",
    "01 / Decision surface",
    "You accept tight authorship",
    "Open ALERTED axis definitions",
    "Sight Is Not Understanding",
    "Trust footer.",
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
    if not OG_ASSET.is_file():
        errors.append(f"Missing required review file: {OG_ASSET.relative_to(ROOT)}")
    dossier_css = read(DOSSIER_CSS, errors)
    dossier_js = read(DOSSIER_JS, errors)
    read(INDEX_CSS, errors)
    provenance = read(PROVENANCE, errors)

    for label, path in REGISTRY_FILES.items():
        text = read(path, errors)
        require(text, ROUTE, label, errors)
        for phrase in OBSOLETE_PHRASES:
            if phrase in text:
                errors.append(f"{label} still contains obsolete review state: {phrase}")

    thought = read(ROOT / "thought" / "index.html", errors)
    require(thought, "/reviews/", "thought orientation", errors)
    require(thought, "/works/", "thought orientation", errors)
    require(thought, "No published record", "thought orientation", errors)

    if review:
        require(review, f'<link rel="canonical" href="{CANONICAL}">', "review page", errors)
        require(review, 'data-review-id="FP-REV-0001"', "review page", errors)
        require(review, "/assets/reviews/metro-2033-redux-og.png", "review page", errors)
        require(review, '<link rel="stylesheet" href="/assets/review-dossier.css?v=20260719-15">', "review page", errors)
        require(review, "/assets/review-dossier.js", "review page", errors)
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
        require(review, "Updated 19 Jul 2026", "review page", errors)
        require(review, '<a href="/works/" aria-current="location">Works</a>', "review page", errors)
        require(review, "01 / Audience verdict", "review editorial contract", errors)
        require(review, "You accept a guided path", "review editorial contract", errors)
        require(review, "Treat 86 as a fit signal, not a universal verdict.", "review editorial contract", errors)
        require(review, "ALERTED axis definitions", "review editorial contract", errors)
        require(review, "03 / Human verdict", "review editorial contract", errors)
        require(review, "What this review promises", "review editorial contract", errors)
        require(review, "Seeing Is Not Knowing", "review editorial contract", errors)
        require(review, "Trust <span>the record.</span>", "review editorial contract", errors)
        require(review, '<a href="#verdict">Verdict</a><span class="dossier-nav-separator" aria-hidden="true">/</span><a href="#score">Score</a><span class="dossier-nav-separator" aria-hidden="true">/</span><a href="#note">Field note</a><span class="dossier-nav-separator" aria-hidden="true">/</span><a href="#evidence">Evidence</a><span class="dossier-nav-separator" aria-hidden="true">/</span><a href="#protocol">Protocol</a>', "review page", errors)

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

        main_match = re.search(r"<main\b[\s\S]*?</main>", review, flags=re.IGNORECASE)
        if not main_match:
            errors.append("Review page is missing its editorial main landmark")
            main_review = ""
        else:
            main_review = main_match.group(0)
        plain_review = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>|<[^>]+>", " ", main_review)
        review_word_count = len(re.findall(r"\b[\w'’/.-]+\b", html.unescape(plain_review), flags=re.UNICODE))
        if not 1850 <= review_word_count <= 1950:
            errors.append(f"Review editorial word count is {review_word_count}, expected 1850-1950")

        if re.search(r'<(?:img|script|link)[^>]+(?:src|href)="https?://', review, re.IGNORECASE):
            allowed = (
                'href="https://github.com/Kenessy/Kenessy/blob/',
                'href="https://final-prime.github.io/',
            )
            external_tags = re.findall(r'<(?:img|script|link)[^>]+(?:src|href)="https?://[^"]+"[^>]*>', review, re.IGNORECASE)
            for tag in external_tags:
                if not any(prefix in tag for prefix in allowed):
                    errors.append(f"Unexpected remote dependency in review page: {tag[:140]}")

    if dossier_css:
        for token in (
            "scroll-margin-top",
            ".evidence-toolbar",
            'a[aria-current="location"]',
            "--dossier-progress",
            "scrollbar-width: none;",
            ".dossier-nav.has-overflow.at-start:not(.at-end)::before",
            ".dossier-actions .button-primary:hover span",
            ".method-disclosure summary::after",
            ".method-disclosure[open] summary::after",
            "text-wrap: balance;",
            ".dossier-axis-body {",
            "margin-top: auto;",
            "align-items: start;",
        ):
            require(dossier_css, token, "consolidated review dossier CSS", errors)
        dossier_css_bytes = len(dossier_css.encode("utf-8"))
        if dossier_css_bytes > 42_000:
            errors.append(f"Consolidated review dossier CSS is {dossier_css_bytes} bytes, expected at most 42000")
        if ".dossier-axis p { min-height: 160px;" in dossier_css:
            errors.append("Consolidated review dossier CSS restored the obsolete fixed axis paragraph height")
        if dossier_css.count("@media (max-width: 1180px)") != 1:
            errors.append("Consolidated review dossier CSS must contain exactly one 1180px breakpoint")
        if dossier_css.count("@media (max-width: 900px)") != 1:
            errors.append("Consolidated review dossier CSS must contain exactly one 900px breakpoint")
        canonical_marker = "/* Canonical dossier shell: open ledgers, five-layer navigation, restrained Metro signal. */"
        if canonical_marker not in dossier_css:
            errors.append("Consolidated review dossier CSS is missing the canonical shell boundary")
        else:
            late_open_block = dossier_css.split(canonical_marker, 1)[1].split(".evidence-toolbar", 1)[0]
            for selector in (
                ".fit-gates", ".fit-gate", ".taste-grid", ".taste-card",
                ".dossier-axis-grid", ".dossier-axis", ".field-note-grid",
                ".field-note", ".fit-tags", ".insight-grid", ".insight-card",
                ".audit-grid", ".audit-card", ".protocol-grid", ".dossier-thesis",
                ".modifier-card", ".friction-ledger",
            ):
                if re.search(rf"(?m)^{re.escape(selector)}\s*\{{", late_open_block):
                    errors.append(f"Consolidated review dossier CSS restored late {selector} overrides")

    if dossier_js:
        for token in (
            "data-evidence-open-light",
            "data-evidence-collapse",
            "aria-current",
            "--dossier-progress",
            'document.addEventListener("toggle", requestNavigationUpdate, true)',
            'link.addEventListener("focus"',
            'revealActiveLink(link, "auto")',
            "bulkPending",
            "bulkAnnouncement",
            "beginBulkUpdate",
            "spoiler-light arcs expanded",
            "All evidence arcs collapsed.",
            "status.textContent !== message",
            'window.addEventListener("beforeprint"',
            'window.addEventListener("afterprint"',
            "printRendering",
        ):
            require(dossier_js, token, "review dossier JavaScript", errors)
    require(
        review,
        "0 of 9 arcs open. Medium and heavy spoilers remain closed unless selected.",
        "review dossier initial evidence status",
        errors,
    )

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
