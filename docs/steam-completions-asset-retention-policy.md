# Steam Completions Asset Retention Policy

Canonical project rule  
Version: `v1.0`  
Owner: Daniel Kenessy  
Applies to: every Steam Completions game dossier, current and future

## 1. New-chat bootstrap rule

Before processing gameplay material in a new chat, read this policy and the active game's review protocol. This document is the durable source of truth when conversation context is incomplete.

Default assumption:

> Every relevant item supplied by Daniel is a retained project asset. Do not silently discard it because it is not yet selected for the public page.

## 2. Retention-first intake

Preserve all relevant supplied material, including:

- screenshots and image batches;
- UI captures and comparison crops;
- written gameplay notes and raw descriptions;
- session summaries and corrections;
- achievement, collection and relationship progress;
- reference images, covers, icons and social candidates;
- audio, video, transcript or measurement files when the available tooling supports them;
- alternate versions, unused candidates and early drafts that may become useful later.

Intake is intentionally broader than publication. Selection, cropping, compression and deletion decisions happen later.

## 3. No silent loss

Each supplied item must receive one of these outcomes:

1. committed as an asset;
2. committed as structured text or metadata;
3. recorded in the asset manifest as pending, blocked or intentionally excluded, with the reason stated.

An item must never disappear merely because it was not immediately used on the public page.

## 4. Raw and derived layers

Keep source material and edited outputs separate.

```text
assets/reviews/<game-slug>/
  raw/        original or closest safely retainable source
  curated/    selected and normalized evidence assets
  gallery/    publication-ready page assets
  social/     cards, covers and platform derivatives
docs/<game-slug>/
  asset-manifest.md
  session-log.md
  evidence-board.md
  screenshot-atlas.md
```

Rules:

- a crop, resize or re-encode does not replace its source;
- never overwrite an earlier asset version;
- use append-only versions when the same source is processed again;
- if an exact original cannot be committed because of size, privacy, rights or repository policy, retain the safest available derivative and record the original filename, hash when available, dimensions, size and blocking reason in the manifest;
- public page selection does not determine archival retention.

## 5. Stable naming

Use the active game's stable namespace.

Example for Moonlight Peaks:

```text
MP-SHOT-001__eye-customization__raw.png
MP-SHOT-001__eye-customization__web.webp
MP-SHOT-001__eye-customization__thumb.webp
```

General pattern:

```text
<asset-id>__<short-description>__<variant>.<ext>
```

Variants may include `raw`, `crop`, `web`, `thumb`, `social`, `annotated` and `comparison`.

## 6. Required manifest metadata

Each retained visual or media asset should track, when known:

- stable asset ID;
- original filename;
- source session or conversation capture;
- capture date and game build;
- byte size, dimensions and file type;
- checksum when available;
- caption and accessible alt text;
- spoiler level;
- source class;
- publication state: raw, private, undecided, public or superseded;
- linked claims, issues, achievements or chapters;
- derivative relationships;
- what the asset supports;
- what the asset cannot establish;
- rights, privacy or upload constraints.

## 7. Publication and privacy boundary

Retention-first does not override safety or rights boundaries.

Do not publish credentials, personal data, confidential material, private client data, trade secrets or unreviewed patent-sensitive content. Third-party game captures may be retained for commentary and review, but must keep their source and rights context explicit.

If an item cannot safely enter the public repository, create a manifest record instead of silently dropping it.

## 8. GitHub synchronization rule

Every Steam Completions update must end with a sync audit:

1. all new assets and derived metadata are committed or explicitly listed as pending;
2. the session log, evidence board, atlas and manifest agree on IDs and counts;
3. the pull request is merged only after required checks pass;
4. the merged files are verified on `main`;
5. the feature branch is deleted;
6. temporary workflows, diagnostic files and audit branches are deleted;
7. only `main` and intentionally active pull-request branches remain.

A step is not complete while relevant supplied material exists only in chat without either a GitHub asset or a manifest entry.

## 9. Public-page cadence

The repository may receive raw assets and evidence records more frequently than the public webpage changes. Public pages update at meaningful evidence milestones; archival sync happens continuously.

## 10. Active Moonlight Peaks application

For `FP-REV-0002`, all supplied Moonlight Peaks screenshots and future gameplay assets are retained by default. Current and future chats should use:

- `docs/moonlight-peaks-session-log.md`;
- `docs/moonlight-peaks-evidence-board.md`;
- `docs/moonlight-peaks-screenshot-atlas.md`;
- the asset structure under `assets/reviews/moonlight-peaks/`;
- this policy as the cross-chat retention rule.

The review remains evidence-led and append-only. Asset retention does not imply that every retained item must appear in the final public gallery.
