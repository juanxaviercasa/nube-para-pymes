import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

SLUG_MAP = {
    "analizador-titulares.html": "headline-analyzer.html",
    "auditor-seo-basico.html": "basic-on-page-seo-auditor.html",
    "calculadora-descuentos-promociones.html": "discount-promotions-calculator.html",
    "calculadora-flete-envio-local.html": "local-shipping-calculator.html",
    "calculadora-precios-venta-igv.html": "sales-pricing-tax-calculator.html",
    "calculadora-prestamos-amortizaciones.html": "loan-amortization-calculator.html",
    "calculadora-sobrecostos-laborales.html": "labor-cost-payroll-burden-calculator.html",
    "comparador-campanas-avanzado.html": "advanced-campaign-comparator.html",
    "consola-campanas.html": "campaign-utm-console.html",
    "conversor-optimizador-imagenes.html": "image-converter-optimizer.html",
    "creador-facturas-proforma.html": "proforma-invoice-generator.html",
    "crm-pymes.html": "smb-crm.html",
    "firma-correo-html.html": "html-email-signature.html",
    "flujo-caja-pymes.html": "cash-flow-tracker.html",
    "generador-codigos-qr.html": "qr-code-generator.html",
    "generador-contrasenas-pymes.html": "smb-password-generator.html",
    "generador-contratos-servicios.html": "service-contracts-generator.html",
    "generador-cotizaciones.html": "quote-estimate-generator.html",
    "generador-paletas-corporativas.html": "brand-palette-generator.html",
    "generador-politicas-devolucion.html": "return-policy-generator.html",
    "generador-politicas-terminos.html": "terms-privacy-generator.html",
    "guiones-manejo-objeciones.html": "objection-handling-scripts.html",
    "inventario-compras-pymes.html": "inventory-purchasing.html",
    "organizador-matriz-contenidos.html": "content-matrix-planner.html",
    "simulador-tco-fisico-nube.html": "cloud-vs-onprem-tco-simulator.html",
    "tareas-proyectos-pymes.html": "tasks-projects-tracker.html"
}

LAST_REPLACEMENTS = {
    'placeholder="hola@empresa.com"': 'placeholder="hello@example.com"',
    '>Empresa *<': '>Company Name *<',
    'placeholder="Ej. Lanzamiento web de cliente"': 'placeholder="e.g. Client website launch"',
    'placeholder="Ej. Abono del cliente ACME"': 'placeholder="e.g. Acme Corp client payment"',
    'Paletas que definen marcas': 'Color palettes that define brands',
    'Copia la lista de paletas': 'Copy the palette list',
    'Tus paletas guardadas': 'Your saved palettes',
    'Aún no has guardado paletas': 'No saved palettes yet',
    'An no has guardado paletas': 'No saved palettes yet',
    'Descargar paleta': 'Download Palette'
}

for es_slug, en_slug in SLUG_MAP.items():
    p = EN_DIR / es_slug
    if not p.exists():
        continue
    content = p.read_text(encoding="utf-8", errors="ignore")
    
    for k, v in LAST_REPLACEMENTS.items():
        if k in content:
            content = content.replace(k, v)
            
    # TCO Axis regex
    content = re.sub(
        r'Eje X:.*?punto de quiebre',
        'X-Axis: Month 1 → 36 · Y-Axis: Cumulative Cost · Dashed orange line = breakeven point',
        content,
        flags=re.IGNORECASE
    )
    
    # Contract obligations clause regex
    content = re.sub(
        r'THE SERVICE PROVIDER ejecutar.*?t.*?rminos acordados\.',
        'THE SERVICE PROVIDER agrees to perform the services with due diligence, professional quality, and within agreed timeframes. THE CLIENT agrees to provide necessary information and support, and to remit payments under the agreed commercial terms.',
        content,
        flags=re.IGNORECASE
    )

    p.write_text(content, encoding="utf-8")
    (EN_DIR / en_slug).write_text(content, encoding="utf-8")

print("Resolved final 5 items and synced!")
