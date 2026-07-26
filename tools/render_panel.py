import svgwrite


output = "assets/sysinfo.svg"


rows = [
    ("role", "AI Engineer"),
    ("focus", "LLMs | Agents | RAG"),
    ("stack", "Python | TypeScript | React"),
    ("runtime", "FastAPI | Docker | Linux"),
    ("ops", "Tracing | Eval | GitHub Actions"),
    ("location", "Bengaluru, India")
]


dwg = svgwrite.Drawing(
    output,
    size=("600", "350")
)


# Background

dwg.add(
    dwg.rect(
        insert=(0,0),
        size=("600","350"),
        rx=15,
        fill="#0d1117"
    )
)


# Terminal header

dwg.add(
    dwg.text(
        "$ system.info",
        insert=(30,45),
        fill="#00ff99",
        font_size="26",
        font_family="monospace"
    )
)


# Terminal dots

for x,color in [(25,"red"),(45,"yellow"),(65,"green")]:
    dwg.add(
        dwg.circle(
            center=(x,25),
            r=7,
            fill=color
        )
    )


# Information rows

y = 95


for key,value in rows:

    dwg.add(
        dwg.text(
            f"{key:<10}: {value}",
            insert=(30,y),
            fill="white",
            font_size="18",
            font_family="monospace"
        )
    )

    y += 38



dwg.save()

print("Created:", output)