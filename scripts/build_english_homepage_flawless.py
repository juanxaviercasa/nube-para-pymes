import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent

TRANSLATIONS = [
    # Hero
    ("¿Qué está frenando el crecimiento de", "What is holding back the growth of"),
    ("tu negocio", "your business"),
    ("Herramientas gratuitas y comparativas para que tu pyme consiga más clientes y deje de perder horas en tareas repetitivas.",
     "Free interactive tools and objective software guides to help your small business acquire more clients and eliminate repetitive administrative work."),
    ("Abrir herramientas", "Open Free Tools"),
    ("Ver por problema", "Solve by Problem"),

    # Stats
    ("herramientas gratuitas", "free interactive tools"),
    ("artículos publicados", "in-depth guides & reviews"),
    ("registros obligatorios", "signups or accounts required"),
    ("uso sin límite", "unlimited browser use"),

    # Problem Bento
    ("EMPIEZA POR AQUÍ", "START HERE"),
    ("EMPIEZA POR AQU&Iacute;", "START HERE"),
    ("Dinos qué necesitas resolver", "Tell us what you need to solve"),
    ("Dinos qu&eacute; necesitas resolver", "Tell us what you need to solve"),
    ("No empieces buscando software. Empieza por el problema: te llevamos a la herramienta, la guía o la comparativa que corresponde.",
     "Don't start by searching for software. Start with the problem: we guide you to the exact tool, walkthrough, or benchmark you need."),
    ("Conseguir más clientes", "Acquire More Clients"),
    ("Conseguir m&aacute;s clientes", "Acquire More Clients"),
    ("Llegan consultas, pero se enfrían antes de cerrar y nadie recuerda a quién le faltaba respuesta.",
     "Leads arrive but go cold before closing, and nobody remembers who needed follow-up."),
    ("Generar una cotización profesional", "Generate a Professional Quote"),
    ("Generar una cotizaci&oacute;n profesional", "Generate a Professional Quote"),
    ("Comparar CRMs para pymes", "Compare SMB CRMs"),
    ("Cómo pasar de Excel a un CRM", "How to Migrate from Excel to a CRM"),
    ("C&oacute;mo pasar de Excel a un CRM", "How to Migrate from Excel to a CRM"),
    ("Cobrar y facturar mejor", "Invoice & Price Accurately"),
    ("No sabes con certeza si el precio que pusiste deja margen después del IGV y los costos.",
     "You're unsure whether your pricing leaves real profit margin after taxes and overhead."),
    ("Calcular precio con IGV y margen", "Calculate Price, Tax & Net Margin"),
    ("Crear una proforma", "Create a Proforma Invoice"),
    ("Cómo facturar siendo independiente en Perú", "How to Invoice as an Independent Professional"),
    ("C&oacute;mo facturar siendo independiente en Per&uacute;", "How to Invoice as an Independent Professional"),
    ("Atender WhatsApp sin perder mensajes", "Handle WhatsApp Without Losing Leads"),
    ("Todo el negocio pasa por un celular y las consultas se entierran entre conversaciones.",
     "The entire business runs on one phone, and inquiries get buried under chats."),
    ("Crear enlace y QR", "Generate WhatsApp Link & QR"),
    ("CRMs con WhatsApp", "CRMs with WhatsApp"),
    ("Qué hace un CRM con WhatsApp integrado", "What a WhatsApp-Integrated CRM Does"),
    ("Qu&eacute; hace un CRM con WhatsApp integrado", "What a WhatsApp-Integrated CRM Does"),
    ("Automatizar lo repetitivo", "Automate Repetitive Work"),
    ("Copiar datos de un lado a otro y rehacer el mismo documento cada semana.",
     "Copy-pasting data between apps and rebuilding the exact same documents every week."),
    ("Planificar contenidos", "Plan Content Matrix"),
    ("Herramientas de IA para automatizar tareas", "AI Tools to Automate Business Tasks"),
    ("Cumplir con lo legal", "Stay Legally Compliant"),
    ("Tu web o tienda necesita documentos obligatorios y no vas a redactarlos desde cero.",
     "Your website or store requires mandatory legal policies and you shouldn't draft them from scratch."),
    ("Políticas y términos", "Terms & Privacy Generator"),
    ("Pol&iacute;ticas y t&eacute;rminos", "Terms & Privacy Generator"),
    ("Contrato de servicios", "Service Agreement Generator"),
    ("Aparecer en Google", "Get Found on Google"),
    ("Tu web existe, pero nadie la encuentra cuando buscan exactamente lo que vendes. Empieza revisando qué está viendo Google de tu página.",
     "Your website exists, but nobody finds it when searching for what you sell. Start by analyzing how search engines see your pages."),
    ("Auditar una página", "Audit a Web Page"),
    ("Auditar una p&aacute;gina", "Audit a Web Page"),
    ("Evaluar un titular", "Evaluate a Headline"),

    # Tools Carousel
    ("22 herramientas que funcionan en tu navegador", "26 Free Tools Running Directly in Your Browser"),
    ("26 herramientas que funcionan en tu navegador", "26 Free Tools Running Directly in Your Browser"),
    ("Calculadoras y generadores que resuelven una tarea concreta en menos de dos minutos. No se instalan y no piden cuenta.",
     "Calculators and generators that solve a specific task in under two minutes. No installation, zero login required."),
    ("Generador de Cotizaciones", "Quote & Estimate Generator"),
    ("Propuestas en PDF con tu marca", "Branded proposals exported to PDF"),
    ("Precios con IGV", "Sales Pricing & Tax"),
    ("Margen neto separando impuestos", "Net margin separating taxes"),
    ("Sobrecostos Laborales", "Labor & Payroll Costs"),
    ("CTS, gratificaciones y aportes", "Benefits, deductions and real employer burden"),
    ("Enlaces y QR de WhatsApp", "WhatsApp Links & QR Codes"),
    ("Chat directo desde cualquier parte", "Direct chat buttons and QR codes"),
    ("Políticas y Términos", "Legal Policies & Terms"),
    ("Pol&iacute;ticas y T&eacute;rminos", "Legal Policies & Terms"),
    ("Documentos legales obligatorios", "Essential compliant documents"),
    ("Auditor SEO", "SEO Page Auditor"),
    ("Títulos y metaetiquetas en un clic", "Page title & meta tags check in one click"),
    ("T&iacute;tulos y metaetiquetas en un clic", "Page title & meta tags check in one click"),
    ("Facturas Proforma", "Proforma Invoice Generator"),
    ("Propuestas rápidas al instante", "Instant commercial invoices & estimates"),
    ("Propuestas r&aacute;pidas al instante", "Instant commercial invoices & estimates"),
    ("Flete Local", "Local Shipping Calculator"),
    ("Peso real contra volumétrico", "Actual weight vs dimensional weight"),
    ("Peso real contra volum&eacute;trico", "Actual weight vs dimensional weight"),
    ("Ver las 22", "View All 26 Free Tools"),
    ("Ver las 26", "View All 26 Free Tools"),
    ("Marketing, finanzas, ventas y legal", "Marketing, finance, sales and operations"),

    # Comparisons
    ("COMPARATIVAS", "SOFTWARE REVIEWS"),
    ("Software comparado con precios reales", "Business Software Compared with Real Pricing"),
    ("Probamos las herramientas, revisamos los planes gratuitos de verdad y decimos para qué tamaño de negocio sirve cada una. En soles cuando el proveedor cobra en soles.",
     "We test software thoroughly, scrutinize free tiers, and determine exactly which company size each fits best—highlighting local currency when billed locally."),
    ("Algunas recomendaciones incluyen enlaces de afiliado. No cambian el precio que pagas y no influyen en el orden de nuestras comparativas.",
     "Some recommendations include affiliate links. They never increase the price you pay and never influence our editorial rankings."),
    ("Cómo evaluamos", "Our Review Methodology"),
    ("C&oacute;mo evaluamos", "Our Review Methodology"),
    ("CRMs para pymes peruanas", "Best CRMs for Small Businesses"),
    ("Comparamos 12 opciones por precio real, límite del plan gratuito, integración con WhatsApp y facilidad de uso sin equipo técnico.",
     "We compared 12 platforms by real pricing, free plan limits, WhatsApp integration, and ease of use without an IT team."),
    ("Ver la comparativa completa", "Read Full Comparison"),
    ("CRMs con WhatsApp integrado", "CRMs with WhatsApp Integration"),
    ("Facturación electrónica para pymes", "Electronic Invoicing for SMBs"),
    ("Facturaci&oacute;n electr&oacute;nica para pymes", "Electronic Invoicing for SMBs"),
    ("Software de gestión de proyectos", "Project Management Software"),
    ("Software de gesti&oacute;n de proyectos", "Project Management Software"),
    ("Plataformas de tienda online", "E-commerce Platforms"),
    ("Ver todas las comparativas", "View All Comparisons"),

    # Industry Sectors
    ("¿Tienes un negocio de un sector concreto?", "Operating in a Specific Industry?"),
    ("&iquest;Tienes un negocio de un sector concreto?", "Operating in a Specific Industry?"),
    ("Hay decisiones que solo tienen sentido dentro de tu rubro. Estas son las que ya analizamos.",
     "Certain software decisions only make sense within your specific vertical. Here is what we've analyzed."),
    ("Restaurantes", "Restaurants"),
    ("Gimnasios y estudios", "Gyms & Fitness Studios"),
    ("Despachos de abogados", "Law Firms"),
    ("Inmobiliarias", "Real Estate Agencies"),
    ("Clínicas y consultorios", "Medical & Dental Clinics"),
    ("Cl&iacute;nicas y consultorios", "Medical & Dental Clinics"),
    ("Academias online", "Online Academies"),
    ("Tiendas online", "E-Commerce Stores"),
    ("Profesores particulares", "Private Tutors & Coaches"),
    ("Ver los 15 análisis por sector", "View All 15 Industry Guides"),
    ("Ver los 15 an&aacute;lisis por sector", "View All 15 Industry Guides"),

    # Featured Articles
    ("Por dónde empezar a leer", "Where to Start Reading"),
    ("Por d&oacute;nde empezar a leer", "Where to Start Reading"),
    ("Cinco artículos que responden las preguntas que más nos llegan.",
     "Five in-depth guides answering the questions we receive most often."),
    ("Cinco art&iacute;culos que responden las preguntas que m&aacute;s nos llegan.",
     "Five in-depth guides answering the questions we receive most often."),
    ("Qué es un CRM y para qué sirve realmente", "What is a CRM and Why Does Your Business Need One?"),
    ("Qu&eacute; es un CRM y para qu&eacute; sirve realmente", "What is a CRM and Why Does Your Business Need One?"),
    ("Qué es, qué hace y cuándo empieza a valer la pena.", "Core features, realistic benefits, and when it becomes worth the investment."),
    ("Qu&eacute; es, qu&eacute; hace y cu&aacute;ndo empieza a valer la pena.", "Core features, realistic benefits, and when it becomes worth the investment."),
    ("Cómo migrar de Excel a un CRM sin perder datos", "How to Migrate from Excel to a CRM Without Data Loss"),
    ("C&oacute;mo migrar de Excel a un CRM sin perder datos", "How to Migrate from Excel to a CRM Without Data Loss"),
    ("El paso a paso para cambiar sin perder tus contactos.", "Step-by-step walkthrough to transition contacts and pipeline cleanly."),
    ("Facturación", "Invoicing"),
    ("Facturaci&oacute;n", "Invoicing"),
    ("Facturación electrónica para independientes", "Electronic Invoicing for Freelancers & Contractors"),
    ("Facturaci&oacute;n electr&oacute;nica para independientes", "Electronic Invoicing for Freelancers & Contractors"),
    ("Lo que necesitas para emitir tus primeros comprobantes.", "Everything required to issue compliant invoices seamlessly."),
    ("Automatización", "Automation"),
    ("Automatizaci&oacute;n", "Automation"),
    ("Cuáles sirven de verdad y para qué tarea usar cada una.", "Which tools actually work and which specific workflows to automate."),
    ("Cu&aacute;les sirven de verdad y para qu&eacute; tarea usar cada una.", "Which tools actually work and which specific workflows to automate."),
    ("Gestión", "Project Management"),
    ("Gesti&oacute;n", "Project Management"),
    ("Alternativas gratuitas a Notion", "Best Free Alternatives to Notion"),
    ("Opciones que ordenan tu trabajo sin pagar suscripción.", "Clean solutions to organize your team without paying monthly fees."),
    ("Opciones que ordenan tu trabajo sin pagar suscripci&oacute;n.", "Clean solutions to organize your team without paying monthly fees."),
    ("Ver los 70 artículos", "Browse All 70 Guides"),
    ("Ver los 70 art&iacute;culos", "Browse All 70 Guides"),

    # How we work
    ("CÓMO TRABAJAMOS", "HOW WE WORK"),
    ("C&Oacute;MO TRABAJAMOS", "HOW WE WORK"),
    ("Primero resolver, después recomendar", "Solve the Problem First, Recommend Tools Second"),
    ("Primero resolver, despu&eacute;s recomendar", "Solve the Problem First, Recommend Tools Second"),
    ("No vendemos software. Probamos herramientas, escribimos lo que aprendemos y construimos utilidades gratuitas con lo que más nos piden.",
     "We don't sell software. We rigorously test tools, document what we learn, and build free web utilities based on real business requests."),
    ("Resuelves la tarea", "1. Solve the Immediate Task"),
    ("Usas la herramienta que necesitas y te llevas el documento o el cálculo. Gratis, sin cuenta y sin límite de veces.",
     "Use the utility you need and download your calculations or documents. 100% free, zero login, no usage limits."),
    ("Entiendes el problema de fondo", "2. Understand the Root Cause"),
    ("Nuestros artículos explican por qué esa tarea se repite y qué la ordena de verdad, no solo qué botón apretar.",
     "Our guides analyze why repetitive friction happens and how to structure your workflow systematically."),
    ("Eliges con criterio", "3. Choose the Right Stack"),
    ("Si al final necesitas software, comparamos opciones con precios reales y te decimos también cuándo no vale la pena cambiar.",
     "When you do need software, we compare real pricing and candidly tell you when upgrading isn't worth it."),

    # Author
    ("Profesor de Matemáticas · Desarrollador Web · Marketer Digital · Especialista en IA & Web Apps",
     "Mathematics Professor · Full-Stack Developer · Digital Marketer · AI & Web Applications Specialist"),
    ("Combino el rigor analítico de las matemáticas con el desarrollo web moderno y la inteligencia artificial para crear aplicaciones ágiles, útiles y de alto rendimiento. Fundé",
     "I combine analytical mathematical rigor with modern web engineering and artificial intelligence to build fast, high-impact business tools. I founded"),
    ("con el propósito de democratizar la tecnología y automatización para pequeñas empresas, transformando procesos complejos en soluciones digitales simples que ahorran tiempo y maximizan ventas.",
     "to democratize technology and workflow automation for small businesses, turning complex operational hurdles into simple digital solutions that save hours and drive revenue."),
    ("Conoce más sobre mi trabajo y proyectos →", "Discover more about my work and portfolio →"),
    ("Conoce m&aacute;s sobre mi trabajo y proyectos &rarr;", "Discover more about my work and portfolio &rarr;"),

    # Newsletter & Footer
    ("Te avisamos cuando publicamos una comparativa nueva", "Get Notified When We Release New Software Benchmarks"),
    ("Una vez al mes como máximo. Sin promociones de terceros.", "At most once a month. Zero third-party spam."),
    ("Correo electrónico", "Your email address"),
    ("Correo electr&oacute;nico", "Your email address"),
    ("Quiero recibirlas", "Subscribe Free"),
    ("Puedes darte de baja en un clic.", "Unsubscribe anytime with one click."),
    ("Cómo tratamos tus datos", "Privacy policy"),
    ("C&oacute;mo tratamos tus datos", "Privacy policy"),
    ("Empieza por donde más te duele", "Start Where the Friction Hurts Most"),
    ("Empieza por donde m&aacute;s te duele", "Start Where the Friction Hurts Most"),
    ("Resuelve algo hoy y vuelve cuando aparezca el siguiente problema.", "Solve one operational bottleneck today, and return whenever the next challenge arises."),
]

