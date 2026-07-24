# Moonlight Peaks Session Intake

Use this as a convenience, not a requirement. Free-form gameplay reports are valid input.

```text
Session date:
Session duration:
Total playtime:
Build / patch:
Platform / device:

What happened:

Best moment:

Main friction:

What was unclear:

Did an earlier opinion change:

Progress:
- story / quest:
- farm / home:
- magic / upgrades:
- relationship:
- achievement / collection:

Screenshots:
- filename or upload order:
- what it shows:
- spoiler level, if known:

Anything that may be a bug:

What should be tested next:
```

## Canonical compressed form

```text
#[MP-Sxx] | [YYYY-MM-DD] | [build]
Milestone: [what changed]
Session: [duration] | Total: [duration] | Mode: solo
Micro: Clarity [0-4] · Mastery [0-4] · Tension [0-4] · Fatigue [0-4] · Social [0-4] · Desire [0-4]
Observation: [loss-aware 1-2 sentence compression]
Axis delta: [MOONLIT or Final Prime axis +1/-1/0, with reason]
Open question: [next useful uncertainty]
```

## Screenshot record

```text
MP-SHOT-xxx
Source session:
Original filename:
Date / build:
Caption:
Alt text:
Spoiler: light / medium / heavy
Publication: private / undecided / public
Supports:
Does not establish:
Linked claims / issues:
```

## Friction or bug record

```text
MP-ISS-xxx
First observed:
Build:
Category:
Frequency:
Severity:
Player impact:
Reproduction notes:
Evidence:
Patch state: open / claimed fixed / retest pending / fixed / partial / regressed
Retest result:
Affected axes:
```

## Achievement or completion record

```text
MP-ACH-xxx
Name / objective:
Unlocked:
Source session:
Category: natural / mainline / mastery / discovery / relationship / collection / volume / cleanup
Missable:
Guide dependence:
Trigger trust:
Time cost:
Did it add new decisions:
Verdict note:
```

## Processing rules

- Preserve the supplied report before compression.
- Do not infer unreported events.
- Separate observation, interpretation and unknown.
- Keep old reactions append-only.
- Treat screenshots as bounded evidence.
- Do not unlock a score from one unusually good or bad session.
