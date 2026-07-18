# Final Prime motto typography research

Date: 2026-07-18

Status: research-only; production is unchanged

Locked copy: `Knowing the next move is survival. / Understanding the game is control.`

## Decision

**Recommended direction: P4 / Inter, two complete desktop sentences, color only on `survival` and `control`, natural responsive wrapping.**

The recommendation is not that two lines are universally better than four. It is specific to this hero: the giant `FINAL \ PRIME` wordmark already supplies the poster-scale drama. A second oversized, two-color call-and-response block competes with it. P4 makes the motto read as a confident proposition beneath the identity rather than another logo.

The documented fallback is **P1 / Inter, balanced four-line stack**. Choose P1 if owner preference strongly favors the manifesto cadence after seeing both desktop and mobile renders.

## What was tested

The study deliberately separates variables before combining them:

1. **Six-family control:** current Aptos Display, Inter, Source Sans 3, IBM Plex Sans, Manrope and Segoe UI Variable use the same four-line structure.
2. **Eleven composition probes:** Inter stays fixed while line count, size hierarchy, color scope, alignment and grouping change.
3. **Six finalists:** the strongest font/structure combinations are rendered in full hero context at 1440×900 and 390×844.
4. **Falsification:** the finalists are measured at 320, 390, 768, 1440 and 1920 CSS px, then tested with a doubled root font size as a 200% text-resize probe.

No participant preference, conversion or comprehension score has been invented. The numerical shortlist is an explicit expert-prior matrix for making the trade-offs inspectable; owner choice remains the decision gate.

## Research interpretation

### Font class is not the answer by itself

The current and proposed fonts are all sans-serif. The visible problem comes from a display cut, heavy outcome weight and extremely tight `-0.07em` tracking acting together. Replacing Aptos Display without changing those settings only partially repairs the composition.

Inter is the strongest neutral base because it was built for screens, has a tall x-height and supports continuous variable weights. Its official documentation also provides the necessary counterpoint: screen optimization does not automatically make a font ideal at giant display sizes. P4 therefore uses Inter around 45-52 px on wide screens while leaving the 176 px identity wordmark in its existing display face. [Inter official repository](https://github.com/rsms/inter)

Source Sans 3 is a credible warmer alternative because Adobe designed it for UI environments. It placed second in the two-line composition, but its softer voice makes the already restrained lower hero feel more editorial. [Source Sans 3 official repository](https://github.com/adobe-fonts/source-sans)

IBM Plex Sans is technically excellent, but IBM explicitly presents Plex as its own design-language typeface and intellectual property. That provenance makes it a weaker fit for an entity whose positioning centers independence. [IBM Design Language](https://www.ibm.com/design/language/typography/typeface/)

Typeface psychology is treated as contextual, not as a lookup table. Childers and Jass found that semantic congruence among type, copy and surrounding visual cues influenced brand perception and memory in their advertising experiments. That supports contextual hero renders; it does not prove that Inter causes trust or that geometric fonts cause competence. [Childers and Jass, 2002](https://doi.org/10.1207/S15327663JCP1202_03)

### Two lines versus four

Both finalist structures preserve meaningful language boundaries:

- four-line: clause / outcome / clause / outcome;
- two-line: complete sentence / complete sentence.

The rejected layouts either created unnecessary line-length variability, added meta-graphics, or split the statements into competing micro-columns. Research indicates that line breaks can act like prosodic boundaries, while excessive variability can counteract the benefit of chunking. These studies use different reading tasks and therefore guide the test rather than dictate the answer. [Hirotani et al., 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC5054017/), [Keenan, 1984](https://eric.ed.gov/?id=EJ308203)

P4 wins locally because:

- each sentence is parsed in one sweep at wide desktop sizes;
- the color lands on the two semantic endpoints rather than coloring half the block;
- the white `is` and full stop keep the accents from turning into two neon banners;
- mobile wraps naturally into phrase-respecting lines;
- at 320 px it uses 131 px of motto height, versus 165.1 px for the four-line finalists;
- at 1440 px it uses about 117 px, versus 225.5 px for the four-line finalists;
- the orientation and CTA become the next clear reading target instead of a weak right-hand afterthought.

### Accessibility and failure discovery

White, cyan and fuchsia measure 18.31:1, 13.05:1 and 5.59:1 against `#090b0d`, so all exceed the WCAG AA requirement for large text. Color is expressive rather than the only carrier of meaning because both sentences remain complete without it. [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

The first P4 prototype forced `white-space: nowrap` to preserve two desktop lines. A 200% text-size falsification pass found internal overflow hidden by the hero's clipping. The rule was removed. At normal wide sizes the sentence still occupies one line because it fits; under enlargement it wraps without loss. All finalists now show zero horizontal overflow at 320 px and in the doubled-font-size probe.

## Adversarial eliminations

- **Current control:** too much compression and a large weight jump; the lowercase glyphs look swollen and crowded.
- **Manrope:** square punctuation/dots and geometric construction introduce the kind of noticeable font mannerism the user already rejected.
- **Segoe UI Variable:** useful control, but platform-dependent and visually less deterministic.
- **IBM Plex winner attempt:** technically credible but unnecessarily imports a recognizable corporate voice.
- **Compressed poster / L5:** uppercase lead-ins turn the motto into a shout and compete with the wordmark.
- **Editorial index / L6:** numbers add an invented system with no semantic job.
- **Offset outcomes / L7:** the small indentation can look accidental at some widths.
- **Maximum accent / L8:** makes cyan and fuchsia equal full-line banners and destroys their signal value.
- **Muted outcomes / L9:** solves intensity by weakening the established palette rather than fixing hierarchy.
- **Quiet statement / L10:** generated an awkward rag and too many short lines.
- **Parallel statements / L11:** creates extra columns on desktop and a longer second chapter on mobile.

## Production specification if P4 is accepted

- Scope the new face to the motto first; do not silently restyle every route.
- Self-host the official Inter variable WOFF2 under an isolated family name such as `FP Inter`.
- Update CSP from `font-src 'none'` to a self-only font policy and add the OFL notice.
- Desktop: weight about 680, `clamp(1.95rem, 3.1vw, 3.25rem)`, line-height 1.04, tracking about `-0.038em`, 24 px sentence gap.
- Color only the words `survival` and `control`; keep `is` and punctuation white.
- Never force the sentence onto one line. Natural wrapping is part of the accessibility contract.
- Mobile: `clamp(1.62rem, 7.6vw, 2.4rem)`, line-height 1.09, 18 px sentence gap.
- Repeat the full production viewport, 200% text, 320 px reflow, console, CSP and site-integrity gates after integration.

## Visual artifacts

- [Font-family sweep](screenshots/fonts-collage.png)
- [Composition and color sweep](screenshots/layouts-collage.png)
- [Desktop and mobile finalists P1-P3](screenshots/finalists-part-1.png)
- [Desktop and mobile finalists P4-P6](screenshots/finalists-part-2.png)
- [Decision matrix](decision-matrix.csv)
- [Evidence ledger](evidence-ledger.csv)
