#!/usr/bin/env python3
"""Verify the published REALOPS-01 dossier, registries, and frozen claim boundary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "works" / "realops-01" / "index.html"
CSS_PATH = ROOT / "assets" / "realops-dossier.css"

PROFILES = (
    {
        "role": "Cheap Worker",
        "cell": "Luna / medium",
        "rsp": "1/5",
        "mrx": "5/5",
        "combined": "6/10",
        "catastrophic": "3",
        "cost": "$0.230991",
        "output": "140,851",
        "reasoning": "30,541",
        "meter": ".token-meter .token-cheap { width: 35.47%; }",
    },
    {
        "role": "Budget Worker",
        "cell": "Terra / high",
        "rsp": "3/5",
        "mrx": "5/5",
        "combined": "8/10",
        "catastrophic": "1",
        "cost": "$0.614593",
        "output": "168,009",
        "reasoning": "51,962",
        "meter": ".token-meter .token-budget { width: 42.31%; }",
    },
    {
        "role": "Sweetspot Agent",
        "cell": "Sol / high",
        "rsp": "4/5",
        "mrx": "5/5",
        "combined": "9/10",
        "catastrophic": "0",
        "cost": "$1.237069",
        "output": "169,900",
        "reasoning": "56,534",
        "meter": ".token-meter .token-sweetspot { width: 42.78%; }",
    },
    {
        "role": "Smart Agent",
        "cell": "Sol / max",
        "rsp": "5/5",
        "mrx": "5/5",
        "combined": "10/10",
        "catastrophic": "0",
        "cost": "$2.543873",
        "output": "397,134",
        "reasoning": "216,476",
        "meter": ".token-meter .token-smart { width: 100%; }",
    },
)


def require(content: str, token: str, surface: str, errors: list[str]) -> None:
    if token not in content:
        errors.append(f"{surface}: missing {token!r}")


def main() -> int:
    errors: list[str] = []
    page = PAGE_PATH.read_text(encoding="utf-8")
    css = CSS_PATH.read_text(encoding="utf-8")
    works = (ROOT / "works" / "index.html").read_text(encoding="utf-8")
    registry = (ROOT / "index" / "index.html").read_text(encoding="utf-8")
    audit = (ROOT / "docs" / "realops-01-import-audit.md").read_text(encoding="utf-8")

    for token in (
        'data-work-id="FP-WRK-0001"',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        '<link rel="canonical" href="https://final-prime.github.io/works/realops-01/">',
        '<meta property="article:published_time" content="2026-07-19">',
        '<meta property="article:modified_time" content="2026-07-19">',
        'Evidence frozen</dt><dd><time datetime="2026-07-18">18 Jul 2026</time>',
        'Standard missions</dt><dd>40</dd>',
        'Profiles</dt><dd>04</dd>',
        'Subagents / network</dt><dd>None</dd>',
        'Primary outcome: deterministic valid mission.',
        'It is not a universal model-intelligence ranking.',
        'Five runs per cell do not establish broad statistical superiority.',
        'MRX-01 saturated at 5/5 for all four profiles.',
        'Estimated list costs are tied to this frozen task mix and price snapshot.',
        'Role labels do not remove the need for task-appropriate checks.',
        'Sol / ultra</span><h3>Managed control</h3>',
        'Public aggregate only. Raw fixtures, prompts, transcripts, live repositories, and hidden grader details remain private.',
    ):
        require(page, token, "REALOPS page", errors)

    if "noindex" in page.lower():
        errors.append("REALOPS page: published route must not declare noindex")

    for profile in PROFILES:
        row = (
            f'<tr><th scope="row">{profile["role"]}</th><td>{profile["cell"]}</td>'
            f'<td>{profile["rsp"]}</td><td>{profile["mrx"]}</td>'
            f'<td>{profile["combined"]}</td><td>{profile["catastrophic"]}</td>'
            f'<td>{profile["cost"]}</td><td>{profile["output"]}</td>'
            f'<td>{profile["reasoning"]}</td></tr>'
        )
        require(page, row, f'{profile["role"]} exact table row', errors)
        require(css, profile["meter"], f'{profile["role"]} token meter', errors)

    for token in (
        'href="/works/realops-01/"',
        'FP-WRK-0001 / Published evidence dossier',
        'Public objects</dt><dd>02</dd>',
    ):
        require(works, token, "Works Index", errors)

    for token in (
        '<span>FP-WRK-0001</span><strong>Published</strong>',
        '<h2>REALOPS-01 Agent Roster</h2>',
        '<dd>/works/realops-01/</dd>',
        'Disclosed records</dt><dd>09</dd>',
    ):
        require(registry, token, "Public Index", errors)

    for token in (
        "8538334F7DDC4E07C8148ACDEEB147CA806DCBAFB2D3B1A5E5D318F919D55837",
        "bfe4867b5f95c728b411a34fbeca503a0cef9c8d685f21f84f50791195d206e8",
        "3a65ca42cf1f9fdbf72cc639681638e1a6ad202dcd967e3bb5b14047fed13505",
        "The homepage featured record remains unchanged.",
    ):
        require(audit, token, "REALOPS import audit", errors)

    public_route_surfaces = "\n".join((page, works, registry))
    for forbidden in (
        "systems-lab-bh-symmetry-research",
        "projects/agent-eval-suite",
        "realops-all-profiles-data.json",
        "C:\\Users\\",
    ):
        if forbidden.lower() in public_route_surfaces.lower():
            errors.append(f"public REALOPS surface exposes protected source location {forbidden!r}")

    if errors:
        print("REALOPS registry check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("REALOPS registry check passed.")
    print("Object: FP-WRK-0001 / REALOPS-01")
    print("Scope: 4 profiles / 40 matched missions / evidence frozen 2026-07-18")
    print("Privacy: aggregate claims only; protected source locations absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
