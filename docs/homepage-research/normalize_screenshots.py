#!/usr/bin/env python3
"""Normalize research captures to metadata-free, repository-safe RGB PNG files."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent / "screenshots"
MAX_BYTES = 1024 * 1024
MAX_DESKTOP_WIDTH = 1100


def encode(image: Image.Image) -> bytes:
    output = BytesIO()
    image.save(output, format="PNG", optimize=True, compress_level=9)
    return output.getvalue()


def normalize(path: Path) -> tuple[int, int, int]:
    with Image.open(path) as source:
        image = source.convert("RGB")

    if image.width > MAX_DESKTOP_WIDTH:
        height = round(image.height * MAX_DESKTOP_WIDTH / image.width)
        image = image.resize((MAX_DESKTOP_WIDTH, height), Image.Resampling.LANCZOS)

    data = encode(image)
    while len(data) > MAX_BYTES:
        scale = max(0.72, (MAX_BYTES / len(data)) ** 0.5 * 0.94)
        width = max(320, round(image.width * scale))
        height = max(180, round(image.height * scale))
        if (width, height) == image.size:
            raise RuntimeError(f"Could not reduce {path} below repository limit")
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        data = encode(image)

    temporary = path.with_suffix(".normalized.png")
    temporary.write_bytes(data)
    temporary.replace(path)
    return image.width, image.height, len(data)


def main() -> None:
    paths = sorted(ROOT.rglob("*.png"))
    for index, path in enumerate(paths, start=1):
        width, height, size = normalize(path)
        relative = path.relative_to(ROOT).as_posix()
        print(f"[{index:02d}/{len(paths):02d}] {relative}: {width}x{height}, {size} bytes", flush=True)


if __name__ == "__main__":
    main()
