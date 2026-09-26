import re
from pathlib import Path
from collections import defaultdict

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

# Only inspect unique 26 tools (original slug)
files = [
    "analizador-titulares.html",
    "auditor-seo-basico.html",
    "calculadora-descuentos-promociones.html",
    "calculadora-flete-envio-local.html",
    "calculadora-precios-venta-igv.html",
    "calculadora-prestamos-amortizaciones.html",
    "calculadora-sobrecostos-laborales.html",
    "comparador-campanas-avanzado.html",
    "consola-campanas.html",
    "conversor-optimizador-imagenes.html",
    "creador-facturas-proforma.html",
    "crm-pymes.html",
    "firma-correo-html.html",
    "flujo-caja-pymes.html",
    "generador-codigos-qr.html",
    "generador-contrasenas-pymes.html",
    "generador-contratos-servicios.html",
    "generador-cotizaciones.html",
    "generador-paletas-corporativas.html",
    "generador-politicas-devolucion.html",
    "generador-politicas-terminos.html",
    "guiones-manejo-objeciones.html",
    "inventario-compras-pymes.html",
    "organizador-matriz-contenidos.html",
    "simulador-tco-fisico-nube.html",
    "tareas-proyectos-pymes.html"
]

all_matches = defaultdict(list)
for fname in files:
    fpath = EN_DIR / fname
    if not fpath.exists():
        continue
    text = fpath.read_text(encoding="utf-8")
    for idx, line in enumerate(text.splitlines(), 1):
        m = pat.search(line)
        if m:
            all_matches[fname].append((idx, m.group(0), line.strip()))

for fname in sorted(all_matches.keys(), key=lambda k: -len(all_matches[k])):
    items = all_matches[fname]
    print(f"=== {fname} ({len(items)} matches) ===")
    for idx, w, l in items[:8]:
        # truncate line
        clean_l = re.sub(r'<[^>]+>', ' ', l)
        clean_l = ' '.join(clean_l.split())[:90]
        print(f"  [{idx}] ({w}): {clean_l}")
    print()
