#!/usr/bin/env python3
"""Validate the complete local navigation and asset graph."""

from __future__ import annotations

from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://final-prime.github.io"
REFERENCE_ATTRIBUTES = ("href", "src", "poster", "action")
ARIA_IDREF_ATTRIBUTES = ("aria-controls", "aria-describedby", "aria-labelledby")
CSS_REFERENCE = re.compile(r"(?:@import\s+url\(|@import\s+|url\()\s*['\"]?([^'\")\s]+)")


class DocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: list[str] = []
        self.references: list[tuple[str, str, str]] = []
        self.idrefs: list[tuple[str, str]] = []
        self.remote_embeds: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
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
    for path in sorted((ROOT / "assets").glob("*.css")):
        relative = path.relative_to(ROOT).as_posix()
        content = path.read_text(encoding="utf-8")
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

    manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
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
        f"{checked_css_references} CSS references, and {len(manifest_urls)} manifest targets verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
