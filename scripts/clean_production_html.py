from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# 1. Clean chrome-extension scripts across ALL html files
all_html = list(ROOT.glob("*.html")) + list(EN_DIR.glob("*.html"))
cleaned_ext_count = 0

for f in all_html:
    content = f.read_text(encoding="utf-8", errors="ignore")
    if "chrome-extension://" in content:
        # remove <script ...chrome-extension://...</script> or <script ...chrome-extension://...></script>
        cleaned = re.sub(r'<script[^>]*src=["\']chrome-extension://[^"\']+["\'][^>]*>.*?</script>\s*', '', content, flags=re.IGNORECASE | re.DOTALL)
        if cleaned != content:
            f.write_text(cleaned, encoding="utf-8")
            cleaned_ext_count += 1

print(f"Removed chrome-extension tags from {cleaned_ext_count} files.")

# 2. Fix root index.html card links: /herramientas/.../slug/ -> ./slug.html
index_file = ROOT / "index.html"
index_content = index_file.read_text(encoding="utf-8")

# Mapping from /herramientas/.../ to ./<slug>.html
TOOL_URL_MAP = {
    "/herramientas/marketing/analizador-titulares/": "./analizador-titulares.html",
    "/herramientas/marketing/auditor-seo-basico/": "./auditor-seo-basico.html",
    "/herramientas/finanzas/calculadora-descuentos-promociones/": "./calculadora-descuentos-promociones.html",
    "/herramientas/operaciones/calculadora-flete-envio-local/": "./calculadora-flete-envio-local.html",
    "/herramientas/finanzas/calculadora-precios-venta-igv/": "./calculadora-precios-venta-igv.html",
    "/herramientas/finanzas/calculadora-prestamos-amortizaciones/": "./calculadora-prestamos-amortizaciones.html",
    "/herramientas/finanzas/calculadora-sobrecostos-laborales/": "./calculadora-sobrecostos-laborales.html",
    "/herramientas/marketing/comparador-campanas-avanzado/": "./comparador-campanas-avanzado.html",
    "/herramientas/marketing/consola-campanas/": "./consola-campanas.html",
    "/herramientas/productividad/conversor-optimizador-imagenes/": "./conversor-optimizador-imagenes.html",
    "/herramientas/ventas/creador-facturas-proforma/": "./creador-facturas-proforma.html",
    "/herramientas/productividad/firma-correo-html/": "./firma-correo-html.html",
    "/herramientas/ventas/generador-codigos-qr/": "./generador-codigos-qr.html",
    "/herramientas/ventas/generador-contrasenas-pymes/": "./generador-contrasenas-pymes.html",
    "/herramientas/ventas/generador-contratos-servicios/": "./generador-contratos-servicios.html",
    "/herramientas/ventas/generador-cotizaciones/": "./generador-cotizaciones.html",
    "/herramientas/productividad/generador-paletas-corporativas/": "./generador-paletas-corporativas.html",
    "/herramientas/ventas/generador-politicas-devolucion/": "./generador-politicas-devolucion.html",
    "/herramientas/ventas/generador-politicas-terminos/": "./generador-politicas-terminos.html",
    "/herramientas/ventas/guiones-manejo-objeciones/": "./guiones-manejo-objeciones.html",
    "/herramientas/marketing/organizador-matriz-contenidos/": "./organizador-matriz-contenidos.html",
    "/herramientas/operaciones/simulador-tco-fisico-nube/": "./simulador-tco-fisico-nube.html",
    "/herramientas/productividad/tareas-proyectos-pymes/": "./tareas-proyectos-pymes.html",
    "/herramientas/operaciones/inventario-compras-pymes/": "./inventario-compras-pymes.html",
    "/herramientas/ventas/crm-pymes/": "./crm-pymes.html",
    "/herramientas/finanzas/flujo-caja-pymes/": "./flujo-caja-pymes.html"
}

fixed_links = 0
for old_href, new_href in TOOL_URL_MAP.items():
    if old_href in index_content:
        index_content = index_content.replace(old_href, new_href)
        fixed_links += 1

index_file.write_text(index_content, encoding="utf-8")
print(f"Fixed {fixed_links} card links in root index.html to point to standalone files.")
