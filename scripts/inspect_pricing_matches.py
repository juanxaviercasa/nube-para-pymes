import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

f = EN_DIR / "calculadora-precios-venta-igv.html"
text = f.read_text(encoding="utf-8")
clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)

kw = [r'\bprecio\b', r'\bcosto\b', r'\bimpuesto\b']
pat = re.compile('|'.join(kw), re.IGNORECASE)

for idx, line in enumerate(clean.splitlines(), 1):
    m = pat.search(line)
    if m:
        print(f"{idx}: [{m.group(0)}] {line.strip()[:100]}")
