#!/usr/bin/env python3
"""Validate the complete local navigation and asset graph."""

from __future__ import annotations

from collections import Counter
from html import unescape
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
    "systems/async/index.html": {
        "/assets/content-a.css",
        "/assets/content-b.css",
        "/assets/hero.css",
        "/assets/catalog.css",
        "/assets/reviews.css",
        "/assets/review-release.css",
    },
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
DOSSIER_REFLOW_PATTERN = re.compile(
    r"\.dossier-axis h3\s*\{[^}]*overflow-wrap:\s*normal;[^}]*text-wrap:\s*balance;",
    re.DOTALL,
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
    "assets/contact-index.css": (
        ".contact-index .catalog-hero h1 {",
        ".contact-layout h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
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
        ".legal-index .catalog-hero h1 {",
        ".legal-card h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 900px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
    ),
    "assets/reviews.css": (
        ".review-index-hero h1 {",
        ".review-card-body h2 {",
        ".review-principles h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
    ),
    "assets/realops-dossier.css": (
        ".realops-hero h1 {",
        ".realops-section .section-head h2 {",
        ".role-card h3 {",
        ".method-copy h2 {",
        ".limits-card h3 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1120px)",
        "@media (max-width: 760px)",
        "@media (max-width: 470px)",
        "@media (max-width: 380px)",
    ),
    "assets/async-dossier.css": (
        ".async-hero h1 {",
        ".async-section-head h2 {",
        ".async-overview-grid h3 {",
        ".async-model h3 {",
        "text-wrap: balance;",
        ".async-hero-meta dd {",
        ".async-ledger dd {",
        "overflow-wrap: anywhere;",
    ),
    "assets/works-index.css": (
        ".works-index .release-lane h2 {",
        ".works-index .work-record h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
    ),
    "assets/theory-index.css": (
        ".theory-index .release-lane h2 {",
        ".theory-index .theory-orientation h2 {",
        ".theory-index .theory-policy h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
    ),
    "assets/public-index.css": (
        ".public-index .registry-body h2 {",
        ".public-index .boundary-copy h2 {",
        "overflow-wrap: normal;",
        "text-wrap: balance;",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
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
        '<link rel="stylesheet" href="/assets/hero.css?v=20260719-10">',
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
        "@media (max-width: 900px)",
        ".hero-grid { grid-template-columns: 1fr; gap: 30px; }",
        ".hero-orientation-panel { max-width: 640px; padding-top: 0; }",
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
        ".hero-grid { gap: 21px; margin-top: 22px; }",
        ".hero-actions { margin-top: 16px; }",
        "@media (prefers-reduced-motion: reduce)",
        "@media (forced-colors: active)",
    ),
}

