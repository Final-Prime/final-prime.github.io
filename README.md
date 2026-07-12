# Final Prime public site

This repository contains the public website for **Final Prime™**.

## Current owner

Original Final Prime materials are currently owned by **Daniel Kenessy**, acting in an individual capacity, unless a file or notice identifies another owner or license. No rights have been assigned to a company.

Any future transfer to a company requires a separate signed assignment. GitHub organization ownership, repository hosting, domains, or public presentation do not by themselves transfer copyright or trademark rights.

## Public architecture

```text
/
├── systems/
├── works/
├── thought/
├── reviews/
│   └── metro-2033-redux/
├── index/
├── legal/
└── .well-known/security.txt
```

The website uses a conservative, logic-oriented visual language, orthogonal geometry, fuchsia and cyan signal modes, explicit public and private boundaries, and progressive enhancement. Core content remains usable without JavaScript.

The first published review record is `FP-REV-0001`, available at `/reviews/metro-2033-redux/`.

## Rights and permissions

This repository is proprietary. It is not released under an open source license.

- `LICENSE` reserves copyright and other rights.
- `NOTICE` identifies the current rights holder and claimed marks.
- `TRADEMARKS.md` defines nominative use and permission boundaries.
- `CONTRIBUTING.md` rejects unsolicited contributions until written terms exist.
- `SECURITY.md` defines private security reporting.
- `/legal/` publishes the current website-facing legal and IP notice.
- `docs/ip-policy.md` defines the publication and ownership gate.
- `docs/ip-register.md` contains the public IP summary.
- `docs/metro-2033-redux-import-audit.md` records the review migration provenance and third-party boundary.

Copyright © 2026 Daniel Kenessy. All rights reserved.

Claimed unregistered marks include Final Prime™, FINAL / PRIME™, the Final Prime logo, A/SYNC™, VRAXION™, the VRAXION logo, AlphaSync™, and INSTNCT™. No registration is claimed unless a later notice states otherwise.

## Legal safeguards

Automated checks reject:

- U+2013 and U+2014 long dash punctuation;
- use of the registered trademark symbol before registration;
- missing legal files or public legal route;
- inconsistent owner, license, and mark notices;
- inconsistent published-review score math, routes, registry state, or provenance.

Run locally:

```bash
python tools/check_editorial_style.py
python tools/check_ip_notices.py
python tools/check_review_registry.py
```

## Deployment

The site is deployed through GitHub Pages from the `main` branch and repository root.

Local preview:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Private boundary

Do not commit confidential source, client information, credentials, personal data, unpublished invention detail, private research evidence, or trade secrets. Patent-sensitive material must remain private until a filing, trade-secret, or intentional disclosure decision has been made.

Permission and rights requests: finalprime.official@gmail.com
