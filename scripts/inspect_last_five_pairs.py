import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

kw = [r'\bFecha\b', r'\bEmpresa\b', r'\bPaletas\b', r'\bdescargar\b', r'\bCompara\b', r'\bcliente\b', r'\bT[eé\ufffd]rminos\b']
pat = re.compile('|'.join(kw), re.IGNORECASE)

files = [
    "generador-cotizaciones.html",
    "brand-palette-generator.html",
    "advanced-campaign-comparator.html",
    "firma-correo-html.html",
    "generador-politicas-terminos.html"
]

for fname in files:
    content = (EN_DIR / fname).read_text(encoding="utf-8", errors="ignore")
    clean = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    print(f"=== {fname} ===")
    for idx, line in enumerate(clean.splitlines(), 1):
        m = pat.search(line)
        if m:
            clean_l = re.sub(r'<[^>]+>', ' ', line)
            clean_l = ' '.join(clean_l.split())[:120]
            print(f"  [L{idx}] [{m.group(0)}]: {clean_l}")
    print()
