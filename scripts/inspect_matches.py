import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

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

for target in ["user-guide.html", "creador-facturas-proforma.html", "calculadora-descuentos-promociones.html"]:
    f = EN_DIR / target
    if not f.exists():
        continue
    text = f.read_text(encoding="utf-8")
    lines = text.splitlines()
    print(f"=== {target} ===")
    for idx, l in enumerate(lines, 1):
        m = pat.search(l)
        if m:
            clean_l = re.sub(r'<[^>]+>', ' ', l)
            clean_l = ' '.join(clean_l.split())[:100]
            print(f"  [{idx}] ({m.group(0)}): {clean_l}")
    print()
