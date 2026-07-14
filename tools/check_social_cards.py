#!/usr/bin/env python3
"""Validate crawler-facing Open Graph and X card image contracts."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from struct import unpack
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE_ORIGIN = "https://final-prime.github.io"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_SIZE = (1200, 630)
MAX_IMAGE_BYTES = 5 * 1024 * 1024


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "meta":
            return
        data = dict(attrs)
        key = data.get("property") or data.get("name")
        content = data.get("content")
        if key and content:
            self.values[key] = content


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != PNG_SIGNATURE or header[12:16] != b"IHDR":
        raise ValueError("not a valid PNG header")
    return unpack(">II", header[16:24])


def validate_page(path: Path) -> list[str]:
    parser = MetadataParser()
    parser.feed(path.read_text(encoding="utf-8"))
    meta = parser.values
    errors: list[str] = []
    relative = path.relative_to(ROOT).as_posix()

    if relative == "404.html":
        if "og:image" in meta or "twitter:image" in meta:
            errors.append(f"{relative}: noindex page must not publish a social card")
        return errors

    required = (
        "og:type",
        "og:locale",
        "og:site_name",
        "og:title",
        "og:description",
        "og:url",
        "og:image",
        "og:image:type",
        "og:image:width",
        "og:image:height",
        "og:image:alt",
        "twitter:card",
        "twitter:title",
        "twitter:description",
        "twitter:image",
        "twitter:image:alt",
    )
    for key in required:
        if not meta.get(key, "").strip():
            errors.append(f"{relative}: missing {key}")

    if errors:
        return errors

    if meta["og:image:type"] != "image/png":
        errors.append(f"{relative}: og:image:type must be image/png")
    if meta["og:locale"] != "en_US":
        errors.append(f"{relative}: og:locale must be en_US")
    if meta["og:site_name"] != "Final Prime":
        errors.append(f"{relative}: og:site_name must be Final Prime")
    if (meta["og:image:width"], meta["og:image:height"]) != ("1200", "630"):
        errors.append(f"{relative}: declared social image size must be 1200x630")
    if meta["og:image"] != meta["twitter:image"]:
        errors.append(f"{relative}: Open Graph and X image URLs must match")
    if meta["og:image:alt"] != meta["twitter:image:alt"]:
        errors.append(f"{relative}: Open Graph and X image alt text must match")

    image_url = urlparse(meta["og:image"])
    if f"{image_url.scheme}://{image_url.netloc}" != SITE_ORIGIN:
        errors.append(f"{relative}: social image must use the canonical HTTPS origin")
        return errors
    if not image_url.path.endswith(".png"):
        errors.append(f"{relative}: social image URL must end in .png")
        return errors

    image_path = ROOT / image_url.path.lstrip("/")
    if not image_path.is_file():
        errors.append(f"{relative}: missing social image {image_url.path}")
        return errors
    if image_path.stat().st_size > MAX_IMAGE_BYTES:
        errors.append(f"{relative}: social image exceeds 5 MB")
    try:
        actual_size = png_size(image_path)
    except ValueError as error:
        errors.append(f"{relative}: {image_url.path} is {error}")
    else:
        if actual_size != EXPECTED_SIZE:
            errors.append(f"{relative}: actual social image size is {actual_size}, expected {EXPECTED_SIZE}")

    return errors


def main() -> int:
    html_files = sorted(ROOT.rglob("*.html"))
    errors = [error for path in html_files for error in validate_page(path)]
    if errors:
        print("Social card check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    card_pages = sum(path.name != "404.html" for path in html_files)
    print("Social card check passed.")
    print(f"Public cards checked: {card_pages}")
    print("Raster contract: PNG / 1200x630 / matching Open Graph and X metadata")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
