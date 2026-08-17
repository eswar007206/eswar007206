"""Generate rounded glass-style product cards for GitHub README."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

assets = Path(__file__).resolve().parent.parent / "assets"
cards_dir = assets / "cards"
cards_dir.mkdir(exist_ok=True)

# Card palette — soft gradients per product
PRODUCTS = [
    ("edutrack-clean.png", "edutrack-card.png", (37, 99, 235), (59, 130, 246)),
    ("eduxam-clean.png", "eduxam-card.png", (29, 78, 216), (96, 165, 250)),
    ("abhyas-clean.png", "abhyas-card.png", (30, 64, 175), (59, 130, 246)),
    ("gamibar-clean.png", "gamibar-card.png", (220, 38, 38), (248, 113, 113)),
]

CLIENTS = [
    ("physioflex-clean.png", "physioflex-card.png", (15, 23, 42), (51, 65, 85)),
    ("corpergo-clean.png", "corpergo-card.png", (13, 148, 136), (45, 212, 191)),
    ("singularis-clean.png", "singularis-card.png", (30, 41, 59), (71, 85, 105)),
    ("apitherapy-clean.png", "apitherapy-card.png", (234, 88, 12), (251, 146, 60)),
    ("swarn-madhu-clean.png", "swarn-madhu-card.png", (180, 83, 9), (245, 158, 11)),
    ("srivani-clean.png", "srivani-card.png", (124, 58, 237), (167, 139, 250)),
    ("retirement-clean.png", "retirement-card.png", (5, 150, 105), (52, 211, 153)),
]


def gradient_card(
    logo_name: str,
    out_name: str,
    color_top: tuple,
    color_bottom: tuple,
    width: int = 420,
    height: int = 200,
    radius: int = 28,
) -> None:
    logo_path = assets / logo_name
    if not logo_path.exists():
        print(f"SKIP {logo_name}")
        return

    # Gradient background
    card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    for y in range(height):
        t = y / height
        r = int(color_top[0] + (color_bottom[0] - color_top[0]) * t)
        g = int(color_top[1] + (color_bottom[1] - color_top[1]) * t)
        b = int(color_top[2] + (color_bottom[2] - color_top[2]) * t)
        for x in range(width):
            card.putpixel((x, y), (r, g, b, 255))

    # Rounded mask
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
    card.putalpha(mask)

    # Subtle inner glow
    glow = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.rounded_rectangle(
        [4, 4, width - 4, height - 4], radius=radius - 2, outline=(255, 255, 255, 40), width=2
    )
    card = Image.alpha_composite(card, glow)

    # Place logo centered
    logo = Image.open(logo_path).convert("RGBA")
    lw, lh = logo.size
    max_logo_w = width - 80
    max_logo_h = height - 60
    scale = min(max_logo_w / lw, max_logo_h / lh, 1.0)
    logo = logo.resize((int(lw * scale), int(lh * scale)), Image.Resampling.LANCZOS)
    lx = (width - logo.width) // 2
    ly = (height - logo.height) // 2
    card.paste(logo, (lx, ly), logo)

    out_path = cards_dir / out_name
    card.save(out_path, optimize=True)
    print(f"card: {out_path.name}")


def gcu_card() -> None:
  gcu = assets / "gcu-rounded.png"
  if not gcu.exists():
    return
  gradient_card("gcu-rounded.png", "gcu-card.png", (127, 29, 29), (185, 28, 28), width=200, height=120, radius=20)
  # gcu-rounded is in assets not clean - fix path
  logo = Image.open(gcu).convert("RGBA")
  width, height, radius = 200, 120, 20
  card = Image.new("RGBA", (width, height), (0, 0, 0, 0))
  for y in range(height):
    t = y / height
    r = int(127 + (185 - 127) * t)
    g = int(29 + (28 - 29) * t)
    b = int(29 + (28 - 29) * t)
    for x in range(width):
      card.putpixel((x, y), (r, g, b, 255))
  mask = Image.new("L", (width, height), 0)
  draw = ImageDraw.Draw(mask)
  draw.rounded_rectangle([0, 0, width, height], radius=radius, fill=255)
  card.putalpha(mask)
  lw, lh = logo.size
  scale = min((width - 40) / lw, (height - 30) / lh)
  logo = logo.resize((int(lw * scale), int(lh * scale)), Image.Resampling.LANCZOS)
  card.paste(logo, ((width - logo.width) // 2, (height - logo.height) // 2), logo)
  card.save(cards_dir / "gcu-card.png")
  print("card: gcu-card.png")


if __name__ == "__main__":
    for args in PRODUCTS:
        gradient_card(*args)
    for args in CLIENTS:
        gradient_card(*args, width=280, height=140, radius=22)
    gcu_card()
