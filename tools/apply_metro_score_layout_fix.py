#!/usr/bin/env python3
"""Apply the focused Metro score-anatomy layout correction idempotently."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML_PATH = ROOT / "reviews" / "metro-2033-redux" / "index.html"
CSS_PATH = ROOT / "assets" / "review-dossier-polish.css"

OLD_TITLE = '<h2 id="score-title">90 minus 4 <span>equals 86.</span></h2>'
NEW_TITLE = '<h2 id="score-title" aria-label="90 minus 4 equals 86">90 &minus; 4 <span class="score-title-result">= 86.</span></h2>'

OLD_RECEIPT = '<div class="score-equation" aria-label="Score calculation: 90 minus 4 equals 86"><div><small>Core axes</small><strong>90</strong></div><span aria-hidden="true">-</span><div><small>Fit / risk</small><strong>4</strong></div><span aria-hidden="true">=</span><div class="final"><small>Final score</small><strong>86</strong></div></div>'
NEW_RECEIPT = '<div class="score-equation" aria-label="Score calculation: 90 minus 4 equals 86"><div><small>Core axes</small><strong>90</strong></div><span aria-hidden="true">&minus;</span><div><small>Fit / risk</small><strong>4</strong></div><span aria-hidden="true">=</span><div class="final"><small>Final score</small><strong>86</strong></div></div>'

CSS_MARKER = "/* Score anatomy correction: symbolic equation, single-line axis labels, and aligned receipts. */"
CSS_PATCH = r'''

/* Score anatomy correction: symbolic equation, single-line axis labels, and aligned receipts. */
.review-dossier-page #score-title {
  font-variant-numeric: tabular-nums;
}

.review-dossier-page #score-title .score-title-result {
  display: block;
}

.review-dossier-page .dossier-axis-grid {
  align-items: stretch;
}

.review-dossier-page .dossier-axis {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  height: 100%;
}

.review-dossier-page .dossier-axis-body {
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto auto;
  height: 100%;
}

.review-dossier-page .dossier-axis h3 {
  overflow-wrap: normal;
  word-break: normal;
  hyphens: none;
}

.review-dossier-page .dossier-axis p {
  min-height: 0;
}

.review-dossier-page .dossier-meter {
  align-self: end;
}

@media (min-width: 1181px) {
  .review-dossier-page .dossier-axis h3 {
    font-size: clamp(1.4rem, 1.75vw, 2.05rem);
    letter-spacing: -0.04em;
    white-space: nowrap;
  }
}
'''


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    if old in text:
        return text.replace(old, new, 1), True
    if new in text:
        return text, False
    raise SystemExit(f"Neither old nor corrected {label} marker was found")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    html, title_changed = replace_once(html, OLD_TITLE, NEW_TITLE, "score title")
    html, receipt_changed = replace_once(html, OLD_RECEIPT, NEW_RECEIPT, "score receipt")
    HTML_PATH.write_text(html, encoding="utf-8")

    css = CSS_PATH.read_text(encoding="utf-8")
    css_changed = CSS_MARKER not in css
    if css_changed:
        CSS_PATH.write_text(css.rstrip() + CSS_PATCH + "\n", encoding="utf-8")

    print(f"Title changed: {title_changed}")
    print(f"Receipt changed: {receipt_changed}")
    print(f"CSS changed: {css_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
