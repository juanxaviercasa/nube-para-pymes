import re
from pathlib import Path

pantheon_path = Path(r"C:\Users\pc\.gemini\antigravity-ide\brain\9f444707-4121-4bd5-96ad-3d8d70a449e9\scratch\pantheon_root.html")
target_export = Path(r"c:\Users\pc\Music\nube-para-pymes\nubepymesexport\index.html")
search_ref_path = Path(r"c:\Users\pc\Music\nube-para-pymes\nubepymesexport\ahorrar-horas-trabajo-administrativo\index.html")

raw = pantheon_path.read_text(encoding="utf-8", errors="ignore")

# 1. Domain replacements
html = raw

# Canonical
html = re.sub(r'<link rel=["\']canonical["\'] href=["\'][^"\']+["\']\s*/?>', '<link rel="canonical" href="https://nubeparapymes.online/" />', html)

# Assets (wp-content, wp-includes, wp-json)
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/wp-content/', '/wp-content/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/wp-includes/', '/wp-includes/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/wp-json/', '/wp-json/')

# Internal WP page routes in header/footer
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/blog/', '/blog/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/herramientas-gratis/', '/herramientas/')
html = html.replace('/herramientas-gratis/', '/herramientas/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/sobre-nosotros/', '/sobre-nosotros/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/politica-de-privacidad/', '/politica-de-privacidad/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/metodologia-de-resenas/', '/metodologia-de-resenas/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/contacto/', '/contacto/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/terminos-y-condiciones/', '/terminos-y-condiciones/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/politica-de-cookies/', '/politica-de-cookies/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/descargo-de-responsabilidad/', '/descargo-de-responsabilidad/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/aviso-legal/', '/aviso-legal/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/feed/', '/feed/')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/comments/feed/', '/comments/feed/')
html = html.replace('href="https://dev-nube-para-pymes.pantheonsite.io/"', 'href="/"')
html = html.replace('href="https://dev-nube-para-pymes.pantheonsite.io"', 'href="/"')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io/', '/')

# Normalize remaining schema / person URLs
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io#', 'https://nubeparapymes.online/#')
html = html.replace('https://dev-nube-para-pymes.pantheonsite.io', 'https://nubeparapymes.online')

# 2. Tool link replacements
tool_replacements = [
    ("https://apps.nubeparapymes.online/generador-cotizaciones.html", "/herramientas/ventas/generador-cotizaciones/"),
    ("https://apps.nubeparapymes.online/calculadora-precios-venta-igv.html", "/herramientas/finanzas/calculadora-precios-venta-igv/"),
    ("https://apps.nubeparapymes.online/calculadora-sobrecostos-laborales.html", "/herramientas/finanzas/calculadora-sobrecostos-laborales/"),
    ("https://apps.nubeparapymes.online/generador-c%C3%B3digos-qr.html", "/herramientas/ventas/generador-codigos-qr/"),
    ("https://apps.nubeparapymes.online/generador-códigos-qr.html", "/herramientas/ventas/generador-codigos-qr/"),
    ("https://apps.nubeparapymes.online/generador-politicas-terminos.html", "/herramientas/legal/generador-politicas-terminos/"),
    ("https://apps.nubeparapymes.online/auditor-seo-b%C3%A1sico.html", "/herramientas/marketing/auditor-seo-basico/"),
    ("https://apps.nubeparapymes.online/auditor-seo-básico.html", "/herramientas/marketing/auditor-seo-basico/"),
    ("https://apps.nubeparapymes.online/creador-facturas-proforma.html", "/herramientas/ventas/creador-facturas-proforma/"),
    ("https://apps.nubeparapymes.online/calculadora-flete-envio-local.html", "/herramientas/operaciones/calculadora-flete-envio-local/"),
    ("https://apps.nubeparapymes.online/organizador-matriz-contenidos.html", "/herramientas/marketing/organizador-matriz-contenidos/"),
    ("https://apps.nubeparapymes.online/generador-contratos-servicios.html", "/herramientas/legal/generador-contratos-servicios/"),
    ("https://apps.nubeparapymes.online/analizador-titulares.html", "/herramientas/marketing/analizador-titulares/"),
    ("https://apps.nubeparapymes.online/", "/herramientas/"),
    ("https://apps.nubeparapymes.online", "/herramientas/"),
    ("/herramientas-gratis/calculadora-de-precios-de-venta-con-igv/", "/herramientas/finanzas/calculadora-precios-venta-igv/"),
    ("/herramientas-gratis/auditor-basico-de-seo-on-page/", "/herramientas/marketing/auditor-seo-basico/"),
]

for old, new in tool_replacements:
    html = html.replace(old, new)

# 3. Inject search modal CSS and script if not present
if "search-modal.css" not in html:
    html = html.replace("</head>", '<link rel="stylesheet" href="/wp-static-arquitect-assets/search-modal.css">\n</head>')

# Extract search markup from reference file
ref_txt = search_ref_path.read_text(encoding="utf-8", errors="ignore")
s_idx = ref_txt.find('<div id="wpsa-search-root"')
e_idx = ref_txt.find('</body>')

if s_idx != -1 and e_idx != -1:
    search_markup = ref_txt[s_idx:e_idx]
    if "wpsa-search-root" not in html:
        html = html.replace("</body>", f"{search_markup}\n</body>")
        print("Injected search markup successfully.")
else:
    print("WARNING: Could not find search markup boundaries.")

target_export.write_text(html, encoding="utf-8")
print(f"Generated {target_export} ({len(html)} chars)")
