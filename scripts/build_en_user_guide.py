import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"
EN_DIR.mkdir(exist_ok=True)

content = (ROOT / "guia-uso-22-apps.html").read_text(encoding="utf-8")

# 1. HTML lang & meta
content = re.sub(r'<html\s+lang=["\']es["\']', '<html lang="en"', content)
content = content.replace(
    '<meta name="description" content="Guía completa de uso de las 26 herramientas gratuitas de NubeParaPymes.">',
    '<meta name="description" content="Complete user guide for the 26 free local tools of SMB Cloud. Step-by-step instructions, workflows, and best practices.">'
)
content = content.replace(
    '<title>Guía de uso · NubeParaPymes</title>',
    '<title>User Guide · SMB Cloud</title>'
)

# 2. Asset relative paths & Header links
content = content.replace('href="./assets/', 'href="../assets/')
content = content.replace('src="./assets/', 'src="../assets/')
content = content.replace('href="./css/', 'href="../css/')
content = content.replace('src="./js/', 'src="../js/')

# Top navbar
content = content.replace('<a class="brand" href="./index.html">NubeParaPymes</a>', '<a class="brand" href="./index.html">SMB Cloud</a>')
content = content.replace('<a class="back" href="./index.html">Volver al directorio</a>', '<a class="back" href="./index.html">Back to Tools Directory</a>')

# Headings & Intro
content = content.replace(
    '<h1 id="guia-completa-de-uso-de-nubeparapymes">Guía completa de uso de NubeParaPymes</h1>',
    '<h1 id="complete-smb-cloud-user-guide">Complete SMB Cloud User Guide</h1>'
)
content = content.replace('<h2 id="introduccion">Introducción</h2>', '<h2 id="introduction">Introduction</h2>')
content = content.replace(
    'NubeParaPymes reúne <strong>26 herramientas gratuitas y locales</strong> para apoyar tareas de marketing, ventas, operaciones, finanzas, documentación y planificación de pequeñas empresas. Cada aplicación se ejecuta en el navegador y conserva sus datos localmente cuando dispone de historial o almacenamiento persistente. No es necesario crear una cuenta, entregar un correo electrónico ni contratar un plan para utilizar las funciones publicadas.',
    'SMB Cloud brings together <strong>26 free, local browser tools</strong> designed to support small business marketing, sales, operations, finance, legal documentation, and planning. Every application runs directly in your browser and stores data locally when history or persistent storage is available. No account creation, email submission, or paid subscription is required.'
)
content = content.replace(
    'La portada del proyecto está disponible en <a href="./index.html">NubeParaPymes</a>. Las aplicaciones se abren mediante archivos HTML independientes en la raíz, por lo que las rutas tienen el formato <code>./nombre-de-la-app.html</code>. La guía de despliegue técnico se encuentra en <a href="./GUIA_DESPLIEGUE_HOSTING.md">GUIA_DESPLIEGUE_HOSTING.md</a>.',
    'The project dashboard is available at <a href="./index.html">SMB Cloud</a>. Applications open as standalone HTML files, formatted as <code>./app-name.html</code>. Technical deployment guidelines can be found in <a href="../GUIA_DESPLIEGUE_HOSTING.md">GUIA_DESPLIEGUE_HOSTING.md</a>.'
)
content = content.replace(
    '<strong>Buenas prácticas generales.</strong> Introduce datos de prueba antes de trabajar con información real, revisa las unidades y monedas, descarga o copia los resultados importantes y utiliza una copia local de respaldo cuando una herramienta ofrezca exportación o importación. Las calculadoras financieras, laborales y legales son instrumentos de apoyo: sus resultados deben revisarse con la normativa, contratos y asesoría profesional aplicables a cada caso.',
    '<strong>General best practices.</strong> Test with sample data before inputting real business records, double-check units and currency formatting, download or copy critical outputs, and keep local backups when a tool offers JSON export/import. Financial, payroll, and legal tools are advisory calculators: verify outcomes with local statutory standards, contracts, and licensed professional advice.'
)

