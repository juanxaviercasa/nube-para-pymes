import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# Extensive translation map for user-guide.html and guia-uso-22-apps.html
GUIDE_TRANSLATIONS = [
    # Subheadings
    ("Cómo utilizarlo", "How to Use"),
    ("Recomendaciones", "Best Practices & Advisory"),
    
    # Tool 1
    ("Permite evaluar un titular y mejorarlo con criterios heurísticos de claridad, fuerza, tono y atractivo. Incluye sugerencias, clasificación de tono, vista previa de resultados de búsqueda y redes sociales, comparación A/B, historial local y exportación del informe.",
     "Evaluates and improves headlines using heuristic criteria for clarity, power words, emotional tone, and viral appeal. Includes improvement suggestions, tone classification, search engine and social media previews, A/B testing, local history, and report export."),
    ("Introduce el titular que quieres analizar y, si la interfaz lo permite, el contexto o palabra clave principal.",
     "Enter the working headline you want to analyze and, if applicable, the primary context or target keyword."),
    ("Revisa la puntuación y las sugerencias. Observa especialmente la claridad, la longitud, la presencia de palabras concretas y el tono general.",
     "Review your score and recommendations. Pay close attention to clarity, character length, power words, and overall sentiment."),
    ("Edita el titular y vuelve a analizarlo para comparar la evolución.",
     "Revise your headline and re-analyze to track score improvements."),
    ("Utiliza la comparación A/B cuando tengas dos alternativas. Conserva la versión que comunique mejor el beneficio sin exagerar la promesa.",
     "Use A/B comparison when testing two variations. Keep the version that best communicates the value proposition without clickbait."),
    ("Consulta la vista previa SERP y social para comprobar cómo se percibiría el texto en distintos espacios.",
     "Review the SERP and social preview to verify how the text appears across Google and social feeds."),
    ("Copia el informe o expórtalo a PDF si necesitas compartirlo con otra persona.",
     "Copy the report summary or export to PDF to share with your team or clients."),
    ("No elijas automáticamente el titular con la puntuación más alta. Comprueba que sea fiel al contenido, comprensible para el público y compatible con la voz de la marca. La herramienta es una ayuda heurística, no una medición de rendimiento real.",
     "Do not blindly choose the highest-scoring headline. Ensure it remains truthful to the content, easily understandable to your target audience, and aligned with your brand voice."),

    # Tool 2
    ("Analiza una URL o los datos introducidos sobre una página y muestra señales relacionadas con título, descripción, palabras clave, H1, vistas previas SERP y sociales, salud general, densidad de contenido y tareas de mejora. También permite conservar historial local y comparar revisiones.",
     "Audits a live webpage URL or manual metadata inputs, analyzing title tags, meta descriptions, target keywords, H1 headers, SERP previews, overall health, content density, and improvement checklists. Supports local audit history and revision tracking."),
    ("Introduce la URL que deseas revisar. Si la página no puede analizarse directamente, completa los campos de título, descripción, palabra clave principal, H1 y contenido.",
     "Enter the URL you wish to audit. If the page cannot be fetched directly, fill in the title, description, target keyword, H1, and content fields manually."),
    ("Ejecuta el análisis y revisa el resumen de salud.",
     "Run the audit and review your consolidated SEO health score."),
    ("Lee las recomendaciones de título, descripción, encabezados, contenido y palabras clave.",
     "Read detailed recommendations regarding title tags, meta descriptions, heading structures, and keyword density."),
    ("Comprueba la vista previa de resultados de búsqueda y de redes sociales.",
     "Check Google search result and social card previews."),
    ("Revisa la densidad y la lista de tareas; corrige primero problemas de claridad, relevancia y contenido insuficiente.",
     "Review content depth and action items; prioritize fixing missing titles, duplicate tags, or thin content."),
    ("Guarda una versión en el historial y vuelve a analizar después de editar la página para comparar.",
     "Save an audit checkpoint to local history and re-audit after updating your site to verify gains."),
    ("La herramienta no sustituye una revisión técnica del servidor, indexación, enlaces, rendimiento o datos de Search Console. Utiliza la auditoría como una lista de comprobación editorial y valida los cambios en el sitio real.",
     "This tool does not replace deep server technical audits, indexing status, backlink analysis, or Google Search Console telemetry. Use it as an on-page editorial checklist and verify changes on your live site."),

    # Tool 3
    ("Reúne calculadoras de precio promocional, margen, punto de equilibrio, combos, valor de vida del cliente, copywriting persuasivo y campaña flash. Los cálculos se realizan con los datos introducidos en el navegador.",
     "Brings together calculators for promotional pricing, margins, break-even volume, product bundles, customer lifetime value (CLV), persuasive sales copy, and flash sales. All simulations run locally in your browser."),
    ("Selecciona la sección que corresponde a tu decisión: descuento, margen, equilibrio, combo, CLV, copy o campaña flash.",
     "Select the module matching your commercial decision: simple discount, margin simulation, break-even point, bundle pricing, CLV, copy, or flash sale."),
    ("Introduce precio base, costo, porcentaje de descuento, unidades y demás datos solicitados.",
     "Enter base price, unit cost, discount percentage, sales volume, and related parameters."),
    ("Revisa el precio final, la ganancia, el margen y el punto de equilibrio cuando corresponda.",
     "Review final customer price, net profit, margin percentages, and required break-even unit volumes."),
    ("En la sección de combos, compara la suma de productos, el precio conjunto y el margen resultante.",
     "In the bundle module, compare individual product prices against the bundle package price and resulting gross margin."),
    ("En CLV, introduce frecuencia de compra, ticket y retención para observar una estimación del valor de vida.",
     "In the CLV module, enter average purchase frequency, average order value, and retention rates to forecast customer lifetime value."),
    ("Usa las secciones de copy y campaña flash para convertir el resultado numérico en una propuesta comercial clara.",
     "Use the copy and flash sale modules to turn mathematical figures into compelling promotional messaging."),
    ("Comprueba que el costo introducido incluya los costos variables relevantes. No confundas margen sobre venta con recargo sobre costo y redondea los precios al final, no antes de realizar el cálculo.",
     "Ensure unit costs account for all direct variable expenses. Never confuse gross margin on revenue with markup on cost, and round prices only at the final step."),

    # Tool 4
    ("Calcula una cotización de despacho a partir del paquete, peso, vehículo sugerido, zona y paradas. Conserva estadísticas e historial local y permite generar un manifiesto o etiqueta de envío.",
     "Calculates shipping and courier rates based on package dimensions, physical weight, recommended vehicle, delivery zones, and drop-off stops. Maintains history and generates shipment manifests and labels."),
    ("Introduce largo, ancho, alto y peso real del paquete.",
     "Enter package length, width, height, and gross scale weight."),
    ("Selecciona el vehículo sugerido: moto, van o camión, según el tamaño y peso de la carga.",
     "Select recommended vehicle class: motorcycle, delivery van, or cargo truck depending on payload."),
    ("Añade las paradas de la ruta y selecciona la zona de destino en el mapa.",
     "Add delivery route stops and designate target delivery zones."),
    ("Revisa el peso cobrable, la tarifa base, los recargos y el total cotizado.",
     "Review billable weight (comparing actual vs. dimensional), base rates, surcharges, and total quote."),
    ("Guarda la cotización si quieres consultarla en el historial.",
     "Save the estimate to local history for recordkeeping."),
    ("Genera el manifiesto o la etiqueta cuando tengas confirmada la ruta.",
     "Generate the shipment manifest or parcel label once the delivery schedule is finalized."),
    ("Verifica las unidades y la tarifa estándar antes de presentar el precio a un cliente. La estimación no reemplaza la confirmación del transportista ni considera automáticamente restricciones de acceso, espera, seguros o mercancía especial.",
     "Confirm dimensional units and tariff rates before quoting clients. This simulation does not replace courier contracts or automatically factor specialized freight insurance or wait-time fees."),

    # Tool 5
    ("Calcula el precio final a partir del costo, margen neto y porcentaje de IGV. Muestra precio neto, ganancia, impuesto y escenarios forward, y permite conservar historial y descargar un PDF.",
     "Calculates final retail price from unit cost, desired net margin, and sales tax / GST. Displays pre-tax price, net profit, tax breakdown, forward scenarios, and exports an itemized PDF."),
    ("Introduce el costo de adquirir o producir el producto.",
     "Enter the wholesale acquisition or manufacturing cost per unit."),
    ("Define el porcentaje de margen neto que deseas obtener.",
     "Define your target net profit margin percentage."),
    ("Confirma el porcentaje de IGV aplicable en tu caso.",
     "Confirm the applicable statutory Sales Tax / GST percentage (e.g. US state tax, AU 10% GST)."),
    ("Revisa el precio neto, el impuesto y el precio final.",
     "Review pre-tax selling price, tax amount, and final customer price."),
    ("Modifica los valores para comparar escenarios y guarda los resultados relevantes en el historial.",
     "Adjust inputs to test price sensitivity and save scenarios to local history."),
    ("Descarga el PDF si necesitas conservar o compartir el desglose.",
     "Download the PDF summary to share itemized price quotes with team members or partners."),

    # Tool 6
    ("Muestra cronograma completo, cuota, intereses acumulados y ahorro de intereses con abonos extraordinarios.",
     "Displays complete loan schedule, periodic payment, cumulative interest, and savings from extra payments."),
    ("Introduce monto, tasa de interés anual y plazo en meses.",
     "Enter loan principal amount, annual interest rate (APR), and loan duration in months."),
    ("Prueba abonos extraordinarios y compara el cronograma modificado con el original.",
     "Simulate lump-sum extra payments to compare modified repayment curves against original loan schedules."),
    
    # Tool 7
    ("Estima el costo laboral total de contratar personal considerando salario base, aportes y beneficios obligatorios.",
     "Estimates true employer labor costs per worker, including base salary, employer taxes, and statutory benefits."),
    ("Añade colaboradores con su salario base, cargo y departamento.",
     "Add team members with gross salary, role, and department."),
    ("Revisa los sobrecostos consolidados y descarga el reporte de nómina.",
     "Review consolidated payroll burdens and export detailed staff cost reports."),

    # Tool 8
    ("Compara métricas de inversión publicitaria (ROAS, CPA, CTR) entre distintas plataformas en un solo panel.",
     "Compares advertising return metrics (ROAS, CPA, CTR, conversion rates) across multiple channels in a unified dashboard."),
    ("Registra inversión, clics y conversiones de cada plataforma.",
     "Input ad spend, impressions, clicks, and attributed conversions for each platform."),
    ("Analiza qué canal ofrece el costo de adquisición más eficiente.",
     "Identify which acquisition channel yields the highest return on ad spend and lowest CPA."),

    # Tool 9
    ("Construye enlaces de seguimiento con parámetros UTM estructurados para medir campañas de marketing digital.",
     "Builds standardized UTM tracking URLs to measure multi-channel digital acquisition performance."),
    ("Introduce URL de destino, fuente, medio y nombre de campaña.",
     "Enter landing page URL, traffic source, medium, and campaign identifier."),
    ("Copia el enlace generado y utilízalo en tus anuncios y publicaciones.",
     "Copy the generated tracking link and deploy it across ads, newsletters, and social posts."),

    # Tool 10
    ("Comprime y convierte imágenes a WebP de forma local e instantánea para acelerar la carga de tu sitio web.",
     "Compresses and converts images to WebP format instantly in your browser to optimize web page speed."),
    ("Arrastra tus archivos de imagen, ajusta calidad y dimensiones, y descarga las versiones optimizadas.",
     "Drag and drop image files, configure compression quality and dimensions, and download optimized assets."),

    # Tool 11
    ("Crea y descarga facturas proforma personalizadas con el catálogo de productos y logotipo de tu negocio.",
     "Generates and downloads professional proforma invoices with your company logo and line-item catalogs."),
    ("Completa datos de emisor y cliente, añade ítems y exporta en PDF.",
     "Fill in business and client details, add product lines, and export a polished PDF."),

    # Tool 12
    ("Crea una firma de correo HTML elegante y adaptable para Gmail, Outlook y otros clientes.",
     "Creates a responsive, professional HTML email signature for Gmail, Microsoft Outlook, and Apple Mail."),
    ("Introduce tus datos de contacto, personaliza colores y redes sociales, y copia el resultado.",
     "Enter contact details, customize brand colors and social icons, and copy the formatted signature."),

    # Tool 13
    ("Genera códigos QR directos y enlaces personalizados para iniciar conversaciones de WhatsApp.",
     "Generates scannable QR codes and pre-filled WhatsApp links for customer interactions."),
    ("Introduce tu número telefónico o URL, personaliza el diseño y descarga la imagen.",
     "Enter phone number or destination URL, customize QR styling, and download the PNG."),

    # Tool 14
    ("Genera contraseñas robustas y seguras localmente con longitud y caracteres configurables.",
     "Generates strong, high-entropy passwords locally with customizable length and character sets."),
    ("Configura longitud y caracteres, genera la clave y cópiala de forma segura.",
     "Configure length and character rules, generate passwords, and copy directly to your password manager."),

    # Tool 15
    ("Redacta contratos de prestación de servicios editables con cláusulas claras y profesionales.",
     "Drafts customizable professional service agreements with clear, protective contract clauses."),
    ("Define partes, alcance, honorarios y plazos, y descarga el borrador legal.",
     "Specify contracting parties, scope of work, fees, and milestones, and download the legal agreement."),

    # Tool 16
    ("Genera cotizaciones comerciales detalladas con cálculo de impuestos y formato PDF profesional.",
     "Generates itemized client quotes and estimates with tax calculations and professional PDF export."),
    ("Añade productos o servicios, define vigencia y condiciones, y genera la cotización.",
     "Add billable items, set quote validity terms, and export a branded estimate."),

    # Tool 17
    ("Crea paletas de colores corporativas con armonías visuales y comprobación de contraste accesible.",
     "Creates corporate color palettes with visual harmonies and WCAG contrast accessibility verification."),
    ("Elige un color base, explora combinaciones cromáticas y copia los códigos HEX/RGB.",
     "Select a base brand color, explore complementary palettes, and copy HEX/RGB tokens."),

    # Tool 18
    ("Redacta políticas de devolución y garantía transparentes adaptadas al tipo de producto que vendes.",
     "Drafts transparent return, exchange, and warranty policies tailored to your business model."),
    ("Selecciona el tipo de comercio, plazos y condiciones, y genera el texto para tu web.",
     "Select business category, return timeframes, and refund rules, and generate the policy text."),

    # Tool 19
    ("Genera documentos legales básicos: Términos y Condiciones, Política de Privacidad y Cookies.",
     "Generates essential website compliance documents: Terms of Service, Privacy Policy, and Cookies."),
    ("Completa los datos de tu empresa y sitio web, y descarga los textos legales redactados.",
     "Enter company details and web practices, and download drafted compliance policies."),

    # Tool 20
    ("Ofrece guiones estructurados y argumentos probados para superar objeciones comerciales en ventas.",
     "Provides structured talk tracks and proven frameworks to overcome buyer sales objections."),
    ("Explora categorías de objeción, practica el tono y guarda los guiones más efectivos.",
     "Browse objection categories, practice delivery in Zen Mode, and save high-converting scripts."),

    # Tool 21
    ("Organiza publicaciones en redes sociales y blog según pilares de contenido, canales y fechas.",
     "Organizes social media and blog publications across content pillars, channels, and dates."),
    ("Añade ideas de contenido, asigna canales y etapas del embudo, y exporta el calendario.",
     "Add content ideas, designate channels and funnel stages, and export your editorial calendar."),

    # Tool 22
    ("Simula y compara el Costo Total de Propiedad entre servidores físicos en oficina y la nube.",
     "Simulates and compares multi-year Total Cost of Ownership between on-premises servers and cloud."),
    ("Introduce costos de hardware, energía y mantenimiento vs. costo mensual de hosting cloud.",
     "Enter hardware, energy, and maintenance costs vs. monthly cloud infrastructure fees."),

    # Tool 23
    ("Gestiona prospectos, clientes y oportunidades comerciales en un pipeline visual interactivo.",
     "Manages leads, contacts, and sales opportunities across an interactive visual pipeline."),
    ("Registra contactos, añade oportunidades con valor y probabilidad, y actualiza etapas.",
     "Add client contacts, create deals with value and win probabilities, and update pipeline stages."),

    # Tool 24
    ("Controla entradas, salidas, cuentas por cobrar y fechas de vencimiento para proyectar liquidez.",
     "Tracks cash inflows, outflows, accounts receivable, and due dates to forecast liquidity."),
    ("Registra transacciones, asigna categorías y marca estados de pago para prever tesorería.",
     "Log income and expense transactions, assign categories, and track payment settlement statuses."),

    # Tool 25
    ("Supervisa productos, costos, existencias, umbrales de reorden y compras a proveedores.",
     "Monitors product inventory, unit costs, stock counts, reorder thresholds, and supplier orders."),
    ("Crea productos con stock mínimo, registra proveedores y aplica compras de reposición.",
     "Create product SKUs with minimum thresholds, register suppliers, and log restocking orders."),

    # Tool 26
    ("Coordina proyectos, tareas operativas, asignaciones de equipo, prioridades y fechas límite.",
     "Coordinates client projects, operational tasks, team assignees, priorities, and deadlines."),
    ("Crea proyectos, asigna tareas a colaboradores y supervisa el progreso en un tablero Kanban.",
     "Create projects, assign tasks to team members, and monitor progress on a Kanban board.")
]

def apply_guide_translations():
    for f in ["user-guide.html", "guia-uso-22-apps.html"]:
        p = EN_DIR / f
        if not p.exists():
            continue
        c = p.read_text(encoding="utf-8")
        for es, en in GUIDE_TRANSLATIONS:
            c = c.replace(es, en)
        p.write_text(c, encoding="utf-8")
    print("User guide thoroughly updated!")

apply_guide_translations()
