# Moonlight Peaks Dossier Adversarial Polish Audit

Record: `FP-REV-0002`
Audit date: `2026-07-24`
Scope: information architecture, copy, visual hierarchy, evidence integrity, accessibility, performance, score lock and mobile resilience
Result: `refined / integration-ready / browser visual pass still required in an authenticated repository environment`

## 1. Executive finding

The original scaffold was methodologically strong but reader-hostile in one important way: it explained the review system before showing the game. That made the route feel like a specification page rather than a living review.

The polish pass changes the order of value:

1. current reading;
2. first-contact evidence;
3. review method;
4. MOONLIT diagnostic;
5. active claims;
6. completion watch;
7. staged questions;
8. publication roadmap;
9. provenance and limits.

The score remains locked. No buyer action or numeric rating is introduced.

## 2. Adversarial findings and resolutions

### A01 - Evidence was buried below process

Risk: a reader could leave before seeing any direct-play material.

Resolution:

- add an actual evidence frame to the hero;
- move `Current reading` and `First contact` above the method;
- publish the eight curated screenshot derivatives with captions, alt text and proof limits.

### A02 - The page gave equal visual weight to unequal information

Risk: methodology, capability, future outputs and current findings all appeared as similarly sized card grids.

Resolution:

- establish a strong hierarchy: hero, current state, evidence, method, diagnostic and later gates;
- reduce repeated generic capability cards;
- use distinct visual roles for pull, drag, risk, next test, claim and unknown.

### A03 - The opening could be mistaken for a provisional review

Risk: polished language and a large dossier surface may imply more confidence than the evidence supports.

Resolution:

- change the hero record to `FIRST CONTACT`;
- state `The fantasy has landed. The routine is still untested.`;
- show `MP-S01 open`, build unknown and score withheld;
- repeat supported versus unsupported scope near the top.

### A04 - Aesthetic preference could inflate the evaluation

Risk: Daniel likes horror and gothic presentation, so visual appeal may contaminate loop judgment.

Resolution:

- preserve the reviewer-taste calibration;
- surface `Aesthetic bias` as an active adversarial test;
- separate presentation craft from mechanical quality.

### A05 - Dialogue choice could be overread as agency

Risk: three tonal responses may be described as meaningful branching before consequences are observed.

Resolution:

- claim only tonal role-play;
- list persistence and later state as a critical unknown;
- set Ownership and Agency to `Watch`, not positive.

### A06 - Dög could be misclassified

Risk: visual resemblance may encourage `pet` or `familiar` language without evidence.

Resolution:

- claim only that Dög is a speaking travel character;
- keep pet, familiar, guide and gameplay-helper classifications open.

### A07 - Screenshot evidence could become decoration

Risk: attractive game captures may function as marketing rather than evidence.

Resolution:

- every image receives an ID, session, caption, alt text, support statement and proof limit;
- opening screenshots are marked as light spoilers;
- the page states what still images cannot establish.

### A08 - The question board created attention overload

Risk: twelve equally active questions are not useful during the first full day.

Resolution:

- activate six day-one questions;
- lock three midgame and three completion questions;
- route attention to the next slice of play.

### A09 - Completion ambition could contaminate the early verdict

Risk: a strong achievement shape on paper could be mistaken for good completion design.

Resolution:

- keep all completion categories locked or on watch;
- state that completion quality is unknown;
- preserve separate mainline and 100 percent verdicts.

### A10 - Asset retention and page curation could conflict

Risk: assets not selected for the gallery might disappear.

Resolution:

- add `docs/moonlight-peaks-asset-manifest.md`;
- retain all eight supplied screenshots as optimized repository derivatives;
- preserve exact original filenames, dimensions, byte sizes and SHA-256 hashes;
- state the 1 MiB source-file limitation explicitly;
- keep raw, curated, gallery and social concepts separate.

### A11 - Page weight could grow without control

Risk: full-resolution screenshots would add more than 18 MiB to a single early capture.

Resolution:

- normalize each public derivative to 1440 px maximum width;
- retain PNG for repository policy compatibility;
- keep each derivative below the repository's 1 MiB tracked-file limit;
- use explicit width and height;
- load the hero image eagerly and all gallery images lazily.

### A12 - Mobile cards could become a long undifferentiated scroll

Risk: dense multi-column layouts collapse into a tedious one-column stack.

Resolution:

- reduce the top-level section count;
- group related questions;
- keep card minimum heights lower on mobile;
- collapse proof bands and metadata into clean single-column rows;
- preserve horizontal section navigation with scroll containment.

### A13 - Motion could undermine accessibility

Risk: hover zoom or section navigation could add unnecessary motion.

Resolution:

- keep motion limited to a slight image hover;
- disable that transition and transform under `prefers-reduced-motion`;
- preserve forced-colors and reduced-transparency fallbacks.

### A14 - Social preview did not communicate lifecycle

Risk: a generic site card could make the route look like a finished scored review.

Resolution:

- add a dedicated 1200x630 first-contact social card;
- include `LIVING REVIEW`, `FIRST CONTACT` and `SCORE WITHHELD`;
- derive the image from `MP-SHOT-008` without adding new evidence.

## 3. Copy refinements

The pass removes or reduces:

- repeated explanations of what the system can theoretically produce;
- generic process language before current findings;
- broad statements that could read as conclusions about the full game;
- repeated use of `unknown` without naming the next falsifier.

The pass adds:

- a direct current-reading sentence;
- a bounded opening chronology;
- claim confidence and proof limits;
- current pull, drag, risk and next test;
- a staged question board;
- clear first-contact lifecycle language.

## 4. Information architecture

New public flow:

```text
Hero and score lock
-> Current reading
-> First-contact evidence
-> Review contract
-> MOONLIT diagnostic
-> Active evidence ledger
-> Completion observatory
-> Staged questions
-> Publication roadmap
-> Provenance and limits
```

This preserves the evidence-led method while making the route useful to a reader who does not need the whole methodology first.

## 5. Static integrity checks

Required checks for the final repository tree:

- exactly one `h1`;
- unique HTML IDs;
- all fragment links resolve;
- every screenshot has non-empty alt text;
- all images expose width and height;
- hero image uses eager priority;
- gallery images use lazy loading;
- no U+2013 or U+2014 punctuation;
- no numeric review score;
- no grade;
- no buyer action;
- no `Review` structured data;
- `SCORE LOCKED` remains visible;
- `MP-S01 open` remains visible;
- all eight screenshot IDs appear;
- all retained assets remain below 1 MiB;
- PNG files contain only allowed chunks;
- social image is exactly 1200x630;
- session, evidence, atlas and manifest counts reconcile;
- merged files are verified on `main`;
- feature and temporary branches are deleted.

## 6. Remaining browser gate

The sandbox Chromium navigation policy blocks local page navigation, so this package does not claim a completed browser-render visual inspection. The authenticated repository pass should still test:

- 320, 390, 768, 1280, 1440 and 1920 px widths;
- horizontal overflow;
- sticky section navigation;
- keyboard focus order;
- image loading and aspect-ratio stability;
- forced-colors;
- reduced-motion;
- print layout;
- no console errors.

The page is statically structured for these checks, but the browser gate remains an explicit final verification rather than an invented success claim.
