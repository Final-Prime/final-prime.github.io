#!/usr/bin/env python3
"""Validate enforceable meta-CSP and RFC 9116 security contact contracts."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://final-prime.github.io"
COMMON_CSP = {
    "default-src": ("'self'",),
    "style-src": ("'self'",),
    "img-src": ("'self'", "data:"),
    "font-src": ("'none'",),
    "media-src": ("'none'",),
    "connect-src": ("'none'",),
    "worker-src": ("'none'",),
    "child-src": ("'none'",),
    "object-src": ("'none'",),
    "frame-src": ("'none'",),
    "form-action": ("'none'",),
    "base-uri": ("'self'",),
}
UNSUPPORTED_META_DIRECTIVES = {"frame-ancestors", "report-uri", "report-to", "sandbox"}


class SecurityParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.position = 0
        self.csp: list[tuple[int, str]] = []
        self.referrers: list[str] = []
        self.fetches: list[tuple[int, str]] = []
        self.inline_scripts = 0
        self.inline_styles = 0
        self.event_handlers: list[str] = []
        self.unsafe_blank_links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.position += 1
        data = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta" and data.get("http-equiv", "").lower() == "content-security-policy":
            self.csp.append((self.position, data.get("content", "")))
        if tag == "meta" and data.get("name", "").lower() == "referrer":
            self.referrers.append(data.get("content", ""))
        if tag in {"link", "script", "img", "iframe", "video", "audio", "source", "object", "embed"}:
            self.fetches.append((self.position, tag))
        if tag == "script" and not data.get("src"):
            self.inline_scripts += 1
        if tag == "style":
            self.inline_styles += 1
        self.event_handlers.extend(key for key in data if key.startswith("on"))
        if tag == "a" and data.get("target", "").lower() == "_blank":
            rel = set(data.get("rel", "").lower().split())
            href = data.get("href", "")
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.unsafe_blank_links.append(href)


def parse_csp(value: str) -> tuple[dict[str, tuple[str, ...]], list[str]]:
    directives: dict[str, tuple[str, ...]] = {}
    errors: list[str] = []
    for raw in value.split(";"):
        tokens = raw.strip().split()
        if not tokens:
            continue
        name = tokens[0].lower()
        if name in directives:
            errors.append(f"duplicate CSP directive {name}")
        directives[name] = tuple(tokens[1:])
    return directives, errors


def validate_html(path: Path) -> list[str]:
    relative = path.relative_to(ROOT).as_posix()
    parser = SecurityParser()
    parser.feed(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if len(parser.csp) != 1:
        errors.append(f"{relative}: must contain exactly one CSP meta")
        return errors
    csp_position, csp_value = parser.csp[0]
    earlier_fetches = [tag for position, tag in parser.fetches if position < csp_position]
    if earlier_fetches:
        errors.append(f"{relative}: fetch-capable elements precede CSP: {earlier_fetches}")
    directives, csp_errors = parse_csp(csp_value)
    errors.extend(f"{relative}: {error}" for error in csp_errors)
    expected = dict(COMMON_CSP)
    if relative == "404.html":
        expected.update({"script-src": ("'none'",), "manifest-src": ("'none'",)})
    else:
        expected.update({"script-src": ("'self'",), "manifest-src": ("'self'",)})
    if directives != expected:
        errors.append(f"{relative}: CSP directives differ from the locked contract")
    unsupported = sorted(UNSUPPORTED_META_DIRECTIVES.intersection(directives))
    if unsupported:
        errors.append(f"{relative}: unsupported meta-CSP directives {unsupported}")
    if parser.referrers != ["no-referrer"]:
        errors.append(f"{relative}: referrer policy must be exactly no-referrer")
    if parser.inline_scripts or parser.inline_styles or parser.event_handlers:
        errors.append(
            f"{relative}: inline executable surface found "
            f"(scripts={parser.inline_scripts}, styles={parser.inline_styles}, handlers={parser.event_handlers})"
        )
    if parser.unsafe_blank_links:
        errors.append(f"{relative}: target=_blank links lack noopener+noreferrer {parser.unsafe_blank_links}")
    return errors


def validate_security_txt(now: datetime) -> list[str]:
    path = ROOT / ".well-known" / "security.txt"
    raw = path.read_bytes()
    errors: list[str] = []
    if len(raw) > 32 * 1024:
        errors.append("security.txt: exceeds the defensive 32 KiB parser limit")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return ["security.txt: must be valid UTF-8"]
    fields: dict[str, list[str]] = {}
    for line in text.splitlines():
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            errors.append(f"security.txt: malformed line {line!r}")
            continue
        name, value = line.split(":", 1)
        fields.setdefault(name, []).append(value.strip())
    required = {"Contact", "Expires", "Preferred-Languages", "Canonical"}
    if set(fields) != required:
        errors.append(f"security.txt: fields must be exactly {sorted(required)}")
    if any(len(values) != 1 for values in fields.values()):
        errors.append("security.txt: each declared field must occur exactly once")
    contact = fields.get("Contact", [""])[0]
    if urlsplit(contact).scheme != "mailto" or contact != "mailto:finalprime.official@gmail.com":
        errors.append("security.txt: Contact must be the controlled reporting mailbox")
    canonical = fields.get("Canonical", [""])[0]
    if canonical != f"{ORIGIN}/.well-known/security.txt":
        errors.append("security.txt: Canonical must match the live HTTPS location")
    if fields.get("Preferred-Languages", [""])[0] != "en, hu":
        errors.append("security.txt: Preferred-Languages must remain en, hu")
    expires_value = fields.get("Expires", [""])[0]
    try:
        expires = datetime.fromisoformat(expires_value.replace("Z", "+00:00"))
        if expires <= now:
            errors.append("security.txt: Expires is stale")
        if expires - now >= timedelta(days=365):
            errors.append("security.txt: Expires must remain less than one year in the future")
    except ValueError:
        errors.append("security.txt: Expires must be RFC 3339 compatible")
    return errors


def main() -> int:
    errors: list[str] = []
    html_paths = sorted(ROOT.rglob("*.html"))
    for path in html_paths:
        errors.extend(validate_html(path))
    errors.extend(validate_security_txt(datetime.now(timezone.utc)))
    if errors:
        print("Security contract validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Security contract OK: {len(html_paths)} CSP documents and RFC 9116 contact verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
