#!/usr/bin/env python3
"""Validate canonical, sitemap, robots, and review search contracts."""

from __future__ import annotations

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://final-prime.github.io"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\((https://final-prime\.github\.io/[^)]*)\)")
LLMS_RIGHTS_NOTICE = (
    "This file is a navigation aid, not a grant of access, reuse, training, or other rights."
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.canonicals: list[str] = []
        self.og_urls: list[str] = []
        self.robots: list[str] = []
        self.descriptions: list[str] = []
        self.itemtypes: list[str] = []
        self.itemprops: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        if tag == "link" and "canonical" in data.get("rel", "").split():
            self.canonicals.append(data.get("href", ""))
        if tag == "meta":
            if data.get("property") == "og:url":
                self.og_urls.append(data.get("content", ""))
            if data.get("name", "").lower() == "robots":
                self.robots.append(data.get("content", ""))
            if data.get("name", "").lower() == "description":
                self.descriptions.append(data.get("content", ""))
        if data.get("itemtype"):
            self.itemtypes.append(data["itemtype"])
        if data.get("itemprop"):
            self.itemprops.append(data)


def expected_url(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return f"{ORIGIN}/"
    return f"{ORIGIN}/{relative.removesuffix('index.html')}"


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def main() -> int:
    errors: list[str] = []
    canonical_urls: set[str] = set()
    descriptions: set[str] = set()

    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT).as_posix()
        page = parse_page(path)
        if relative == "404.html":
            robots = ",".join(page.robots).lower()
            if "noindex" not in robots:
                errors.append("404.html: must declare noindex")
            if page.canonicals:
                errors.append("404.html: must not declare a canonical URL")
            continue

        wanted = expected_url(path)
        if page.canonicals != [wanted]:
            errors.append(f"{relative}: canonical must be exactly {wanted}")
        if page.og_urls != [wanted]:
            errors.append(f"{relative}: og:url must be exactly {wanted}")
        if len(page.descriptions) != 1:
            errors.append(f"{relative}: must expose exactly one meta description")
        else:
            description = page.descriptions[0]
            if not 70 <= len(description) <= 160:
                errors.append(
                    f"{relative}: meta description length {len(description)} is outside 70-160 characters"
                )
            if description in descriptions:
                errors.append(f"{relative}: duplicate meta description")
            descriptions.add(description)
        if any("noindex" in value.lower() for value in page.robots):
            errors.append(f"{relative}: indexable route declares noindex")
        parsed = urlparse(wanted)
        if parsed.scheme != "https" or parsed.netloc != "final-prime.github.io":
            errors.append(f"{relative}: canonical must be absolute and same-origin")
        if wanted in canonical_urls:
            errors.append(f"{relative}: duplicate canonical {wanted}")
        canonical_urls.add(wanted)

    sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
    sitemap_urls: list[str] = []
    for entry in sitemap.findall("sm:url", NS):
        loc = entry.findtext("sm:loc", default="", namespaces=NS).strip()
        sitemap_urls.append(loc)
        lastmod = entry.findtext("sm:lastmod", default="", namespaces=NS).strip()
        try:
            date.fromisoformat(lastmod)
        except ValueError:
            errors.append(f"sitemap.xml: invalid lastmod for {loc}")
        if entry.find("sm:priority", NS) is not None or entry.find("sm:changefreq", NS) is not None:
            errors.append(f"sitemap.xml: ignored priority/changefreq field remains for {loc}")
    if len(sitemap_urls) != len(set(sitemap_urls)):
        errors.append("sitemap.xml: duplicate loc entries")
    if set(sitemap_urls) != canonical_urls:
        errors.append("sitemap.xml: loc set does not exactly match indexable canonicals")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if f"Sitemap: {ORIGIN}/sitemap.xml" not in robots.splitlines():
        errors.append("robots.txt: missing exact absolute Sitemap directive")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    if not llms.startswith("# Final Prime\n\n> "):
        errors.append("llms.txt: must start with the exact H1 and a blockquote summary")
    if LLMS_RIGHTS_NOTICE not in llms:
        errors.append("llms.txt: missing explicit non-permission rights notice")
    llms_urls = MARKDOWN_LINK.findall(llms)
    if len(llms_urls) != len(set(llms_urls)):
        errors.append("llms.txt: duplicate public route links")
    if set(llms_urls) != canonical_urls:
        errors.append("llms.txt: route set does not exactly match indexable canonicals")

    review = parse_page(ROOT / "reviews" / "metro-2033-redux" / "index.html")
    required_types = {
        "https://schema.org/Review",
        "https://schema.org/Game",
        "https://schema.org/Person",
        "https://schema.org/Organization",
        "https://schema.org/Rating",
    }
    missing_types = required_types.difference(review.itemtypes)
    if missing_types:
        errors.append(f"review: missing schema types {sorted(missing_types)}")
    required_properties = {"itemReviewed", "name", "author", "publisher", "reviewRating", "ratingValue", "bestRating", "worstRating", "datePublished"}
    present_properties = {item["itemprop"] for item in review.itemprops}
    missing_properties = required_properties.difference(present_properties)
    if missing_properties:
        errors.append(f"review: missing schema properties {sorted(missing_properties)}")
    expected_values = {"ratingValue": "86", "bestRating": "100", "worstRating": "0", "datePublished": "2026-07-12"}
    for prop, value in expected_values.items():
        if not any(
            item.get("itemprop") == prop and (item.get("content") == value or item.get("datetime") == value)
            for item in review.itemprops
        ):
            errors.append(f"review: {prop} must expose value {value}")

    if errors:
        print("Search contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Search contract OK: {len(canonical_urls)} canonical routes, sitemap, agent map, "
        "and review schema verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
