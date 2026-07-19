# Final Prime: game-review surface audit

## Scope

This audit covers the current public game-review surface reviewed on 2026-07-19:

- the homepage `Work & Evidence` feature;
- the `Works / Analysis + Reviews` lane;
- the dedicated `/reviews/` index;
- the published `FP-REV-0001` Metro 2033 Redux dossier;
- the review pipeline and declared methodology; and
- the public/private evidence boundary.

## Design result

The review surface follows the existing Final Prime system language:

- open ledgers, whitespace and functional disclosure borders;
- disciplined amber for Metro identity and score;
- cyan for verified/current state;
- magenta for deductions, danger and heavy spoilers;
- one published review object and one method inspector;
- a five-link sticky dossier path using breadcrumb separators instead of boxed tabs;
- a visible four-stage pipeline: `Experience / Model / Verify / Publish`;
- explicit score anatomy, friction, audit and evidence structures; and
- no fake cover, placeholder title, invented publication date or decorative score.

## Current public state

- `FP-REV-0001` is published at `/reviews/metro-2033-redux/`.
- The final score is `86 / A`, derived from a 90-point core subtotal and a -4 fit-and-risk correction.
- The dossier exposes four friction rows, eight adversarial checks and nine route-level evidence arcs.
- The archive contains one published dossier.
- Game Reviews are classified under `Works / Evidence`; the canonical review URLs are unchanged.
- Later review formats may differ, but each public dossier must expose its thesis, evidence path, caveats, spoiler boundary and lifecycle state.

## Truthfulness boundary

- Review claims are limited to the evidence and caveats disclosed in the dossier.
- The final interpretation identifies reconstructed evidence where direct capture was blocked.
- Unpublished notes, private research trails and source material are not represented as public.
- Metro 2033 Redux and related third-party marks remain attributed to their respective owners.
- No relationship with the game publisher or developer is implied.

## Accessibility and resilience

- one H1 on each review document;
- semantic article, section, list, definition-list, header, main and footer structures;
- keyboard-operable links, disclosure controls and mobile navigation;
- minimum action-target and visible-focus contracts;
- no-JavaScript review content and navigation remain visible;
- display headlines and cards permit narrow-screen and 200% text reflow;
- status meaning is present in text, not only color; and
- forced-colors, reduced-motion and print fallbacks are included.

## Automated result

- Review object: `FP-REV-0001`.
- Canonical route: `/reviews/metro-2033-redux/`.
- Score contract: `90 - 4 = 86 / A`.
- Evidence arcs: `9`.
- Audit checks: `8`.
- Friction rows: `4`.
- Review registry, social metadata, schema, site integrity, accessibility, security and public-surface checks: passed.
- W3C Nu structural HTML errors on the review index and dossier: `0`.

## Adversarial findings retained

1. Large review headings use viewport-capped mobile sizing and shrinkable containers.
2. Review cards and metadata explicitly permit min-content shrinkage.
3. Conversion links route to Works, public methodology, the dossier or Contact rather than soliciting unpublished material.
4. Empty publication lanes explain their state instead of presenting placeholders as work.
5. Score math, correction layers and caveats remain inspectable rather than being compressed into a single promotional rating.
