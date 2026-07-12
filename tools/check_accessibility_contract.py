#!/usr/bin/env python3
"""Validate durable HTML semantics and accessibility invariants."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
ARIA_CURRENT_VALUES = {"page", "step", "location", "date", "time", "true", "false"}
NAMEABLE_DIV_ROLES = {"alert", "complementary", "group", "img", "list", "main", "meter", "navigation", "region", "status"}
DYNAMIC_DIV = re.compile(r'const\s+(\w+)\s*=\s*document\.createElement\("div"\);')


class SemanticsParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.stack: list[str] = []
        self.first_body_child: tuple[str, dict[str, str]] | None = None
        self.in_body = False
        self.html_elements: list[dict[str, str]] = []
        self.titles: list[str] = []
        self.title_buffer: list[str] | None = None
        self.mains: list[dict[str, str]] = []
        self.headings: list[tuple[int, str]] = []
        self.heading_level: int | None = None
        self.heading_buffer: list[str] = []
        self.article_heading_counts: list[int] = []
        self.closed_articles: list[int] = []
        self.images: list[dict[str, str]] = []
        self.buttons: list[dict[str, str]] = []
        self.button_buffer: list[str] | None = None
        self.current_items: list[tuple[str, str, str]] = []
        self.invalid_labels: list[str] = []
        self.meters: list[dict[str, str]] = []
        self.positive_tabindex: list[str] = []
        self.nav_names: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key.lower(): value or "" for key, value in attrs}
        if tag == "html":
            self.html_elements.append(data)
        if self.in_body and self.stack and self.stack[-1] == "body" and self.first_body_child is None:
            self.first_body_child = (tag, data)
        if tag == "body":
            self.in_body = True
        if tag == "title":
            self.title_buffer = []
        if tag == "main":
            self.mains.append(data)
        if tag.startswith("h") and len(tag) == 2 and tag[1].isdigit():
            self.heading_level = int(tag[1])
            self.heading_buffer = []
            for index in range(len(self.article_heading_counts)):
                self.article_heading_counts[index] += 1
        if tag == "article":
            self.article_heading_counts.append(0)
        if tag == "img":
            self.images.append(data)
        if tag == "button":
            self.buttons.append(data)
            self.button_buffer = []
        if data.get("aria-current"):
            self.current_items.append((tag, data["aria-current"], data.get("href", "")))
        if data.get("aria-label"):
            if tag in {"p", "span", "strong", "small"}:
                self.invalid_labels.append(tag)
            if tag == "div" and data.get("role") not in NAMEABLE_DIV_ROLES:
                self.invalid_labels.append(f"div[role={data.get('role', '')}]")
        if data.get("role") == "meter":
            self.meters.append(data)
        tabindex = data.get("tabindex")
        if tabindex and tabindex.lstrip("+").isdigit() and int(tabindex) > 0:
            self.positive_tabindex.append(f"{tag}[tabindex={tabindex}]")
        if tag == "nav":
            self.nav_names.append(data.get("aria-label") or data.get("aria-labelledby") or "")
        self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self.title_buffer is not None:
            self.title_buffer.append(data)
        if self.heading_level is not None:
            self.heading_buffer.append(data)
        if self.button_buffer is not None:
            self.button_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_buffer is not None:
            self.titles.append("".join(self.title_buffer).strip())
            self.title_buffer = None
        if self.heading_level is not None and tag == f"h{self.heading_level}":
            self.headings.append((self.heading_level, "".join(self.heading_buffer).strip()))
            self.heading_level = None
            self.heading_buffer = []
        if tag == "button" and self.button_buffer is not None:
            self.buttons[-1]["_text"] = "".join(self.button_buffer).strip()
            self.button_buffer = None
        if tag == "article" and self.article_heading_counts:
            self.closed_articles.append(self.article_heading_counts.pop())
        if tag == "body":
            self.in_body = False
        if tag in self.stack:
            reverse_index = self.stack[::-1].index(tag)
            del self.stack[len(self.stack) - reverse_index - 1 :]


def route_for(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return "/"
    if relative == "404.html":
        return "/404.html"
    return f"/{relative.removesuffix('index.html')}"


def validate_page(path: Path) -> list[str]:
    relative = path.relative_to(ROOT).as_posix()
    route = route_for(path)
    parser = SemanticsParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors: list[str] = []

    if len(parser.html_elements) != 1 or parser.html_elements[0].get("lang") != "en":
        errors.append(f"{relative}: html language must be exactly en")
    if parser.titles == [] or len(parser.titles) != 1 or not parser.titles[0]:
        errors.append(f"{relative}: must have one non-empty title")
    if len(parser.mains) != 1 or parser.mains[0].get("id") != "main-content":
        errors.append(f"{relative}: must have one main#main-content")
    if parser.first_body_child is None:
        errors.append(f"{relative}: body is empty")
    else:
        tag, data = parser.first_body_child
        if tag != "a" or data.get("class") != "skip-link" or data.get("href") != "#main-content":
            errors.append(f"{relative}: first body element must be the main-content skip link")
    h1s = [text for level, text in parser.headings if level == 1]
    if len(h1s) != 1 or not h1s[0]:
        errors.append(f"{relative}: must have one non-empty h1")
    previous_level: int | None = None
    for level, text in parser.headings:
        if not text:
            errors.append(f"{relative}: empty h{level}")
        if previous_level is not None and level > previous_level + 1:
            errors.append(f"{relative}: heading level jumps h{previous_level} to h{level}")
        previous_level = level
    if any(count == 0 for count in parser.closed_articles):
        errors.append(f"{relative}: article without a heading")
    for image in parser.images:
        if "alt" not in image:
            errors.append(f"{relative}: img missing alt")
        if image.get("src", "").endswith("mark.svg") and image.get("alt") != "":
            errors.append(f"{relative}: redundant brand mark must remain decorative")
    for button in parser.buttons:
        if button.get("type") not in {"button", "submit", "reset"}:
            errors.append(f"{relative}: button missing an explicit valid type")
        if not button.get("aria-label") and not button.get("_text"):
            errors.append(f"{relative}: button has no accessible name")
    if parser.invalid_labels:
        errors.append(f"{relative}: aria-label used on non-nameable elements {parser.invalid_labels}")
    if parser.positive_tabindex:
        errors.append(f"{relative}: positive tabindex found {parser.positive_tabindex}")
    if any(not name for name in parser.nav_names):
        errors.append(f"{relative}: every navigation landmark must have a name")
    if len(parser.nav_names) != len(set(parser.nav_names)):
        errors.append(f"{relative}: navigation landmark names must be unique")

    for tag, value, href in parser.current_items:
        if value not in ARIA_CURRENT_VALUES:
            errors.append(f"{relative}: invalid aria-current value {value}")
        target_path = urlsplit(href).path
        if value == "page" and (tag != "a" or target_path != route):
            errors.append(f"{relative}: aria-current=page points to {target_path}, not {route}")
        if value == "location" and target_path == route:
            errors.append(f"{relative}: exact page link must use page, not location")
    for meter in parser.meters:
        try:
            minimum = float(meter["aria-valuemin"])
            maximum = float(meter["aria-valuemax"])
            current = float(meter["aria-valuenow"])
            if not minimum <= current <= maximum:
                raise ValueError
        except (KeyError, ValueError):
            errors.append(f"{relative}: meter has invalid or out-of-range ARIA values")
        if not meter.get("aria-label") and not meter.get("aria-labelledby"):
            errors.append(f"{relative}: meter lacks an accessible name")
    return errors


def validate_dynamic_div_names(content: str, source: str = "assets/home.js") -> list[str]:
    errors: list[str] = []
    for variable in DYNAMIC_DIV.findall(content):
        label_call = f'{variable}.setAttribute("aria-label"'
        role_call = f'{variable}.setAttribute("role"'
        if label_call in content and role_call not in content:
            errors.append(
                f"{source}: dynamic div {variable} has aria-label without an explicit nameable role"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    paths = sorted(ROOT.rglob("*.html"))
    for path in paths:
        errors.extend(validate_page(path))
    home_runtime = (ROOT / "assets" / "home.js").read_text(encoding="utf-8")
    errors.extend(validate_dynamic_div_names(home_runtime))
    if errors:
        print("Accessibility contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Accessibility contract OK: {len(paths)} documents passed semantic and ARIA invariants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
