#!/usr/bin/env python3
"""
Convert source-prepped.png → vachan-ascii.svg

A monochrome ASCII portrait that "types" itself in row by row using
SMIL animations inside the SVG. GitHub renders these when embedded via <img>.

Each row has a horizontal clip-rect wipe (left→right) staggered top→bottom.
Plays once and freezes — no looping.
"""

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "source-prepped.png"
OUT = ROOT / "vachan-ascii.svg"

# ASCII density ramp: bright (sparse) → dark (dense)
RAMP = " .`:-=+*cs#%@"

# Grid size
COLS = 100
ROWS = 53

# SVG settings
CHAR_W = 6.0     # monospace char width
CHAR_H = 10.0    # line height
FILL = "#b0b0b0"  # single monochrome color
BG = "#0d1117"

# Animation
ROW_WIPE_DURATION = 0.06   # seconds per row wipe
ROW_STAGGER = 0.02         # seconds between row starts
CURSOR_W = 3               # cursor block width in chars


def to_ascii(img_path: Path) -> list[str]:
    img = Image.open(img_path).convert("L")
    # Resize to grid (width adjusted for char aspect ratio ~0.55)
    img = img.resize((COLS, ROWS), Image.LANCZOS)
    arr = np.array(img)

    lines = []
    for row in arr:
        line = ""
        for px in row:
            idx = int(px / 255 * (len(RAMP) - 1))
            line += RAMP[idx]
        lines.append(line)
    return lines


def build_svg(lines: list[str]):
    w = COLS * CHAR_W + 20
    h = ROWS * CHAR_H + 20
    total_anim_time = ROWS * ROW_STAGGER + ROW_WIPE_DURATION + 0.5

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">')

    # Background
    parts.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>')

    # Defs: clip paths for each row
    parts.append("<defs>")
    for i in range(len(lines)):
        clip_id = f"clip-row-{i}"
        y = 6 + i * CHAR_H
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(f'  <rect x="0" y="{y}" width="0" height="{CHAR_H + 2}">')
        begin = f"{i * ROW_STAGGER:.3f}s"
        parts.append(f'    <animate attributeName="width" '
                     f'from="0" to="{w}" '
                     f'dur="{ROW_WIPE_DURATION}s" '
                     f'begin="{begin}" fill="freeze"/>')
        parts.append(f'  </rect>')
        parts.append(f'</clipPath>')
    parts.append("</defs>")

    # Text rows
    for i, line in enumerate(lines):
        clip_id = f"clip-row-{i}"
        y = 10 + i * CHAR_H + CHAR_H
        # Escape XML special chars
        escaped = (line.replace("&", "&amp;")
                       .replace("<", "&lt;")
                       .replace(">", "&gt;")
                       .replace('"', "&quot;"))
        parts.append(
            f'<text x="10" y="{y}" '
            f'clip-path="url(#{clip_id})" '
            f'fill="{FILL}" font-family="monospace" font-size="{CHAR_H}" '
            f'xml:space="preserve">{escaped}</text>'
        )

    # Cursor blocks riding each row's wipe edge
    for i in range(len(lines)):
        y = 6 + i * CHAR_H
        begin = f"{i * ROW_STAGGER:.3f}s"
        end_time = i * ROW_STAGGER + ROW_WIPE_DURATION
        cursor_w = CURSOR_W * CHAR_W
        parts.append(
            f'<rect x="0" y="{y}" width="{cursor_w}" height="{CHAR_H + 1}" '
            f'fill="#58a6ff" opacity="0.7">'
            f'  <animate attributeName="x" '
            f'from="0" to="{w}" '
            f'dur="{ROW_WIPE_DURATION}s" '
            f'begin="{begin}" fill="freeze"/>'
            f'  <animate attributeName="opacity" '
            f'from="0.7" to="0" '
            f'dur="0.1s" '
            f'begin="{end_time:.3f}s" fill="freeze"/>'
            f'</rect>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_INPUT
    if not src.exists():
        print(f"✗ Source not found: {src}")
        print("  Run prep_photo.py first, or pass the prepped image path.")
        sys.exit(1)

    print(f"-> Converting {src} to ASCII...")
    lines = to_ascii(src)
    svg = build_svg(lines)
    OUT.write_text(svg, encoding="utf-8")
    print(f"[OK] Wrote {OUT}")


if __name__ == "__main__":
    main()
