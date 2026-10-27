#!/usr/bin/env python3
"""
Simplified photo prep using only Pillow + numpy (no rembg/opencv needed).
Converts photo to high-contrast grayscale suitable for ASCII art.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = ROOT / "source-photo.jpg"
OUT = ROOT / "source-prepped.png"


def prep(source: str = None):
    src = Path(source) if source else DEFAULT_INPUT
    if not src.exists():
        print(f"[ERR] File not found: {src}")
        sys.exit(1)

    print(f"-> Reading {src}...")
    img = Image.open(src).convert("RGB")

    # 1. Convert to grayscale
    gray = ImageOps.grayscale(img)

    # 2. Auto-contrast to use full dynamic range
    gray = ImageOps.autocontrast(gray, cutoff=2)

    # 3. Boost contrast further for ASCII clarity
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(1.8)

    # 4. Slight sharpening to preserve edges
    gray = gray.filter(ImageFilter.SHARPEN)

    # 5. Brighten the background: the blue-gray background is mid-tone,
    #    boost brightness so it maps to spaces in ASCII
    enhancer = ImageEnhance.Brightness(gray)
    gray = enhancer.enhance(1.15)

    # Save
    gray.save(OUT)
    print(f"[OK] Wrote {OUT}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else None
    prep(src)
