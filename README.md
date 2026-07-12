# Final Prime — public site

This repository contains the public website for **Final Prime**.

## Current design system

- conservative, logic-oriented visual language;
- orthogonal geometry with no decorative rounding;
- fuchsia `#f5054d` as the primary signal and cyan `#0ae8f7` as the rare verified/access signal;
- four-branch public information architecture: `Systems / Works / Thought / Index`;
- product surfaces remain public where reviewable; source code, research internals and serious business activity remain private by default;
- a dedicated game-review surface under `Thought`, with an honest pre-publication state and reusable review pipeline;
- no external fonts, frameworks, analytics, cookies or trackers;
- truthful early-stage positioning without implying a registered legal entity, launched account platform, clients or public technical results;
- responsive and keyboard-accessible static implementation;
- progressive enhancement: core content remains usable without JavaScript.

## Structure

```text
.
├── index.html
├── reviews/
│   └── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── .nojekyll
├── assets/
│   ├── app.js
│   ├── styles.css
│   ├── base.css
│   ├── hero.css
│   ├── content-a.css
│   ├── content-b.css
│   ├── responsive.css
│   ├── hardening.css
│   ├── reviews.css
│   ├── mark.svg
│   ├── favicon.svg
│   └── og-cover.svg
└── docs/
    ├── quality-report.md
    └── review-surface-audit.md
```

## Local preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deployment

The site is deployed through GitHub Pages from the `main` branch, repository root.

## Game review surface

The homepage contains an upcoming-review slot and links to `/reviews/`. Until the first review is actually ready, the public surface shows only:

- the stable object ID `FP-REV-0001`;
- the truthful state `In research`;
- the production pipeline `Experience → Model → Verify → Publish`;
- the declared review lens;
- an explicit empty archive.

No game title, verdict, score or publication date is invented in advance.

## Prime Access wording

Prime Access is presented as an interface and operating-model preview only. No public account or proposal-tracking backend is claimed to be live.

## Rights

No open-source license is granted by this repository. Unless stated otherwise, all rights are reserved.
