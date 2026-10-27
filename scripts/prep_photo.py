#!/usr/bin/env python3
"""
Prep a photo for ASCII art conversion.

Steps:
  1. Remove background with rembg
  2. Boost local contrast with CLAHE
  3. Composite onto pure white

Usage: python scripts/prep_photo.py <source-photo.jpg>
Output: source-prepped.png
"""

import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep(source: str):
    src = Path(source)
    if not src.exists():
        print(f"✗ File not found: {src}")
        sys.exit(1)

    print(f"→ Reading {src}…")
    raw = Image.open(src).convert("RGBA")

    # 1. Remove background
    print("→ Removing background…")
    no_bg = remove(raw)

    # 2. Convert to grayscale numpy for CLAHE
    arr = np.array(no_bg)
    alpha = arr[:, :, 3]
    gray = cv2.cvtColor(arr[:, :, :3], cv2.COLOR_RGB2GRAY)

    # 3. CLAHE – boost local contrast
    print("→ Applying CLAHE…")
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # 4. Composite onto white
    white = np.full_like(enhanced, 255)
    mask = (alpha / 255.0).astype(np.float32)
    composited = (enhanced * mask + white * (1 - mask)).astype(np.uint8)

    out = src.parent / "source-prepped.png"
    Image.fromarray(composited, mode="L").save(out)
    print(f"✓ Wrote {out}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/prep_photo.py <source-photo.jpg>")
        sys.exit(1)
    prep(sys.argv[1])
