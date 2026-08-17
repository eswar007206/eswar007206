"""Restore full README with social icons and original logos."""
from pathlib import Path
import re

root = Path(__file__).resolve().parent.parent
src = (root / "README.old.txt").read_text(encoding="utf-8", errors="replace")

fixes = {
    "ΓÇö": "—", "ΓÇô": "–", "┬╖": "·", "ΓåÆ": "→",
    "≡ƒÅó": "🏢", "≡ƒº⌐": "🧩", "≡ƒºá": "🧠", "≡ƒÄô": "🎓",
    "≡ƒôì": "📍", "≡ƒôº": "📧", "≡ƒîÉ": "🌐", "≡ƒîì": "🌍",
    "≡ƒº¡": "🧭", "ΓÜÖ∩╕Å": "⚙️",
}
for k, v in fixes.items():
    src = src.replace(k, v)

src = re.sub(
    r'<p align="center">\s*<img src="\./assets/hero-banner\.webp".*?</p>',
    '<p align="center">\n  <img src="./assets/header-card.webp" alt="Eswar N — NorthNode" width="100%"/>\n</p>',
    src,
    count=1,
    flags=re.S,
)

src = src.replace("./assets/northnode-card-hero.webp", "./assets/northnode-card.png")
src = src.replace('width="340"', 'width="280"')

for card, png in [
    ("cards/edutrack-card.webp", "edutrack.png"),
    ("cards/eduxam-card.webp", "eduxam.png"),
    ("cards/abhyas-card.webp", "abhyas.png"),
    ("cards/gamibar-card.webp", "gamibar.png"),
    ("cards/physioflex-card.webp", "physioflex.png"),
    ("cards/corpergo-card.webp", "corpergo.png"),
    ("cards/singularis-card.webp", "singularis.png"),
    ("cards/apitherapy-card.webp", "apitherapy.png"),
    ("cards/swarn-madhu-card.webp", "swarn-madhu.png"),
    ("cards/srivani-card.webp", "srivani.png"),
    ("cards/retirement-card.webp", "retirement.png"),
    ("cards/gcu-card.webp", "gcu.png"),
    ("cards/gcu-incubation-card.webp", "gcu-incubation.png"),
]:
    src = src.replace(f"./assets/{card}", f"./assets/{png}")

src = src.replace('width="96%"', 'height="92"')
src = src.replace('width="95%"', 'height="78"')

social_top = """
<p align="center">
  <img src="https://img.shields.io/badge/System_Design-Architect-0F172A?style=for-the-badge&labelColor=1D4ED8"/>
  <img src="https://img.shields.io/badge/Founder_%26_CEO-NorthNode-1D4ED8?style=for-the-badge&labelColor=0F172A"/>
  <img src="https://img.shields.io/badge/Lead-Developer-2563EB?style=for-the-badge&labelColor=0F172A"/>
</p>

<h3 align="center">Connect with me</h3>

<p align="center">
  <a href="https://northnode.live" target="_blank" title="Website"><img src="https://img.icons8.com/color/48/domain.png" alt="Website" height="42" width="42"/></a>
  &nbsp;
  <a href="https://github.com/eswar007206" target="_blank" title="GitHub"><img src="https://img.icons8.com/color/48/github--v1.png" alt="GitHub" height="42" width="42"/></a>
  &nbsp;
  <a href="https://github.com/NorthNodeTech" target="_blank" title="NorthNode GitHub"><img src="https://img.icons8.com/color/48/source-code.png" alt="NorthNode Org" height="42" width="42"/></a>
  &nbsp;
  <a href="https://www.linkedin.com/in/eswar-n/" target="_blank" title="LinkedIn"><img src="https://img.icons8.com/color/48/linkedin.png" alt="LinkedIn" height="42" width="42"/></a>
  &nbsp;
  <a href="https://www.instagram.com/eswar_sonu" target="_blank" title="Instagram Personal"><img src="https://img.icons8.com/color/48/instagram-new--v1.png" alt="Instagram" height="42" width="42"/></a>
  &nbsp;
  <a href="https://www.instagram.com/northnode.live/" target="_blank" title="Instagram NorthNode"><img src="https://img.icons8.com/color/48/instagram-new.png" alt="Instagram NorthNode" height="42" width="42"/></a>
  &nbsp;
  <a href="mailto:nalamalaeswar@gmail.com" title="Personal Email"><img src="https://img.icons8.com/color/48/gmail-new.png" alt="Personal Email" height="42" width="42"/></a>
  &nbsp;
  <a href="mailto:support@northnode.live" title="NorthNode Email"><img src="https://img.icons8.com/color/48/new-post.png" alt="NorthNode Email" height="42" width="42"/></a>
</p>
"""

pattern = (
    r'<p align="center">\s*<img src="https://readme-typing-svg.*?lines=Eswar\+N.*?</p>\s*'
    r'<p align="center">\s*<img src="https://img.shields.io/badge/System_Design.*?'
    r'mailto:support@northnode\.live.*?</p>\s*'
)
src = re.sub(pattern, social_top + "\n", src, count=1, flags=re.S)

social_footer = """
<p align="center">
  <a href="https://northnode.live" target="_blank"><img src="https://img.icons8.com/color/48/domain.png" height="40" width="40" alt="Website"/></a>
  &nbsp;
  <a href="https://github.com/eswar007206" target="_blank"><img src="https://img.icons8.com/color/48/github--v1.png" height="40" width="40" alt="GitHub"/></a>
  &nbsp;
  <a href="https://www.linkedin.com/in/eswar-n/" target="_blank"><img src="https://img.icons8.com/color/48/linkedin.png" height="40" width="40" alt="LinkedIn"/></a>
  &nbsp;
  <a href="https://www.instagram.com/eswar_sonu" target="_blank"><img src="https://img.icons8.com/color/48/instagram-new--v1.png" height="40" width="40" alt="Instagram"/></a>
  &nbsp;
  <a href="mailto:nalamalaeswar@gmail.com"><img src="https://img.icons8.com/color/48/gmail-new.png" height="40" width="40" alt="Email"/></a>
  &nbsp;
  <a href="mailto:support@northnode.live"><img src="https://img.icons8.com/color/48/new-post.png" height="40" width="40" alt="NorthNode Email"/></a>
  &nbsp;
  <a href="https://github.com/NorthNodeTech" target="_blank"><img src="https://img.icons8.com/color/48/source-code.png" height="40" width="40" alt="Org"/></a>
</p>
"""

footer_badges = (
    r'<p align="center">\s*<a href="https://northnode\.live">'
    r'<img src="https://img\.shields\.io/badge/Website.*?</p>'
)
src = re.sub(footer_badges, social_footer, src, count=1, flags=re.S)

(root / "README.md").write_text(src, encoding="utf-8")
print(f"Done — {len(src.splitlines())} lines")
