import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

f = EN_DIR / "user-guide.html"
text = f.read_text(encoding="utf-8")

kw = [
    r'\bpara pymes\b', r'\bherramientas gratuitas\b', r'\bdescargar\b', r'\bguardar\b',
    r'\blimpiar\b', r'\bselecciona\b', r'\bseleccionar\b', r'\belige\b', r'\bejecuta\b',
    r'\bcalcula\b', r'\bcalcular\b', r'\bintroduc[ea]\b', r'\bcompara\b', r'\bcomparar\b',
    r'\bempresa\b', r'\bcliente\b', r'\bproveedor\b', r'\bfecha\b', r'\bmoneda\b',
    r'\bdescuento\b', r'\bprecio\b', r'\bganancia\b', r'\bcosto\b', r'\bimpuesto\b',
    r'\bsobrecostos\b', r'\bprestamo\b', r'\bpréstamo\b', r'\bamortizacion\b', r'\bamortización\b',
    r'\bcontrasenas\b', r'\bcontraseñas\b', r'\bpolitica\b', r'\bpolítica\b', r'\bdevolucion\b', r'\bdevolución\b',
    r'\bterminos\b', r'\btérminos\b', r'\bobjecion\b', r'\bobjeción\b', r'\bguiones\b',
    r'\bmatriz\b', r'\bcontenido\b', r'\bproforma\b', r'\bcotizacion\b', r'\bcotización\b',
    r'\bfirma de correo\b', r'\bcodigos qr\b', r'\bcódigos qr\b', r'\bpaletas\b',
    r'\bflujo de caja\b', r'\binventario\b', r'\btareas y proyectos\b',
    r'\bvolver al\b', r'\bportal de\b', r'\btodos los\b', r'\btodas las\b'
]
pat = re.compile('|'.join(kw), re.IGNORECASE)

lines = text.splitlines()
matches = []
for idx, l in enumerate(lines, 1):
    m = pat.search(l)
    if m:
        matches.append((idx, m.group(0), l.strip()[:110]))

print(f"Total matches in user-guide.html: {len(matches)}")
for idx, word, line in matches[:25]:
    print(f"{idx}: [{word}] {line}")
