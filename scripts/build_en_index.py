import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"
EN_DIR.mkdir(exist_ok=True)

content = (ROOT / "index.html").read_text(encoding="utf-8")

# 1. HTML lang & meta
content = re.sub(r'<html\s+lang=["\']es["\']', '<html lang="en"', content)

# 2. Asset relative paths ./assets/ -> ../assets/, ./css/ -> ../css/, ./js/ -> ../js/
content = content.replace('href="./assets/', 'href="../assets/')
content = content.replace('src="./assets/', 'src="../assets/')
content = content.replace('href="./css/', 'href="../css/')
content = content.replace('src="./js/', 'src="../js/')

# 3. Title & Meta
old_title = "<title>Nube para Pymes — Portal de Herramientas</title>"
new_title = """<title>SMB Cloud — Free Business Tools Portal</title>
  <meta name="description" content="26 free, local browser tools for small businesses. Calculate prices, create invoices, audit SEO, build UTM links, and streamline operations with zero login.">"""
content = content.replace(old_title, new_title)

# 4. Header & Branding
content = content.replace('aria-label="NubeParaPymes - Inicio"', 'aria-label="SMB Cloud - Home"')
content = content.replace('alt="NubeParaPymes"', 'alt="SMB Cloud"')
content = content.replace('placeholder="Buscar herramienta..."', 'placeholder="Search tools..."')
content = content.replace('aria-label="Buscar herramienta"', 'aria-label="Search tools"')
content = content.replace('aria-label="Buscar por voz"', 'aria-label="Search by voice"')
content = content.replace('aria-label="Alternar modo oscuro"', 'aria-label="Toggle dark mode"')

# 5. Hero Banner
content = content.replace('26 herramientas gratuitas', '26 Free Business Tools')
content = content.replace(
    'Potencia tu Pyme con nuestras <span class="text-brand-soft">Herramientas Gratuitas</span>',
    'Empower Your Small Business with <span class="text-brand-soft">Free Tools</span>'
)
content = content.replace(
    'Un solo panel de control con todo lo que necesitas para calcular, vender, optimizar y hacer crecer tu negocio. Elige una herramienta y empieza en segundos.',
    'An all-in-one control panel with everything you need to calculate, sell, optimize, and scale your business. Choose a tool and get started in seconds.'
)

# 6. Activity widget
content = content.replace('>Mi Actividad<', '>My Activity<')
content = content.replace('>0 clics · 0 herramientas usadas<', '>0 clicks · 0 tools used<')

# 7. Directory header & Tabs
content = content.replace('>Directorio de herramientas<', '>Tools Directory<')
content = content.replace('>26 resultados<', '>26 results<')
content = content.replace('aria-label="Filtrar por categoría"', 'aria-label="Filter by category"')

# Tabs translation
content = re.sub(r'(\s*)Todas(\s*<span)', r'\1All\2', content)
content = re.sub(r'(\s*)Finanzas(\s*<span)', r'\1Finance\2', content)
content = re.sub(r'(\s*)Ventas(\s*<span)', r'\1Sales\2', content)
content = re.sub(r'(\s*)Operaciones(\s*<span)', r'\1Operations\2', content)
content = re.sub(r'(\s*)Productividad(\s*<span)', r'\1Productivity\2', content)
# Note: Marketing and Legal are already English names!

# 8. Button texts
content = content.replace('>Abrir Herramienta<', '>Open Tool<')
content = content.replace('Abrir Herramienta <span', 'Open Tool <span')
content = content.replace('Agregar ', 'Add ')
content = content.replace(' a favoritos', ' to favorites')

