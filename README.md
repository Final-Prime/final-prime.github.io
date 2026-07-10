# Final Prime — public site

This repository contains the public website for **Final Prime**.

## Design intent

- conservative, logic-oriented visual language;
- no external fonts, frameworks, analytics, or tracking;
- truthful early-stage positioning without implying a registered legal entity or launched product;
- responsive and keyboard-accessible static implementation;
- progressive enhancement: core content remains usable without JavaScript.

## Structure

```text
.
├── index.html
├── 404.html
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── .nojekyll
├── assets/
│   ├── app.js
│   ├── styles.css
│   ├── mark.svg
│   ├── favicon.svg
│   └── og-cover.svg
└── docs/
    └── quality-report.md
```

## Local preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Deployment

The site is designed for GitHub Pages from the `main` branch, repository root.

## Rights

No open-source license is granted by this repository. Unless stated otherwise, all rights are reserved.
