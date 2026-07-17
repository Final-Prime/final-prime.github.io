#!/usr/bin/env python3
"""Reject accidental secrets, private context, risky files, and image metadata."""

from __future__ import annotations

import argparse
from binascii import crc32
import os
from pathlib import Path
import re
from struct import unpack
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MAX_TRACKED_BYTES = 1024 * 1024
ALLOWED_SUFFIXES = {
    ".css", ".csv", ".html", ".js", ".md", ".png", ".py", ".svg",
    ".txt", ".webmanifest", ".xml", ".yml",
}
ALLOWED_EXTENSIONLESS_PATHS = {".github/CODEOWNERS", ".nojekyll", "LICENSE", "NOTICE"}
RISKY_BASENAMES = {".env", "credentials", "id_dsa", "id_ed25519", "id_rsa", "secrets"}
RISKY_SUFFIXES = {
    ".7z", ".bak", ".db", ".env", ".gz", ".key", ".kdbx", ".log", ".map",
    ".p12", ".pem", ".pfx", ".rar", ".sqlite", ".swp", ".tar", ".tmp", ".zip",
}
EXPECTED_EMAIL = "finalprime.official@gmail.com"
PNG_ALLOWED_CHUNKS = {b"IHDR", b"IDAT", b"IEND"}


SECRET_PATTERNS = {
    "private key": re.compile(("-----BEGIN " + r"(?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----").encode()),
    "AWS access key": re.compile(("AK" + r"IA[0-9A-Z]{16}").encode()),
    "GitHub token": re.compile(("gh" + r"[pousr]_[A-Za-z0-9_]{20,}").encode()),
    "Google API key": re.compile(("AI" + r"za[0-9A-Za-z_-]{30,}").encode()),
    "Slack token": re.compile(("xo" + r"x[baprs]-[0-9A-Za-z-]{10,}").encode()),
    "Stripe live key": re.compile(("sk" + r"_live_[0-9A-Za-z]{16,}").encode()),
    "JWT": re.compile(("ey" + r"J[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}").encode()),
    "Bearer credential": re.compile(rb"(?i:authorization)\s*[:=]\s*(?i:bearer)\s+[A-Za-z0-9._-]{12,}"),
}
EMAIL_PATTERN = re.compile(rb"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
WINDOWS_PRIVATE_PATH = re.compile(rb"(?i:[A-Z]:[\\/](?:Users|Git|AI|tmp)[\\/])")
UNIX_PRIVATE_PATH = re.compile(rb"/(?:home|Users)/[^/\s]+/")
PRIVATE_IPV4 = re.compile(rb"\b(?:10\.(?:\d{1,3}\.){2}\d{1,3}|192\.168\.(?:\d{1,3}\.)\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.(?:\d{1,3}\.)\d{1,3})\b")


def git(*args: str, check: bool = True) -> bytes:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def tracked_paths() -> list[Path]:
    return [
        ROOT / item.decode("utf-8")
        for item in git("ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0")
        if item
    ]


def scan_secret_bytes(data: bytes, label: str) -> list[str]:
    errors: list[str] = []
    for name, pattern in SECRET_PATTERNS.items():
        if pattern.search(data):
            errors.append(f"{label}: detected {name} pattern")
    return errors


def validate_text(path: Path, data: bytes) -> list[str]:
    relative = path.relative_to(ROOT).as_posix()
    errors = scan_secret_bytes(data, relative)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [*errors, f"{relative}: tracked text must be valid UTF-8"]
    if "\x00" in text:
        errors.append(f"{relative}: unexpected binary NUL in text file")
    emails = {match.decode("ascii").lower() for match in EMAIL_PATTERN.findall(data)}
    unexpected_emails = sorted(emails.difference({EXPECTED_EMAIL}))
    if unexpected_emails:
        errors.append(f"{relative}: unexpected public email address count={len(unexpected_emails)}")
    if WINDOWS_PRIVATE_PATH.search(data) or UNIX_PRIVATE_PATH.search(data):
        errors.append(f"{relative}: local machine path disclosed")
    if PRIVATE_IPV4.search(data):
        errors.append(f"{relative}: private network address disclosed")
    local_endpoint_pattern = r"(?i)\b(?:" + "local" + "host|" + "127" + r"\.0\.0\.1|" + "0" + r"\.0\.0\.0)\b"
    localhost_mentions = len(re.findall(local_endpoint_pattern, text))
    if localhost_mentions:
        preview_url = "http://local" + "host:8000"
        allowed = relative == "README.md" and localhost_mentions == 1 and preview_url in text
        if not allowed:
            errors.append(f"{relative}: unexpected local endpoint disclosure count={localhost_mentions}")
    return errors


def validate_png(path: Path, data: bytes) -> list[str]:
    relative = path.relative_to(ROOT).as_posix()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return [f"{relative}: invalid PNG signature"]
    errors: list[str] = []
    offset = 8
    chunks: list[bytes] = []
    while offset + 12 <= len(data):
        length = unpack(">I", data[offset : offset + 4])[0]
        kind = data[offset + 4 : offset + 8]
        end = offset + 12 + length
        if end > len(data):
            errors.append(f"{relative}: truncated PNG chunk")
            break
        payload = data[offset + 8 : offset + 8 + length]
        expected_crc = unpack(">I", data[offset + 8 + length : end])[0]
        if crc32(kind + payload) & 0xFFFFFFFF != expected_crc:
            errors.append(f"{relative}: invalid PNG CRC")
        chunks.append(kind)
        if kind not in PNG_ALLOWED_CHUNKS:
            errors.append(f"{relative}: ancillary or unexpected PNG chunk {kind.decode('ascii', 'replace')}")
        offset = end
        if kind == b"IEND":
            break
    if not chunks or chunks[0] != b"IHDR" or chunks[-1] != b"IEND" or b"IDAT" not in chunks:
        errors.append(f"{relative}: invalid PNG chunk structure")
    if offset != len(data):
        errors.append(f"{relative}: trailing data after PNG IEND")
    return errors


def validate_svg(path: Path, data: bytes) -> list[str]:
    relative = path.relative_to(ROOT).as_posix()
    errors = validate_text(path, data)
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return [*errors, f"{relative}: invalid SVG XML"]
    for element in root.iter():
        local_tag = element.tag.rsplit("}", 1)[-1].lower()
        if local_tag in {"script", "foreignobject"}:
            errors.append(f"{relative}: active SVG element {local_tag} is forbidden")
        for attribute, value in element.attrib.items():
            local_attribute = attribute.rsplit("}", 1)[-1].lower()
            if local_attribute.startswith("on"):
                errors.append(f"{relative}: SVG event handler is forbidden")
            if local_attribute in {"href", "src"} and url_is_external(value):
                errors.append(f"{relative}: external SVG resource is forbidden")
    return errors


def url_is_external(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith(("http://", "https://", "//"))


def validate_current_tree() -> tuple[list[str], int]:
    errors: list[str] = []
    paths = [path for path in tracked_paths() if path.is_file()]
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        suffix = path.suffix.lower()
        if path.name.lower() in RISKY_BASENAMES or suffix in RISKY_SUFFIXES:
            errors.append(f"{relative}: risky public filename")
        if not suffix and relative not in ALLOWED_EXTENSIONLESS_PATHS:
            errors.append(f"{relative}: unapproved extensionless file")
        elif suffix and suffix not in ALLOWED_SUFFIXES:
            errors.append(f"{relative}: unapproved public file type {suffix}")
        data = path.read_bytes()
        if len(data) > MAX_TRACKED_BYTES:
            errors.append(f"{relative}: tracked file exceeds 1 MiB")
        if suffix == ".png":
            errors.extend(validate_png(path, data))
        elif suffix == ".svg":
            errors.extend(validate_svg(path, data))
        else:
            errors.extend(validate_text(path, data))
    return errors, len(paths)


def validate_history() -> tuple[list[str], int]:
    errors: list[str] = []
    object_lines = git("rev-list", "--objects", "HEAD").splitlines()
    object_ids = list(dict.fromkeys(line.split(b" ", 1)[0] for line in object_lines))
    scanned = 0
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        for object_id in object_ids:
            process.stdin.write(object_id + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().strip().split()
            if len(header) != 3:
                errors.append(f"history object {object_id[:8].decode()}: unreadable batch header")
                break
            _, kind, raw_size = header
            size = int(raw_size)
            data = process.stdout.read(size)
            process.stdout.read(1)
            if kind != b"blob":
                continue
            if size > MAX_TRACKED_BYTES:
                errors.append(f"history blob {object_id[:8].decode()}: exceeds 1 MiB")
                continue
            errors.extend(scan_secret_bytes(data, f"history blob {object_id[:8].decode()}"))
            scanned += 1
    finally:
        process.stdin.close()
        process.wait(timeout=10)
    names = set(git("log", "--format=", "--name-only", "HEAD").decode("utf-8", "replace").splitlines())
    for name in sorted(filter(None, names)):
        path = Path(name)
        if path.name.lower() in RISKY_BASENAMES or path.suffix.lower() in RISKY_SUFFIXES:
            errors.append(f"history path {name}: risky filename")
    return errors, scanned


def validate_future_commit_identity() -> list[str]:
    configured = git("config", "--local", "user.email", check=False).decode().strip().lower()
    if configured:
        email = configured
    else:
        ref = "HEAD^2" if os.environ.get("GITHUB_EVENT_NAME") == "pull_request" else "HEAD"
        email = git("log", "-1", "--format=%ae", ref).decode().strip().lower()
    if not email.endswith("@users.noreply.github.com"):
        return ["future commit identity must use a GitHub noreply address"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--history", action="store_true", help="scan every blob reachable from HEAD")
    args = parser.parse_args()
    errors, files = validate_current_tree()
    errors.extend(validate_future_commit_identity())
    history_blobs = 0
    if args.history:
        history_errors, history_blobs = validate_history()
        errors.extend(history_errors)
    if errors:
        print("Public surface validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    history_note = f", {history_blobs} history blobs" if args.history else ""
    print(f"Public surface OK: {files} tracked files{history_note}; privacy, secret, and metadata contracts verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
