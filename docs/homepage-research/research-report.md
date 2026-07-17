# Final Prime homepage - evidence-first research report

Date: 2026-07-17
Status: literature, baseline, benchmark, and prototype stages complete; human test not yet run
Implementation status: the owner approved a provisional live homepage iteration; deployment does not count as human validation

## Executive decision

The current hero's core problem is not simply “too many boxes.” It gives the first screen three competing jobs: manifesto, method, and navigation, while the actual primary route falls out of view at a common 1280×720 desktop size. Root Trace then repeats the Method section below. On mobile it cannot behave as a right-hand counterweight at all; it becomes a long second chapter.

The provisional recommendation is **Sparse signal**:

- keep the exact motto and a short, truthful founder-led orientation on the left;
- make `Explore selected work` completely visible in the first viewport;
- let the right field provide only category / route orientation and deliberate negative space;
- move all root-cause explanation to one later Method section;
- begin Selected Work immediately after the hero.

The documented reserve direction is **Proof-led**, but only after a real, inspectable work item exists. The current A/SYNC public concept surface is not strong enough to carry a credibility claim by itself. A concept presented as proof would be more damaging than a sparse, honest signal.

This is an expert prior, not a final winner. The predeclared two-cohort human gate remains binding before the direction is treated as final. The live v1 iteration is therefore an inspectable working version, not evidence that a hypothesis has won.

## What was measured

### Current homepage baseline

The baseline was measured at 320×568, 390×844, 412×915, 768×1024, 1280×720, 1440×900, and 1920×1080. Full raw measurements are in [`baseline-metrics.csv`](baseline-metrics.csv); annotated captures are in [`screenshot-notes.md`](screenshot-notes.md).

| Finding | Evidence | Consequence |
|---|---|---|
| Primary CTA begins at y=738 on 1280×720 | Entire action is below the viewport | The declared primary route is not a first-screen route at this size |
| Primary CTA begins at y=802 on 390×844 | Only 42 px of the two-action group is visible | Mobile comprehension precedes action by too much content |
| Primary CTA begins at y=772 on 320×568 | Manifesto is only 40% visible | A small phone sees an unfinished opening thought and no action |
| Root Trace begins around y=1161-1190 on phones | It cannot share the first screen with the motto | Desktop “right side” becomes a later mobile chapter |
| Root Trace repeats Surface → Trace → Origin → Reframe from Method | Two sections perform the same explanatory job | Perceived density stays high even if borders are removed |
| Hero has 58 descendants, two complete frames, and ten partial-border elements | Multiple visual boundaries compete | The shell feels instrument-like before any proof is present |

At 320 CSS px the current page did not show horizontal overflow. The browser host did not expose a reliable text-only 200% zoom state, so formal 200% resize validation is still a later implementation gate and is not reported as passed.

### Palette and structural contrast