# Table of Applications
content = content.replace('<h2 id="tabla-de-aplicaciones">Tabla de aplicaciones</h2>', '<h2 id="applications-table">Tools Directory Table</h2>')
content = content.replace('<th>Aplicación</th>', '<th>Tool</th>')
content = content.replace('<th>Uso principal</th>', '<th>Primary Use</th>')
content = content.replace('<th>Acceso</th>', '<th>Access</th>')
content = content.replace('>Abrir<', '>Open<')

# App Names in table & descriptions
TABLE_REPLACEMENTS = [
    ("Analizador de Titulares", "Headline Analyzer", "Evaluar y mejorar titulares de contenido", "Analyze and improve headlines for higher CTR"),
    ("Auditor Básico de SEO On-Page", "Basic SEO On-Page Auditor", "Revisar señales SEO de una página", "Audit on-page SEO signals and metadata"),
    ("Calculadora de Descuentos y Promociones", "Discounts & Promotions Calculator", "Simular precios, márgenes y promociones", "Simulate discount pricing, margins, and promotions"),
    ("Calculadora de Flete y Envío Local", "Local Shipping & Freight Calculator", "Cotizar despachos y rutas locales", "Calculate delivery rates and local delivery routes"),
    ("Calculadora de Precios de Venta con IGV", "Sales Pricing & Tax Calculator", "Calcular precio, margen e impuesto", "Calculate selling price, net margin, and sales tax / GST"),
    ("Calculadora de Préstamos y Amortizaciones", "Loan & Amortization Calculator", "Comparar créditos y cuotas", "Compare commercial loans, rates, and amortization"),
    ("Calculadora de Sobrecostos Laborales", "Labor Cost & Payroll Burden Calculator", "Estimar el costo total de una plantilla", "Estimate total employer cost of payroll and benefits"),
    ("Comparador Avanzado de Campañas", "Ad Campaign Performance Comparator", "Comparar campañas y escenarios", "Compare ad campaigns, ROI, CPA, and return across channels"),
    ("Consola de Campañas", "UTM Campaign Builder Console", "Crear UTMs y organizar campañas", "Generate UTM tracking URLs and campaign naming conventions"),
    ("WebP Forge", "WebP Image Converter & Optimizer", "Convertir y optimizar imágenes", "Convert and compress images directly in browser"),
    ("Creador de Facturas Proforma", "Proforma Invoice Generator", "Generar proformas rápidas y catálogos", "Generate quick proforma invoices and product lines"),
    ("Firma de Correo HTML", "HTML Email Signature Generator", "Diseñar firmas profesionales para correo", "Design professional HTML email signatures"),
    ("Generador de Códigos QR", "QR Code & WhatsApp Direct Generator", "Crear códigos QR y enlaces directos", "Create scannable QR codes and direct message links"),
    ("Generador de Cotizaciones", "Quote & Estimate Generator", "Generar presupuestos y cotizaciones", "Create professional client quotes and estimates in PDF"),
    ("Generador de Paletas Corporativas", "Brand Color Palette Generator", "Definir paletas y contrastes de marca", "Generate harmonic brand color palettes and contrast metrics"),
    ("Generador de Políticas de Devolución", "Return & Refund Policy Generator", "Redactar condiciones de garantía y devolución", "Draft customized return and refund policies"),
    ("Generador de Políticas y Términos", "Terms & Privacy Policy Generator", "Crear términos, privacidad y cookies", "Generate Terms of Service, Privacy, and Cookie notices"),
    ("Guiones para Manejo de Objeciones", "Sales Objection Handling Scripts", "Practicar respuestas comerciales estructuradas", "Access proven objection responses and sales scripts"),
    ("Organizador de Matriz de Contenidos", "Content Matrix & Editorial Planner", "Planificar contenidos y canales", "Plan and organize content pillars across channels"),
    ("Simulador TCO: Físico vs. Nube", "Cloud vs On-Premises TCO Simulator", "Comparar costos de servidor físico y nube", "Compare Total Cost of Ownership: On-prem vs. Cloud"),
    ("SecuKey", "SecuKey Password Generator", "Generar contraseñas seguras para equipos", "Generate strong, randomized passwords for small teams"),
    ("Contratos de Servicios", "Professional Service Agreement Generator", "Redactar borradores editables de contratos", "Draft customized professional service contracts"),
    ("CRM y Pipeline Comercial", "SMB CRM & Sales Pipeline", "Seguimiento de prospectos y ventas", "Track contacts, sales pipelines, and follow-up tasks"),
    ("Flujo de Caja y Cobranzas", "Cash Flow & Receivables Tracker", "Controlar ingresos, gastos y liquidez", "Track operational cash inflows, outflows, and receivables"),
    ("Inventario, Proveedores y Compras", "Inventory, Suppliers & Purchase Orders", "Controlar existencias y pedidos", "Track stock levels, suppliers, and purchase orders"),
    ("Tareas y Proyectos Operativos", "Operational Tasks & Project Tracker", "Organizar entregas, prioridades y equipo", "Manage operational team tasks, deadlines, and project statuses")
]

