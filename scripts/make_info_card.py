#!/usr/bin/env python3
"""
Generate a neofetch-style info card SVG for vachan18's GitHub profile.

Output: info-card.svg in the repo root.
Each line fades and slides in on a short stagger.
Set STATIC=1 env var for a frozen frame (Quick Look previews).
"""

import os
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.environ.get("STATIC", "") == "1"

# ── Config ──────────────────────────────────────────────
TITLE_USER = "vachan18"
TITLE_HOST = "github"
SEPARATOR_LEN = 32

LINES = [
    ("OS",         "Linux x86_64 (Developer Edition)"),
    ("Role",       "Junior Software Engineer @ Synapx"),
    ("Education",  "B.Tech CSE · Dr. Ambedkar Inst. of Tech"),
    ("Stack",      "React · Next.js · Node.js · Python · Django"),
    ("AI",         "LangChain · CrewAI · GenAI · Agent AI"),
    ("DB",         "MongoDB · PostgreSQL · Firebase"),
    ("Cloud",      "AWS · GCP · Docker · Git"),
    ("Editor",     "VS Code / Cursor"),
    ("Shell",      "zsh + oh-my-zsh"),
    ("Uptime",     "Coding since 2020"),
]

# Colors
BG      = "#0d1117"
BORDER  = "#30363d"
KEY_CLR = "#79c0ff"   # blue for keys
VAL_CLR = "#c9d1d9"   # light gray for values
TITLE   = "#58a6ff"   # bright blue
SEP_CLR = "#484f58"   # dim separator
BAR_COLORS = ["#f85149","#d29922","#3fb950","#58a6ff","#bc8cff","#f0883e","#79c0ff","#e3b341"]

# Typography
FONT = "monospace"
FONT_SIZE = 13
LINE_H = 22
PADDING_X = 20
PADDING_Y = 20

def build():
    # Calculate dimensions
    n_lines = len(LINES) + 3  # title + separator + blank + data lines
    content_h = n_lines * LINE_H + 2 * PADDING_Y + 30  # +30 for color bar
    w = 480
    h = content_h

    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">')

    # CSS animations
    if not STATIC:
        parts.append("<defs><style>")
        parts.append("""
          @keyframes lineIn {
            0%   { opacity: 0; transform: translateX(-12px); }
            100% { opacity: 1; transform: translateX(0); }
          }
          .info-line {
            opacity: 0;
            animation: lineIn 0.35s ease-out forwards;
          }
        """)
        parts.append("</style></defs>")

    # Background
    parts.append(f'<rect width="{w}" height="{h}" rx="8" fill="{BG}" '
                 f'stroke="{BORDER}" stroke-width="1"/>')

    y = PADDING_Y + FONT_SIZE
    line_idx = 0

    def anim(idx):
        if STATIC:
            return ""
        delay = 0.5 + idx * 0.1
        return f'class="info-line" style="animation-delay:{delay:.2f}s"'

    # Title: user@host
    parts.append(f'<text x="{PADDING_X}" y="{y}" '
                 f'{anim(line_idx)} fill="{TITLE}" '
                 f'font-family="{FONT}" font-size="{FONT_SIZE}" font-weight="bold">'
                 f'{TITLE_USER}@{TITLE_HOST}</text>')
    line_idx += 1
    y += LINE_H

    # Separator
    sep = "─" * SEPARATOR_LEN
    parts.append(f'<text x="{PADDING_X}" y="{y}" '
                 f'{anim(line_idx)} fill="{SEP_CLR}" '
                 f'font-family="{FONT}" font-size="{FONT_SIZE}">'
                 f'{sep}</text>')
    line_idx += 1
    y += LINE_H

    # Key-value lines
    for key, val in LINES:
        parts.append(
            f'<text x="{PADDING_X}" y="{y}" '
            f'{anim(line_idx)} font-family="{FONT}" font-size="{FONT_SIZE}">'
            f'<tspan fill="{KEY_CLR}">{key}</tspan>'
            f'<tspan fill="{SEP_CLR}"> ~ </tspan>'
            f'<tspan fill="{VAL_CLR}">{val}</tspan>'
            f'</text>'
        )
        line_idx += 1
        y += LINE_H

    # Color bar (like neofetch terminal colors)
    y += 10
    bar_w = 22
    bar_h = 14
    bar_gap = 4
    bar_x = PADDING_X
    parts.append(f'<g {anim(line_idx)}>')
    for i, c in enumerate(BAR_COLORS):
        bx = bar_x + i * (bar_w + bar_gap)
        parts.append(f'<rect x="{bx}" y="{y}" width="{bar_w}" '
                     f'height="{bar_h}" rx="3" fill="{c}"/>')
    parts.append("</g>")

    parts.append("</svg>")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"[OK] Wrote info-card.svg -> {OUT}")


if __name__ == "__main__":
    build()
