#!/usr/bin/env python3
"""
Render data/contributions.json as an animated SVG heatmap.

Output: contrib-heatmap.svg in the repo root.
The grid is 53 weeks × 7 days with a GitHub-ish green ramp.
CSS keyframe animations reveal columns diagonally, then freeze.
"""

import json
import math
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

# GitHub-ish green ramp (dark theme)
PALETTE = [
    "#161b22",  # level 0 – empty
    "#0e4429",  # level 1
    "#006d32",  # level 2
    "#26a641",  # level 3
    "#39d353",  # level 4
    "#69f0a0",  # level 5 (neon top-end, for "best" days)
]

CELL = 13        # box size px
GAP = 3          # gap between boxes
RADIUS = 2       # corner radius
MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]
DAY_LABELS = ["Mon","","Wed","","Fri","","Sun"]

# Animation timing
ANIM_DURATION_S = 2.0   # total reveal time


def level_color(level: int) -> str:
    return PALETTE[min(level, len(PALETTE) - 1)]


def render():
    data = json.loads(DATA.read_text())
    days = data["days"]
    total = data.get("total_contributions", data.get("total", 0))

    # Build week columns (Sun=0 … Sat=6 in GitHub, but we remap Mon-first)
    weeks: list[list[dict | None]] = []
    if not days:
        print("No contribution data found.")
        return

    # Map into 7-row, N-col grid
    from datetime import date as dt_date
    first = datetime.strptime(days[0]["date"], "%Y-%m-%d").date()
    last = datetime.strptime(days[-1]["date"], "%Y-%m-%d").date()

    # Weekday: 0=Mon … 6=Sun
    day_map = {d["date"]: d for d in days}
    # Start from the Monday of the first week
    start = first - timedelta(days=first.weekday())

    current = start
    col = []
    while current <= last:
        key = current.strftime("%Y-%m-%d")
        entry = day_map.get(key)
        dow = current.weekday()  # 0=Mon
        if dow == 0 and col:
            weeks.append(col)
            col = []
        col.append(entry if entry else {"date": key, "count": 0, "level": 0})
        current += timedelta(days=1)
    if col:
        weeks.append(col)

    n_weeks = len(weeks)
    left_margin = 36
    top_margin = 24
    grid_w = n_weeks * (CELL + GAP)
    grid_h = 7 * (CELL + GAP)
    svg_w = left_margin + grid_w + 20
    legend_h = 50
    stats_h = 30
    svg_h = top_margin + grid_h + legend_h + stats_h

    parts = []

    # SVG header
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" '
                 f'width="{svg_w}" height="{svg_h}" '
                 f'viewBox="0 0 {svg_w} {svg_h}">')

    # CSS animations
    parts.append("<defs><style>")
    parts.append("""
      @keyframes fadeSlideIn {
        0%   { opacity: 0; transform: translateY(-8px); }
        100% { opacity: 1; transform: translateY(0); }
      }
      .hm-col {
        opacity: 0;
        animation: fadeSlideIn 0.3s ease-out forwards;
      }
      .hm-label {
        opacity: 0;
        animation: fadeSlideIn 0.4s ease-out forwards;
      }
      .hm-stats {
        opacity: 0;
        animation: fadeSlideIn 0.5s ease-out forwards;
      }
    """)

    # Per-column delay
    for i in range(n_weeks):
        delay = (i / max(n_weeks - 1, 1)) * ANIM_DURATION_S
        parts.append(f".hm-col-{i} {{ animation-delay: {delay:.3f}s; }}")

    parts.append("</style></defs>")

    # Background
    parts.append(f'<rect width="{svg_w}" height="{svg_h}" rx="6" fill="#0d1117"/>')

    # Month labels
    month_positions = {}
    for wi, week in enumerate(weeks):
        first_day = week[0]
        d = datetime.strptime(first_day["date"], "%Y-%m-%d")
        m = d.month
        if m not in month_positions:
            month_positions[m] = wi

    for m, wi in month_positions.items():
        x = left_margin + wi * (CELL + GAP)
        parts.append(f'<text x="{x}" y="{top_margin - 6}" '
                     f'class="hm-label" style="animation-delay:{wi / max(n_weeks,1) * ANIM_DURATION_S:.2f}s" '
                     f'fill="#8b949e" font-family="monospace" font-size="10">'
                     f'{MONTH_LABELS[m - 1]}</text>')

    # Day labels (left side)
    for i, label in enumerate(DAY_LABELS):
        if label:
            y = top_margin + i * (CELL + GAP) + CELL - 2
            parts.append(f'<text x="2" y="{y}" '
                         f'class="hm-label" style="animation-delay:0s" '
                         f'fill="#8b949e" font-family="monospace" font-size="10">'
                         f'{label}</text>')

    # Grid cells
    for wi, week in enumerate(weeks):
        parts.append(f'<g class="hm-col hm-col-{wi}">')
        for di, day in enumerate(week):
            if day is None:
                continue
            x = left_margin + wi * (CELL + GAP)
            y = top_margin + di * (CELL + GAP)
            color = level_color(day["level"])
            tooltip = f'{day["count"]} contributions on {day["date"]}'
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="{RADIUS}" fill="{color}">'
                f'<title>{tooltip}</title></rect>'
            )
        parts.append("</g>")

    # Legend (Less → More)
    legend_y = top_margin + grid_h + 16
    legend_x = svg_w - 200
    stats_delay = ANIM_DURATION_S + 0.3

    parts.append(f'<g class="hm-stats" style="animation-delay:{stats_delay:.2f}s">')
    parts.append(f'<text x="{legend_x}" y="{legend_y + 10}" '
                 f'fill="#8b949e" font-family="monospace" font-size="10">Less</text>')
    for i, c in enumerate(PALETTE):
        bx = legend_x + 34 + i * (CELL + 2)
        parts.append(f'<rect x="{bx}" y="{legend_y}" width="{CELL}" '
                     f'height="{CELL}" rx="{RADIUS}" fill="{c}"/>')
    more_x = legend_x + 34 + len(PALETTE) * (CELL + 2) + 4
    parts.append(f'<text x="{more_x}" y="{legend_y + 10}" '
                 f'fill="#8b949e" font-family="monospace" font-size="10">More</text>')
    parts.append("</g>")

    # Stats footer
    footer_y = legend_y + 30
    parts.append(f'<g class="hm-stats" style="animation-delay:{stats_delay + 0.2:.2f}s">')
    parts.append(f'<text x="{left_margin}" y="{footer_y}" '
                 f'fill="#c9d1d9" font-family="monospace" font-size="12">'
                 f'{total:,} contributions in the last year</text>')

    streak = data.get("current_streak", 0)
    longest = data.get("longest_streak", 0)
    best = data.get("best_day", {})
    best_str = f'{best.get("count", 0)} on {best.get("date", "N/A")}'

    mid_x = svg_w // 2
    parts.append(f'<text x="{mid_x}" y="{footer_y}" '
                 f'fill="#8b949e" font-family="monospace" font-size="11" text-anchor="middle">'
                 f'Current Streak: {streak}d · Longest: {longest}d · Best: {best_str}</text>')
    parts.append("</g>")

    parts.append("</svg>")

    OUT.write_text("\n".join(parts))
    print(f"[OK] Rendered heatmap -> {OUT}")


if __name__ == "__main__":
    render()
