"""
Script to build:
1. en/tools/index.html (Tools Portal in English)
2. en/index.html (English Homepage matching main site design)
3. en/about-us/index.html (English About Us page)
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent

def build_english_tools_portal():
    print("Building en/tools/index.html...")
    src_portal = ROOT / "en" / "index.html"
    dest_dir = ROOT / "en" / "tools"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    if src_portal.exists():
        txt = src_portal.read_text(encoding="utf-8")
        # Ensure asset paths are correct for 2 levels deep
        txt = txt.replace('href="../assets/', 'href="/assets/')
        txt = txt.replace('src="../assets/', 'src="/assets/')
        txt = txt.replace('src="../js/', 'src="/herramientas/js/')
        txt = txt.replace('href="../css/', 'href="/css/')
        txt = txt.replace('href="../index.html"', 'href="/herramientas/"')
        txt = txt.replace('href="/"', 'href="/en/"')
        txt = re.sub(r'<script[^>]*geo-lang-detect[^>]*></script>', '', txt)
        dest_file.write_text(txt, encoding="utf-8")
        print("en/tools/index.html built.")

def build_english_about_us():
    print("Building en/about-us/index.html...")
    src_about = ROOT / "dist" / "sobre-nosotros" / "index.html"
    dest_dir = ROOT / "en" / "about-us"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "index.html"

    if not src_about.exists():
        print("Warning: dist/sobre-nosotros/index.html not found.")
        return

    txt = src_about.read_text(encoding="utf-8")
    
    # Update lang and canonical
    txt = txt.replace('<html lang="es"', '<html lang="en"')
    txt = re.sub(r'<title>.*?</title>', '<title>About Us: Digital Infrastructure Experts | SMB Cloud</title>', txt)
    txt = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', '<meta name="description" content="Meet SMB Cloud (Nube para Pymes). We help small businesses make informed software decisions through objective reviews, benchmarks, and free web tools." />', txt)
    txt = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']\s*/?>', '<link rel="canonical" href="https://nubeparapymes.online/en/about-us/" />', txt)

    # Translations of headings and content
    txt = txt.replace('No somos un blog de consejos. Somos tu Motor de Infraestructura Digital.', 'We are not just a tips blog. We are your Digital Infrastructure Engine.')
    txt = txt.replace('NubeParaPymes nació para resolver un problema crítico en el sector B2B: la falta de datos empíricos en la elección de software. Nuestra misión es proporcionar a las empresas la arquitectura tecnológica necesaria para automatizar sus flujos de trabajo y maximizar la eficiencia operativa.', 'SMB Cloud was born to solve a critical problem in the business sector: the lack of empirical data when choosing software. Our mission is to provide companies with the technical architecture needed to automate workflows and maximize operational efficiency.')
    txt = txt.replace('NubeParaPymes naci&oacute; para resolver un problema cr&iacute;tico en el sector B2B: la falta de datos emp&iacute;ricos en la elecci&oacute;n de software. Nuestra misi&oacute;n es proporcionar a las empresas la arquitectura tecnol&oacute;gica necesaria para automatizar sus flujos de trabajo y maximizar la eficiencia operativa.', 'SMB Cloud was born to solve a critical problem in the business sector: the lack of empirical data when choosing software. Our mission is to provide companies with the technical architecture needed to automate workflows and maximize operational efficiency.')
    txt = txt.replace('Decisiones basadas en Arquitectura, no en Opiniones', 'Decisions Based on Architecture, Not Opinions')
    txt = txt.replace('Analizamos el software desde una perspectiva de ingeniería y negocio. Evaluamos la capacidad de integración, la escalabilidad y la robustez de cada herramienta. Ayudamos a los dueños de Pymes y directores de operaciones a elegir el stack tecnológico exacto para escalar sin fricciones técnicas.', 'We evaluate software from an engineering and business perspective. We assess integration capabilities, scalability, and robustness for every tool. We help SMB owners and operations leaders choose the exact tech stack to scale without technical friction.')
    txt = txt.replace('Analizamos el software desde una perspectiva de ingenier&iacute;a y negocio. Evaluamos la capacidad de integraci&oacute;n, la escalabilidad y la robustez de cada herramienta. Ayudamos a los due&ntilde;os de Pymes y directores de operaciones a elegir el stack tecnol&oacute;gico exacto para escalar sin fricciones t&eacute;cnicas.', 'We evaluate software from an engineering and business perspective. We assess integration capabilities, scalability, and robustness for every tool. We help SMB owners and operations leaders choose the exact tech stack to scale without technical friction.')
    txt = txt.replace('Política de Transparencia Radical', 'Radical Transparency Policy')
    txt = txt.replace('Pol&iacute;tica de Transparencia Radical', 'Radical Transparency Policy')
    txt = txt.replace('Para mantener esta plataforma gratuita y operativa, utilizamos enlaces de afiliados. Esto significa que si implementas un sistema a través de nosotros, generamos una comisión. Sin embargo, nuestras comparativas se basan en datos duros, precios reales y pruebas de estrés objetivas. Nuestra integridad técnica es el motor de nuestro negocio.', 'To keep this platform free and accessible, we use affiliate links. This means that if you adopt software through our recommendations, we may earn a commission. However, our reviews and comparisons are strictly based on empirical benchmarks, transparent pricing, and objective stress testing. Technical integrity is our primary foundation.')
    txt = txt.replace('Para mantener esta plataforma gratuita y operativa, utilizamos enlaces de afiliados. Esto significa que si implementas un sistema a trav&eacute;s de nosotros, generamos una comisi&oacute;n. Sin embargo, nuestras comparativas se basan en datos duros, precios reales y pruebas de estr&eacute;s objetivas. Nuestra integridad t&eacute;cnica es el motor de nuestro negocio.', 'To keep this platform free and accessible, we use affiliate links. This means that if you adopt software through our recommendations, we may earn a commission. However, our reviews and comparisons are strictly based on empirical benchmarks, transparent pricing, and objective stress testing. Technical integrity is our primary foundation.')
    txt = txt.replace('¿Por qué confiar en NubeParaPymes?', 'Why Trust SMB Cloud?')
    txt = txt.replace('&iquest;Por qu&eacute; confiar en NubeParaPymes?', 'Why Trust SMB Cloud?')
    txt = txt.replace('Pruebas de Estrés Reales:', 'Real-World Stress Testing:')
    txt = txt.replace('Pruebas de Estr&eacute;s Reales:', 'Real-World Stress Testing:')
    txt = txt.replace('No nos limitamos a leer la documentación; sometemos a cada herramienta a flujos de trabajo reales.', 'We do not simply read marketing copy; we deploy each tool in realistic small business workflows.')
    txt = txt.replace('No nos limitamos a leer la documentaci&oacute;n; sometemos a cada herramienta a flujos de trabajo reales.', 'We do not simply read marketing copy; we deploy each tool in realistic small business workflows.')
    txt = txt.replace('Enfoque en Integraciones:', 'Integration-First Approach:')
    txt = txt.replace('Evaluamos qué tan bien se conecta el software con tu ecosistema actual.', 'We examine how cleanly each platform integrates with your existing workflow, APIs, and tools.')
    txt = txt.replace('Evaluamos qu&eacute; tan bien se conecta el software con tu ecosistema actual.', 'We examine how cleanly each platform integrates with your existing workflow, APIs, and tools.')
    txt = txt.replace('Actualización Constante:', 'Continuous Updates:')
    txt = txt.replace('Actualizaci&oacute;n Constante:', 'Continuous Updates:')
    txt = txt.replace('La tecnología avanza rápido, y nuestras comparativas también.', 'SaaS features and pricing change quickly, and our benchmarks are constantly updated.')
    txt = txt.replace('La tecnolog&iacute;a avanza r&aacute;pido, y nuestras comparativas tambi&eacute;n.', 'SaaS features and pricing change quickly, and our benchmarks are constantly updated.')

    # Navigation bar in English
    txt = txt.replace('>Sobre Nosotros<', '>About Us<')
    txt = txt.replace('>Herramientas Gratis<', '>Free Tools<')
    txt = txt.replace('>Categorías<', '>Categories<')
    txt = txt.replace('>Categor&iacute;as<', '>Categories<')
    txt = txt.replace('href="/herramientas/"', 'href="/en/tools/"')
    txt = txt.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    txt = txt.replace('href="/"', 'href="/en/"')

    dest_file.write_text(txt, encoding="utf-8")
    print("en/about-us/index.html built.")

def build_english_homepage():
    print("Building en/index.html (English Homepage)...")
    src_home = ROOT / "dist" / "index.html"
    dest_file = ROOT / "en" / "index.html"

    if not src_home.exists():
        src_home = ROOT / "nubepymesexport" / "index.html"
    
    txt = src_home.read_text(encoding="utf-8")

    # Basic language and meta replacements
    txt = txt.replace('<html lang="es"', '<html lang="en"')
    txt = re.sub(r'<title>.*?</title>', '<title>SMB Cloud: Software Reviews, Guides & Free Business Tools</title>', txt)
    txt = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>', '<meta name="description" content="Digital infrastructure portal for small businesses. Objective software comparisons, automation guides, and 26 free business tools to scale your company." />', txt)
    txt = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']\s*/?>', '<link rel="canonical" href="https://nubeparapymes.online/en/" />', txt)

    # Clean out any geo-lang-detect script or aside
    txt = re.sub(r'<script[^>]*geo-lang-detect[^>]*></script>', '', txt)
    txt = re.sub(r'<aside[^>]*np-lang-switch-floating[^>]*>[\s\S]*?</aside>', '', txt)

    # Navigation translations
    txt = txt.replace('>Herramientas Gratis<', '>Free Tools<')
    txt = txt.replace('>Sobre Nosotros<', '>About Us<')
    txt = txt.replace('>Categorías<', '>Categories<')
    txt = txt.replace('>Categor&iacute;as<', '>Categories<')
    txt = txt.replace('href="/herramientas/"', 'href="/en/tools/"')
    txt = txt.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    txt = txt.replace('href="/"', 'href="/en/"')

    # Dropdown menu items
    txt = txt.replace('Automatización y productividad con IA', 'AI Automation & Productivity')
    txt = txt.replace('Automatizaci&oacute;n y productividad con IA', 'AI Automation & Productivity')
    txt = txt.replace('Comunicación y colaboración', 'Team Communication & Collaboration')
    txt = txt.replace('Comunicaci&oacute;n y colaboraci&oacute;n', 'Team Communication & Collaboration')
    txt = txt.replace('CRM y gestión de clientes', 'CRM & Customer Management')
    txt = txt.replace('CRM y gesti&oacute;n de clientes', 'CRM & Customer Management')
    txt = txt.replace('Facturación y contabilidad', 'Invoicing & Accounting')
    txt = txt.replace('Facturaci&oacute;n y contabilidad', 'Invoicing & Accounting')
    txt = txt.replace('Gestión de proyectos y tareas', 'Project & Task Management')
    txt = txt.replace('Gesti&oacute;n de proyectos y tareas', 'Project & Task Management')
    txt = txt.replace('Software por sector específico', 'Industry-Specific Software')
    txt = txt.replace('Software por sector espec&iacute;fico', 'Industry-Specific Software')

    # Hero section translations
    txt = txt.replace('INFRAESTRUCTURA DIGITAL PARA PYMES', 'DIGITAL INFRASTRUCTURE FOR SMBS')
    txt = txt.replace('Guías de Software y Herramientas Gratuitas', 'Software Guides & Free Business Tools')
    txt = txt.replace('Gu&iacute;as de Software y Herramientas Gratuitas', 'Software Guides & Free Business Tools')
    txt = txt.replace('para tu Pequeña Empresa', 'for Small & Growing Businesses')
    txt = txt.replace('para tu Peque&ntilde;a Empresa', 'for Small & Growing Businesses')
    txt = txt.replace('Comparativas independientes, guías de automatización paso a paso y 26 herramientas web locales sin registro para elegir y operar el software que tu negocio necesita.', 'Independent software comparisons, practical step-by-step guides, and 26 browser-based business tools with zero login, designed to help small businesses choose and operate the right technology.')
    txt = txt.replace('Comparativas independientes, gu&iacute;as de automatizaci&oacute;n paso a paso y 26 herramientas web locales sin registro para elegir y operar el software que tu negocio necesita.', 'Independent software comparisons, practical step-by-step guides, and 26 browser-based business tools with zero login, designed to help small businesses choose and operate the right technology.')
    txt = txt.replace('Explorar 26 Herramientas Gratis', 'Explore 26 Free Tools')
    txt = txt.replace('Ver Guías y Comparativas', 'Browse Guides & Reviews')
    txt = txt.replace('Ver Gu&iacute;as y Comparativas', 'Browse Guides & Reviews')

    # Stats section
    txt = txt.replace('Artículos y comparativas publicados', 'In-depth guides & comparisons')
    txt = txt.replace('Art&iacute;culos y comparativas publicados', 'In-depth guides & comparisons')
    txt = txt.replace('Herramientas interactivas gratis', 'Free interactive business tools')
    txt = txt.replace('Local y privado (sin registro)', 'Local & private (zero login)')
    txt = txt.replace('Costo para pequeñas empresas', 'Cost for small businesses')
    txt = txt.replace('Costo para peque&ntilde;as empresas', 'Cost for small businesses')

    # Bento section
    txt = txt.replace('COMPARATIVAS DE SOFTWARE', 'SOFTWARE REVIEWS')
    txt = txt.replace('Elegir software sin perder tiempo ni dinero', 'Choose the Right Software Without Guesswork')
    txt = txt.replace('Evaluamos CRM, gestión de proyectos, facturación y comunicación con criterios de ingeniería y costos reales para pymes.', 'We evaluate CRM, project management, invoicing, and team collaboration with real-world testing and transparent pricing.')
    txt = txt.replace('AUTOMATIZACIÓN CON IA', 'AI & AUTOMATION')
    txt = txt.replace('Automatizar tareas repetitivas con criterio', 'Automate Repetitive Business Tasks')
    txt = txt.replace('Guías prácticas para conectar herramientas con Make y Zapier, usar chatbots con sentido y reducir horas de trabajo administrativo.', 'Practical guides to connect software via Zapier and Make, deploy useful chatbots, and reclaim wasted administrative hours.')

    # Tools carousel section
    txt = txt.replace('HERRAMIENTAS LOCALES Y PRIVADAS', 'LOCAL & PRIVATE BROWSER TOOLS')
    txt = txt.replace('26 herramientas gratuitas listas para usar', '26 Free Business Tools Ready in Seconds')
    txt = txt.replace('Sin registro, sin enviar tus datos a ningún servidor y con exportación directa a Excel, CSV y PDF.', 'Zero login, zero data sent to external servers, and instant export to Excel, CSV, and PDF.')
    txt = txt.replace('Ver todas las herramientas', 'View all 26 free tools')
    txt = txt.replace('Ver todas las 26 herramientas', 'View all 26 free tools')

    # Tool names in rail
    txt = txt.replace('Calculadora de Precios e IGV', 'Sales Pricing & Tax Calculator')
    txt = txt.replace('Calculadora de Descuentos', 'Discount & Promotions Calculator')
    txt = txt.replace('Calculadora de Envíos Locales', 'Local Shipping Calculator')
    txt = txt.replace('Calculadora de Env&iacute;os Locales', 'Local Shipping Calculator')
    txt = txt.replace('Calculadora de Préstamos', 'Loan Amortization Calculator')
    txt = txt.replace('Calculadora de Pr&eacute;stamos', 'Loan Amortization Calculator')
    txt = txt.replace('Calculadora de Sobrecostos Laborales', 'Labor Cost & Payroll Burden Calculator')
    txt = txt.replace('Simulador TCO: Físico vs Nube', 'Cloud vs On-Premises TCO Simulator')
    txt = txt.replace('Simulador TCO: F&iacute;sico vs Nube', 'Cloud vs On-Premises TCO Simulator')
    txt = txt.replace('CRM para Pymes', 'SMB CRM')
    txt = txt.replace('Generador de Cotizaciones', 'Quote & Estimate Generator')
    txt = txt.replace('Creador de Facturas Proforma', 'Proforma Invoice Generator')
    txt = txt.replace('Control de Flujo de Caja', 'Cash Flow Tracker')
    txt = txt.replace('Gestor de Tareas y Proyectos', 'Tasks & Projects Tracker')
    txt = txt.replace('Control de Inventario y Compras', 'Inventory & Purchasing Manager')
    txt = txt.replace('Conversor y Optimizador de Imágenes', 'Image Converter & Optimizer')
    txt = txt.replace('Conversor y Optimizador de Im&aacute;genes', 'Image Converter & Optimizer')
    txt = txt.replace('Generador de Códigos QR', 'QR Code Generator')
    txt = txt.replace('Generador de C&oacute;digos QR', 'QR Code Generator')

    # Comparisons section
    txt = txt.replace('DECISIONES DE SOFTWARE', 'SOFTWARE COMPARISONS')
    txt = txt.replace('Comparativas directas entre las herramientas líderes', 'Side-by-Side Comparisons of Leading Tools')
    txt = txt.replace('Las comparativas más consultadas', 'Most Popular Comparisons')
    txt = txt.replace('Las comparativas m&aacute;s consultadas', 'Most Popular Comparisons')
    txt = txt.replace('Ver todas las comparativas', 'Browse all software comparisons')

    # Replace links to Spanish posts with English post links
    import json
    slug_map_file = ROOT / "scripts" / "posts_slug_map.json"
    if slug_map_file.exists():
        es_to_en = json.loads(slug_map_file.read_text(encoding="utf-8"))
        for es_slug, en_slug in es_to_en.items():
            txt = txt.replace(f'href="/{es_slug}/"', f'href="/en/{en_slug}/"')

    # Replace tool links
    tool_map = {
        "crm-pymes": "smb-crm",
        "generador-cotizaciones": "quote-estimate-generator",
        "creador-facturas-proforma": "proforma-invoice-generator",
        "flujo-caja-pymes": "cash-flow-tracker",
        "tareas-proyectos-pymes": "tasks-projects-tracker",
        "inventario-compras-pymes": "inventory-purchasing",
        "calculadora-precios-venta-igv": "sales-pricing-tax-calculator",
        "calculadora-descuentos-promociones": "discount-promotions-calculator",
        "calculadora-flete-envio-local": "local-shipping-calculator",
        "calculadora-prestamos-amortizaciones": "loan-amortization-calculator",
        "calculadora-sobrecostos-laborales": "labor-cost-payroll-burden-calculator",
        "simulador-tco-fisico-nube": "cloud-vs-onprem-tco-simulator",
        "conversor-optimizador-imagenes": "image-converter-optimizer",
        "generador-codigos-qr": "qr-code-generator",
        "generador-contrasenas-pymes": "smb-password-generator",
        "firma-correo-html": "html-email-signature",
        "generador-paletas-corporativas": "brand-palette-generator",
        "analizador-titulares": "headline-analyzer",
        "auditor-seo-basico": "basic-on-page-seo-auditor",
        "consola-campanas": "campaign-utm-console",
        "comparador-campanas-avanzado": "advanced-campaign-comparator",
        "organizador-matriz-contenidos": "content-matrix-planner",
        "generador-politicas-terminos": "terms-privacy-generator",
        "generador-politicas-devolucion": "return-policy-generator",
        "generador-contratos-servicios": "service-contracts-generator",
        "guiones-manejo-objeciones": "objection-handling-scripts",
    }
    for es_t, en_t in tool_map.items():
        txt = re.sub(rf'href=["\']/herramientas/[^/]+/{es_t}/?["\']', f'href="/en/{en_t}.html"', txt)

    # How we work section
    txt = txt.replace('CÓMO TRABAJAMOS', 'HOW WE WORK')
    txt = txt.replace('C&Oacute;MO TRABAJAMOS', 'HOW WE WORK')
    txt = txt.replace('Criterio técnico, pruebas reales y transparencia', 'Technical Rigor, Real Tests & Transparency')
    txt = txt.replace('Criterio t&eacute;cnico, pruebas reales y transparencia', 'Technical Rigor, Real Tests & Transparency')
    txt = txt.replace('Diseñado y Desarrollado por', 'Designed and Developed by')
    txt = txt.replace('Dise&ntilde;ado y Desarrollado por', 'Designed and Developed by')

    dest_file.write_text(txt, encoding="utf-8")
    print("en/index.html built successfully.")

if __name__ == "__main__":
    build_english_tools_portal()
    build_english_about_us()
    build_english_homepage()
