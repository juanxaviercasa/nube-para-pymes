import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

f = EN_DIR / "guiones-manejo-objeciones.html"
text = f.read_text(encoding="utf-8")
clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)

kw = [r'\bcliente\b', r'\bcosto\b', r'\bproveedor\b', r'\bobjecion\b', r'\bobjeción\b']
pat = re.compile('|'.join(kw), re.IGNORECASE)

for idx, line in enumerate(clean.splitlines(), 1):
    m = pat.search(line)
    if m:
        clean_l = re.sub(r'<[^>]+>', ' ', line)
        clean_l = ' '.join(clean_l.split())[:110]
        print(f"{idx}: [{m.group(0)}] {clean_l}")
