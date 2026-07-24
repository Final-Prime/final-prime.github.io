# Moonlight Peaks Living Review Protocol

Record: `FP-REV-0002`  
Route: `/reviews/moonlight-peaks/`  
Lifecycle: `Sketch -> In Progress -> Provisional -> Stable -> Complete -> Revisit Needed`  
Working lens: `MOONLIT / Fantasy vs Routine`

## 1. Purpose

Build one append-only evidence base from the full Moonlight Peaks playthrough. The evidence base should support:

- a living public dossier;
- a final buyer review;
- an edited written playthrough;
- a screenshot evidence atlas;
- a completion and achievement analysis;
- patch and friction retests;
- short Steam and catalogue cards;
- narration-ready review and documentary scripts.

The public score, grade and buy action remain withheld until repeated evidence supports a stable collapse.

## 2. Source classes

Every material record must declare one source class:

- `PLAYER`: direct report from the reviewed run;
- `SCREENSHOT`: visible evidence supplied from the run;
- `PROGRESS`: playtime, achievement, collection or relationship state;
- `OFFICIAL`: store, patch or developer context;
- `INTERPRETATION`: an inference built from evidence;
- `UNKNOWN`: material uncertainty that remains open.

Official or public context can route testing. It cannot substitute for direct-play evidence.

## 3. Stable identifiers

Use these namespaces:

- `MP-Sxx`: gameplay session;
- `MP-CLM-xxx`: review claim;
- `MP-ISS-xxx`: friction, bug or trust issue;
- `MP-SHOT-xxx`: screenshot evidence object;
- `MP-ACH-xxx`: achievement or completion event;
- `MP-REL-xxx`: relationship thread;
- `MP-PAT-xxx`: patch or build retest;
- `MP-Qxx`: open question;
- `MP-CHxx`: edited playthrough chapter.

Identifiers are never reused after publication or rejection.

## 4. MOONLIT axes

### M - Myth and Identity / 15%

Does vampirehood alter rules, choices, routines, relationships and the world, or mainly provide aesthetic framing?

### O - Ongoing Loop / 20%

Does farming, magic, collection, travel and social play remain satisfying after novelty decays?

### O - Ownership and Agency / 10%

Do schedule, economy, upgrade, relationship and homestead choices produce meaningfully different priorities?

### N - Neighbourhood and Narrative / 10%

Do characters, families and story threads develop beyond task delivery and repeated gifts?

### L - Long-tail Completion / 20%

Does completion reward mastery, discovery and authored closure, or mostly require volume and cleanup?

### I - Information and Trust / 10%

Are quests, gifts, seasons, collections, rules and achievement conditions readable and dependable?

### T - Technical Readiness / 15%

Can saves, input, performance, progression and achievements support a long run across patches?

## 5. Final Prime crosswalk

MOONLIT feeds the shared public hero axes:

- Promise;
- Core Loop;
- Agency;
- Trust;
- Time;
- Readiness.

The legacy PLATER card is a final compact export only. It must be derived from the mature evidence board rather than independently mood-scored.

## 6. Session processing

For each gameplay report:

1. preserve the raw supplied material;
2. create one `MP-Sxx` session record;
3. separate event, reaction, interpretation and unknown;
4. create or update linked claim and issue records;
5. assign screenshot and progress identifiers;
6. record axis deltas with reasons;
7. identify counterevidence and the next useful question;
8. update confidence only when evidence repeats or closes a major unknown;
9. publish only when a milestone changes the public state.

Old observations remain append-only. A later contradiction creates a new record and visible revision path.

## 7. Evidence gates

### Gate 0 - Scaffold

Required:

- explicit lens;
- score lock;
- capability boundary;
- open-question board;
- source and identifier rules.

Public state: `Sketch`.

### Gate 1 - First loop / approximately 0-8 hours

Test:

- onboarding and control trust;
- first-night rhythm;
- early farming, magic and economy;
- movement and travel;
- initial relationship structure;
- save, performance and build baseline.

Target public state: `In Progress`.

### Gate 2 - Novelty decay / approximately 15-25 hours

Test:

- repeated routine fatigue;
- economy scaling;
- new systems and decision value;
- relationship depth;
- information debt;
- achievement trust;
- repeated friction across sessions.

Possible public state: `Provisional`.

### Gate 3 - Mainline closure

Test:

- narrative payoff;
- mature-system quality;
- late economy and progression;
- audience fit;
- evidence consistency;
- score eligibility.

Possible public state: `Stable`.

### Gate 4 - Completion tail

Test:

- cleanup duration and quality;
- collection legibility;
- missables and guide dependence;
- mastery versus volume;
- achievement triggers;
- effect of the final hours on the verdict.

Target public state: `Complete`.

### Gate R - Material change

A material patch, DLC, progression repair or achievement change opens a bounded retest and may move the dossier to `Revisit Needed`.

## 8. Completion taxonomy

Classify each tracked objective as one or more of:

- natural progress;
- mainline;
- mastery;
- discovery;
- relationship;
- collection;
- economy or volume;
- cleanup-only;
- missable;
- guide-dependent;
- patch-sensitive;
- trigger-risk.

The final dossier must distinguish the quality of finishing the game from the quality of completing it.

## 9. Screenshot protocol

Each screenshot record stores:

- identifier;
- source session;
- original filename;
- date and build when known;
- caption and accessible alt text;
- spoiler level: `light`, `medium` or `heavy`;
- publication state: `private`, `undecided` or `public`;
- linked claims or issues;
- what the image supports;
- what the image cannot establish.

A screenshot cannot establish continuous motion, audio balance, frame pacing or events outside the captured frame.

## 10. Written playthrough protocol

The edited chronicle may contain:

1. Arrival and First Night;
2. Routine Takes Shape;
3. The Town Opens;
4. Novelty Decay;
5. Mainline Closure;
6. Completion Afterlife.

Only supplied or directly supported events may be reconstructed. Missing connective scenes must not be invented.

## 11. Narration protocol

Supported outputs:

- 60-90 second verdict;
- 5-8 minute buyer review;
- 15-25 minute documentary review;
- chapter timing;
- screenshot and on-screen-text cues;
- spoiler boundaries;
- pronunciation notes.

Without original footage or audio, the durable artifact is the script and cue sheet, not a fabricated finished gameplay video or custom authored voice track.

## 12. Adversarial checks

Before a public verdict, test:

- lens honesty;
- comfort and aesthetic bias;
- sampling bias;
- novelty decay;
- friction blindness;
- patch volatility;
- achievement and save trust;
- audience confusion;
- completion survivorship bias;
- whether the current opinion could be falsified by an untested late-game condition.

## 13. Collapse rules

Do not publish a numeric score while:

- the core loop is not understood;
- repeated sessions have not converged;
- a major save, progression or achievement risk remains unresolved;
- the mainline or relevant completion layer remains materially untested;
- the review cannot state what evidence would overturn its verdict.

Confidence measures verdict stability, not enjoyment.
