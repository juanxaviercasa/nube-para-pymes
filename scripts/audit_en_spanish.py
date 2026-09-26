import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# True Spanish indicators in visible text
SPANISH_KEYWORDS = [
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

pattern = re.compile('|'.join(SPANISH_KEYWORDS), re.IGNORECASE)

print(f"Auditing visible HTML content in {EN_DIR}...")
files = list(EN_DIR.glob("*.html"))
print(f"Found {len(files)} HTML files to check.")

findings = {}
details = {}
for f in sorted(files):
    text = f.read_text(encoding="utf-8", errors="ignore")
    # Strip <script> and <style>
    clean = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    
    # Strip tag attributes except placeholder and title
    # First extract visible text inside tags
    visible_texts = re.findall(r'>([^<]+)<', clean)
    # Also extract placeholder and title
    attrs = re.findall(r'(?:placeholder|title|aria-label)="([^"]+)"', clean)
    
    all_visible = " ".join(visible_texts + attrs)
    
    matches = pattern.findall(all_visible)
    if matches:
        findings[f.name] = len(matches)
        details[f.name] = matches[:10]

print(f"\nFiles with detected Spanish keywords in visible text: {len(findings)}/{len(files)}")
for fname, count in sorted(findings.items(), key=lambda x: -x[1])[:20]:
    print(f"  {fname}: {count} occurrences -> {details[fname]}")

if not findings:
    print("\nSUCCESS: 0 files contain untranslated Spanish in visible text!")
