# Research worklog

## 2026-07-17 - Baseline checkpoint 01

- Confirmed the intended Final Prime Website checkout.
- Confirmed working branch: `VraxTemp/homepage-v1`.
- Preserved all pre-existing homepage worktree changes; research files are isolated under `docs/homepage-research/`.
- Measured seven agreed viewport sizes against the current local homepage.
- Hero text count is 145 words at 320-412 px and 146 words at 768 px and above; the difference is caused by responsive navigation visibility, not changing hero copy.
- Hero contains 58 descendant elements, two fully framed groups, and ten elements with partial borders.
- At 1280×720 the primary CTA begins at y=738 and is completely outside the viewport.
- At 390×844 the primary CTA begins at y=802; only 42 px of the two-button action group is visible.
- At 320×568 the CTA begins at y=772 and the manifesto is only 40% visible.
- On mobile, Root Trace begins at y=1161-1190 and therefore cannot function as a first-screen right-column counterweight.
- The Root Trace content repeats the later Method section's Surface/Trace/Origin/Reframe explanation.
- Baseline conclusion: the principal issue is allocation and repetition, not merely border styling.

Next checkpoint: standards and primary-research evidence ledger.

## 2026-07-17 - Evidence checkpoint 02

- Added 17 evidence entries: three normative WCAG requirements, thirteen primary/review research entries, and one official platform-guidance entry.
- Separated hard requirements from psychological hypotheses and observational transfer.
- Recorded an explicit counterexample or failure mode for every recommendation.
- Current palette contrast against `#090b0d`: primary text 17.87:1, muted 9.34:1, muted-dark 5.58:1, cyan 13.05:1, fuchsia text 5.59:1, primary-button text 4.82:1.
- Structural-line contrast: normal line 1.66:1 and strong line 2.41:1. These are acceptable only when decorative; meaningful component boundaries or focus cues need 3:1.
- Browser-host zoom commands did not alter the CSS viewport, so 320 px/400% reflow was measured directly. A formal 200% text-only check remains a prototype/implementation gate and is not falsely reported as passed.
- Evidence-level conclusion: mystery should live in the proposition and atmosphere; navigation, offer, proof, and next action should remain highly fluent.

Next checkpoint: fixed-schema audit of 18 live benchmark homepages.

## 2026-07-17 - Benchmark checkpoint 03

- Audited all 18 planned homepages at 1440×900 and 390×844 with a fixed measurement schema.
- Captured 34 benchmark screenshots: desktop and mobile for 17 sites. Active Theory's animated WebGL surface timed out twice during screenshot capture; both viewport metrics are preserved and the audit is explicitly marked partial.
- No audited page produced horizontal overflow at either measured size.
- The independent group most often lets one authored artefact or visual language carry character; full container borders are rare.
- The technical-authority group pairs a literal proposition with product, research, client, or corpus evidence. Their right-side content rarely repeats a method explanation.
- The experimental group can sustain much more ambiguity when the atmosphere is itself a working product, live output, artwork, or project reel and an explicit route remains visible.
- Nothing's consent layer obscured both captures, so it is retained as an overlay-risk observation rather than used as clean hero evidence.
- Ink & Switch is the closest structural analogue for proof-led Final Prime. Vercel is the clearest orientation-led analogue. Midjourney, FIELD, and Resn define progressively riskier immersive extremes.
- Benchmark conclusion: the right field should perform exactly one job, honest proof or compact orientation. Root Trace should not remain in the hero if Method retains the same logic below.

Next checkpoint: three isolated hero hypotheses and the anonymous human-test kit.

## 2026-07-17 - Prototype checkpoint 04

- Created three isolated research directions under `docs/homepage-research/hypotheses/`; none is imported by the production homepage. Each has a controlled desktop/mobile SVG stimulus and an editable responsive source snapshot.
- Kept the exact motto and the same founder-led orientation and primary route across all variants.
- Control retains Root Trace as the structure to falsify.
- Proof-led gives the right field to one evidence object and explicitly states that the current A/SYNC concept surface is not yet strong production proof.
- Sparse signal uses negative space, one orientation code, two rules, and no content frame.
- All three place the primary and secondary actions before the right-side material on mobile.
- At 1280×720 the primary CTA starts at y=665 and ends at y=713 for all three variants; the baseline CTA began at y=738 and was fully outside the viewport.
- At 390×844 the prototype CTA starts at y=460; at 320×568 it starts at y=457. No measured prototype has horizontal overflow.
- Added the moderated and self-test protocol, counterbalanced allocation, coding rules, raw-result CSV, honest empty result summary, and decision matrix.
- Provisional expert screening favours Sparse signal. This is not a winner declaration; the participant gates remain binding.

Next checkpoint: integrated report, adversarial review, accessibility/static validation, and repository-scope audit.

## 2026-07-17 - Validation checkpoint 05

- Integrated the baseline, evidence, benchmark, hypothesis, adversarial, and recommendation findings into `research-report.md`.
- Converted all 48 browser captures into true metadata-free RGB PNG files and kept every file below the repository's 1 MiB public-surface limit.
- Preserved the responsive prototype markup as three editable source snapshots and produced six controlled, clickable desktop/mobile SVG test stimuli.
- Verified all six `Explore selected work` overlays in the in-app browser; each reaches the selected-work research target.
- Parsed 7 baseline rows, 17 evidence rows, 18 benchmark rows, 12 prototype measurement rows, and 7 decision-matrix rows.
- Verified every local Markdown and SVG target and confirmed the exact locked motto in all three editable sources.
- Passed all nine repository checks: site integrity, security, search, review registry, public surface, IP notices, editorial style, accessibility contract, and social cards.
- Preserved all pre-existing homepage worktree changes. Research additions remain isolated under `docs/homepage-research/`.
- No production homepage edit, commit, push, pull request, or public deploy was performed.
- Human test status remains pending. No participant score or final winner has been fabricated.

Research package complete. Next external checkpoint: run the predeclared anonymous participant protocol, then apply its decision gate without moving the thresholds.
