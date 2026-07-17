# Final Prime homepage - solo-first validation protocol

Status: active operating gate for provisional homepage iterations

This protocol allows the homepage to improve without depending on a large participant pool. It does not manufacture human evidence and does not replace the original two-cohort study. A version may become the live working version after passing the solo gate; it may be called a human-validated winner only after real participant data exists.

## Decision levels

1. **Working version:** deterministic checks pass and the owner finds no critical comprehension or tone failure. It may be published as the current v1/v2 iteration.
2. **Externally reinforced version:** two to four suitable English-reading reviewers independently confirm the domain and primary route. This is useful but optional.
3. **Human-validated direction:** the original cohort protocol and thresholds pass. Only this level can declare a research hypothesis the winner.

## Mandatory solo gate

### 1. Truth and scope

- The page identifies software, research, and systems before any abstract manifesto.
- Founder-led wording appears as a factual operating model, not an apology or a simulated team.
- No `we`, `our company`, fabricated client, fabricated result, or concept-presented-as-proof claim appears.
- The exact locked motto remains unchanged.
- Selected work states lifecycle, evidence surface, and limits explicitly.

### 2. Structural contract

- The hero contains one orientation paragraph and one sparse signal, not a matrix, pipeline, capability list, or second manifesto.
- `Explore selected work` is the dominant first action.
- Selected Work immediately follows the hero in source and visual order.
- Root-cause explanation appears once, in the later Method section.
- Complete frames are reserved for controls or inspectable evidence objects; ordinary grouping uses spacing and rules.

### 3. Browser matrix

Test at 320×568, 390×844, 412×915, 768×1024, 1280×720, 1440×900, and 1920×1080.

For every viewport:

- horizontal overflow is no greater than 1 CSS pixel;
- the primary CTA is visible without horizontal scrolling;
- headings and actions do not overlap or clip;
- the visual reading order matches the intended mobile or desktop order;
- the Selected Work anchor receives the route correctly.

At 1280×720, 390×844, and 320×568, the primary CTA must end inside the initial viewport. The 320 CSS-pixel view also acts as the required 400%/320 px reflow proxy.

### 4. Interaction and accessibility

- The focusable DOM order reaches the primary action before the secondary action and later-section links.
- Run a real Tab traversal whenever the available browser driver can synthesize it. If it cannot, record that limitation instead of claiming a dynamic keyboard pass.
- Focus is visible on navigation and both hero actions.
- The page remains understandable in grayscale and does not use cyan/fuchsia as the only carrier of meaning.
- Forced-colors and reduced-motion contracts remain present.
- No browser console error, broken local reference, critical WCAG contract failure, or missing mobile content is allowed.

### 5. Adversarial self-review

Run these questions after viewing only the first screen:

1. What does Final Prime make or investigate?
2. What is the first intended action?
3. Which visible element could be mistaken for invented proof?
4. Does any sentence sound like a larger team exists?
5. Is mystery delaying comprehension or the route?
6. Does the sparse field feel deliberate only because concrete work follows it?

Any critical failure sends the page back to implementation. The owner review is an acceptance check, not an unbiased first-impression measurement.

## Optional low-recruitment reinforcement

If suitable people become available, use two to four English-reading reviewers. Show only the first screen for five seconds, then ask what the site is, what it makes, and where they would open the work. Do not coach them and do not combine their results with the original 12-16 participant thresholds.

## Publication rule

A provisional version may move to `main` when:

- every mandatory automated and browser check passes;
- the measured results are recorded in `implementation-v2-metrics.csv`;
- the owner has no critical objection;
- the release is described as a working iteration, not a human-validated winner.

GitHub `main` and the deployed Pages site remain the source of truth. The local server is only a preview and measurement surface.

## Recorded v2 run - 2026-07-17

- All seven required viewports passed with zero horizontal overflow and zero visibly clipped watched elements.
- The primary CTA ended inside the initial viewport at 320x568, 390x844, and 1280x720; the full measurements are in `implementation-v2-metrics.csv`.
- Selected Work is the hero's immediate source and visual sibling at every measured viewport.
- Activating `Explore selected work` produced `#selected-work` and moved focus to the selected-work section.
- Browser console errors: 0.
- Mobile focusable DOM order: skip link, brand, menu control, primary CTA, secondary CTA, then Selected Work links.
- The connected browser driver did not synthesize Tab key movement, so live sequential Tab traversal is not claimed. Static DOM order, semantic checks, and the focus-visible CSS contract passed; this remains a manual spot-check rather than invented evidence.
