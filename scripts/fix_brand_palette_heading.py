from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

for name in ["generador-paletas-corporativas.html", "brand-palette-generator.html"]:
    f = EN_DIR / name
    c = f.read_text(encoding="utf-8")
    c = c.replace(
        'Paletas que definen <span class="text-brand-500">marcas</span>, no solo pantallas.',
        'Color palettes that define <span class="text-brand-500">brands</span>, not just screens.'
    )
    c = c.replace('Empieza abajo', 'Get Started Below')
    f.write_text(c, encoding="utf-8")

print("Fixed brand palette heading!")
