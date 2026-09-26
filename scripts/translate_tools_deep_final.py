import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

FINAL_REPLACEMENTS = {
    # calculadora-descuentos-promociones
    'Ingresa el <span class="text-blue-light" data-visual-edit-loc="src/pages/Home.tsx:143:23" data-visual-edit-component="span" data-visual-edit-editable="true">costo</span> y el <span class="text-blue-light" data-visual-edit-loc="src/pages/Home.tsx:144:12" data-visual-edit-component="span" data-visual-edit-editable="true">precio normal</span> para ver la comparativa de rentabilidad.':
    'Enter the <span class="text-blue-light" data-visual-edit-loc="src/pages/Home.tsx:143:23" data-visual-edit-component="span" data-visual-edit-editable="true">cost</span> and <span class="text-blue-light" data-visual-edit-loc="src/pages/Home.tsx:144:12" data-visual-edit-component="span" data-visual-edit-editable="true">regular price</span> above to view the profitability comparison.',

    'aria-label="Costo producto 1"': 'aria-label="Product 1 Cost"',
    'aria-label="Precio producto 1"': 'aria-label="Product 1 Price"',
    'aria-label="Costo producto 2"': 'aria-label="Product 2 Cost"',
    'aria-label="Precio producto 2"': 'aria-label="Product 2 Price"',
    'aria-label="Costo producto 3"': 'aria-label="Product 3 Cost"',
    'aria-label="Precio producto 3"': 'aria-label="Product 3 Price"',

    # generador-paletas-corporativas
    'Copia la lista de paletas para pegar en tu proyecto.': 'Copy the palette list to paste into your project.',
    'Tus paletas guardadas en este navegador.': 'Your saved palettes stored in this browser.',
    'Aún no has guardado paletas.': 'No saved palettes yet.',
    'An no has guardado paletas.': 'No saved palettes yet.',
    '>Paletas que definen marcas': '>Color palettes that define brands',

    # guiones-manejo-objeciones
    'Me alegra que ya tengas un proveedor, significa que valoras esto. No te pido que cambies. Te propongo ser tu segunda opinión: si algún día tu proveedor falla o sube precios, ya me conoces. ¿Qué pierdes con tenerme en el radar?':
    '"I appreciate that you already have a trusted vendor; that shows you value this service. I\'m not asking you to switch. I propose being your backup option: if your vendor ever bottlenecks or raises prices, you\'ll already know us. What do you have to lose by keeping us on your radar?"',
    'Me alegra que ya tengas un proveedor, significa que valoras esto. No te pido que cambies. Te propongo ser tu segunda opinin: si algn da tu proveedor falla o sube precios, ya me conoces. Qu pierdes con tenerme en el radar?':
    '"I appreciate that you already have a trusted vendor; that shows you value this service. I\'m not asking you to switch. I propose being your backup option: if your vendor ever bottlenecks or raises prices, you\'ll already know us. What do you have to lose by keeping us on your radar?"',

    'No pelea la objeción, la valida. La prueba social de "mis mejores clientes decían lo mismo" reabre la puerta sin sonar insistente.':
    'Validates the objection rather than confronting it. Social proof showing "our best clients felt the same way" reopens conversation naturally.',
    'No pelea la objecin, la valida. La prueba social de "mis mejores clientes decan lo mismo" reabre la puerta sin sonar insistente.':
    'Validates the objection rather than confronting it. Social proof showing "our best clients felt the same way" reopens conversation naturally.',

    'Convierte la falta de tiempo (la objeción) en la razón principal para escuchar, prometiendo devolver ese mismo recurso escaso.':
    'Turns lack of time (the objection) into the primary reason to listen, promising to return that scarce resource.',
    'Convierte la falta de tiempo (la objecin) en la razn principal para escuchar, prometiendo devolver ese mismo recurso escaso.':
    'Turns lack of time (the objection) into the primary reason to listen, promising to return that scarce resource.',

    # auditor-seo-basico
    'Inserte una única etiqueta &lt;h1&gt; descriptiva que resume el contenido de la página.':
    'Insert a single descriptive &lt;h1&gt; heading that summarizes the core page topic.',
    'Inserte una nica etiqueta &lt;h1&gt; descriptiva que resume el contenido de la pgina.':
    'Insert a single descriptive &lt;h1&gt; heading that summarizes the core page topic.',

    'Pega aquí el contenido de tu artículo para analizar la frecuencia de palabras y su legibilidad…':
    'Paste your article body text here to analyze keyword frequency and readability...',
    'Pega aqu el contenido de tu artculo para analizar la frecuencia de palabras y su legibilidad…':
    'Paste your article body text here to analyze keyword frequency and readability...',
    'Pega aqu el contenido de tu artculo para analizar la frecuencia de palabras y su legibilidad':
    'Paste your article body text here to analyze keyword frequency and readability',

    # simulador-tco-fisico-nube
    'Eje X: Mes 1 → 36 · Eje Y: Costo acumulado · Línea naranja punteada = punto de quiebre':
    'X-Axis: Month 1 → 36 · Y-Axis: Cumulative Cost · Dashed orange line = breakeven point',
    'Eje X: Mes 1 → 36  Eje Y: Costo acumulado  Lnea naranja punteada = punto de quiebre':
    'X-Axis: Month 1 → 36 · Y-Axis: Cumulative Cost · Dashed orange line = breakeven point',

    # firma-correo-html
    'placeholder="www.empresa.com"': 'placeholder="www.example.com"',

    # generador-politicas-terminos
    'Any modifications will be published on this misma página con su fecha de actualización correspondiente.':
    'Any modifications will be published on this page along with the updated revision date.',
    'Any modifications will be published on this misma pgina con su fecha de actualizacin correspondiente.':
    'Any modifications will be published on this page along with the updated revision date.',

    # consola-campanas
    '>Contenido<': '>Content (utm_content)<',

    # flujo-caja-pymes
    'placeholder="Ej. Abono del cliente ACME"': 'placeholder="e.g. Acme Corp client payment"'
}

# Also handle the long TCO recommendation block via regex in simulador-tco-fisico-nube.html
TCO_REC_EN = "Based on the 36-month cluster simulation, Cloud infrastructure delivers approximately 14% total savings ($6,543 USD) while eliminating hardware refresh risks. Cloud remains the most cost-effective and flexible option throughout the projected period."

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

for es_slug, en_slug in SLUG_MAP.items():
    p = EN_DIR / es_slug
    if not p.exists():
        continue
    content = p.read_text(encoding="utf-8", errors="ignore")
    
    for k, v in FINAL_REPLACEMENTS.items():
        if k in content:
            content = content.replace(k, v)
            
    # TCO recommendation replace
    if "simulador-tco" in es_slug:
        content = re.sub(r'Seg.*?n la simulaci.*?n del cl.*?flexibilidad\.', TCO_REC_EN, content)

    p.write_text(content, encoding="utf-8")
    (EN_DIR / en_slug).write_text(content, encoding="utf-8")

print("Final deep replacements applied and synced across all paired tools!")
