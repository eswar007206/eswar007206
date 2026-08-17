"""Process logo assets: remove backgrounds and create rounded variants."""
from pathlib import Path
from PIL import Image, ImageDraw
import rembg

assets = Path(__file__).resolve().parent.parent / "assets"

TO_REMOVE_BG = [
    "edutrack.png", "eduxam.png", "gamibar.png", "abhyas.png",
    "physioflex.png", "corpergo.png", "singularis.png", "apitherapy.png",
    "swarn-madhu.png", "srivani.png", "retirement.png",
    "northnode-logo.png", "northnode-card.png", "gcu-incubation.png",
]


def remove_background(name: str) -> None:
    path = assets / name
    if not path.exists():
        print(f"SKIP missing: {name}")
        return
    with open(path, "rb") as f:
        result = rembg.remove(f.read())
    out = assets / name.replace(".png", "-transparent.png")
    with open(out, "wb") as f:
        f.write(result)
    print(f"transparent: {out.name}")


def round_corners(name: str, out_name: str, radius_ratio: float = 6) -> None:
    path = assets / name
    if not path.exists():
        return
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    radius = min(w, h) // radius_ratio
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, w, h], radius=radius, fill=255)
    img.putalpha(mask)
    img.save(assets / out_name)
    print(f"rounded: {out_name}")


def pad_logo(name: str, out_name: str, padding: int = 24, max_height: int = 100) -> None:
    """Scale logo to max_height and add transparent padding for card placement."""
    path = assets / name
    if not path.exists():
        return
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    scale = max_height / h
    new_w, new_h = int(w * scale), int(h * scale)
    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    out = Image.new("RGBA", (new_w + padding * 2, new_h + padding * 2), (0, 0, 0, 0))
    out.paste(img, (padding, padding), img)
    out.save(assets / out_name)
    print(f"padded: {out_name}")


if __name__ == "__main__":
    for name in TO_REMOVE_BG:
        remove_background(name)

    round_corners("gcu.png", "gcu-rounded.png")

    transparent_logos = [n.replace(".png", "-transparent.png") for n in TO_REMOVE_BG]
    for tname in transparent_logos:
        pad_logo(tname, tname.replace("-transparent.png", "-clean.png"), padding=16, max_height=90)
