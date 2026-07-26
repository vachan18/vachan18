from pathlib import Path

import svgwrite


OUTPUT = Path("assets/dev-dashboard.svg")


cards = [
    ("role", "AI Software Engineer"),
    ("focus", "LLM Applications | AI Agents | RAG"),
    ("stack", "Python | React | Django | Flask"),
    ("cloud", "AWS | Docker | Linux | GitHub Actions"),
]


def build_svg() -> str:
    width = 1100
    height = 520
    dwg = svgwrite.Drawing(size=(width, height))
    dwg.viewbox(0, 0, width, height)

    defs = dwg.defs
    bg = dwg.linearGradient(id="bg", x1="0%", y1="0%", x2="100%", y2="100%")
    bg.add_stop_color("0%", "#050816")
    bg.add_stop_color("100%", "#0b1220")
    defs.add(bg)

    card = dwg.linearGradient(id="card", x1="0%", y1="0%", x2="100%", y2="100%")
    card.add_stop_color("0%", "#111827")
    card.add_stop_color("100%", "#0b1120")
    defs.add(card)

    glow = dwg.filter(id="glow", x="-30%", y="-30%", width="160%", height="160%")
    glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=8, result="blur")
    defs.add(glow)

    grid = dwg.pattern(id="grid", size=(48, 48), patternUnits="userSpaceOnUse")
    grid.add(dwg.path(d="M 48 0 L 0 0 0 48", fill="none", stroke="#1f2937", stroke_width=1))
    defs.add(grid)

    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), rx=28, fill="url(#bg)"))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), rx=28, fill="url(#grid)", opacity=0.22))
    dwg.add(dwg.circle(center=(965, 78), r=170, fill="#14b8a6", opacity=0.08))
    dwg.add(dwg.circle(center=(120, 420), r=185, fill="#22c55e", opacity=0.06))

    dwg.add(dwg.rect(insert=(42, 40), size=(1016, 440), rx=24, fill="#0a0f1d", stroke="#22314f", stroke_width=1.2))
    dwg.add(dwg.rect(insert=(42, 40), size=(1016, 68), rx=24, fill="#0d1324"))
    dwg.add(dwg.rect(insert=(42, 82), size=(1016, 26), fill="#0d1324"))

    for x, color in [(76, "#2ee59d"), (104, "#22c55e"), (132, "#16a34a")]:
        dwg.add(dwg.circle(center=(x, 74), r=8, fill=color))

    dwg.add(
        dwg.text(
            "$ developer.stats",
            insert=(188, 84),
            fill="#2ee59d",
            font_size="28",
            font_family="monospace",
            font_weight="700",
        )
    )
    dwg.add(
        dwg.text(
            "AI engineer dashboard | production-minded profile snapshot",
            insert=(188, 104),
            fill="#94a3b8",
            font_size="14",
            font_family="monospace",
        )
    )

    positions = [(68, 140), (560, 140), (68, 290), (560, 290)]
    for (label, value), (x, y) in zip(cards, positions):
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(472, 122),
                rx=18,
                fill="url(#card)",
                stroke="#1f2a44",
                stroke_width=1.2,
            )
        )
        dwg.add(
            dwg.rect(
                insert=(x + 18, y + 18),
                size=(6, 86),
                rx=3,
                fill="#2ee59d",
                filter="url(#glow)",
            )
        )
        dwg.add(
            dwg.text(
                label.upper(),
                insert=(x + 40, y + 42),
                fill="#2ee59d",
                font_size="16",
                font_family="monospace",
                font_weight="700",
            )
        )
        dwg.add(
            dwg.text(
                value,
                insert=(x + 40, y + 76),
                fill="#f8fafc",
                font_size="22",
                font_family="monospace",
                font_weight="700",
            )
        )

    dwg.add(
        dwg.text(
            "> Building AI systems that feel sharp, useful, and ready for production",
            insert=(68, 448),
            fill="#cbd5e1",
            font_size="15",
            font_family="monospace",
        )
    )

    return dwg.tostring()


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()