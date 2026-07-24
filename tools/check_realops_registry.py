#!/usr/bin/env python3
"""Verify the published REALOPS-01 dossier, registries, and frozen claim boundary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE_PATH = ROOT / "works" / "realops-01" / "index.html"
CSS_PATH = ROOT / "assets" / "realops-dossier.css"
PAGE03_PATH = ROOT / "works" / "realops-03" / "index.html"
CSS03_PATH = ROOT / "assets" / "realops03-dossier.css"

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
    page03 = PAGE03_PATH.read_text(encoding="utf-8")
    css03 = CSS03_PATH.read_text(encoding="utf-8")
    works = (ROOT / "works" / "index.html").read_text(encoding="utf-8")
    registry = (ROOT / "index" / "index.html").read_text(encoding="utf-8")
    audit = (ROOT / "docs" / "realops-01-import-audit.md").read_text(encoding="utf-8")
    audit03 = (ROOT / "docs" / "realops-03-import-audit.md").read_text(encoding="utf-8")

    for token in (
        'data-work-id="FP-WRK-0001"',
        '<meta name="robots" content="index,follow,max-image-preview:large">',
        '<link rel="canonical" href="https://final-prime.github.io/works/realops-01/">',
        '<link rel="stylesheet" href="/assets/realops-dossier.css?v=20260719-3">',
        '<meta property="article:published_time" content="2026-07-19">',
        '<meta property="article:modified_time" content="2026-07-23">',
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
        'data-work-id="FP-WRK-0002"',
        '<link rel="canonical" href="https://final-prime.github.io/works/realops-03/">',
        '<link rel="stylesheet" href="/assets/realops03-dossier.css?v=20260724-2">',
        '<script src="/assets/realops03-charts.js?v=20260724-1" defer></script>',
        '<meta property="article:published_time" content="2026-07-23">',
        '<h1 id="realops-title" itemprop="headline">The <span>Reliability Frontier</span></h1>',
        '<p class="frontier-subtitle">A 500-mission field test for AI agents</p>',
        'Agent missions</dt><dd>500 / 500 complete</dd>',
        'Blind Codex audit</dt><dd>500 + 140</dd>',
        'Use Sol / high by default.',
        'id="visual-evidence"',
        'Reliability × cost',
        'Reliability × active time',
        'Mission outcomes by profile',
        'id="profile-sol-high"',
        '100 / 100',
        '$0.752',
        '17 DAT disagreements',
        '27 OPS disagreements',
        'A routing result, not a universal leaderboard.',
        'no subagents, network, live repositories, credentials, or private raw evidence were exposed.',
        '/assets/works/realops-03/realops03-final-intelligence-cost.png',
        '/assets/works/realops-03/realops03-final-speed-intelligence-cost.png',
    ):
        require(page03, token, "REALOPS-03 page", errors)

    for token in (
        ".frontier-status-rail",
        ".realops03-route-grid",
        ".frontier-map-grid",
        ".native-plot",
        ".plot-point:hover .plot-tooltip",
        ".outcome-chart",
        ".realops03-figure-stack",
        ".realops03-scenario-grid",
        ".evidence-disclosure",
        "@media (max-width: 680px)",
        "@media (prefers-reduced-motion: reduce)",
        "@media print",
    ):
        require(css03, token, "REALOPS-03 CSS", errors)

    for relative in (
        "assets/works/realops-03/realops03-final-intelligence-cost.png",
        "assets/works/realops-03/realops03-final-intelligence-cost.svg",
        "assets/works/realops-03/realops03-final-speed-intelligence-cost.png",
        "assets/works/realops-03/realops03-final-speed-intelligence-cost.svg",
        "assets/works/realops-03/og-reliability-frontier.png",
    ):
        if not (ROOT / relative).is_file():
            errors.append(f"REALOPS-03 assets: missing {relative!r}")

    for token in (
        'href="/works/realops-01/"',
        'FP-WRK-0001 / Historical evidence dossier',
        'Public objects</dt><dd>03</dd>',
        'href="/works/realops-03/"',
        'FP-WRK-0002 / REALOPS-03 / Published evidence dossier',
    ):
        require(works, token, "Works Index", errors)

    for token in (
        '<span>FP-WRK-0001</span><strong>Published</strong>',
        '<h2>REALOPS-01 Agent Roster</h2>',
        '<dd>/works/realops-01/</dd>',
        'Disclosed records</dt><dd>10</dd>',
        '<span>FP-WRK-0002 / REALOPS-03</span><strong>Published</strong>',
        '<h2>The Reliability Frontier</h2>',
        '<dd>/works/realops-03/</dd>',
    ):
        require(registry, token, "Public Index", errors)

    for token in (
        "8538334F7DDC4E07C8148ACDEEB147CA806DCBAFB2D3B1A5E5D318F919D55837",
        "bfe4867b5f95c728b411a34fbeca503a0cef9c8d685f21f84f50791195d206e8",
        "3a65ca42cf1f9fdbf72cc639681638e1a6ad202dcd967e3bb5b14047fed13505",
        "The homepage featured record remains unchanged.",
    ):
        require(audit, token, "REALOPS import audit", errors)

    for token in (
        "095e074f3298ba1f3e5aba4193dd187dbb1c9fdf",
        "8da570e070021601ed458dcf3040470ed68620f5a05f14b0bbcffdafeda50888",
        "500 deterministic grades",
        "47 machine/audit disagreements",
        "Raw workspaces and the blind identity map remain private.",
    ):
        require(audit03, token, "REALOPS-03 import audit", errors)

    public_route_surfaces = "\n".join((page, page03, works, registry))
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
    print("Objects: FP-WRK-0001 / REALOPS-01; FP-WRK-0002 / REALOPS-03")
    print("Current scope: 5 profiles / 500 missions / evidence frozen 2026-07-23")
    print("Privacy: aggregate claims only; protected source locations absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
