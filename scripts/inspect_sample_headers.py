from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

sample_tools = [
    "analizador-titulares.html",
    "creador-facturas-proforma.html",
    "crm-pymes.html",
    "calculadora-descuentos-promociones.html"
]

for t in sample_tools:
    p = EN_DIR / t
    content = p.read_text(encoding="utf-8", errors="ignore")
    # find header or nav
    m = re.search(r'(<header.*?</header>|<nav.*?</nav>)', content, flags=re.DOTALL)
    print(f"=== {t} ===")
    if m:
        print(m.group(0)[:300])
    else:
        # print first 30 lines
        lines = content.splitlines()[:30]
        print("\n".join(lines[:15]))
    print()
