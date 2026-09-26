from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

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

patterns = {}
for t in tools:
    p = ROOT / t
    content = p.read_text(encoding="utf-8", errors="ignore")
    # find links to index.html or back links
    back_links = re.findall(r'<a[^>]*href=["\'][^"\']*index\.html["\'][^>]*>.*?</a>', content, flags=re.DOTALL)
    patterns[t] = back_links[:1]

out_file = ROOT / "scripts" / "tool_nav_patterns.txt"
with open(out_file, "w", encoding="utf-8") as out:
    for t, bl in patterns.items():
        out.write(f"=== {t} ===\n")
        for b in bl:
            out.write(f"  {b.strip()}\n")
        out.write("\n")

print(f"Tool nav patterns written to {out_file}")
