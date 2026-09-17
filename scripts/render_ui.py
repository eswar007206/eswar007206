"""Render portfolio-matching UI sections for the GitHub README."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
HTML = Path(__file__).resolve().parent / "readme_ui.html"
OUT = ROOT / "assets" / "ui"
OUT.mkdir(parents=True, exist_ok=True)

SECTIONS = [
    ("hero", "hero.png"),
    ("tech", "tech.png"),
    ("experience", "experience.png"),
    ("projects", "projects.png"),
    ("awards", "awards.png"),
]


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1064, "height": 800}, device_scale_factor=2)
        page.goto(HTML.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(400)
        for section_id, filename in SECTIONS:
            loc = page.locator(f"#{section_id}")
            loc.screenshot(path=str(OUT / filename), type="png")
            print("wrote", filename)
        browser.close()


if __name__ == "__main__":
    main()
