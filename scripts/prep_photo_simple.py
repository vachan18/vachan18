#!/usr/bin/env python3
"""
Prep photo for ASCII art conversion:
1. Isolate background using corner color sampling.
2. Set background to pure white (255) so it maps to spaces ' '.
3. Enhance facial contrast for crisp ASCII definition.
"""
from pathlib import Path
import sys
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
    arr = np.array(img, dtype=float)

    # Sample background color from the corners
    bg_corners = np.concatenate([
        arr[:50, :50].reshape(-1, 3),
        arr[:50, -50:].reshape(-1, 3),
        arr[-50:, :50].reshape(-1, 3),
        arr[-50:, -50:].reshape(-1, 3)
    ])
    bg_col = np.median(bg_corners, axis=0)

    # Calculate distance to background color
    dist = np.linalg.norm(arr - bg_col, axis=2)
    bg_mask = dist < 28

    # Convert to grayscale
    gray = ImageOps.grayscale(img)
    gray_arr = np.array(gray, dtype=np.uint8)

    # Set background to pure white
    gray_arr[bg_mask] = 255

    # Local enhancement
    out_im = Image.fromarray(gray_arr, mode="L")
    out_im = ImageOps.autocontrast(out_im, cutoff=1)
    enhancer = ImageEnhance.Contrast(out_im)
    out_im = enhancer.enhance(1.4)
    out_im = out_im.filter(ImageFilter.SHARPEN)

    out_im.save(OUT)
    print(f"[OK] Wrote {OUT}")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else None
    prep(src)
