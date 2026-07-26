from __future__ import annotations

import collections
import datetime as dt
import subprocess
from pathlib import Path


OUTPUT = Path("assets/graph.svg")
BG = "#0b1117"
TEXT = "#8bffb0"
PALETTE = ["#0e4429", "#006d32", "#26a641", "#39d353", "#9be9a8"]


def git_commit_counts() -> dict[str, int]:
    command = ["git", "log", "--since=365 days ago", "--date=short", "--format=%ad"]
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        cwd=Path(__file__).resolve().parent.parent,
    )
    counts: dict[str, int] = collections.defaultdict(int)
    for line in result.stdout.splitlines():
        counts[line.strip()] += 1
    return counts


def level_for(count: int, maximum: int) -> int:
    if count <= 0:
        return 0
    if maximum <= 1:
        return 1
    ratio = count / maximum
    if ratio < 0.25:
        return 1
    if ratio < 0.5:
        return 2
    if ratio < 0.75:
        return 3
    return 4


def build_svg() -> str:
    today = dt.date.today()
    start = today - dt.timedelta(days=364)
    counts = git_commit_counts()

    dates: list[dt.date] = [start + dt.timedelta(days=offset) for offset in range(365)]
    maximum = max(counts.values(), default=0)
    total_commits = sum(counts.values())
    active_days = sum(1 for count in counts.values() if count > 0)
    peak_day = max(counts.items(), key=lambda item: item[1], default=(today.isoformat(), 0))

    cell = 14
    gap = 4
    offset_x = 42
    offset_y = 104
    width = offset_x + 53 * (cell + gap) + 24
    height = 262
    title = f"{total_commits} commits in the last year"

    month_labels = []
    seen_months: set[tuple[int, int]] = set()
    for current_date in dates:
        if current_date.day != 1:
            continue
        marker = (current_date.year, current_date.month)
        if marker in seen_months:
            continue
        seen_months.add(marker)
        week_index = ((current_date - start).days) // 7
        x = offset_x + week_index * (cell + gap)
        month_labels.append(
            f'<text x="{x}" y="70" font-family="monospace" font-size="11" fill="#5f7f6e">{current_date.strftime("%b")}</text>'
        )

    day_labels = []
    for label, row in [("Sun", 0), ("Mon", 1), ("Tue", 2), ("Wed", 3), ("Thu", 4), ("Fri", 5), ("Sat", 6)]:
        if row not in (0, 2, 4, 6):
            continue
        y = offset_y + row * (cell + gap) + 12
        day_labels.append(
            f'<text x="10" y="{y}" font-family="monospace" font-size="10" fill="#5f7f6e">{label}</text>'
        )

    summary = [(f"{total_commits}", "commits"), (f"{active_days}", "active days"), (f"{peak_day[1]}", "peak day")]
    summary_blocks = []
    summary_x = width - 304
    for index, (value, label) in enumerate(summary):
        x = summary_x + index * 102
        summary_blocks.append(
            f'<rect x="{x}" y="44" width="94" height="28" rx="8" fill="#081015" stroke="#1f3a2d" stroke-width="1" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{0.4 + index * 0.2:.2f}s" fill="freeze" />'
            f'</rect>'
            f'<text x="{x + 8}" y="61" font-family="monospace" font-size="12" fill="#8fffb7">{value}</text>'
            f'<text x="{x + 8}" y="70" font-family="monospace" font-size="8" fill="#5f7f6e">{label}</text>'
        )

    cells = []
    for index, current_date in enumerate(dates):
        week_index = ((current_date - start).days) // 7
        row = current_date.weekday() + 1
        if row == 7:
            row = 0
        x = offset_x + week_index * (cell + gap)
        y = offset_y + row * (cell + gap)
        count = counts.get(current_date.isoformat(), 0)
        level = level_for(count, maximum)
        fill = PALETTE[level]
        delay = index * 0.01
        cells.append(
            f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{fill}" opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.18s" begin="{delay:.2f}s" fill="freeze" />'
            f'</rect>'
        )

    legend = []
    legend_x = width - 108
    legend_y = 64
    for index, color in enumerate(PALETTE):
        x = legend_x + index * 18
        legend.append(f'<rect x="{x}" y="{legend_y}" width="12" height="12" rx="3" fill="{color}" />')

    reveal_width = width - 28

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated contribution graph">
    <style>
      <![CDATA[
        .soft-glow {{ animation: pulse 3.2s ease-in-out infinite; }}
        .sweep {{ animation: sweep 2.8s ease-in-out infinite; }}
        @keyframes pulse {{
          0%, 100% {{ opacity: 0.18; }}
          50% {{ opacity: 0.42; }}
        }}
        @keyframes sweep {{
          0% {{ transform: translateX(0px); }}
          100% {{ transform: translateX({reveal_width}px); }}
        }}
      ]]>
    </style>
    <defs>
        <linearGradient id="shell" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0%" stop-color="#13261a" />
            <stop offset="100%" stop-color="#081015" />
        </linearGradient>
        <radialGradient id="glow" cx="50%" cy="35%" r="70%">
            <stop offset="0%" stop-color="#39d353" stop-opacity="0.16" />
            <stop offset="100%" stop-color="#39d353" stop-opacity="0" />
        </radialGradient>
        <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="0" stdDeviation="1.2" flood-color="#39d353" flood-opacity="0.22" />
        </filter>
        <clipPath id="reveal">
          <rect x="18" y="18" width="0" height="{height - 36}">
            <animate attributeName="width" from="0" to="{reveal_width}" dur="2.4s" begin="0s" fill="freeze" />
          </rect>
        </clipPath>
    </defs>

    <rect width="{width}" height="{height}" rx="18" fill="#03060a" />
    <rect x="8" y="8" width="{width - 16}" height="{height - 16}" rx="14" fill="url(#shell)" opacity="0.92" />
    <rect x="14" y="14" width="{width - 28}" height="{height - 28}" rx="10" fill="{BG}" stroke="#1f3a2d" stroke-width="1.2" />
    <rect x="14" y="14" width="{width - 28}" height="{height - 28}" rx="10" fill="url(#glow)" class="soft-glow" />

    <circle cx="32" cy="28" r="5" fill="#ff5f57" />
    <circle cx="48" cy="28" r="5" fill="#febc2e" />
    <circle cx="64" cy="28" r="5" fill="#28c840" />

    <text x="88" y="33" font-family="monospace" font-size="14" fill="{TEXT}">$ cat contributions.log</text>
    <text x="18" y="58" font-family="monospace" font-size="11" fill="#5f7f6e">{title}</text>
    <text x="{width - 150}" y="33" font-family="monospace" font-size="10" fill="#5f7f6e">live.activity</text>

    {''.join(summary_blocks)}
    {''.join(month_labels)}
    {''.join(day_labels)}

    <g shape-rendering="crispEdges" filter="url(#shadow)" clip-path="url(#reveal)">
        {''.join(cells)}
    </g>

    {''.join(legend)}
    <text x="{legend_x - 46}" y="74" font-family="monospace" font-size="10" fill="#5f7f6e">Less</text>
    <text x="{legend_x + 94}" y="74" font-family="monospace" font-size="10" fill="#5f7f6e">More</text>
    <text x="18" y="{height - 30}" font-family="monospace" font-size="10" fill="#5f7f6e">auto-updated from git history · peak {peak_day[0]}</text>

    <rect x="18" y="{height - 18}" width="{width - 36}" height="2" fill="#2ee59d" opacity="0.35">
        <animate attributeName="opacity" values="0.2;0.75;0.2" dur="2.4s" repeatCount="indefinite" />
    </rect>
    <rect x="18" y="{height - 18}" width="120" height="2" fill="#8fffb7" opacity="0.85" class="sweep" />
</svg>
'''


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()