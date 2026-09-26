import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

kw = [
    r'\bFecha\b', r'\bEmpresa\b', r'\bPaletas\b', r'\bdescargar\b',
    r'\bCompara\b', r'\bCosto\b', r'\bempresa\b', r'\bcliente\b',
    r'\bt[eé\ufffd]rminos\b'
]
pat = re.compile('|'.join(kw), re.IGNORECASE)

files_to_check = [
    "generador-cotizaciones.html",
    "brand-palette-generator.html",
    "advanced-campaign-comparator.html",
    "cloud-vs-onprem-tco-simulator.html",
    "creador-facturas-proforma.html",
    "firma-correo-html.html",
    "generador-contratos-servicios.html",
    "generador-politicas-terminos.html",
    "inventario-compras-pymes.html",
    "tareas-proyectos-pymes.html"
]

for fname in files_to_check:
    fpath = EN_DIR / fname
    if not fpath.exists():
        continue
    content = fpath.read_text(encoding="utf-8", errors="ignore")
    clean = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    
    print(f"=== {fname} ===")
    for idx, line in enumerate(clean.splitlines(), 1):
        tags = re.findall(r'>([^<]+)<', line)
        for t in tags:
            m = pat.search(t)
            if m:
                print(f"  [L{idx}] TAG: '{t.strip()}' (matched {m.group(0)})")
        attrs = re.findall(r'(?:placeholder|title|aria-label)="([^"]+)"', line)
        for a in attrs:
            m = pat.search(a)
            if m:
                print(f"  [L{idx}] ATTR: '{a.strip()}' (matched {m.group(0)})")
    print()