HOMEPAGE_FIELDS_CONTRACT = {
    "index.html": (
        '<link rel="stylesheet" href="/assets/hero.css?v=20260719-10">',
        '<link rel="stylesheet" href="/assets/home-v1.css?v=20260719-28">',
        '<div class="field-region" id="fields">',
        'data-field-layer="theory"',
        'data-field-layer="systems"',
        'data-field-layer="work"',
        '<h2 id="theory-title">Theory <span><span class="field-joiner">&amp;</span><span class="field-secondary">Research</span></span></h2>',
        '<h2 id="systems-layer-title">Systems <span><span class="field-joiner">&amp;</span><span class="field-secondary">Software</span></span></h2>',
        '<h2 id="work-layer-title">Work <span><span class="field-joiner">&amp;</span><span class="field-secondary">Evidence</span></span></h2>',
        '<span class="sr-only">Field 1 of 3</span><span class="field-index-visual" aria-hidden="true"><span class="field-index-protocol">FP://</span><span>Field</span><strong>01</strong><span>/ 03</span></span>',
        '<span class="sr-only">Field 2 of 3</span><span class="field-index-visual" aria-hidden="true"><span class="field-index-protocol">FP://</span><span>Field</span><strong>02</strong><span>/ 03</span></span>',
        '<span class="sr-only">Field 3 of 3</span><span class="field-index-visual" aria-hidden="true"><span class="field-index-protocol">FP://</span><span>Field</span><strong>03</strong><span>/ 03</span></span>',
        '<div><dt>Selected record</dt><dd>A/SYNC / Theoretical Foundations</dd></div>',
        '<div><dt>Selected record</dt><dd>A/SYNC / Software System</dd></div>',
        '<div><dt>Selected record</dt><dd>Metro 2033 Redux / Game Review</dd></div>',
        '<span class="sr-only">Stage 1 of 5: In development</span>',
        '<span class="sr-only">Stage 3 of 5: Prototype</span>',
        '<span class="sr-only">Stage 5 of 5: Published</span>',
        '<span class="field-availability-stage" aria-hidden="true"><strong>I</strong><span>/ V</span></span>',
        '<span class="field-availability-stage" aria-hidden="true"><strong>III</strong><span>/ V</span></span>',
        '<span class="field-availability-stage" aria-hidden="true"><strong>V</strong><span>/ V</span></span>',
        '</dl>\n            <div class="field-parent-intro"><p>Public principles and models for tracing complex failures back to the logic that enables them.</p><a class="button button-secondary" href="/thought/">Explore theory</a></div>',
        '</dl>\n            <div class="field-parent-intro"><p>Software and engineered systems built from those principles, with declared states and limits.</p><a class="button button-secondary" href="/systems/">Explore systems</a></div>',
        '</dl>\n            <div class="field-parent-intro"><p>Published analysis and completed records supported by explicit evidence and boundaries.</p><a class="button button-secondary" href="/works/">Explore work</a></div>',
        '<span class="field-feature-identity"><span class="field-feature-protocol">FP://</span><span>Preview / Theory</span></span><strong><span class="sr-only">Stage 1 of 5: In development</span>',
        '<span class="field-feature-identity"><span class="field-feature-protocol">FP://</span><span>SYS-0003 / System</span></span><strong><span class="sr-only">Stage 3 of 5: Prototype</span>',
        '<span class="field-feature-identity"><span class="field-feature-protocol">FP://</span><span>REV-0001 / Analysis</span></span><strong><span class="sr-only">Stage 5 of 5: Published</span>',
        '<span class="field-feature-stage"><b>I</b><span>/ V</span></span><span class="field-feature-state-separator">&middot;</span><span>In development</span>',
        '<span class="field-feature-stage"><b>III</b><span>/ V</span></span><span class="field-feature-state-separator">&middot;</span><span>Prototype</span>',
        '<span class="field-feature-stage"><b>V</b><span>/ V</span></span><span class="field-feature-state-separator">&middot;</span><span>Published</span>',
        '<h3 id="theory-feature-title"><span class="field-title-primary">A/SYNC <span class="field-title-mark">/</span></span> <span class="field-title-accent">Theoretical</span> <span class="field-title-accent">Foundations</span></h3>',
        '<h3 id="async-title"><span class="field-title-primary">A/SYNC <span class="field-title-mark">/</span></span> <span class="field-title-accent">Software</span> <span class="field-title-accent">System</span></h3>',
        '<h3 id="metro-title"><span class="field-title-primary">Metro 2033</span> <span class="field-title-primary">Redux <span class="field-title-mark">/</span></span> <span class="field-title-accent">Game Review</span></h3>',
        '<span class="field-title-accent">Foundations</span></h3>\n                <dl class="field-record-meta">',
        '<span class="field-title-accent">System</span></h3>\n                <dl class="field-record-meta">',
        '<span class="field-title-accent">Game Review</span></h3>\n                <div class="field-score"',
        '<div class="field-feature-intro"><p>The theory record remains in development. Publication begins when its thesis, evidence path and public boundary are stable.</p></div>',
        '<div class="field-feature-intro"><p>A coordination-system concept organized around objectives, constraints, signals and resolved outcomes. The public record exposes the capability model while implementation and research internals remain private.</p><a class="button button-primary" href="/systems/async/">Open A/SYNC dossier</a></div>',
        '<div class="field-feature-intro"><p>An atmosphere-first survival FPS examined through explicit score math, audience fit, friction, risk and route-level evidence.</p><a class="button button-primary" href="/reviews/metro-2033-redux/">Open Metro dossier</a></div>',
        '<div><dt>Related system</dt><dd>FP-SYS-0003</dd></div>',
        '<div><dt>Publication</dt><dd>Not yet published</dd></div>',
        'href="/thought/">Explore theory</a>',
        'href="/systems/">Explore systems</a>',
        'href="/systems/async/">Open A/SYNC dossier</a>',
        'href="/works/">Explore work</a>',
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
        ".field-region:focus { outline: none; }",
        ".field-region:focus > [data-field-layer]:first-child::before {",
        "outline: 2px solid CanvasText;",
        "[data-field-layer]::before {",
        "width: clamp(240px, 23vw, 340px);",
        "height: 28px;",
        "viewBox='0%200%2064%2028'",
        "d='M4%2012L2%2014L4%2016' stroke='%230ae8f7' stroke-opacity='.18'",
        "d='M29%203L20%2014L29%2025' stroke='%230ae8f7' stroke-opacity='.82'",
        "d='M32%202L35%2014L32%2026L29%2014Z' stroke='%23f2f4f5' stroke-opacity='.96'",
        "d='M35%203L44%2014L35%2025' stroke='%23f5054d' stroke-opacity='.86'",
        "d='M60%2012L62%2014L60%2016' stroke='%23f5054d' stroke-opacity='.20'",
        "center / 64px 28px no-repeat,",
        "linear-gradient(90deg, transparent 0%, rgba(10, 232, 247, 0.06) 14%,",
        "rgba(245, 5, 77, 0.06) 86%, transparent 100%) center / 100% 1px no-repeat;",
        "drop-shadow(-4px 0 4px rgba(10, 232, 247, 0.12))",
        "drop-shadow(4px 0 4px rgba(245, 5, 77, 0.12));",
        "transform: translateX(-50%);",
        "width: 96px;",
        "height: 1px;",
        "background: CanvasText;",
        ".field-layer-grid {",
        "grid-template-columns: minmax(260px, 0.72fr) minmax(0, 1.28fr);",
        ".field-parent h2 .field-joiner,",
        ".field-parent h2 .field-secondary { display: block; }",
        ".field-feature-theory h3 {",
        "font-size: clamp(2.65rem, 4.15vw, 4.5rem);",
        "font-size: 1em;",
        "font: 700 0.75rem/1.3 var(--mono);",
        "letter-spacing: 0.11em;",
        ".field-index > .sr-only,",
        ".field-availability > .sr-only,",
        ".field-feature-topline .sr-only {",
        "clip: rect(0, 0, 0, 0) !important;",
        ".field-index-visual {",
        "gap: 0.58em;",
        ".field-index-protocol {",
        "color: var(--muted-dark);",
        "letter-spacing: 0.04em;",
        ".field-index-visual strong {",
        ".field-index-visual { gap: 0.45em; }",
        "margin: clamp(20px, 1.6vw, 24px) 0 0;",
        ".field-parent h2 { margin-top: 18px; font-size: min(16vw, 4.8rem); }",
        ".field-parent-intro {",
        "grid-template-columns: minmax(0, 1fr) auto;",
        "gap: clamp(18px, 2vw, 26px);",
        "margin: auto 0 0;",
        "padding-top: 42px;",
        ".field-parent-intro p {",
        "max-width: 30ch;",
        ".field-parent-intro .button {",
        "justify-self: end;",
        "white-space: nowrap;",
        ".field-availability {",
        "justify-content: flex-end;",
        ".field-availability-stage {",
        ".field-availability-stage strong {",
        '[data-field-layer="theory"] .field-availability-stage strong { color: var(--cyan); }',
        '[data-field-layer="work"] .field-availability-stage strong { color: var(--fuchsia-text); }',
        "margin: 32px 0 0;",
        "padding-top: 0;",
        "@media (min-width: 1081px) and (max-width: 1240px)",
        ".field-parent-intro .button { justify-self: end; }",
        ".field-parent-intro { grid-template-columns: 1fr; gap: 20px; }",
        ".field-parent-intro .button { justify-self: start; }",
        ".field-feature-list > li + li {",
        "border-top: 1px solid var(--line);",
        ".field-feature-topline {",
        "grid-template-columns: minmax(0, 1fr) auto;",
        "padding-bottom: 12px;",
        "border-bottom: 1px solid var(--line-soft);",
        ".field-feature-protocol { color: var(--muted-dark); letter-spacing: 0.04em; }",
        ".field-feature-stage b { color: var(--cyan); font-weight: 900; }",
        ".field-feature-review .field-feature-stage b { color: var(--fuchsia-text); }",
        ".field-feature-topline { grid-template-columns: 1fr; gap: 7px; }",
        ".field-feature-topline,",
        "font-weight: 790;",
        "line-height: 0.88;",
        "letter-spacing: -0.075em;",
        "overflow-wrap: normal;",
        "text-transform: uppercase;",
        ".field-feature h3 > span { display: block; }",
        ".field-feature h3 .field-title-primary { color: var(--text); }",
        ".field-feature h3 .field-title-accent,",
        ".field-feature h3 .field-title-mark { color: var(--cyan); }",
        ".field-feature-review h3 .field-title-accent,",
        ".field-feature-review h3 .field-title-mark { color: var(--fuchsia-text); }",
        ".field-feature-intro {",
        "grid-template-columns: minmax(0, 1fr) auto;",
        "align-items: end;",
        "margin-top: auto;",
        ".field-feature-intro p {",
        ".field-feature-intro .button {",
        "justify-self: end;",
        ".field-feature-intro { grid-template-columns: 1fr; gap: 24px; }",
        ".field-feature-intro .button { justify-self: start; }",
        "@media (max-width: 1080px)",
        "width: min(240px, calc(100vw - 48px));",
        "background-size: 56px 25px, 100% 1px;",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

ASYNC_DOSSIER_CONTRACT = {
    "systems/index.html": (
        '<body class="systems-index">',
        '<link rel="stylesheet" href="/assets/async-dossier.css?v=20260719-4">',
        'id="async"',
        'III / V &middot; Prototype',
        '<dt>Type</dt><dd>Coordination system</dd>',
        '<dt>Method</dt><dd>Constraint-led</dd>',
        '<dt>Access</dt><dd>Concept surface</dd>',
        '<dt>Entry</dt><dd>Qualified enquiry</dd>',
        'href="/systems/async/">Open A/SYNC dossier →</a>',
        '<p class="catalog-code">Disclosure rail / Explicit</p>',
        '<dt>Public</dt><dd>Identity / lifecycle / model / route</dd>',
        '<dt>Conditional</dt><dd>Business fit / scope / integration context</dd>',
        '<dt>Private</dt><dd>Source / architecture / research / client records</dd>',
    ),
    "systems/async/index.html": (
        '<link rel="canonical" href="https://final-prime.github.io/systems/async/">',
        '<link rel="stylesheet" href="/assets/async-dossier.css?v=20260719-4">',
        '<main class="async-main" id="main-content" tabindex="-1" data-system-id="FP-SYS-0003">',
        '<span>FP:// SYS-0003 / Coordination system</span><strong>III / V &middot; Prototype</strong>',
        '<h1 id="async-page-title"><span>A/SYNC <i>/</i></span><span>Coordination</span><span>System</span></h1>',
        'A prototype coordination-system concept for making objectives, constraints, signals and resolved outcomes explicit.',
        '<dt>Evidence</dt><dd>No public performance claim</dd>',
        '<nav class="async-nav" aria-label="A/SYNC sections"><div class="shell"><a href="#overview">Overview</a><span aria-hidden="true">/</span><a href="#model">Model</a><span aria-hidden="true">/</span><a href="#state">State</a><span aria-hidden="true">/</span><a href="#evidence">Evidence</a><span aria-hidden="true">/</span><a href="#access">Access</a>',
        '<ol class="async-model" aria-label="A/SYNC public model">',
        '<h3>Objective</h3>',
        '<h3>Constraints</h3>',
        '<h3>Signals</h3>',
        '<h3>Resolved outcome</h3>',
        'Public model. Not an implementation diagram.',
        'No public A/SYNC benchmark, deployment record, case study or client outcome is currently claimed.',
        'Separate Final Prime evidence, not A/SYNC validation:',
        '<p class="section-kicker">Qualified discussion / Context first</p>',
        '<h2 id="access-title">Bring the coordination problem, not protected material.</h2>',
        'href="/contact/"><span>Open a project enquiry</span>',
        'href="/systems/">Back to Systems</a>',
        'A/SYNC is a prototype concept. No public release or performance result is claimed.',
    ),
    "assets/async-dossier.css": (
        ".async-hero-grid {",
        ".async-hero-grid > * { min-width: 0; }",
        ".async-nav {",
        "position: sticky;",
        ".async-model {",
        "grid-template-columns: repeat(4, minmax(0, 1fr));",
        ".systems-index .catalog-boundary {",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        ".systems-index .catalog-hero { padding-top: 34px; padding-bottom: 44px; }",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

ASYNC_DOSSIER_CSS_BUDGET = 24000

WORKS_INDEX_CONTRACT = {
    "works/index.html": (
        '<body class="works-index">',
        '<link rel="stylesheet" href="/assets/works-index.css?v=20260719-1">',
        'class="release-lane"',
        'class="release-lane surface-current"',
        'class="catalog-empty surface-current work-record record-realops"',
        'class="catalog-empty surface-current work-record record-metro"',
        'href="/works/realops-01/">Open REALOPS-01</a>',
        'href="/reviews/metro-2033-redux/">Open Metro dossier</a>',
    ),
    "assets/works-index.css": (
        ".works-index .catalog-meta {",
        ".works-index .catalog-grid {",
        ".works-index .release-lane {",
        "grid-template-columns: minmax(150px, 0.55fr) minmax(0, 1.45fr) minmax(210px, 0.72fr);",
        ".works-index .release-protocol {",
        ".works-index .protocol-step {",
        ".works-index .work-record {",
        ".works-index .record-metro .registry-cell.state dd { color: var(--works-amber); }",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

WORKS_INDEX_CSS_BUDGET = 18000

THEORY_INDEX_CONTRACT = {
    "thought/index.html": (
        '<body class="theory-index">',
        '<link rel="stylesheet" href="/assets/theory-index.css?v=20260719-1">',
        '<h2 id="thought-lanes-title">Three declared lanes. No published record.</h2>',
        'class="catalog-empty theory-orientation"',
        'class="catalog-empty theory-policy"',
        'href="/reviews/">Open Game Reviews</a>',
        'href="/works/">Open Works Index</a>',
    ),
    "assets/theory-index.css": (
        ".theory-index .catalog-meta {",
        ".theory-index .catalog-grid {",
        "grid-template-columns: repeat(3, minmax(0, 1fr));",
        ".theory-index .release-lane {",
        ".theory-index .theory-orientation {",
        ".theory-index .release-protocol {",
        ".theory-index .protocol-step {",
        ".theory-index .theory-policy {",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

THEORY_INDEX_CSS_BUDGET = 18000

PUBLIC_INDEX_CONTRACT = {
    "index/index.html": (
        '<body class="public-index">',
        '<link rel="stylesheet" href="/assets/public-index.css?v=20260719-1">',
        '<article class="registry-card surface-current record-realops">',
        '<article class="registry-card surface-current record-metro">',
        '<h2 id="boundary-title">The public index is not the private inventory.</h2>',
        '<dt>Public</dt><dd>Identity / state / route / declared boundary</dd>',
        '<dt>Private</dt><dd>Source / implementation / research / client records</dd>',
    ),
    "assets/public-index.css": (
        ".public-index .catalog-meta {",
        ".public-index .registry-list {",
        ".public-index .registry-card {",
        "grid-template-columns: minmax(138px, 0.42fr) minmax(0, 1.58fr);",
        ".public-index .registry-data {",
        ".public-index .record-metro .registry-cell.state dd { color: var(--index-amber); }",
        ".public-index .catalog-boundary {",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

PUBLIC_INDEX_CSS_BUDGET = 16000

CONTACT_INDEX_CONTRACT = {
    "contact/index.html": (
        '<body class="contact-index">',
        '<link rel="stylesheet" href="/assets/contact-index.css?v=20260719-1">',
        'href="mailto:finalprime.official@gmail.com?subject=Final%20Prime%20enquiry">Start by email</a>',
        'Do not send credentials, client data, private source, unpublished research or other protected material in the first message.',
        'No form. No analytics. No required phone call.',
    ),
    "assets/contact-index.css": (
        ".contact-index .catalog-meta {",
        ".access-layout {",
        "grid-template-columns: minmax(0, 1.22fr) minmax(330px, 0.78fr);",
        ".access-benefits span + span::before {",
        ".private-boundary-card dl {",
        ".contact-section::before {",
        ".contact-routing {",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

CONTACT_INDEX_CSS_BUDGET = 16000

LEGAL_INDEX_CONTRACT = {
    "legal/index.html": (
        '<body class="legal-index">',
        '<link rel="stylesheet" href="/assets/legal.css?v=20260719-1">',
        '<div><dt>Last updated</dt><dd>2026-07-19</dd></div>',
        'Until that transfer is executed, Final Prime remains an initiative and brand, not the legal owner named in these notices.',
    ),
    "assets/legal.css": (
        ".legal-index .catalog-meta {",
        ".legal-grid {",
        "grid-template-columns: 1fr;",
        ".legal-card {",
        "grid-template-columns: minmax(160px, 0.42fr) minmax(0, 1.58fr);",
        ".legal-mark-list {",
        "grid-template-columns: repeat(4, minmax(0, 1fr));",
        ".legal-index .catalog-boundary {",
        ".legal-index .boundary-list {",
        "@media (max-width: 1080px)",
        "@media (max-width: 900px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

LEGAL_INDEX_CSS_BUDGET = 16000

REVIEWS_INDEX_CONTRACT = {
    "reviews/index.html": (
        '<body class="reviews-index">',
        '<link rel="stylesheet" href="/assets/reviews.css?v=20260719-1">',
        '<span>FP-REV-0001 / Metro 2033 Redux</span>',
        '<dt>Evidence</dt><dd>9 arcs / 8 audit checks</dd>',
        '<small>12 Jul 2026</small>',
        'href="/reviews/metro-2033-redux/">Open full dossier</a>',
    ),
    "assets/reviews.css": (
        ".review-index-meta {",
        ".review-index-grid {",
        "grid-template-columns: minmax(0, 1.32fr) minmax(300px, 0.68fr);",
        ".review-card,",
        ".review-score-receipt {",
        ".review-pipeline {",
        ".review-principles {",
        "@media (max-width: 1080px)",
        "@media (max-width: 760px)",
        "@media (max-width: 420px)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

REVIEWS_INDEX_CSS_BUDGET = 16000

REALOPS_POLISH_CONTRACT = {
    "works/realops-01/index.html": (
        '<link rel="stylesheet" href="/assets/realops-dossier.css?v=20260719-3">',
        'class="realops-scope"',
        'class="roster-grid"',
        'class="routing-rail"',
    ),
    "assets/realops-dossier.css": (
        ".realops-hero::after {",
        ".realops-scope {",
        "grid-template-columns: repeat(2, minmax(0, 1fr));",
        ".role-card article {",
        "background: transparent;",
        ".role-stats > div::before {",
        ".routing-rail > div::before {",
        ".method-steps::before {",
        ".limits-card::before {",
        ".ablation-grid article::before {",
        "@media (max-width: 1120px)",
        "@media (max-width: 760px)",
        "@media (max-width: 470px)",
        "@media (max-width: 380px)",
        "@media (forced-colors: active)",
        "@media print",
    ),
}

REALOPS_DOSSIER_CSS_BUDGET = 26000

RETIRED_HOMEPAGE_FIELD_TOKENS = (
    'class="field-index">01 / Field</p>',
    'class="field-index">02 / Field</p>',
    'class="field-index">03 / Field</p>',
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
    'class="field-parent-actions"',
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

HOMEPAGE_CLOSING_CONTRACT = {
    "index.html": (
        '<link rel="stylesheet" href="/assets/home-v1.css?v=20260719-28">',
        '<p class="section-kicker">Selected projects / Direct line</p>',
        '<h2 id="closing-title">Bring the problem. Fit comes before commitment.</h2>',
        'Each enquiry is reviewed for fit before any commitment. Begin with the objective, current constraint and available evidence. Keep protected material out of the first message.',
        '<a class="button button-primary closing-primary" href="/contact/">',
        '<span>Open a project enquiry</span>',
        '<a class="closing-secondary" href="/index/">',
        '<span>Inspect public index</span>',
    ),
    "assets/home-v1.css": (
        ".closing-section {",
        ".closing-section::before {",
        ".closing-route {",
        "grid-template-columns: minmax(0, 1fr) minmax(260px, 340px);",
        ".closing-actions .closing-primary {",
        "17px 0 28px -10px rgba(245, 5, 77, 0.24)",
        ".closing-secondary {",
        "transform: translateX(2px);",
        "@media (prefers-reduced-motion: reduce)",
        "@media (prefers-reduced-transparency: reduce)",
        "@media (forced-colors: active)",
    ),
}

THEORY_LABEL_PAGES = (
    "index.html",
    "systems/index.html",
    "systems/async/index.html",
    "works/index.html",
    "works/realops-01/index.html",
    "thought/index.html",
    "reviews/index.html",
    "reviews/metro-2033-redux/index.html",
    "index/index.html",
    "contact/index.html",
    "legal/index.html",
)

THEORY_TAXONOMY_CONTRACT = {
    "thought/index.html": (
        "The Final Prime Theory Index",
        "Final Prime Theory Index",
        "<title>Theory Index | Final Prime</title>",
        '<span aria-current="page">Theory</span>',
        '<p class="section-kicker">Theory / Public interpretation index</p>',
        '<h1 id="thought-title">Theory <span>Index</span></h1>',
        "A theory record appears only when its thesis, evidence path and publication boundary are stable.",
        "Theory publication protocol",
    ),
    "index/index.html": (
        "systems, works, theory, reviews",
        "<h2>Theory Index</h2>",
        "No theory object is currently published.",
        'href="/thought/">Open Theory Index</a>',
    ),
    "site.webmanifest": (
        '"name": "Theory Index", "short_name": "Theory", "url": "/thought/"',
    ),
}

FOOTER_PAGES = (
    "index.html",
    "systems/index.html",
    "systems/async/index.html",
    "works/index.html",
    "works/realops-01/index.html",
    "thought/index.html",
    "reviews/index.html",
    "reviews/metro-2033-redux/index.html",
    "index/index.html",
    "contact/index.html",
    "legal/index.html",
)

FOOTER_REQUIRED_TOKENS = (
    '<link rel="stylesheet" href="/assets/surface-polish.css?v=20260719-6">',
    '<div class="shell footer-shell">',
    '<div class="footer-primary">',
    'Independent software, research and public evidence with explicit claims, states and limits.',
    '<nav class="footer-nav" aria-label="Footer navigation">',
    '<p class="footer-nav-label" id="footer-explore-label">Explore</p>',
    '<p class="footer-nav-label" id="footer-records-label">Records</p>',
    '<p class="footer-nav-label" id="footer-direct-label">Direct</p>',
    '<p class="footer-trust"><span>No analytics</span><span>No cookies</span><span>No behavioral tracking</span></p>',
    '<p class="footer-email"><a href="mailto:finalprime.official@gmail.com">finalprime.official@gmail.com</a></p>',
    'Final Prime™',
    'All rights reserved.',
)

FOOTER_FORBIDDEN_TOKENS = ('class="shell footer-grid"', 'class="footer-meta"')

FOOTER_STYLE_CONTRACT = (
    ".footer-primary {",
    "grid-template-columns: minmax(250px, 1.35fr) minmax(0, 2.65fr);",
    ".footer-nav {",
    "grid-template-columns: repeat(3, minmax(0, 1fr));",
    ".footer-nav-group {",
    ".footer-nav a[aria-current]::after {",
    ".footer-rail {",
    ".footer-trust {",
    ".footer-email a {",
    ".footer-legal {",
    'grid-template-areas: "explore records" "explore direct";',
    "@media (max-width: 360px)",
    "@media (prefers-reduced-transparency: reduce)",
    "@media (forced-colors: active)",
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

    field_sections = re.findall(
        r'<section\b(?=[^>]*\bdata-field-layer="([^"]+)")[^>]*>(.*?)</section>',
        content,
        flags=re.DOTALL,
    )
    if len(field_sections) != 3:
        errors.append("index.html must expose three parseable field sections for record sync")
    for layer, section in field_sections:
        selected_match = re.search(
            r'<dt>\s*Selected record\s*</dt>\s*<dd[^>]*>(.*?)</dd>',
            section,
            flags=re.DOTALL,
        )
        feature_match = re.search(
            r'<ol class="field-feature-list"[^>]*>.*?<h3[^>]*>(.*?)</h3>',
            section,
            flags=re.DOTALL,
        )
        if not selected_match or not feature_match:
            errors.append(f"{layer}: selected-record sync contract is incomplete")
            continue
        visible_selected = " ".join(
            unescape(re.sub(r"<[^>]+>", "", selected_match.group(1))).split()
        )
        visible_feature = " ".join(
            unescape(re.sub(r"<[^>]+>", "", feature_match.group(1))).split()
        )
        if visible_selected != visible_feature:
            errors.append(
                f"{layer}: Selected record must match the displayed feature title "
                f"({visible_selected!r} != {visible_feature!r})"
            )

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
    dossier_css = (ROOT / "assets" / "review-dossier.css").read_text(encoding="utf-8")
    if not DOSSIER_REFLOW_PATTERN.search(dossier_css):
        errors.append("consolidated dossier CSS must preserve safe balanced axis heading wrapping")
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
    for relative, tokens in HOMEPAGE_CLOSING_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: homepage closing contract is missing {missing}")
    for relative, tokens in HOMEPAGE_FIELDS_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: homepage fields contract is missing {missing}")
    for relative, tokens in ASYNC_DOSSIER_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: A/SYNC dossier contract is missing {missing}")
    async_css_size = len(
        (ROOT / "assets/async-dossier.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if async_css_size > ASYNC_DOSSIER_CSS_BUDGET:
        errors.append(
            "assets/async-dossier.css: "
            f"{async_css_size} bytes exceeds the {ASYNC_DOSSIER_CSS_BUDGET}-byte budget"
        )
    async_page = (ROOT / "systems/async/index.html").read_text(encoding="utf-8")
    if re.search(r"\b\d+(?:\.\d+)?%", async_page):
        errors.append("systems/async/index.html: unverified percentage claim is forbidden")
    for relative, tokens in WORKS_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Works Index contract is missing {missing}")
    works_css_size = len(
        (ROOT / "assets/works-index.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if works_css_size > WORKS_INDEX_CSS_BUDGET:
        errors.append(
            "assets/works-index.css: "
            f"{works_css_size} bytes exceeds the {WORKS_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in THEORY_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Theory Index contract is missing {missing}")
    theory_page = (ROOT / "thought/index.html").read_text(encoding="utf-8")
    theory_lane_count = theory_page.count('class="release-lane"')
    if theory_lane_count != 3:
        errors.append(
            "thought/index.html: expected exactly 3 declared Theory lanes, "
            f"found {theory_lane_count}"
        )
    theory_css_size = len(
        (ROOT / "assets/theory-index.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if theory_css_size > THEORY_INDEX_CSS_BUDGET:
        errors.append(
            "assets/theory-index.css: "
            f"{theory_css_size} bytes exceeds the {THEORY_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in PUBLIC_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Public Index contract is missing {missing}")
    public_index_page = (ROOT / "index/index.html").read_text(encoding="utf-8")
    public_record_count = public_index_page.count('class="registry-card')
    if public_record_count != 9:
        errors.append(
            "index/index.html: expected exactly 9 disclosed registry records, "
            f"found {public_record_count}"
        )
    public_index_css_size = len(
        (ROOT / "assets/public-index.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if public_index_css_size > PUBLIC_INDEX_CSS_BUDGET:
        errors.append(
            "assets/public-index.css: "
            f"{public_index_css_size} bytes exceeds the {PUBLIC_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in CONTACT_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Contact Index contract is missing {missing}")
    contact_page = (ROOT / "contact/index.html").read_text(encoding="utf-8")
    if "<form" in contact_page.lower():
        errors.append("contact/index.html: forms are forbidden on the direct email surface")
    contact_css_size = len(
        (ROOT / "assets/contact-index.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if contact_css_size > CONTACT_INDEX_CSS_BUDGET:
        errors.append(
            "assets/contact-index.css: "
            f"{contact_css_size} bytes exceeds the {CONTACT_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in LEGAL_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Legal Index contract is missing {missing}")
    legal_page = (ROOT / "legal/index.html").read_text(encoding="utf-8")
    legal_card_count = legal_page.count('class="legal-card"')
    if legal_card_count != 6:
        errors.append(
            "legal/index.html: expected exactly 6 rights ledger chapters, "
            f"found {legal_card_count}"
        )
    legal_css_size = len(
        (ROOT / "assets/legal.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if legal_css_size > LEGAL_INDEX_CSS_BUDGET:
        errors.append(
            "assets/legal.css: "
            f"{legal_css_size} bytes exceeds the {LEGAL_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in REVIEWS_INDEX_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Reviews Index contract is missing {missing}")
    reviews_index_page = (ROOT / "reviews/index.html").read_text(encoding="utf-8")
    if reviews_index_page.count('class="review-card"') != 1:
        errors.append("reviews/index.html: expected exactly one published review record")
    if "review-archive" in reviews_index_page:
        errors.append("reviews/index.html: duplicate single-record archive restored")
    if (ROOT / "assets/review-release.css").exists():
        errors.append("assets/review-release.css: retired split stylesheet restored")
    reviews_css_size = len(
        (ROOT / "assets/reviews.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if reviews_css_size > REVIEWS_INDEX_CSS_BUDGET:
        errors.append(
            "assets/reviews.css: "
            f"{reviews_css_size} bytes exceeds the {REVIEWS_INDEX_CSS_BUDGET}-byte budget"
        )
    for relative, tokens in REALOPS_POLISH_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: REALOPS polish contract is missing {missing}")
    realops_css_size = len(
        (ROOT / "assets/realops-dossier.css").read_text(encoding="utf-8").encode("utf-8")
    )
    if realops_css_size > REALOPS_DOSSIER_CSS_BUDGET:
        errors.append(
            "assets/realops-dossier.css: "
            f"{realops_css_size} bytes exceeds the {REALOPS_DOSSIER_CSS_BUDGET}-byte budget"
        )
    theory_link_pattern = re.compile(r'href="/thought/"[^>]*>Theory</a>')
    for relative in THEORY_LABEL_PAGES:
        content = (ROOT / relative).read_text(encoding="utf-8")
        theory_labels = theory_link_pattern.findall(content)
        if len(theory_labels) != 2:
            errors.append(
                f"{relative}: expected Theory in both primary and footer navigation, "
                f"found {len(theory_labels)}"
            )
        if ">Thought</a>" in content:
            errors.append(f"{relative}: retired Thought navigation label restored")
    for relative, tokens in THEORY_TAXONOMY_CONTRACT.items():
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in tokens if token not in content]
        if missing:
            errors.append(f"{relative}: Theory taxonomy contract is missing {missing}")
    for relative in FOOTER_PAGES:
        content = (ROOT / relative).read_text(encoding="utf-8")
        missing = [token for token in FOOTER_REQUIRED_TOKENS if token not in content]
        restored = [token for token in FOOTER_FORBIDDEN_TOKENS if token in content]
        if missing:
            errors.append(f"{relative}: global footer contract is missing {missing}")
        if restored:
            errors.append(f"{relative}: retired footer token(s) restored {restored}")
        if content.count('class="footer-nav-group"') != 3:
            errors.append(f"{relative}: footer must contain exactly three navigation groups")
    footer_styles = (ROOT / "assets/surface-polish.css").read_text(encoding="utf-8")
    missing_footer_styles = [token for token in FOOTER_STYLE_CONTRACT if token not in footer_styles]
    if missing_footer_styles:
        errors.append(f"assets/surface-polish.css: global footer style contract is missing {missing_footer_styles}")
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
