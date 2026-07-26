from pathlib import Path


OUTPUT = Path("assets/sysinfo.svg")


ROWS = [
        ("experience", "Software Engineer @ Synapx"),
        ("current focus", "Building AI-powered applications"),
        ("learning", "AI Agents | RAG Systems | Cloud Architecture"),
        ("tech focus", "Python | LLMs | Automation"),
]


def escape(text: str) -> str:
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_svg() -> str:
        width = 980
        height = 400
        panel_x = 24
        panel_y = 24
        panel_w = width - 48
        panel_h = height - 48
        start_y = 138
        row_gap = 56
        line_width = 680

        clips = []
        lines = []
        for index, (label, value) in enumerate(ROWS):
                y = start_y + index * row_gap
                delay = 0.45 + index * 0.62
                clip_id = f"line-{index}"
                clips.append(
                        f'<clipPath id="{clip_id}"><rect x="0" y="{y - 20}" width="0" height="34">'
                        f'<animate attributeName="width" from="0" to="{line_width}" dur="1.05s" begin="{delay:.2f}s" fill="freeze" />'
                        f'</rect></clipPath>'
                )
                lines.append(
                        f'<g clip-path="url(#{clip_id})">'
                        f'<text x="64" y="{y}" font-family="monospace" font-size="16" fill="#6ee7b7">{escape(label)}:</text>'
                        f'<text x="250" y="{y}" font-family="monospace" font-size="20" font-weight="700" fill="#f8fafc">{escape(value)}</text>'
                        f'<rect x="{248 + len(value) * 12}" y="{y - 16}" width="10" height="22" rx="2" fill="#2ee59d" opacity="0.95" />'
                        f'</g>'
                )

        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated system information panel">
    <style>
        <![CDATA[
            .blink {{ animation: blink 1s steps(1, end) infinite; }}
            .panel-glow {{ animation: pulse 3.5s ease-in-out infinite; }}
            .typebar {{ animation: sweep 5.5s linear infinite; }}
            @keyframes blink {{
                0%, 49% {{ opacity: 1; }}
                50%, 100% {{ opacity: 0; }}
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 0.28; }}
                50% {{ opacity: 0.58; }}
            }}
            @keyframes sweep {{
                0% {{ transform: translateX(-18px); }}
                100% {{ transform: translateX({panel_w + 18}px); }}
            }}
        ]]>
    </style>
    <defs>
        <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#050816" />
            <stop offset="100%" stop-color="#0b1220" />
        </linearGradient>
        <linearGradient id="frame" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#132033" />
            <stop offset="100%" stop-color="#0a111c" />
        </linearGradient>
        <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#2ee59d" />
            <stop offset="100%" stop-color="#7dd3fc" />
        </linearGradient>
        <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
            <path d="M 36 0 L 0 0 0 36" fill="none" stroke="#17263a" stroke-width="1" opacity="0.7" />
        </pattern>
        {''.join(clips)}
    </defs>

    <rect width="{width}" height="{height}" rx="24" fill="url(#bg)" />
    <rect width="{width}" height="{height}" rx="24" fill="url(#grid)" opacity="0.25" />
    <circle cx="842" cy="60" r="156" fill="#14b8a6" opacity="0.08" />
    <circle cx="120" cy="336" r="176" fill="#7c3aed" opacity="0.07" />

    <rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" rx="22" fill="url(#frame)" stroke="#22314f" stroke-width="1.2" />
    <rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="72" rx="22" fill="#0d1324" />
    <rect x="{panel_x}" y="{panel_y + 42}" width="{panel_w}" height="30" fill="#0d1324" />

    <circle cx="58" cy="62" r="8" fill="#ef4444" />
    <circle cx="86" cy="62" r="8" fill="#f59e0b" />
    <circle cx="114" cy="62" r="8" fill="#22c55e" />

    <text x="160" y="66" font-family="monospace" font-size="28" font-weight="700" fill="#2ee59d">$ system.info</text>
    <text x="160" y="86" font-family="monospace" font-size="14" fill="#94a3b8">typewriter-driven snapshot of the local engineering stack</text>
    <text x="{width - 162}" y="66" font-family="monospace" font-size="10" fill="#5f7f6e">live.panel</text>

    <rect x="64" y="118" width="{line_width}" height="1" fill="url(#accent)" opacity="0.16" />
    <rect x="64" y="118" width="100" height="1" fill="#2ee59d" opacity="0.65" class="typebar" />

    {''.join(lines)}

    <rect x="64" y="{height - 72}" width="{panel_w - 128}" height="1" fill="#1f3a2d" opacity="0.7" />
    <text x="64" y="{height - 48}" font-family="monospace" font-size="12" fill="#8fffb7">$ echo "shipping AI systems with clarity, speed, and production discipline"</text>
    <rect x="{width - 104}" y="{height - 58}" width="10" height="16" rx="2" fill="#8fffb7" class="blink" />
    <rect x="64" y="{height - 18}" width="{panel_w - 128}" height="2" fill="#2ee59d" opacity="0.45">
        <animate attributeName="opacity" values="0.2;0.8;0.2" dur="2.2s" repeatCount="indefinite" />
    </rect>
    <rect x="{panel_x + 18}" y="{panel_y + 18}" width="{panel_w - 36}" height="{panel_h - 36}" rx="18" fill="#ffffff" opacity="0.02" class="panel-glow" />
</svg>
'''


def main() -> None:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(build_svg(), encoding="utf-8")
        print(f"Created: {OUTPUT}")


if __name__ == "__main__":
        main()