for es_name, en_name, es_desc, en_desc in TABLE_REPLACEMENTS:
    content = content.replace(f"<td>{es_name}</td>", f"<td>{en_name}</td>")
    content = content.replace(f"<td>{es_desc}</td>", f"<td>{en_desc}</td>")

# Section Headings and Labels
SECTION_LABELS = [
    ("<h3>Para qué sirve</h3>", "<h3>Primary Purpose</h3>"),
    ("<h3>Cómo utilizarla</h3>", "<h3>How to Use It</h3>"),
    ("<h3>Cuándo usarla</h3>", "<h3>When to Use It</h3>"),
    ("<h3>Buenas prácticas</h3>", "<h3>Best Practices</h3>"),
    ("<h3>Datos necesarios</h3>", "<h3>Required Inputs</h3>"),
    ("<h3>Qué entrega</h3>", "<h3>Output</h3>"),
    ("<h3>Consejos prácticos</h3>", "<h3>Practical Tips</h3>"),
]
for es_l, en_l in SECTION_LABELS:
    content = content.replace(es_l, en_l)

# Summary and Footer sections
content = content.replace(
    '<h2 id="flujo-recomendado-para-trabajar-con-varias-aplicaciones">Flujo recomendado para trabajar con varias aplicaciones</h2>',
    '<h2 id="recommended-workflow-combining-apps">Recommended Multi-App Workflow</h2>'
)
content = content.replace(
    'Una pyme puede combinar las herramientas en un flujo local. Primero define la propuesta comercial con la <strong>Calculadora de Precios de Venta</strong>, la <strong>Calculadora de Descuentos</strong> y el <strong>Generador de Cotizaciones</strong>. Después prepara la presencia digital con el <strong>Analizador de Titulares</strong>, el <strong>Auditor SEO</strong>, la <strong>Consola de Campañas</strong> y el <strong>Organizador de Matriz de Contenidos</strong>. Para operación y administración, utiliza el <strong>Creador de Facturas Proforma</strong>, la <strong>Calculadora de Flete</strong>, la <strong>Calculadora de Sobrecostos Laborales</strong> y el <strong>Simulador TCO</strong>. Finalmente, documenta la relación comercial con el <strong>Generador de Contratos</strong>, <strong>LegalForge</strong> y la <strong>Política de Devoluciones</strong>.',
    'A small business can combine these tools into a seamless local-first workflow. First, establish pricing and quotes with the <strong>Sales Pricing & Tax Calculator</strong>, <strong>Discounts & Margin Calculator</strong>, and <strong>Quote & Estimate Generator</strong>. Next, refine your digital reach using the <strong>Headline Analyzer</strong>, <strong>On-Page SEO Auditor</strong>, <strong>UTM Campaign Console</strong>, and <strong>Content Matrix Planner</strong>. For operations and bookkeeping, use the <strong>Proforma Invoice Generator</strong>, <strong>Shipping Calculator</strong>, <strong>Labor Cost Calculator</strong>, and <strong>Cloud TCO Simulator</strong>. Finally, formalize agreements with the <strong>Service Agreement Generator</strong>, <strong>Terms & Privacy Policy Generator</strong>, and <strong>Return Policy Generator</strong>.'
)

