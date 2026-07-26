from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image


OUTPUT = Path("assets/portrait.svg")
AVATAR_URL = "https://avatars.githubusercontent.com/u/173434739?v=4"
WIDTH = 42
FONT_SIZE = 11
LINE_HEIGHT = 13
MARGIN_X = 24
MARGIN_Y = 34
BG = "#0b1117"
FG = "#8bffb0"
ACCENT = "#2ee59d"
PALETTE = "@%#*+=-:. "


def fetch_avatar(url: str) -> Image.Image:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(request, timeout=20) as response:
        data = response.read()
    return Image.open(BytesIO(data)).convert("L")


def crop_square(image: Image.Image) -> Image.Image:
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def remap_tone(value: int) -> int:
    normalized = value / 255.0
    normalized = max(0.0, min(1.0, (normalized - 0.06) * 1.14))
    normalized = normalized ** 0.82
    return int(normalized * 255)


def build_ascii_lines(image: Image.Image) -> list[str]:
    image = crop_square(image)
    image = image.resize((WIDTH, WIDTH), Image.Resampling.LANCZOS)
    pixels = image.tobytes()
    lines: list[str] = []

    for row in range(WIDTH):
        chars = []
        for col in range(WIDTH):
            value = remap_tone(pixels[row * WIDTH + col])
            index = int((255 - value) / 256 * len(PALETTE))
            index = min(len(PALETTE) - 1, index)
            chars.append(PALETTE[index])
        lines.append("".join(chars).rstrip())

    return lines


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(lines: list[str]) -> str:
    width = 42 * 8 + 48
    height = MARGIN_Y * 2 + len(lines) * LINE_HEIGHT + 32
    reveal_height = height - 18
    first_line_y = MARGIN_Y

    body_lines = []
    for index, line in enumerate(lines):
        y = first_line_y + index * LINE_HEIGHT
        delay = index * 0.035
        escaped_line = svg_escape(line or " ")
        body_lines.append(
            f'<text x="{MARGIN_X}" y="{y}" opacity="0" '
            f'font-family="monospace" font-size="{FONT_SIZE}" '
            f'fill="{FG}" xml:space="preserve">'
            f'{escaped_line}'
            f'<animate attributeName="opacity" from="0" to="1" dur="0.01s" '
            f'begin="{delay:.3f}s" fill="freeze" />'
            f'</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="Animated ASCII portrait">
  <defs>
    <linearGradient id="frame" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#14311f" />
      <stop offset="50%" stop-color="#0f1d16" />
      <stop offset="100%" stop-color="#081015" />
    </linearGradient>
    <radialGradient id="glow" cx="50%" cy="35%" r="70%">
      <stop offset="0%" stop-color="#2ee59d" stop-opacity="0.22" />
      <stop offset="100%" stop-color="#2ee59d" stop-opacity="0" />
    </radialGradient>
    <clipPath id="reveal">
      <rect x="18" y="18" width="{width - 36}" height="0">
        <animate attributeName="height" from="0" to="{reveal_height}" dur="2.6s" begin="0s" fill="freeze" />
      </rect>
    </clipPath>
    <pattern id="scanlines" width="100%" height="6" patternUnits="userSpaceOnUse">
      <rect width="100%" height="1" fill="#ffffff" opacity="0.05" />
    </pattern>
  </defs>

  <rect width="{width}" height="{height}" rx="18" fill="#03060a" />
  <rect x="7" y="7" width="{width - 14}" height="{height - 14}" rx="14" fill="url(#frame)" opacity="0.92" />
  <rect x="14" y="14" width="{width - 28}" height="{height - 28}" rx="10" fill="{BG}" stroke="#1f3a2d" stroke-width="1.2" />
  <rect x="14" y="14" width="{width - 28}" height="{height - 28}" rx="10" fill="url(#glow)" opacity="0.8" />

  <circle cx="32" cy="28" r="5" fill="#ff5f57" />
  <circle cx="48" cy="28" r="5" fill="#febc2e" />
  <circle cx="64" cy="28" r="5" fill="#28c840" />

  <text x="88" y="33" font-family="monospace" font-size="14" fill="#8fffb7">$ whoami</text>
  <text x="{width - 126}" y="33" font-family="monospace" font-size="10" fill="#5f7f6e">portrait.online</text>
  <g clip-path="url(#reveal)">
    {''.join(body_lines)}
  </g>

  <rect x="18" y="36" width="{width - 36}" height="{height - 54}" rx="8" fill="url(#scanlines)" opacity="0.42" />

  <rect x="18" y="{height - 18}" width="{width - 36}" height="2" fill="{ACCENT}" opacity="0.55">
    <animate attributeName="opacity" values="0.25;0.8;0.25" dur="2.2s" repeatCount="indefinite" />
  </rect>
</svg>
'''


def main() -> None:
    avatar = fetch_avatar(AVATAR_URL)
    lines = build_ascii_lines(avatar)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(lines), encoding="utf-8")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()