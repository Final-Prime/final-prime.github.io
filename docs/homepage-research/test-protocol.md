# Anonymous homepage test protocol

Status: ready to run; no participant data has been collected. Version: 2026-07-17.

## Research question

Which hero structure produces controlled disorientation: visibly original and mysterious, while both non-specialists and business / technical visitors still understand the field, trust the source, and reach selected work?

This protocol compares structure, not final copy. The locked motto and the same orientation, founder status, and primary route appear in all three prototypes.

## Participants

- 12-16 anonymous participants total.
- 6-8 non-specialists who are not professionally responsible for software procurement or research.
- 6-8 people with business, technical, product, research, or commissioning experience.
- Recruit from the founder's own network and relevant communities.
- Record no name, handle, email, employer, IP address, analytics identifier, or screen recording.
- Assign only an anonymous code such as `L01` or `T01`.
- At least four moderated screen-share sessions in each cohort; remaining sessions may use the controlled self-test pack.

This is a small directional usability study, not a population estimate. Percentages are decision gates for this project, not generalised market claims.

## Materials

- Control: [desktop](hypotheses/control-root-trace-desktop.svg) / [mobile](hypotheses/control-root-trace-mobile.svg)
- Proof-led: [desktop](hypotheses/proof-led-desktop.svg) / [mobile](hypotheses/proof-led-mobile.svg)
- Sparse signal: [desktop](hypotheses/sparse-signal-desktop.svg) / [mobile](hypotheses/sparse-signal-mobile.svg)
- [Raw result template](test-results-template.csv)
- [Decision matrix](decision-matrix.csv)
- Desktop test size: 1440×900 or the nearest available size, recorded.
- Mobile test size: 390×844 or a real phone of comparable width, recorded.

Serve the prototypes locally or from a private preview. Do not place them on the public production route during research.

## Counterbalanced first exposure

The first five-second response is the primary datum. Each participant sees one randomly allocated first variant before knowing alternatives exist. Use the next unused row within the participant's cohort.

| Allocation | First | Second | Third |
|---|---|---|---|
| A | Control | Proof-led | Sparse signal |
| B | Control | Sparse signal | Proof-led |
| C | Proof-led | Control | Sparse signal |
| D | Proof-led | Sparse signal | Control |
| E | Sparse signal | Control | Proof-led |
| F | Sparse signal | Proof-led | Control |

Repeat A-F evenly inside each cohort. Randomise desktop-first versus mobile-first independently where possible. Do not change the first allocation after seeing a participant's reaction.

## Moderated session - 12 to 16 minutes

1. Read: “You are testing the page, not yourself. There are no right words. Please say what you believe you saw.”
2. Open the assigned first variant at the assigned device size. Show it for five seconds without scrolling or pointing.
3. Hide the page.
4. Ask, in this order, without prompting:
   - “What do you think this is?”
   - “What does it make or do?”
   - “Who do you think it is for?”
   - “What three words describe it?”
5. Show the page again. Say only: “Show me the work.” Start the timer when the page appears. Stop at the first activation of `Explore selected work`, a different route, or ten seconds.
6. Ask for 1-7 ratings: competent, human / approachable, original, mysterious, credible, confusing, arrogant, amateur, hostile, scam-like, and generic.
7. Repeat steps 2-6 for the remaining variants, but mark their reactions as comparison data, not independent first impressions.
8. Repeat the route task on the other device size. Ask the participant to narrate the order in which they read the hero.
9. Finish with: “What one thing would make you trust it more?” and “What one thing would you remove?”

Moderator must not explain Final Prime, define A/SYNC, name the intended CTA, defend the copy, or ask leading questions such as “Did it feel mysterious?” before free recall is complete.

## Controlled self-test pack

1. Give each participant a unique link or local instruction that opens only their allocated first variant.
2. Instruct them to start a five-second timer, close or cover the page when it ends, and answer the recall prompts before reopening it.
3. Use a local copy of the result sheet or an anonymous form with no login, analytics, or email collection.
4. Reveal the comparison links only after first-impression and first route-task answers are submitted.
5. Mark any participant who viewed a Final Prime variant beforehand; retain the data as contextual but exclude it from the primary first-impression gate.

## Coding rules

- `recognized_domain = 1` only if unaided recall clearly includes software, technical systems, research, or a close equivalent. “Creative agency” alone is 0.
- `recognized_primary_route = 1` only if the participant recalls that work / projects can be explored.
- `selected_work_first_try = 1` only when the first activated route is `Explore selected work`.
- `selected_work_under_10s = 1` only when first activation is at or below 10.0 seconds.
- Preserve the three adjectives verbatim, then code negative categories separately. Do not transform “cold” into “hostile” automatically.
- Ratings use integers 1-7, anchored as 1 “not at all” and 7 “extremely”.
- Missing values remain blank; never impute a pass.

## Decision gate

A variant can win only if **each cohort separately** meets all of the following:

- at least 75% recognise software / research / systems and the route to work;
- at least 80% find `Explore selected work` on the first attempt within ten seconds;
- median competence, originality, and interest is at least 5/7;
- median human / approachable is at least 4/7;
- median confusing, amateur, arrogant, hostile, and scam-like is at most 2/7;
- no critical WCAG AA failure and no mobile information loss is present.

With 6 participants in a cohort, 75% means at least 5 and 80% also means at least 5. With 7, each means at least 6. With 8, each means at least 6 for 75% and at least 7 for 80%. Report counts next to percentages so the small denominator remains visible.

If no variant passes every gate in both cohorts, declare **no winner**. Diagnose the failing dimensions, change only the relevant structure or copy, and run a new first-exposure round with new participants.

## Stop / invalidate rules

- Stop a session if the participant requests it or the page exposes personal information.
- Mark a five-second trial invalid if the page did not load, a modal covered it, or the participant had already studied that variant.
- Do not replace an invalid trial with a different first variant for the same participant; recruit a replacement for primary first-impression data.
- Do not pool the two cohorts to hide a cohort-level failure.
