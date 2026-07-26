import svgwrite


output = "assets/dev-dashboard.svg"


cards = [
    {
        "title": "Experience",
        "body": "Software Engineer @ Synapx",
        "accent": "#2ee59d",
    },
    {
        "title": "Current Focus",
        "body": "Building AI-powered applications",
        "accent": "#7dd3fc",
    },
    {
        "title": "Learning",
        "body": "AI Agents • RAG Systems • Cloud Architecture",
        "accent": "#fbbf24",
    },
    {
        "title": "Tech Focus",
        "body": "Python • LLMs • Automation",
        "accent": "#a78bfa",
    },
]


dwg = svgwrite.Drawing(output, size=("1100", "520"))
dwg.viewbox(0, 0, 1100, 520)


defs = dwg.defs
bg = dwg.linearGradient(id="bg", x1="0%", y1="0%", x2="100%", y2="100%")
defs.add(bg)
bg.add_stop_color("0%", "#050816")
bg.add_stop_color("55%", "#0b1220")
bg.add_stop_color("100%", "#0f172a")

card = dwg.linearGradient(id="card", x1="0%", y1="0%", x2="100%", y2="100%")
defs.add(card)
card.add_stop_color("0%", "#111827")
card.add_stop_color("100%", "#0b1120")

glow = dwg.filter(id="glow", x="-30%", y="-30%", width="160%", height="160%")
defs.add(glow)
glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=8, result="blur")

grid = dwg.pattern(id="grid", size=(48, 48), patternUnits="userSpaceOnUse")
defs.add(grid)
grid.add(dwg.path(d="M 48 0 L 0 0 0 48", fill="none", stroke="#1f2937", stroke_width=1))


dwg.add(dwg.rect(insert=(0, 0), size=(1100, 520), rx=28, fill="url(#bg)"))
dwg.add(dwg.rect(insert=(0, 0), size=(1100, 520), rx=28, fill="url(#grid)", opacity=0.25))
dwg.add(dwg.circle(center=(1020, 70), r=170, fill="#14b8a6", opacity=0.09))
dwg.add(dwg.circle(center=(120, 430), r=190, fill="#7c3aed", opacity=0.08))


# Terminal frame
dwg.add(dwg.rect(insert=(48, 42), size=(1004, 436), rx=22, fill="#0a0f1d", stroke="#22314f", stroke_width=1.2))
dwg.add(dwg.rect(insert=(48, 42), size=(1004, 70), rx=22, fill="#0d1324"))
dwg.add(dwg.rect(insert=(48, 84), size=(1004, 28), fill="#0d1324"))

for x, color in [(80, "#ef4444"), (108, "#f59e0b"), (136, "#22c55e")]:
    dwg.add(dwg.circle(center=(x, 77), r=8, fill=color))

dwg.add(
    dwg.text(
        "$ developer.stats",
        insert=(188, 86),
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


card_positions = [
    (74, 138, 470, 126),
    (556, 138, 470, 126),
    (74, 286, 470, 126),
    (556, 286, 470, 126),
]

for card_data, (x, y, width, height) in zip(cards, card_positions):
    accent = card_data["accent"]
    dwg.add(
        dwg.rect(
            insert=(x, y),
            size=(width, height),
            rx=18,
            fill="url(#card)",
            stroke="#1f2a44",
            stroke_width=1.2,
        )
    )
    dwg.add(
        dwg.rect(
            insert=(x + 18, y + 18),
            size=(6, height - 36),
            rx=3,
            fill=accent,
            filter="url(#glow)",
            opacity=0.95,
        )
    )
    dwg.add(
        dwg.text(
            card_data["title"],
            insert=(x + 40, y + 42),
            fill=accent,
            font_size="18",
            font_family="monospace",
            font_weight="700",
        )
    )
    dwg.add(
        dwg.text(
            card_data["body"],
            insert=(x + 40, y + 78),
            fill="#e5e7eb",
            font_size="22",
            font_family="monospace",
            font_weight="700",
        )
    )


dwg.add(
    dwg.text(
        "> Building AI systems that feel sharp, useful, and ready for production",
        insert=(74, 454),
        fill="#cbd5e1",
        font_size="15",
        font_family="monospace",
    )
)

dwg.save()

print("Created:", output)