Against `#090b0d`, current primary text, muted text, cyan, and fuchsia text all exceed 4.5:1. The current faint line colours measure 1.66:1 and 2.41:1. Those lines are acceptable only where decorative; a meaningful control boundary or focus cue needs 3:1 under [WCAG 2.2 non-text contrast](https://www.w3.org/TR/WCAG22/#non-text-contrast).

The research prototypes therefore separate decorative `#343c43` rules from meaningful control / evidence boundaries at `#56616b` (3.11:1 against the background).

## Evidence synthesis

The claim-level record, including method, applicability, limitation, counterevidence, and confidence, is in [`evidence-ledger.csv`](evidence-ledger.csv). The important combined reading is:

1. **Fast impression makes excess expensive.** Very brief exposure can produce stable aesthetic judgments, and tested visual complexity can harm early appeal ([Lindgaard et al.](https://doi.org/10.1080/01449290500330448); [Tuch et al.](https://research.google/pubs/the-role-of-visual-complexity-and-prototypicality-regarding-first-impression-of-websites-working-towards-understanding-aesthetic-judgments/)). These studies do not prove a conversion formula, but they justify testing the uncontaminated first five seconds.
2. **Mystery needs a legible gap.** Processing fluency often supports positive aesthetic response, while curiosity depends on recognising an information gap ([Reber et al.](https://doi.org/10.1207/S15327957PSPR0804_3); [Loewenstein](https://doi.org/10.1037/0033-2909.116.1.75)). Therefore the thesis may be enigmatic, but category, proof status, and next action should be fluent.
3. **Competence cannot replace warmth.** Social perception separates competence and warmth ([Fiske et al.](https://doi.org/10.1037/0022-3514.82.6.878)). The sharp industrial language can support authority, but founder-led wording and plain invitations must counter coldness and arrogance.
4. **Expressive and orderly aesthetics can coexist.** Classical order and expressive originality are distinguishable rather than mutually exclusive ([Lavie and Tractinsky](https://doi.org/10.1016/j.ijhcs.2003.09.002)). Final Prime should use an orderly shell for an expressive proposition, not make every layer strange.
5. **Aesthetics can affect credibility, but do not create evidence.** In identical-content comparisons, more aesthetic pages were usually rated more credible ([Robins and Holmes](https://doi.org/10.1016/j.ipm.2007.02.003)). This supports craft quality; it does not justify substituting a decorative matrix for real work.
6. **Colour and contour findings are contextual.** Colour effects vary with context, and the classic curve-preference result was a controlled object task, not a law for brands ([Elliot and Maier](https://pubmed.ncbi.nlm.nih.gov/23808916/); [Bar and Neta](https://cris.biu.ac.il/en/publications/humans-prefer-curved-visual-objects-4/)). Cyan / fuchsia roles and sharp / soft detail must therefore be tested as hypotheses.

The resulting design law for this project is:

```text
expressive thesis
      +
fluent category + honest proof status + obvious next action
      =
controlled disorientation
```

Remove the fluent layer and mystery becomes confusion. Remove the expressive layer and Final Prime becomes a generic studio.

## 18-site benchmark audit

The fixed matrix is in [`benchmark-matrix.csv`](benchmark-matrix.csv), with desktop and mobile first-screen measurements and transfer / failure notes for every site.

Benchmarks are observational. They reveal role patterns, not causation or guaranteed conversion.

### Independent / outsider group

Teenage Engineering, Panic, 100 Rabbits, Ink & Switch, Dynamicland, and Low-tech Magazine generally place identity in one authored artefact, product, environment, or editorial voice. Container frames are rare. Ink & Switch is the closest proof-led analogue: a concrete artefact takes the larger field, with a short interpretation and route beside it. Low-tech Magazine shows how a small number of rules and direct content can replace a dashboard shell.

### Technical-authority group

Anthropic, Palantir, Wolfram, Linear, Vercel, and Stripe connect a literal proposition to research, product UI, client evidence, or a visible corpus. Their right field usually provides proof or a concise qualifier. Vercel most clearly demonstrates an orientation-only right field; Palantir and Linear make product UI the counterweight; Wolfram's density works because decades of real corpus support it and would be unsafe to imitate prematurely.

### Experimental / mysterious group

Nothing, Midjourney, FIELD, Active Theory, Refik Anadol Studio, and Resn tolerate greater ambiguity because the surface is itself a product, live output, artwork, project reel, or interactive craft. Midjourney and Resn still expose an explicit exploration route. This establishes the risk boundary: immersive ambiguity is safest when the strange thing is already real work.

Capture limitations are not hidden: Nothing's consent layer covered both viewports; Active Theory's WebGL surface produced metrics but timed out during both screenshot attempts. Automated word counts can also overcount responsive duplicates and modal content.

## Hypothesis comparison

All prototypes use the exact motto, the same provisional founder-led orientation, the same two routes, and a mobile order designed independently from the desktop columns. The controlled test stimuli are paired desktop/mobile SVG files with clickable routes; editable responsive source snapshots remain beside them. None is loaded by the production site.

| Hypothesis | What the right field does | First-screen load | Main risk | Expert prior |
|---|---|---|---|---:|
| Control / Root Trace | Explains the root-cause method | Highest; 78 measured words at 1440×900 | Repetition, delayed route, “invented instrument” feeling | 2.25 / 5 |
| Proof-led | Presents one selected-work evidence slot | 90 words because the evidence warning is explicit | Pretension if concept is mistaken for proof | 3.50 / 5 |
| Sparse signal | Provides field and route orientation | Lowest; 41 measured words | Can feel empty if real work does not follow immediately | 4.15 / 5 |

The weighted scores in [`decision-matrix.csv`](decision-matrix.csv) are ordinal screening, not behavioural precision. Human gates override them.

Prototype routing improved without horizontal overflow:

- 1280×720: primary CTA y=665-713, fully visible;
- 390×844: primary CTA begins at y=460;
- 320×568: primary CTA begins at y=457 and ends at y=503.

Raw measurements are in [`prototype-metrics.csv`](prototype-metrics.csv).

## Recommended homepage specification

### Desktop hero

```text
┌ wordmark + minimal navigation ───────────────────────────────────────┐

  SOFTWARE · RESEARCH · SYSTEMS       FP / INDEPENDENT / 01
  locked four-line motto              restrained spatial signal
  one founder-led orientation         field + route, 15-25 words total
  [Explore selected work] [Discuss]

──────────────────── first Selected Work immediately follows ─────────
```

- **Left, approximately 56-60%:** category eyebrow, exact motto, one orientation paragraph, actions.
- **Right, approximately 40-44%:** sparse signal with one semantic purpose. No matrix, pipeline, capability list, or second manifesto.
- **Primary action:** `Explore selected work`, visually dominant and completely visible at 1280×720.
- **Secondary action:** quieter, still at least 44 px tall with a 3:1 meaningful boundary.
- **Next section:** one or a few selected works. The homepage routes into proof instead of becoming the full catalogue.
- **Method:** one later section only. Root Trace may be absorbed there, not duplicated in the hero.

### Mobile priority order

```text
1. Wordmark
2. Software · research · systems
3. Exact motto
4. One founder-led orientation
5. Explore selected work
6. Discuss a problem
7. Compact signal OR real proof
8. Selected work
9. Method
```

This is deliberate reprioritisation, not a desktop grid mechanically stacked into one column.

### Frame policy

Use a complete frame only for:

- an interactive control;
- an inspectable evidence object;
- a group whose relationship would otherwise be ambiguous.

Use spacing, alignment, and a single rule for everything else. Decorative rules may stay subtle. Meaningful boundaries and focus indicators must reach 3:1.

### Colour roles

- **Cyan:** primary route, current state, access, or a positive system signal.
- **Fuchsia:** tension, anomaly, thesis accent, or a single counter-signal.
- **Neutral text:** all explanatory content.
- **Neutral lines:** structure only; never let cyan and fuchsia highlight every element equally.

The page must remain understandable in grayscale and without colour labels. Strong-light and low-brightness device checks remain an implementation QA gate; dark-mode legibility cannot be inferred from desktop screenshots alone.

### Shape roles

- Keep the foundational grid and signal geometry sharp.
- Use a modestly softer treatment only where approachability has a semantic reason, such as the invitation to contact or the selected-work media crop.
- Do not round every surface to manufacture warmth, and do not interpret sharpness as a universal competence signal.

### Motion

The hero does not need continuous motion. If motion is later introduced, it should reveal a relationship or proof state, stop on its own, and have a meaningful static equivalent under `prefers-reduced-motion`. The prototypes contain no essential animation.

## Adversarial review

### How the recommendation can fail

1. **Sparse becomes empty theatre.** If Selected Work below the fold is vague, the negative space no longer signals confidence; it signals absence.
2. **Founder-led becomes apologetic.** The page should state independence once, not repeat “solo” as a limitation. Competence must come from work and reasoning.
3. **The motto consumes all comprehension.** If the category eyebrow or orientation is reduced further, non-specialists may recall only a dramatic quote.
4. **Proof-led overclaims.** A concept image, diagram, or aspirational system name is not shipped work, research evidence, or an inspectable result.
5. **Industrial becomes hostile.** Dense uppercase labels, aggressive magenta, and repeated hard frames can move competence toward coldness and arrogance.
6. **Colour becomes hierarchy noise.** Equal cyan and fuchsia emphasis destroys both meanings and is weaker in grayscale or colour-vision variation.
7. **Mystery delays the route.** Any reintroduction of a pre-CTA manifesto, diagnostic diagram, or intro animation recreates the baseline failure.
8. **One cohort hides the other.** A strong technical response cannot compensate for general-audience confusion, and vice versa.

### Falsification conditions

Reject Sparse signal if either cohort fails category / route recognition, warmth, or credibility gates. Promote Proof-led only if its evidence object is real and it passes both cohorts. Retain neither if the human test shows “scam-like,” “arrogant,” or “confusing” medians above the predeclared ceiling.

## Human decision gate

The complete procedure is in [`test-protocol.md`](test-protocol.md). It specifies 12-16 anonymous participants, two equal cohorts, at least four moderated sessions per cohort, counterbalanced first exposure, five-second recall, the route task, 1-7 ratings, coding rules, and cohort-by-cohort thresholds.

[`human-test-results.md`](human-test-results.md) is intentionally empty. No synthetic participant scores, invented conversion estimate, or fake winner has been created.

## Delivery boundary and next decision

Research artefacts are complete enough to start real participant sessions. The only unresolved evidence is the human counter-test and the formal implementation QA that depends on a chosen direction. Until the user accepts the research and closes the provisional hero sentence element by element:

- do not modify the production homepage;
- do not present A/SYNC as proof;
- do not commit, push, or deploy the research as a live redesign;
- do not declare a winner from the expert prior alone.

After real test results are entered, apply the decision gate without adjusting thresholds to fit the favourite variant. If one passes, lock the final orientation copy with the founder, implement the selected specification, then run 200% text resize, 320 px reflow, keyboard focus, reduced motion, grayscale / colour-vision, strong-light, and low-brightness QA before production publication.