# 9. Tool Cards mapping (Titles and Descriptions)
CARD_TRANSLATIONS = [
    (
        "Analizador de Titulares",
        "Headline Analyzer",
        "Evalúa el impacto psicológico y SEO de tus titulares antes de publicarlos para maximizar tus clics.",
        "Assess psychological impact and SEO strength of your headlines before publishing to maximize click-through rates."
    ),
    (
        "Auditor SEO Básico",
        "Basic SEO Auditor",
        "Escanea tu web y verifica al instante si tus títulos y metaetiquetas están optimizados para Google.",
        "Scan your webpage and instantly check if your titles, meta tags, and headings are optimized for search engines."
    ),
    (
        "Calculadora de Descuentos",
        "Discount & Margin Calculator",
        "Simula la rentabilidad de tus campañas promocionales y descubre tu punto de equilibrio exacto.",
        "Simulate promotional campaigns, calculate margins, and determine your exact break-even point."
    ),
    (
        "Calculadora de Flete Local",
        "Local Shipping & Freight Calculator",
        "Calcula los costos de despacho logístico al instante comparando peso real vs. volumétrico.",
        "Calculate freight and delivery costs instantly by comparing actual weight vs. dimensional weight."
    ),
    (
        "Calculadora de Precios con IGV",
        "Sales Pricing & Tax Calculator",
        "Fija los precios de tus productos correctamente y calcula tu margen de ganancia neto separando impuestos.",
        "Set profitable selling prices and determine your net margin while calculating sales tax / GST."
    ),
    (
        "Calculadora de Préstamos",
        "Loan & Amortization Calculator",
        "Proyecta pagos mensuales, simula pagos anticipados y descubre cuánto ahorrarás en intereses.",
        "Project monthly payments, simulate early repayments, and calculate total interest savings."
    ),
    (
        "Calculadora de Sobrecostos Laborales",
        "Labor Cost & Payroll Burden Calculator",
        "Calcula el costo real de contratar personal proyectando gratificaciones, CTS y aportes de ley.",
        "Estimate the true employer cost of hiring staff, including mandatory benefits, payroll taxes, and provisions."
    ),
    (
        "Comparador de Campañas",
        "Ad Campaign Comparator",
        "Mide y compara el rendimiento (ROI, CPA, CTR) de tus campañas de marketing en un solo panel interactivo.",
        "Measure and compare marketing performance (ROI, ROAS, CPA, CTR) across ad platforms in a unified view."
    ),
    (
        "Consola de Campañas UTM",
        "UTM Campaign Builder Console",
        "Organiza, etiqueta y supervisa todos tus enlaces de seguimiento en un solo lugar.",
        "Organize, tag, and standardize your campaign tracking links in one place."
    ),
    (
        "Optimizador de Imágenes WebP",
        "WebP Image Converter & Optimizer",
        "Reduce el peso de tus fotos sin perder calidad para que tu web cargue a la velocidad del rayo.",
        "Compress photos without quality loss so your website loads lightning fast."
    ),
    (
        "Creador de Facturas Proforma",
        "Proforma Invoice Generator",
        "Genera cotizaciones rápidas, gestiona tu catálogo y envía propuestas profesionales al instante.",
        "Create quick commercial proformas, manage line items, and export professional proposals in seconds."
    ),
    (
        "Firma de Correo en HTML",
        "HTML Email Signature Generator",
        "Diseña una firma de email corporativa y profesional compatible con Gmail y Outlook.",
        "Design a sleek, professional email signature compatible with Gmail, Outlook, and Apple Mail."
    ),
    (
        "Enlaces y QR para WhatsApp",
        "QR Code & WhatsApp Link Generator",
        "Crea links directos y códigos QR escaneables para que tus clientes inicien chats rápidamente.",
        "Generate direct chat links and scannable QR codes so customers can message you instantly."
    ),
    (
        "Generador de Cotizaciones",
        "Quote & Estimate Generator",
        "Arma propuestas comerciales estructuradas y envíalas en formato PDF con la identidad de tu marca.",
        "Build structured commercial estimates with custom branding and export ready-to-send PDFs."
    ),
    (
        "Paletas Corporativas",
        "Brand Color Palette Generator",
        "Extrae o genera esquemas de color profesionales para tu marca y asegura la armonía visual.",
        "Extract and generate cohesive, accessible color schemes for your brand and user interface."
    ),
    (
        "Políticas de Devolución",
        "Return & Refund Policy Generator",
        "Redacta textos claros sobre garantías y reembolsos basados en el tipo de producto que vendes.",
        "Draft clear warranties and refund terms tailored to your product or service type."
    ),
    (
        "Políticas y Términos",
        "Terms of Service & Privacy Policy Generator",
        "Crea los documentos legales obligatorios (Privacidad y Aviso Legal) para tu web o tienda online.",
        "Generate essential website policies (Privacy Policy and Terms of Service) for your online business or store."
    ),
    (
        "Guiones para Objeciones",
        "Sales Objection Handling Scripts",
        "Equipa a tu equipo de ventas con las mejores respuestas ante cualquier cliente difícil.",
        "Equip your sales team with proven frameworks and responses for challenging buyer objections."
    ),
    (
        "Matriz de Contenidos",
        "Content Matrix & Editorial Planner",
        "Planifica, estructura y recicla las publicaciones de tus redes sociales en un tablero interactivo.",
        "Plan, organize, and repurpose social media and blog posts across an interactive matrix."
    ),
    (
        "Simulador TCO: Físico vs Nube",
        "Cloud vs. On-Premises TCO Simulator",
        "Compara los costos totales entre comprar infraestructura física o alquilar servicios Cloud.",
        "Compare total cost of ownership between purchasing physical servers and running cloud infrastructure."
    ),
    (
        "Generador de Contraseñas para Pymes",
        "Password Generator for Small Teams",
        "Crea contraseñas seguras y personalizadas de forma local, rápida y gratuita.",
        "Create strong, randomized passwords locally in your browser with zero data exposure."
    ),
    (
        "Generador de Contratos de Servicios",
        "Service Agreement Generator",
        "Redacta contratos de servicios editables con una plantilla local para tu negocio.",
        "Draft customizable professional contractor and service agreements for your business."
    ),
    (
        "CRM y Pipeline Comercial",
        "SMB CRM & Sales Pipeline",
        "Centraliza contactos, oportunidades y seguimientos para convertir conversaciones en ventas.",
        "Track contacts, sales opportunities, and follow-ups in a lightweight, local-first CRM."
    ),
    (
        "Flujo de Caja y Cobranzas",
        "Cash Flow & Receivables Tracker",
        "Registra ingresos, egresos, vencimientos y pendientes para anticipar problemas de liquidez.",
        "Record income, expenses, due dates, and receivables to forecast and protect liquidity."
    ),
    (
        "Inventario, Proveedores y Compras",
        "Inventory, Suppliers & Purchase Orders",
        "Controla productos, stock mínimo, proveedores y compras de reposición.",
        "Track product levels, reorder thresholds, supplier directories, and purchase orders."
    ),
    (
        "Tareas y Proyectos Operativos",
        "Operational Tasks & Project Tracker",
        "Organiza proyectos, responsables, prioridades y fechas de entrega.",
        "Organize team projects, assignees, deadlines, and priorities on an operational board."
    ),
]

