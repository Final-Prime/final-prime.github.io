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
    "assets/app.js": 6500,
    "assets/home.js": 11500,
    "assets/review-dossier.js": 7500,
}
FORBIDDEN_SCRIPT_PATTERNS = ("document.write(", "eval(", "new Function(")
FORBIDDEN_ROUTE_STYLESHEETS = {
    "index.html": {"/assets/catalog.css", "/assets/review-release.css"},
    "404.html": {"/assets/content-a.css", "/assets/hero.css"},
    "systems/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "works/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "thought/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css", "/assets/reviews.css", "/assets/review-release.css"},
    "reviews/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "reviews/metro-2033-redux/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css", "/assets/reviews.css", "/assets/catalog.css", "/assets/review-release.css"},
    "index/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
    "legal/index.html": {"/assets/content-a.css", "/assets/content-b.css", "/assets/hero.css"},
}
REQUIRED_ICON_LINKS = {
    ("icon", "/assets/favicon.svg", "image/svg+xml", ""),
    ("icon", "/assets/icon-192.png", "image/png", "192x192"),
    ("apple-touch-icon", "/apple-touch-icon.png", "", "180x180"),
}
REQUIRED_MANIFEST_ICONS = {
    ("/assets/favicon.svg", "any", "image/svg+xml", "any"),
    ("/assets/icon-192.png", "192x192", "image/png", "any maskable"),
    ("/assets/icon-512.png", "512x512", "image/png", "any maskable"),
}
REQUIRED_PNG_DIMENSIONS = {
    "apple-touch-icon.png": (180, 180),
    "assets/icon-192.png": (192, 192),
    "assets/icon-512.png": (512, 512),
}
PRINT_CONTRACT_TOKENS = (
    "@media print",
    "--bg: #fff;",
    ".skip-link,",
    ".menu-toggle,",
    ".site-progress,",
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
        ".status-layout h2, .contact-layout h2 {",
        "overflow-wrap: anywhere;",
    ),
    "assets/hardening.css": (
        ".feature-layout > *,",
        ".object-stage.is-enhanced > * { min-width: 0; max-width: 100%; }",
        "grid-template-columns: minmax(72px, auto) minmax(0, 1fr);",
    ),
    "assets/hero.css": (
        ".hero-wordmark {",
        "flex-wrap: wrap;",
    ),
    "assets/legal.css": (
        ".legal-card h2 {",
        "overflow-wrap: anywhere;",
    ),
}
NO_JS_CONTRACT_TOKENS = (
    "html [data-demo-track]",
    "html .review-dossier-page .evidence-toolbar-actions",
    "html .menu-toggle { display: none; }",
    "html .site-nav {",
)
PROGRESSIVE_ENHANCEMENT_CONTRACT = {
    "index.html": ("data-demo-track hidden",),
    "assets/home.js": ("demoTrack.hidden = false",),
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


def main() -> int:
    errors: list[str] = []
    documents: dict[Path, DocumentParser] = {}
    html_paths = sorted(ROOT.rglob("*.html"))

    for path in html_paths:
        document = parse_document(path)
        documents[path.resolve()] = document
        relative = path.relative_to(ROOT).as_posix()
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
        linked_stylesheets = {value for tag, _, value in document.references if tag == "link"}
        forbidden_stylesheets = linked_stylesheets.intersection(FORBIDDEN_ROUTE_STYLESHEETS.get(relative, set()))
        if forbidden_stylesheets:
            errors.append(f"{relative}: unused route stylesheets restored {sorted(forbidden_stylesheets)}")

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

    checked_scripts = 0
    for relative, budget in SCRIPT_BUDGETS.items():
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"{relative}: required runtime script is missing")
            continue
        checked_scripts += 1
        size = path.stat().st_size
        if size > budget:
            errors.append(f"{relative}: {size} bytes exceeds the {budget}-byte runtime budget")
        content = path.read_text(encoding="utf-8")
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