content = content.replace(
    '<h2 id="privacidad-almacenamiento-y-respaldo">Privacidad, almacenamiento y respaldo</h2>',
    '<h2 id="privacy-storage-and-backup">Privacy, Storage, and Backups</h2>'
)
content = content.replace(
    'Las herramientas están preparadas para operar localmente. Cuando una aplicación ofrece historial, catálogo, favoritos, campañas o matriz, esa información puede almacenarse en el navegador mediante almacenamiento local. Borrar los datos del sitio, utilizar navegación privada o cambiar de navegador puede eliminar ese contenido. Exporta documentos, PDF, CSV o respaldos cuando la herramienta lo permita y conserva los archivos en una ubicación segura.',
    'These tools operate completely client-side in your browser. Whenever an application maintains history, catalogs, favorites, campaigns, or matrices, data is saved locally via browser localStorage. Clearing site data, using incognito mode, or switching browsers may reset stored items. Export documents, PDFs, CSVs, or JSON backups whenever offered and archive them securely.'
)

content = content.replace(
    '<h2 id="solucion-rapida-de-problemas">Solución rápida de problemas</h2>',
    '<h2 id="troubleshooting-guide">Quick Troubleshooting Guide</h2>'
)
content = content.replace('<th>Síntoma</th>', '<th>Symptom</th>')
content = content.replace('<th>Comprobación recomendada</th>', '<th>Recommended Check</th>')

TROUBLESHOOTING = [
    ("Aparece un 404 al abrir una app", "404 error when opening a tool"),
    ("Comprueba que la URL termine en el nombre exacto del archivo <code>.html</code> y que se haya publicado la raíz completa.", "Verify that the URL points to the exact <code>.html</code> file and that all root static files are deployed."),
    ("Solo se ve el fondo de color", "Page displays only background color"),
    ("Actualiza con <code>Ctrl + F5</code>, revisa la consola y confirma que el JS de <code>/js/</code> responde con HTTP 200.", "Hard refresh with <code>Ctrl + F5</code>, check the developer console, and confirm scripts in <code>../js/</code> return HTTP 200."),
    ("Las tildes aparecen como <code>Ã</code>", "Special characters display improperly"),
    ("Verifica que el servidor entregue UTF‑8 y que el HTML incluya <code>&lt;meta charset=\"UTF-8\"&gt;</code>.", "Confirm your server serves UTF-8 encoding and the page contains <code>&lt;meta charset=\"UTF-8\"&gt;</code>."),
    ("No aparece el CSS", "Styles are missing"),
    ("Comprueba que <code>/css/nombre-de-la-app.css</code> exista y que la referencia sea relativa a la raíz.", "Check that the stylesheet exists in <code>../css/</code> and relative paths resolve correctly."),
    ("Se perdieron datos del historial", "Stored history or records disappeared"),
    ("Revisa si cambiaste de navegador, borraste el almacenamiento del sitio o usaste una ventana privada.", "Check if you switched browsers, cleared cookies/site data, or opened an incognito session."),
    ("Un PDF o ZIP no descarga", "PDF or ZIP file fails to download"),
    ("Permite las descargas del navegador y prueba con una ventana normal; el procesamiento se realiza localmente.", "Allow browser downloads and popups; generation is performed locally inside your browser.")
]

for es_s, en_s in TROUBLESHOOTING:
    content = content.replace(es_s, en_s)

content = content.replace(
    '<p><strong>NubeParaPymes · herramientas locales y gratuitas para pequeñas empresas.</strong></p>',
    '<p><strong>SMB Cloud · Free local tools for small businesses.</strong></p>'
)
content = content.replace(
    '<p><em>Documento preparado para la versión publicada en <code>main</code>.</em></p>',
    '<p><em>Official documentation for the version published on <code>main</code>.</em></p>'
)
content = content.replace(
    'Guía de uso de las 26 aplicaciones · NubeParaPymes · Diseñado y Desarrollado por',
    'User Guide for 26 Business Tools · SMB Cloud · Designed & Developed by'
)

# Write both en/user-guide.html and en/guia-uso-22-apps.html
(EN_DIR / "user-guide.html").write_text(content, encoding="utf-8")
(EN_DIR / "guia-uso-22-apps.html").write_text(content, encoding="utf-8")
print("en/user-guide.html and en/guia-uso-22-apps.html generated successfully.")