for es_title, en_title, es_desc, en_desc in CARD_TRANSLATIONS:
    content = content.replace(f">{es_title}<", f">{en_title}<")
    content = content.replace(f">{es_desc}<", f">{en_desc}<")
    # Also replace within aria-labels
    content = content.replace(f"Agregar {es_title} a favoritos", f"Add {en_title} to favorites")

# Card category badge labels inside cards
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Finanzas(</span>)', r'\1Finance\2', content)
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Ventas(</span>)', r'\1Sales\2', content)
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Operaciones(</span>)', r'\1Operations\2', content)
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Productividad(</span>)', r'\1Productivity\2', content)
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Seguridad(</span>)', r'\1Security\2', content)
content = re.sub(r'(<span class="mb-2 text-xs font-semibold uppercase tracking-widest text-brand">)Legal y Administración(</span>)', r'\1Legal & Admin\2', content)

# 10. Footer translation
content = content.replace('Herramientas gratuitas y locales para pequeñas empresas.', 'Free and local browser tools for small businesses.')
content = content.replace('Guía completa de uso →', 'Complete User Guide →')
content = content.replace('href="./guia-uso-22-apps.html"', 'href="./user-guide.html"')
content = content.replace('Diseñado y Desarrollado por', 'Designed & Developed by')

# 11. Modal Tour translation
content = content.replace('Paso 1 de 3', 'Step 1 of 3')
content = content.replace('Saltar Tour', 'Skip Tour')
content = content.replace('Buscador inteligente', 'Smart Search')
content = content.replace(
    'Escribe el nombre de una herramienta. Tolera errores de tipeo y resalta las coincidencias al instante.',
    'Type any tool name. Tolerates typos and highlights matching tools instantly.'
)
content = content.replace('>Atrás<', '>Back<')
content = content.replace('>Siguiente<', '>Next<')
content = content.replace('aria-label="Configuraciones globales"', 'aria-label="Global settings"')

out_path = EN_DIR / "index.html"
out_path.write_text(content, encoding="utf-8")
print(f"en/index.html created successfully ({len(content)} chars).")
