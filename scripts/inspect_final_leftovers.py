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
    r'\bmatriz\b', r'\bcontenido\b', r'\bcotizacion\b', r'\bcotización\b',
    r'\bfirma de correo\b', r'\bcodigos qr\b', r'\bcódigos qr\b', r'\bpaletas\b',
    r'\bflujo de caja\b', r'\binventario\b', r'\btareas y proyectos\b',
    r'\bvolver al\b', r'\bportal de\b', r'\btodos los\b', r'\btodas las\b'
]
pat = re.compile('|'.join(kw), re.IGNORECASE)

files_to_check = [
    "calculadora-descuentos-promociones.html",
    "generador-paletas-corporativas.html",
    "guiones-manejo-objeciones.html",
    "generador-cotizaciones.html",
    "auditor-seo-basico.html",
    "simulador-tco-fisico-nube.html",
    "firma-correo-html.html",
    "generador-politicas-terminos.html",
    "comparador-campanas-avanzado.html",
    "consola-campanas.html",
    "flujo-caja-pymes.html"
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
        # find in tag text
        tags = re.findall(r'>([^<]+)<', line)
        for t in tags:
            m = pat.search(t)
            if m:
                print(f"  [L{idx}] TAG: '{t.strip()}' (matched {m.group(0)})")
        # find in attrs
        attrs = re.findall(r'(?:placeholder|title|aria-label)="([^"]+)"', line)
        for a in attrs:
            m = pat.search(a)
            if m:
                print(f"  [L{idx}] ATTR: '{a.strip()}' (matched {m.group(0)})")
    print()
