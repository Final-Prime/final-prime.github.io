#!/usr/bin/env python3
"""Validate the complete local navigation and asset graph."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import struct
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://final-prime.github.io"
REFERENCE_ATTRIBUTES = ("href", "src", "poster", "action")
ARIA_IDREF_ATTRIBUTES = ("aria-controls", "aria-describedby", "aria-labelledby")
CSS_REFERENCE = re.compile(r"(?:@import\s+url\(|@import\s+|url\()\s*['\"]?([^'\")\s]+)")
CSS_CLASS_SELECTOR = re.compile(r"(?<![\w-])\.([A-Za-z_-][\w-]*)")
SCRIPT_BUDGETS = {
    "assets/app.js": 7100,
    "assets/home.js": 11500,
    "assets/motto-glitch.js": 1300,
    "assets/review-dossier.js": 7600,
    "assets/scroll-readout.js": 1400,
}
FORBIDDEN_SCRIPT_PATTERNS = ("document.write(", "eval(", "new Function(")
FORBIDDEN_ROUTE_STYLESHEETS = {
    "index.html": {"/assets/catalog.css", "/assets/review-release.css"},
    "404.html": {
        "/assets/content-a.css",
        "/assets/content-b.css",
        "/assets/hero.css",
        "/assets/responsive.css",
        "/assets/surface-polish.css",
    },
    "contact/index.html": {
        "/assets/content-a.css",
        "/assets/hardening.css",
        "/assets/hero.css",
        "/assets/reviews.css",
        "/assets/review-release.css",
    },
    "systems/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "works/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "thought/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css", "/assets/reviews.css", "/assets/review-release.css"},
    "reviews/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "reviews/metro-2033-redux/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css", "/assets/reviews.css", "/assets/catalog.css", "/assets/review-release.css"},
    "index/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "legal/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
}
RESPONSIVE_PRECEDENCE_STYLES = {
    "/assets/hero.css",
    "/assets/content-a.css",
    "/assets/content-b.css",
}
REQUIRED_ICON_LINKS = {
    ("icon", "/assets/favicon.svg", "image/svg+xml", ""),
    ("icon", "/assets/icon-192.png", "image/png", "192x192"),
    ("apple-touch-icon", "/apple-touch-icon.png", "", "180x180"),
}
REQUIRED_MANIFEST_ICONS = {
    ("/assets/favicon.svg", "any", "image/svg+xml", "any"),
    ("/assets/icon-192.png", "192x192", "image/png", "any"),
    ("/assets/icon-512.png", "512x512", "image/png", "any"),
    ("/assets/icon-maskable-192.png", "192x192", "image/png", "maskable"),
    ("/assets/icon-maskable-512.png", "512x512", "image/png", "maskable"),
}
REQUIRED_PNG_DIMENSIONS = {
    "apple-touch-icon.png": (180, 180),
    "assets/icon-192.png": (192, 192),
    "assets/icon-512.png": (512, 512),
    "assets/icon-maskable-192.png": (192, 192),
    "assets/icon-maskable-512.png": (512, 512),
}
PRINT_CONTRACT_TOKENS = (
    "@media print",
    "--bg: #fff;",
    ".skip-link,",
    ".menu-toggle,",
    "body * {",
    "background-image: none !important;",
    "button { display: none !important; }",
    "animation: none !important;",
    "orphans: 3; widows: 3;",
    "break-inside: avoid-page;",
    ".dossier-hero-grid { grid-template-columns: 1fr !important; }",
    ".evidence-arc-body {",
    "[data-evidence-status] { display: none !important; }",
    ".evidence-arc summary::after { display: none !important; }",
    "display: grid !important;",
)
REFLOW_CONTRACT_TOKENS = (
    ".dossier-section-head h2 {",
    "overflow-wrap: anywhere;",
    ".dossier-axis > header,",
    ".score-equation > div {",
)
DOSSIER_POLISH_REFLOW_TOKEN = (
    ".review-dossier-page .dossier-axis h3 {\n"
    "  overflow-wrap: anywhere;"
)
ROUTE_REFLOW_CONTRACTS = {
    "assets/base.css": (
        "html { scroll-behavior: auto;",
        "transition: none;",
        ".section-head > * { min-width: 0; }",
        ".section-head h2 {",
        "overflow-wrap: anywhere;",
    ),
    "assets/catalog.css": (
        ".catalog-hero h1 {",
        ".catalog-intro {",
        ".release-lane h2 {",
        ".boundary-copy h2 {",
        ".catalog-empty h2 {",
        "overflow-wrap: anywhere;",
    ),
    "assets/content-b.css": (
        ".contact-layout h2 {",
        "overflow-wrap: anywhere;",
    ),
    "assets/hero.css": (
        ".eyebrow-copy {",
        ".eyebrow-term { white-space: nowrap; }",
        ".hero-wordmark {",
        ".wordmark-prime {",
        ".doctrine strong {",
        ".hero-orientation-panel {",
    ),
    "assets/legal.css": (
        ".legal-card h2 {",
        "overflow-wrap: anywhere;",
    ),
}
NO_JS_CONTRACT_TOKENS = (
    "html .review-dossier-page .evidence-toolbar-actions",
    "html .menu-toggle { display: none; }",
    "html .site-nav {",
)
PROGRESSIVE_ENHANCEMENT_CONTRACT = {
    "assets/app.js": ('classList.replace("no-js", "js")', "menuToggle.hidden = false"),
    "assets/responsive.css": (
        "html.no-js .site-nav",
        "max-height: calc(100dvh - var(--header-height) - 16px);",
        "overflow-y: auto;",
        "overscroll-behavior: contain;",
    ),
    "reviews/metro-2033-redux/index.html": ('class="evidence-toolbar-actions" hidden',),
    "assets/review-dossier.js": ('.removeAttribute("hidden")',),
    "assets/base.css": ("[hidden] { display: none !important; }",),
}

NAVIGATION_POLISH_CONTRACT = (
    ".site-header.is-scrolled {",
    "0 10px 28px rgba(245, 5, 77, 0.08)",
    ".site-nav a::after {",
    "background: var(--cyan);",
    ".site-nav a:hover::after,",
    ".site-nav a:focus-visible::after",
)

HEADER_LAYOUT_CONTRACT = {
    "assets/base.css": (
        "--header-height: 64px;",
        "position: sticky;",
        "height: var(--header-height);",
        "background-color: #0c0e10;",
        "linear-gradient(180deg, rgba(255, 255, 255, 0.026) 0%, transparent 58%)",
        "linear-gradient(90deg, rgba(10, 232, 247, 0.025) 0%, transparent 26%, transparent 70%, rgba(245, 5, 77, 0.04) 100%)",
        "inset 0 1px 0 rgba(255, 255, 255, 0.026)",
        "background-color: rgba(9, 11, 13, 0.80);",
        "background-color: rgba(9, 11, 13, 0.92);",
        "backdrop-filter: blur(18px) saturate(112%);",
        "transition: background-color 200ms ease, border-color 200ms ease, box-shadow 200ms ease;",
        "@supports ((-webkit-backdrop-filter: blur(1px)) or (backdrop-filter: blur(1px)))",
        "@media (prefers-reduced-transparency: reduce)",
        "@media print {",
        "background-image: none;",
        "min-height: 44px;",
        ".brand-name { display: inline-flex; gap: 0.42em;",
        ".brand-divider { min-width: 0.75em;",
        ".menu-toggle { display: none; width: 46px; height: 46px;",
        "gap: clamp(18px, 2.2vw, 28px);",
        "gap: clamp(16px, 2vw, 26px);",
    ),
    "assets/responsive.css": (
        "--header-height: 60px;",
        ".site-nav a { min-height: 52px;",
    ),
    "assets/error.css": ("--header-height: 60px;",),
    "assets/surface-polish.css": (
        '.site-nav a[aria-current="page"]::after,',
        "opacity: 1;",
        "background: var(--fuchsia);",
        "transform: scaleX(1);",
    ),
}

SCROLL_READOUT_CONTRACT = {
    "assets/scroll-readout.js": (
        'document.createElement("output")',
        'readout.setAttribute("aria-hidden", "true")',
        'document.body.classList.contains("review-dossier-page")',
        'window.matchMedia("(min-width: 1081px)")',
        'window.requestAnimationFrame(update)',
        'readout.hidden = percent === 0',
        'readout.value = `${percent}%`',
        'window.addEventListener("scroll", scheduleUpdate, { passive: true })',
    ),
    "assets/surface-polish.css": (
        ".scroll-readout {",
        "body.menu-open .scroll-readout { display: none; }",
        "@media (max-width: 1080px)",
    ),
}

RETIRED_HEADER_TOKENS = (
    "site-progress",
    "data-scroll-progress",
    "is-header-hidden",
    "header-scroll-direction",
)
HEADER_GLITCH_CONTRACT = {
    "assets/app.js": (
        'header.querySelector(".brand")',
        'matchMedia("(prefers-reduced-motion: reduce)")',
        '30000 + Math.random() * 20000',
        'document.querySelector(".hero-motto.is-glitching,.brand:is(:hover,:focus-visible,.is-glitching)")',
        'document.hidden',
        '"is-glitching"',
        '"pointerdown"',
        '"visibilitychange"',
    ),
    "assets/signal-glitch.css": (
        ".site-header .brand-mark",
        ".site-header .brand-name",
        ".site-header .brand-word-final",
        ".site-header .brand-word-prime",
        ".site-header .brand-divider",
        "var(--echo-near) 0 0 rgba(var(--echo-rgb), 0.46)",
        "var(--echo-mid) 0 1px rgba(var(--echo-rgb), 0.23)",
        "var(--echo-far) 0 2.4px rgba(var(--echo-rgb), 0.10)",
        "-1px -1px 0.2px rgba(10, 232, 247, 0.54)",
        "1px 1px 0.2px rgba(245, 5, 77, 0.58)",
        ".site-header .brand.is-glitching .brand-mark",
        ".site-header .brand.is-glitching .brand-name",
        ".site-header .brand.is-glitching .brand-word",
        ".site-header .brand.is-glitching .brand-divider",
        "460ms steps(1, end) 1",
        "@keyframes fp-brand-mark-trigger",
        "@keyframes fp-brand-name-trigger",
        "@keyframes fp-brand-echo-trigger",
        "@keyframes fp-brand-divider-trigger",
        "@media (prefers-reduced-motion: reduce)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

HERO_WORDMARK_CONTRACT = {
    "assets/hero.css": (
        ".hero-wordmark > span {",
        ".wordmark-final {",
        "-0.118em 0.014em 0.07em rgba(10, 232, 247, 0.07)",
        ".wordmark-prime {",
        "0.118em 0.014em 0.07em rgba(245, 5, 77, 0.07)",
        ".wordmark-divider {",
        "transform: translateY(-0.035em) scaleX(0.96);",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

HOMEPAGE_MOTTO_CONTRACT = {
    "index.html": (
        '<link rel="preload" href="/assets/fonts/inter-v4.1/InterVariable.woff2" as="font" type="font/woff2" crossorigin>',
        '<link rel="stylesheet" href="/assets/hero.css?v=20260718-9">',
        '<script src="/assets/motto-glitch.js?v=20260718-2" defer></script>',
        '<p class="doctrine hero-motto">',
        '<strong class="doctrine-cyan"><span class="doctrine-effect" aria-hidden="true">is survival.</span><span class="doctrine-core">is survival.</span></strong>',
        '<strong class="doctrine-fuchsia"><span class="doctrine-effect" aria-hidden="true">is control.</span><span class="doctrine-core">is control.</span></strong>',
    ),
    "assets/hero.css": (
        'font-family: "FP Inter";',
        'src: url("fonts/inter-v4.1/InterVariable.woff2") format("woff2");',
        'font-family: "FP Inter", var(--sans);',
        "font-weight: 620;",
        "font-size: clamp(2.95rem, 5.1vw, 5.25rem);",
        "font-weight: 770;",
        "line-height: 0.94;",
        "letter-spacing: -0.025em;",
        "overflow-wrap: anywhere;",
        "text-transform: uppercase;",
        ".doctrine-effect {",
        "color: rgba(var(--motto-echo-rgb), 0.34);",
        ".hero-motto.is-glitching .doctrine-effect {",
        "animation: fp-motto-complementary-glitch 560ms steps(1, end) 1;",
        "@keyframes fp-motto-complementary-glitch",
        "color: rgba(var(--motto-glitch-rgb), 0.40);",
        "@media (prefers-reduced-transparency: reduce)",
        "font-size: clamp(2.25rem, calc(1.7rem + 2.9vw), 2.95rem);",
        "@media (max-width: 360px) and (max-height: 640px)",
        ".hero-grid { gap: 15px; margin-top: 18px; }",
    ),
    "assets/motto-glitch.js": (
        'document.querySelector(".hero-motto")',
        'matchMedia("(prefers-reduced-motion: reduce)")',
        '"pointerenter"',
        '"pointerdown"',
        '"visibilitychange"',
        '40000 + Math.random() * 20000',
        '"fp-motto-complementary-glitch"',
    ),
}

HOMEPAGE_CTA_CONTRACT = {
    "index.html": (
        'href="#fields"',
        '<span>Explore the fields</span>',
        'class="button-icon button-icon-down" aria-hidden="true" focusable="false"',
        '<span>Discuss a project</span>',
        'class="button-icon button-icon-right" aria-hidden="true" focusable="false"',
    ),
    "assets/hero.css": (
        ".hero .button {",
        ".hero .button-icon {",
        "transform 150ms cubic-bezier(0.2, 0.8, 0.2, 1)",
        "@media (hover: hover) and (pointer: fine)",
        ".hero .button-secondary { color: var(--fuchsia-text); border-color: var(--fuchsia); }",
        "transform: translateY(-1px);",
        "box-shadow: -5px 0 12px -3px rgba(10, 232, 247, 0.58), -16px 0 26px -9px rgba(10, 232, 247, 0.28);",
        "box-shadow: 5px 0 12px -3px rgba(245, 5, 77, 0.58), 16px 0 26px -9px rgba(245, 5, 77, 0.28);",
        ".hero .button:hover .button-icon-down,",
        "transform: translateY(2px);",
        ".hero .button:hover .button-icon-right,",
        "transform: translateX(2px);",
        ".hero .button:active {",
        "transform: translateY(1px);",
        "transition-duration: 80ms;",
        ".hero .button-primary:active { border-color: #08d7e5; background: #08d7e5; }",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
    ),
}

HOMEPAGE_FIELDS_CONTRACT = {
    "index.html": (
        '<link rel="stylesheet" href="/assets/hero.css?v=20260718-9">',
        '<link rel="stylesheet" href="/assets/home-v1.css?v=20260718-7">',
        '<div class="field-region" id="fields">',
        'data-field-layer="theory"',
        'data-field-layer="systems"',
        'data-field-layer="work"',
        '<span>A/SYNC / Theory preview</span><strong>In development</strong>',
        '<h3 id="theory-feature-title">A/SYNC / Theoretical foundations</h3>',
        '<div><dt>Related system</dt><dd>FP-SYS-0003</dd></div>',
        '<div><dt>Publication</dt><dd>Not yet published</dd></div>',
        'href="/systems/#async">Open system record</a>',
        'href="/reviews/metro-2033-redux/">Open Metro dossier</a>',
    ),
    "assets/hero.css": (
        "border-bottom: 0;",
    ),
    "assets/home-v1.css": (
        "scroll-behavior: smooth;",
        "scroll-padding-top: 0;",
        ".field-region {",
        "scroll-margin-top: var(--header-height);",
        "[data-field-layer]::before {",
        "width: 22px;",
        "height: 24px;",
        "viewBox='0%200%2022%2024'",
        "d='M1%203L7%2021' stroke='%230ae8f7'",
        "d='M7%200L15%2024' stroke='%23f2f4f5'",
        "d='M15%203L21%2021' stroke='%23f5054d'",
        "drop-shadow(-3px 0 4px rgba(10, 232, 247, 0.18))",
        "drop-shadow(3px 0 4px rgba(245, 5, 77, 0.18));",
        "transform: translateX(-50%);",
        "transform: translateX(-50%) rotate(-22deg);",
        ".field-layer-grid {",
        "grid-template-columns: minmax(260px, 0.72fr) minmax(0, 1.28fr);",
        ".field-feature-list > li + li {",
        "border-top: 1px solid var(--line);",
        "@media (max-width: 1080px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

RETIRED_HOMEPAGE_FIELD_TOKENS = (
    "Discuss A/SYNC",
    "Review index",
    "Explore selected work",
    "Parent field",
    "Curated TopK",
    'id="selected-work"',
    'class="section selected-section"',
    'class="section focus-section"',
    'class="section method-section"',
    "Open Thought Index",
)

BRAND_LOCKUP_REQUIRED_TOKENS = (
    'class="brand-name" aria-hidden="true"',
    'class="brand-word brand-word-final">FINAL</span>',
    'class="brand-divider">\\</span>',
    'class="brand-word brand-word-prime">PRIME</span>',
)

RETIRED_BRAND_LOCKUP = '<span class="brand-name">FINAL <span aria-hidden="true">/</span> PRIME</span>'

HOMEPAGE_IDENTITY_REQUIRED_TOKENS = (
    'class="hero identity-hero"',
    'class="eyebrow-copy">Independent studio · software &amp; ',
    'class="eyebrow-term">technical research</span>',
    'class="hero-wordmark"',
    'aria-label="Final Prime"',
    'class="wordmark-final">FINAL</span>',
    'class="wordmark-divider" aria-hidden="true">\\</span>',
    'class="wordmark-prime">PRIME</span>',
    'Knowing the next move',
    'is survival.',
    'Understanding the game',
    'is control.',
    'Final Prime is an <b>independent, cross-domain</b> research and engineering effort',
    'effort by <b>Daniel Kenessy</b>',
    'It pursues a more <b>unified understanding</b> of complex systems',
    'class="hero-intro hero-method"',
    'Rather than treating <b>visible symptoms</b>',
    'the <b>logic</b> that makes them possible.',
    'It formulates and tests <b>hypotheses</b>.',
    'It develops theory and builds software on foundations designed',
    '<b>no longer arises</b>.',
    'href="#fields"',
    '<span>Explore the fields</span>',
    'href="/contact/">Discuss a project</a>',
    'class="hero-orientation-panel"',
    'class="field-region" id="fields"',
    'data-field-layer="theory"',
    'data-field-layer="systems"',
    'data-field-layer="work"',
)

HOMEPAGE_IDENTITY_FORBIDDEN_TOKENS = (
    'class="prime-matrix',
    'class="root-trace',
    'class="sparse-signal',
    'final prime is founder-led.',
    'our company',
    'our team',
)


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[tuple[str, str, str]] = []
        self.idrefs: list[tuple[str, str]] = []
        self.remote_embeds: list[tuple[str, str]] = []
        self.icon_links: set[tuple[str, str, str, str]] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "link":
            for relation in data.get("rel", "").split():
                if relation in {"icon", "apple-touch-icon"}:
                    self.icon_links.add(
                        (relation, data.get("href", ""), data.get("type", ""), data.get("sizes", ""))
                    )
        if data.get("id"):
            self.ids.append(data["id"])
        for attribute in REFERENCE_ATTRIBUTES:
            value = data.get(attribute)
            if value:
                self.references.append((tag, attribute, value))
                parsed = urlsplit(value)
                if parsed.scheme in {"http", "https"} and parsed.netloc != "final-prime.github.io":
                    if tag in {"img", "script", "iframe", "video", "audio", "source"} or (
                        tag == "link" and "stylesheet" in data.get("rel", "").split()
                    ):
                        self.remote_embeds.append((tag, value))
        for attribute in ARIA_IDREF_ATTRIBUTES:
            for target in data.get(attribute, "").split():
                self.idrefs.append((attribute, target))


def parse_document(path: Path) -> DocumentParser:
    parser = DocumentParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def route_file(path: str) -> Path:
    relative = unquote(path).lstrip("/")
    candidate = ROOT / relative
    if not relative or path.endswith("/"):
        candidate /= "index.html"
    return candidate


def local_target(value: str, source: Path) -> tuple[Path, str] | None:
    parsed = urlsplit(value)
    if parsed.scheme in {"mailto", "tel", "data", "javascript"}:
        return None
    if parsed.scheme in {"http", "https"}:
        if parsed.netloc != "final-prime.github.io":
            return None
        target = route_file(parsed.path)
    elif parsed.scheme or parsed.netloc:
        return None
    elif parsed.path.startswith("/"):
        target = route_file(parsed.path)
    elif parsed.path:
        target = (source.parent / unquote(parsed.path)).resolve()
        if parsed.path.endswith("/"):
            target /= "index.html"
    else:
        target = source
    return target, unquote(parsed.fragment)


def unreferenced_css_classes(css: str, runtime_sources: str) -> list[str]:
    classes = set(CSS_CLASS_SELECTOR.findall(css))
    return sorted(
        class_name
        for class_name in classes
        if not re.search(rf"(?<![\w-]){re.escape(class_name)}(?![\w-])", runtime_sources)
    )


def validate_print_contract(content: str) -> list[str]:
    return [token for token in PRINT_CONTRACT_TOKENS if token not in content]


def validate_reflow_contract(content: str) -> list[str]:
    return [token for token in REFLOW_CONTRACT_TOKENS if token not in content]


def validate_homepage_identity_contract(content: str) -> list[str]:
    errors: list[str] = []
    missing = [token for token in HOMEPAGE_IDENTITY_REQUIRED_TOKENS if token not in content]
    if missing:
        errors.append(
            "index.html is missing identity-homepage contract token(s): "
            + ", ".join(repr(token) for token in missing)
        )

    lowered = content.lower()
    forbidden = [token for token in HOMEPAGE_IDENTITY_FORBIDDEN_TOKENS if token in lowered]
    if forbidden:
        errors.append(
            "index.html contains retired or misleading homepage token(s): "
            + ", ".join(repr(token) for token in forbidden)
        )

    hero_index = content.find('class="hero identity-hero"')
    fields_index = content.find('class="field-region" id="fields"')
    theory_index = content.find('data-field-layer="theory"')
    systems_index = content.find('data-field-layer="systems"')
    work_index = content.find('data-field-layer="work"')
    closing_index = content.find('class="section closing-section"')
    if not (-1 < hero_index < fields_index < theory_index < systems_index < work_index < closing_index):
        errors.append(
            "index.html section order must be identity hero, Theory, Systems, Work, then closing"
        )

    if not re.search(
        r'</section>\s*<div class="field-region" id="fields">\s*<section class="section"[^>]+data-field-layer="theory"',
        content,
    ):
        errors.append("The fields region and Theory must directly follow the identity hero")

    if content.count('data-field-layer=') != 3:
        errors.append("index.html must contain exactly three field layers")
    if content.count('<ol class="field-feature-list"') != 3:
        errors.append("index.html must contain exactly one ordered record list per field layer")
    if content.count('<article class="field-feature') != 3:
        errors.append("index.html v1 must contain exactly one selected article per field layer")

    return errors


def main() -> int:
    errors: list[str] = []
    documents: dict[Path, DocumentParser] = {}
    html_paths = sorted(ROOT.rglob("*.html"))

    for path in html_paths:
        document = parse_document(path)
        documents[path.resolve()] = document
        relative = path.relative_to(ROOT).as_posix()
        html_content = path.read_text(encoding="utf-8")
        duplicates = sorted(key for key, count in Counter(document.ids).items() if count > 1)
        if duplicates:
            errors.append(f"{relative}: duplicate IDs {duplicates}")
        known_ids = set(document.ids)
        for attribute, target in document.idrefs:
            if target not in known_ids:
                errors.append(f"{relative}: {attribute} points to missing #{target}")
        for tag, value in document.remote_embeds:
            errors.append(f"{relative}: remote {tag} dependency is not allowed: {value}")
        if document.icon_links != REQUIRED_ICON_LINKS:
            errors.append(f"{relative}: platform icon links do not match the required contract")
        stylesheet_order = [
            urlsplit(value).path
            for tag, _, value in document.references
            if tag == "link"
        ]
        linked_stylesheets = set(stylesheet_order)
        forbidden_stylesheets = linked_stylesheets.intersection(FORBIDDEN_ROUTE_STYLESHEETS.get(relative, set()))
        if forbidden_stylesheets:
            errors.append(f"{relative}: unused route stylesheets restored {sorted(forbidden_stylesheets)}")
        if "/assets/responsive.css" in linked_stylesheets:
            responsive_index = stylesheet_order.index("/assets/responsive.css")
            late_component_styles = sorted(
                stylesheet
                for stylesheet in linked_stylesheets.intersection(RESPONSIVE_PRECEDENCE_STYLES)
                if stylesheet_order.index(stylesheet) > responsive_index
            )
            if late_component_styles:
                errors.append(
                    f"{relative}: responsive stylesheet must follow component styles "
                    f"{late_component_styles}"
                )
        if relative == "index.html":
            errors.extend(validate_homepage_identity_contract(html_content))
        if 'class="site-header"' in html_content:
            missing_brand_tokens = [
                token for token in BRAND_LOCKUP_REQUIRED_TOKENS if token not in html_content
            ]
            if missing_brand_tokens:
                errors.append(f"{relative}: header brand lockup is missing {missing_brand_tokens}")
            if RETIRED_BRAND_LOCKUP in html_content:
                errors.append(f"{relative}: retired forward-slash brand lockup restored")

    checked_references = 0
    for source, document in documents.items():
        relative = source.relative_to(ROOT).as_posix()
        for tag, attribute, value in document.references:
            resolved = local_target(value, source)
            if resolved is None:
                continue
            checked_references += 1
            target, fragment = resolved
            if not target.exists() or not target.is_file():
                errors.append(f"{relative}: {tag}[{attribute}] missing target {value}")
                continue
            if fragment:
                target_document = documents.get(target.resolve())
                if target_document is None:
                    errors.append(f"{relative}: fragment used on non-HTML target {value}")
                elif fragment not in target_document.ids:
                    errors.append(f"{relative}: missing fragment target {value}")

    checked_css_references = 0
    css_sources: list[str] = []
    for path in sorted((ROOT / "assets").glob("*.css")):
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
        css_sources.append(content)
        if "@import" in content:
            errors.append(f"{relative}: CSS @import is forbidden; use direct stylesheet discovery")
        for match in CSS_REFERENCE.finditer(content):
            value = match.group(1)
            if value.startswith(("#", "data:")):
                continue
            checked_css_references += 1
            parsed = urlsplit(value)
            if parsed.scheme in {"http", "https"} or parsed.netloc:
                errors.append(f"{relative}: remote CSS dependency is not allowed: {value}")
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists() or not target.is_file():
                errors.append(f"{relative}: missing CSS asset {value}")

    runtime_sources = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [*html_paths, *sorted((ROOT / "assets").glob("*.js"))]
    )
    css_content = "\n".join(css_sources)
    unreachable_classes = unreferenced_css_classes(css_content, runtime_sources)
    if unreachable_classes:
        errors.append(f"CSS classes have no HTML or JavaScript runtime source: {unreachable_classes}")
    css_class_count = len(set(CSS_CLASS_SELECTOR.findall(css_content)))
    missing_print_tokens = validate_print_contract(
        (ROOT / "assets" / "surface-polish.css").read_text(encoding="utf-8")
    )
    if missing_print_tokens:
        errors.append(f"print stylesheet contract is missing {missing_print_tokens}")
    missing_reflow_tokens = validate_reflow_contract(
        (ROOT / "assets" / "review-dossier.css").read_text(encoding="utf-8")
    )
    if missing_reflow_tokens:
        errors.append(f"text-spacing reflow contract is missing {missing_reflow_tokens}")
    dossier_polish = (ROOT / "assets" / "review-dossier-polish.css").read_text(encoding="utf-8")
    if DOSSIER_POLISH_REFLOW_TOKEN not in dossier_polish:
        errors.append("dossier polish must preserve narrow-screen axis heading wrapping")
    for relative, tokens in ROUTE_REFLOW_CONTRACTS.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative} route reflow contract is missing {missing}")
    no_js_content = (ROOT / "assets" / "no-js.css").read_text(encoding="utf-8")
    missing_no_js_tokens = [token for token in NO_JS_CONTRACT_TOKENS if token not in no_js_content]
    if missing_no_js_tokens:
        errors.append(f"no-JavaScript fallback contract is missing {missing_no_js_tokens}")
    for relative, tokens in PROGRESSIVE_ENHANCEMENT_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: progressive-enhancement contract is missing {missing}")
    base_content = (ROOT / "assets" / "base.css").read_text(encoding="utf-8")
    missing_navigation_polish = [
        token for token in NAVIGATION_POLISH_CONTRACT if token not in base_content
    ]
    if missing_navigation_polish:
        errors.append(
            "assets/base.css: navigation polish contract is missing "
            f"{missing_navigation_polish}"
        )
    for relative in ("assets/app.js", "assets/base.css", "assets/surface-polish.css"):
        content = (ROOT / relative).read_text(encoding="utf-8")
        retired = [token for token in RETIRED_HEADER_TOKENS if token in content]
        if retired:
            errors.append(f"{relative}: retired header token(s) restored {retired}")
    for relative, tokens in HEADER_LAYOUT_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: header layout contract is missing {missing}")
    for relative, tokens in SCROLL_READOUT_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: scroll readout contract is missing {missing}")
    for relative, tokens in HEADER_GLITCH_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: header glitch contract is missing {missing}")
    for relative, tokens in HERO_WORDMARK_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: hero wordmark contract is missing {missing}")
    for relative, tokens in HOMEPAGE_MOTTO_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: homepage motto contract is missing {missing}")
    for relative, tokens in HOMEPAGE_CTA_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: homepage CTA contract is missing {missing}")
    for relative, tokens in HOMEPAGE_FIELDS_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: homepage fields contract is missing {missing}")
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    retired_fields = [token for token in RETIRED_HOMEPAGE_FIELD_TOKENS if token in homepage]
    if retired_fields:
        errors.append(f"index.html: retired homepage field token(s) restored {retired_fields}")

    checked_scripts = 0
    for relative, budget in SCRIPT_BUDGETS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{relative}: required runtime script is missing")
            continue
        checked_scripts += 1
        # Text mode normalizes CRLF to LF, so the budget measures source bytes
        # consistently on Windows and Unix checkouts.
        content = path.read_text(encoding="utf-8")
        size = len(content.encode("utf-8"))
        if size > budget:
            errors.append(f"{relative}: {size} bytes exceeds the {budget}-byte runtime budget")
        for pattern in FORBIDDEN_SCRIPT_PATTERNS:
            if pattern in content:
                errors.append(f"{relative}: forbidden dynamic script pattern {pattern}")

    for relative, expected in REQUIRED_PNG_DIMENSIONS.items():
        path = ROOT / relative
        try:
            data = path.read_bytes()
            if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
                raise ValueError("invalid PNG signature or IHDR")
            dimensions = struct.unpack(">II", data[16:24])
            if dimensions != expected:
                errors.append(f"{relative}: PNG dimensions {dimensions} do not match {expected}")
        except (OSError, ValueError, struct.error) as error:
            errors.append(f"{relative}: invalid required PNG: {error}")

    manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    manifest_icons = {
        (item.get("src", ""), item.get("sizes", ""), item.get("type", ""), item.get("purpose", ""))
        for item in manifest.get("icons", [])
    }
    if manifest_icons != REQUIRED_MANIFEST_ICONS:
        errors.append("site.webmanifest: icons do not match the required platform contract")
    manifest_urls = [manifest.get("start_url", ""), manifest.get("id", "")]
    manifest_urls.extend(item.get("src", "") for item in manifest.get("icons", []))
    manifest_urls.extend(item.get("url", "") for item in manifest.get("shortcuts", []))
    for value in manifest_urls:
        if not value:
            errors.append("site.webmanifest: empty required URL")
            continue
        resolved = local_target(value, ROOT / "site.webmanifest")
        if resolved is None or not resolved[0].exists():
            errors.append(f"site.webmanifest: missing local target {value}")

    if errors:
        print("Site integrity validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Site integrity OK: "
        f"{len(documents)} HTML documents, {checked_references} local references, "
        f"{checked_css_references} CSS references, {css_class_count} reachable CSS classes, "
        f"print/reflow rendering and {checked_scripts} budgeted scripts, "
        f"and {len(manifest_urls)} manifest targets verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