def build_perfect_english_homepage():
    print("Building English homepage with complete text translation...")
    src_path = ROOT / "dist" / "index.html"
    content = src_path.read_text(encoding="utf-8")

    # 1. Update HTML language and metadata
    content = content.replace('<html lang="es"', '<html lang="en"')
    content = re.sub(r'<title>.*?</title>', '<title>SMB Cloud: Software Reviews, Guides & Free Business Tools</title>', content)
    content = re.sub(
        r'<meta\s+name=["\']description["\']\s+content=["\'].*?["\']\s*/?>',
        '<meta name="description" content="Digital infrastructure portal for small businesses. Objective software comparisons, automation guides, and 26 free business tools to scale your company." />',
        content
    )
    content = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'].*?["\']\s*/?>',
        '<link rel="canonical" href="https://nubeparapymes.online/en/" />',
        content
    )

    # 2. Navigation items
    content = content.replace('>Herramientas Gratis<', '>Free Tools<')
    content = content.replace('>Sobre Nosotros<', '>About Us<')
    content = content.replace('>Categorías<', '>Categories<')
    content = content.replace('>Categor&iacute;as<', '>Categories<')
    content = content.replace('Automatización y productividad con IA', 'AI Automation & Productivity')
    content = content.replace('Automatizaci&oacute;n y productividad con IA', 'AI Automation & Productivity')
    content = content.replace('Comunicación y colaboración', 'Team Communication & Collaboration')
    content = content.replace('Comunicaci&oacute;n y colaboraci&oacute;n', 'Team Communication & Collaboration')
    content = content.replace('CRM y gestión de clientes', 'CRM & Customer Management')
    content = content.replace('CRM y gesti&oacute;n de clientes', 'CRM & Customer Management')
    content = content.replace('Facturación y contabilidad', 'Invoicing & Accounting')
    content = content.replace('Facturaci&oacute;n y contabilidad', 'Invoicing & Accounting')
    content = content.replace('Gestión de proyectos y tareas', 'Project & Task Management')
    content = content.replace('Gesti&oacute;n de proyectos y tareas', 'Project & Task Management')
    content = content.replace('Software por sector específico', 'Industry-Specific Software')
    content = content.replace('Software por sector espec&iacute;fico', 'Industry-Specific Software')

    # 3. Apply all body translations
    applied = 0
    for es_text, en_text in TRANSLATIONS:
        if es_text in content:
            content = content.replace(es_text, en_text)
            applied += 1

    print(f"Applied {applied}/{len(TRANSLATIONS)} homepage translations.")

    # 4. Update internal links for English
    content = content.replace('href="/herramientas/"', 'href="/en/tools/"')
    content = content.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')
    content = content.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    content = content.replace('href="/que-es-un-crm-para-que-sirve/"', 'href="/en/what-is-a-crm-guide/"')
    content = content.replace('href="/como-migrar-de-excel-a-un-crm/"', 'href="/en/how-to-migrate-excel-to-crm/"')
    content = content.replace('href="/facturacion-electronica-independientes-peru/"', 'href="/en/freelance-invoicing-peru-guide/"')
    content = content.replace('href="/herramientas-ia-para-automatizar-tareas-pymes/"', 'href="/en/ai-tools-automate-business-tasks/"')
    content = content.replace('href="/alternativas-gratuitas-a-notion/"', 'href="/en/free-notion-alternatives/"')
    content = content.replace('href="/crm-para-pymes/"', 'href="/en/best-free-crm-platforms/"')

    # Reemplazo de enlaces de herramientas interactivas
    from fix_multilingual_issues import TOOLS_MAP
    for slug, info in TOOLS_MAP.items():
        canonical_es = f"/herramientas/{info['cat']}/{info['slug']}/"
        canonical_en = f"/en/{info['en_slug']}.html"
        content = content.replace(f'href="{canonical_es}"', f'href="{canonical_en}"')
        content = content.replace(f"href='{canonical_es}'", f"href='{canonical_en}'")

    content = content.replace('href="/herramientas/auditor-basico-de-seo-on-page/"', 'href="/en/basic-on-page-seo-auditor.html"')
    content = content.replace('href="/herramientas/calculadora-de-precios-de-venta-con-igv/"', 'href="/en/sales-pricing-tax-calculator.html"')


    # 5. Fix switcher inside English homepage to link back to Spanish home '/'
    en_pill = '''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin-left:14px!important;padding:0!important;list-style:none!important;">
  <a href="/" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;" title="Cambiar a español" aria-label="Cambiar a español">
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
    <span style="color:#f97316;font-weight:700;">EN</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">ES</span>
  </a>
</li>'''

    # Replace old bulky switcher
    content = re.sub(
        r'<li[^>]*class=["\'][^"\']*menu-item-lang-switcher[^"\']*["\'][^>]*>[\s\S]*?</li>',
        en_pill,
        content
    )

    # Save to both dist/en/index.html and en/index.html
    (ROOT / "en").mkdir(parents=True, exist_ok=True)
    (ROOT / "dist" / "en").mkdir(parents=True, exist_ok=True)
    (ROOT / "en" / "index.html").write_text(content, encoding="utf-8")
    (ROOT / "dist" / "en" / "index.html").write_text(content, encoding="utf-8")
    print("dist/en/index.html and en/index.html successfully updated with full English translation!")

if __name__ == "__main__":
    build_perfect_english_homepage()
