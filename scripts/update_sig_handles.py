from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

for name in ["firma-correo-html.html", "html-email-signature.html"]:
    f = EN_DIR / name
    if f.exists():
        t = f.read_text(encoding="utf-8")
        t = t.replace("anagarcia", "sarahjenkins")
        t = t.replace("novastudio", "acmestudio")
        f.write_text(t, encoding="utf-8")

print("Updated sample signature handles in en/ email signature!")
