import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# Check the unique tool files
tools = [
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

results = {}
for t in tools:
    fpath = EN_DIR / t
    if not fpath.exists():
        continue
    content = fpath.read_text(encoding="utf-8", errors="ignore")
    # Find text inside tags: >Some Text<
    # Exclude script and style tags
    clean = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    clean = re.sub(r'<style.*?</style>', '', clean, flags=re.DOTALL | re.IGNORECASE)
    
    # Extract visible texts
    tags = re.findall(r'>([^<]{3,})<', clean)
    spanish_snippets = []
    for snippet in tags:
        s = snippet.strip()
        if not s or s.startswith('&') or s.isdigit() or len(s) < 3:
            continue
        # Check if contains spanish words / accents
        if re.search(r'[áéíóúñ¿¡]', s, re.IGNORECASE) or any(w in s.lower().split() for w in ['de', 'la', 'el', 'en', 'para', 'con', 'por', 'los', 'las', 'del', 'una', 'un', 'guardar', 'descargar', 'precio', 'costo', 'calcular', 'cotizacion', 'cliente']):
            spanish_snippets.append(s)
            
    # Also check placeholders and titles
    attrs = re.findall(r'(?:placeholder|title|aria-label)="([^"]+)"', clean)
    for a in attrs:
        a_str = a.strip()
        if re.search(r'[áéíóúñ¿¡]', a_str, re.IGNORECASE) or any(w in a_str.lower().split() for w in ['de', 'la', 'el', 'en', 'para', 'con', 'por', 'los', 'las', 'del', 'una', 'un', 'guardar', 'descargar', 'precio', 'costo', 'calcular', 'cotizacion', 'cliente']):
            spanish_snippets.append(f"[ATTR] {a_str}")

    results[t] = spanish_snippets

out_file = ROOT / "scripts" / "tool_spanish_scan_output.txt"
with open(out_file, "w", encoding="utf-8") as out:
    for t, snippets in results.items():
        out.write(f"=== {t} ({len(snippets)} snippets) ===\n")
        for s in snippets[:30]:
            out.write(f"  - {s}\n")
        out.write("\n")

print(f"Scan complete. Output written to {out_file}")
