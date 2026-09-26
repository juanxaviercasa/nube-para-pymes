import re
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# ==============================================================================
# 1. TRANSLATION DICTIONARY FOR USER GUIDE (en/user-guide.html & en/guia-uso-22-apps.html)
# ==============================================================================

GUIDE_REPLACEMENTS = [
    # General terms
    ("Cuándo usarla", "When to Use"),
    ("Cómo funciona", "How It Works"),
    ("Qué datos necesita", "Required Inputs"),
    ("Qué entrega", "Output"),
    ("Consejos prácticos", "Practical Tips"),
    ("Para qué sirve", "Purpose"),
    ("Cómo utilizarla", "How to Use"),
    
    # Specific tool sections in guide
    ("1. Analizador de Titulares", "1. Headline Analyzer"),
    ("Evalúa y mejora titulares de contenido para aumentar clics y relevancia.", "Evaluates and improves content headlines to maximize clicks, engagement, and relevance."),
    ("Antes de publicar un artículo, anuncio, página de venta o publicación en redes sociales.", "Before publishing any blog post, digital ad, sales page, or social media announcement."),
    ("Analiza la longitud, las palabras de poder, el sentimiento emocional y el formato.", "Analyzes character length, power words, emotional sentiment, and structural formatting."),
    ("Introduce el titular y, opcionalmente, la palabra clave objetivo.", "Enter your working headline and optionally target keywords."),
    ("Puntuación general, desglose de métricas, recomendaciones y vista previa.", "Overall score, metric breakdowns, recommendations, and search result previews."),
    ("No sacrifiques la claridad por la persuasión; el titular debe cumplir la promesa del contenido.", "Never sacrifice clarity for clickbait; the headline must deliver on the promise of the body content."),
    
    ("2. Auditor Básico de SEO On-Page", "2. Basic On-Page SEO Auditor"),
    ("Revisa señales técnicas y de contenido esenciales para el posicionamiento web.", "Reviews essential technical and editorial on-page signals for search engine rankings."),
    ("Al auditar páginas existentes o preparar nuevos contenidos para indexación.", "When auditing existing website pages or preparing new content for search indexing."),
    ("Inspecciona etiquetas de título, meta descripción, encabezados H1-H3, enlaces y legibilidad.", "Inspects title tags, meta descriptions, H1-H3 heading hierarchies, link structures, and readability."),
    ("URL de la página o introducción manual de metadatos y contenido.", "Live webpage URL or manual input of metadata and body text."),
    ("Semáforo de salud SEO, lista de advertencias y recomendaciones accionables.", "SEO health score, warning flags, and prioritized actionable recommendations."),
    ("Prioriza corregir títulos duplicados o ausentes antes de optimizar la densidad de palabras clave.", "Prioritize fixing missing or duplicate title tags before fine-tuning keyword densities."),
    
    ("3. Calculadora de Descuentos y Promociones", "3. Discounts & Promotions Calculator"),
    ("Evalúa la rentabilidad y el impacto de descuentos y promociones en el margen comercial.", "Evaluates profitability and margin impact of discounts, combos, and promotions."),
    ("Al planificar campañas comerciales, rebajas de temporada o promociones por volumen.", "When planning marketing campaigns, seasonal sales, volume combos, or flash promotions."),
    ("Calcula el margen neto resultante, el punto de equilibrio y el incremento de ventas necesario.", "Calculates resulting net margin, break-even sales volume, and required sales lifts."),
    ("Precio regular, costo unitario, porcentaje de descuento y volumen estimado.", "Regular price, unit cost, discount percentage, and estimated sales volume."),
    ("Precio con descuento, margen bruto y neto, y unidades adicionales a vender.", "Discounted price, gross/net margins, and extra units needed to sustain gross profit."),
    ("Asegúrate de que el margen resultante cubra los costos operativos fijos.", "Ensure your discounted margin comfortably covers variable fulfillment and fixed overhead costs."),
    
    ("4. Calculadora de Flete y Envío Local", "4. Local Shipping & Freight Calculator"),
    ("Calcula tarifas de despacho local considerando peso físico y volumétrico.", "Calculates local delivery rates considering physical vs. dimensional package weight."),
    ("Para tiendas online, distribuidoras y comercios con entregas urbanas o interurbanas.", "For online stores, distributors, and retailers managing local and regional deliveries."),
    ("Aplica la fórmula estándar de cubicaje y compara con el peso en báscula.", "Applies volumetric weight formulas and compares them with actual scale weight."),
    ("Dimensiones del paquete (largo, ancho, alto), peso en kilogramos y zona de destino.", "Package dimensions (length, width, height), gross weight, and destination delivery zone."),
    ("Tarifa base, recargos volumétricos aplicables y costo final de envío.", "Base delivery rate, applicable dimensional surcharges, and total delivery fee."),
    ("Compara siempre las tarifas volumétricas de tus transportistas para evitar sobrecostos.", "Always verify courier dimensional divisors to prevent unexpected freight surcharges."),
    
    ("5. Calculadora de Precios de Venta con IGV", "5. Sales Pricing & Tax Calculator"),
    ("Determina precios de venta al público desglosando impuestos sobre las ventas (Sales Tax / GST).", "Determines customer retail prices while isolating profit margins and sales tax / GST."),
    ("Al fijar precios de nuevos productos o renegociar costos con proveedores.", "When launching new product lines or factoring supplier wholesale cost increases."),
    ("Aplica el margen sobre el costo o sobre la venta y añade la tasa impositiva.", "Calculates markup on cost or gross margin on sales and calculates applicable statutory taxes."),
    ("Costo de compra, margen deseado y porcentaje de impuesto aplicable.", "Wholesale purchase cost, target margin percentage, and applicable sales tax/GST rate."),
    ("Precio neto, importe del impuesto, precio final al consumidor y ganancia unitaria.", "Pre-tax net price, tax amount, final retail price, and net profit per unit."),
    ("Distingue claramente entre margen sobre venta y margen sobre costo para no perder dinero.", "Never confuse markup on cost with gross margin on revenue; miscalculations erode margins."),
    
    ("6. Calculadora de Préstamos y Amortizaciones", "6. Loan & Amortization Calculator"),
    ("Genera cronogramas de pago y evalúa el costo total de financiamiento comercial.", "Generates repayment schedules and calculates total borrowing costs for business loans."),
    ("Al solicitar créditos empresariales o evaluar compras de maquinaria e inventario.", "When evaluating commercial bank credit, equipment financing, or working capital lines."),
    ("Utiliza el sistema de cuota fija o amortización constante con intereses sobre saldo.", "Applies standard amortization algorithms (fixed payment or equal principal) on outstanding balance."),
    ("Monto del préstamo, tasa de interés anual y plazo en meses.", "Principal loan amount, annual percentage rate (APR), and loan term in months."),
    ("Cuota periódica, desglose de capital e intereses y cronograma completo de pagos.", "Monthly payment, principal/interest breakdown, and complete amortization schedule."),
    ("Revisa el costo financiero total incluyendo comisiones bancarias y seguros obligatorios.", "Evaluate the total APR including origination fees, closing costs, and mandatory insurance."),
    
    ("7. Calculadora de Sobrecostos Laborales", "7. Labor Cost & Payroll Burden Calculator"),
    ("Proyecta el costo real de contratar colaboradores considerando cargas sociales y beneficios.", "Projects the true employer cost of hiring staff, including payroll taxes and benefits."),
    ("Al preparar presupuestos de contratación o evaluar incrementos salariales.", "When budgeting new hires, reviewing compensation packages, or forecasting payroll."),
    ("Suma al salario base los aportes patronales, provisiones de beneficios y seguros obligatorios.", "Adds statutory payroll contributions, mandatory leave accruals, and workers' compensation to base pay."),
    ("Salario bruto y porcentajes legales de aportes y beneficios de tu jurisdicción.", "Gross wage and statutory employer contribution percentages for your jurisdiction."),
    ("Costo laboral mensual y anual por trabajador y factor de sobrecosto consolidado.", "Total monthly and annual employer cost per employee and consolidated burden factor."),
    ("Provisiona mensualmente las obligaciones anuales para evitar problemas de liquidez.", "Accrue annual obligations monthly to prevent cash flow crunches during bonus or holiday periods."),
    
    ("8. Comparador Avanzado de Campañas", "8. Ad Campaign Performance Comparator"),
    ("Compara la efectividad de campañas publicitarias en diferentes canales y plataformas.", "Compares ad performance across multiple acquisition channels and platforms."),
    ("Al asignar presupuesto de marketing entre Meta, Google, TikTok, LinkedIn u otros medios.", "When allocating advertising budgets across Google Ads, Meta, LinkedIn, and social media."),
    ("Calcula CPA, ROAS, CTR y tasa de conversión para medir el retorno por canal.", "Calculates CPA, ROAS, CTR, and conversion rates to measure channel acquisition efficiency."),
    ("Inversión, impresiones, clics, conversiones y valor monetario de las conversiones.", "Ad spend, impressions, clicks, conversions, and total attributed conversion value."),
    ("Tabla comparativa de métricas clave y ranking de rentabilidad por plataforma.", "Side-by-side metric comparison table and profitability ranking by platform."),
    ("No compares canales con objetivos distintos (ej. branding de video vs. búsqueda de intención).", "Avoid comparing top-of-funnel brand campaigns directly with bottom-of-funnel search intent."),
    
    ("9. Consola de Campañas", "9. UTM Campaign Builder Console"),
    ("Genera enlaces de seguimiento UTM estandarizados para analítica web.", "Generates standardized UTM tracking URLs for Google Analytics 4 and digital tracking."),
    ("Al lanzar campañas en redes sociales, boletines de email, banners o colaboraciones.", "When launching email campaigns, paid ads, partner links, or social media promotions."),
    ("Construye URLs con parámetros normalizados en minúsculas y sin caracteres conflictivos.", "Constructs validated URLs formatted in lowercase without special characters or spaces."),
    ("URL de destino, fuente (source), medio (medium) y nombre de campaña (campaign).", "Destination URL, traffic source, marketing medium, and campaign identifier."),
    ("URL completa de seguimiento lista para copiar y probar.", "Clean, formatted tracking URL ready to copy and deploy."),
    ("Establece una guía de nomenclatura clara para todo tu equipo para no fragmentar los datos.", "Establish a unified naming taxonomy for your team to avoid fragmented analytics reports."),
    
    ("10. WebP Forge · Conversor y Optimizador de Imágenes", "10. WebP Forge — Image Converter & Optimizer"),
    ("Convierte y comprime imágenes a formato WebP directamente en el navegador.", "Converts and compresses image assets to modern WebP format directly in the browser."),
    ("Al subir fotos a tu tienda online, catálogo digital o sitio web institucional.", "Before uploading product photos, blog assets, or hero banners to your website."),
    ("Utiliza la API Canvas del navegador para comprimir sin enviar archivos a servidores externos.", "Uses browser Canvas APIs to compress files client-side without external server uploads."),
    ("Archivos PNG, JPG o WebP seleccionados o arrastrados al área de trabajo.", "PNG, JPG, or WebP files dragged and dropped into the browser interface."),
    ("Imágenes optimizadas individuales o paquete ZIP con reducción de peso calculada.", "Optimized files or bulk ZIP package with calculated byte savings."),
    ("Una reducción del 70% en el peso de las imágenes acelera notablemente la carga de tu web.", "A 70% reduction in image weight substantially improves Core Web Vitals and SEO rankings."),
    
    ("11. Creador de Facturas Proforma", "11. Proforma Invoice Generator"),
    ("Genera documentos comerciales proforma elegantes listos para enviar a clientes.", "Generates professional proforma invoice documents ready for client presentation."),
    ("Para enviar cotizaciones formales previas a la emisión de factura fiscal definitiva.", "When issuing preliminary commercial invoices and payment requests before tax billing."),
    ("Permite gestionar catálogo de productos, impuestos y condiciones de pago locales.", "Manages line item catalogs, tax calculations, payment terms, and client details."),
    ("Datos del emisor, datos del cliente, detalle de ítems, cantidades y precios.", "Seller details, buyer information, line items, quantities, unit prices, and tax rates."),
    ("Documento proforma listo para impresión o exportación a PDF.", "Formatted proforma invoice ready to print or export as PDF."),
    ("Indica siempre la fecha de validez y las condiciones de entrega para evitar disputas.", "Always include an explicit expiration date and delivery terms to prevent scope creep."),
    
    ("12. Firma de Correo HTML", "12. HTML Email Signature Generator"),
    ("Diseña firmas de correo profesionales compatibles con todos los clientes de correo.", "Designs responsive, professional email signatures compatible with all major email clients."),
    ("Al estandarizar la imagen corporativa de tu equipo en Gmail, Outlook o Apple Mail.", "When standardizing team email branding across Gmail, Microsoft Outlook, and Apple Mail."),
    ("Genera código HTML con estilos en línea para asegurar visualización consistente.", "Generates clean inline-styled HTML markup to ensure consistent rendering across email clients."),
    ("Nombre, cargo, empresa, teléfono, redes sociales, logo y colores de marca.", "Full name, role, company name, contact numbers, social links, logo URL, and brand colors."),
    ("Firma visual copiable directamente o código HTML para configuración manual.", "Formatted signature ready for one-click copy, or raw HTML for advanced client setup."),
    ("Aloja tu logo en un servidor HTTPS rápido y accesible para que cargue sin bloqueos.", "Host your company logo on a secure HTTPS CDN so images load reliably across recipients."),
    
    ("13. Generador de Códigos QR", "13. QR Code & WhatsApp Direct Generator"),
    ("Crea códigos QR personalizados y enlaces directos a WhatsApp para conectar con clientes.", "Generates customizable QR codes and direct WhatsApp messaging links."),
    ("Para material impreso, vitrinas, empaques, tarjetas de presentación o cartas de restaurante.", "For product packaging, retail storefronts, business cards, restaurant menus, and flyers."),
    ("Codifica texto, URLs o números telefónicos en matrices bidimensionales legibles.", "Encodes destination URLs, phone numbers, or text into high-contrast 2D barcodes."),
    ("Tipo de contenido, enlace o número de WhatsApp y mensaje predeterminado.", "Content type, destination URL, or phone number with pre-filled greeting message."),
    ("Código QR descargable en alta resolución y enlace web directo.", "High-resolution downloadable PNG QR code and direct click-to-chat URL."),
    ("Prueba siempre el QR escaneándolo con varios teléfonos antes de enviarlo a imprimir.", "Always scan-test printed samples with multiple smartphone cameras before bulk printing."),
    
    ("14. SecuKey · Generador de Contraseñas para Pymes", "14. SecuKey — Password Generator for Small Teams"),
    ("Genera contraseñas aleatorias de alta seguridad para proteger cuentas corporativas.", "Generates cryptographically random, high-entropy passwords to protect team accounts."),
    ("Al crear cuentas de colaboradores, accesos a sistemas críticos o rotar contraseñas.", "When provisioning employee accounts, setting up SaaS tools, or enforcing credential rotation."),
    ("Aplica generación criptográfica aleatoria en el navegador con longitud personalizable.", "Employs browser cryptographic random algorithms with customizable character sets."),
    ("Longitud deseada y tipos de caracteres a incluir (mayúsculas, números, símbolos).", "Desired key length and character options (uppercase, lowercase, numbers, symbols)."),
    ("Contraseña generada y medidor de entropía y robustez.", "Generated secure password with live entropy scoring and visual strength indicator."),
    ("Almacena tus contraseñas en un gestor seguro como 1Password o Bitwarden, nunca en hojas de cálculo.", "Store team passwords in dedicated encrypted vaults like Bitwarden or 1Password, never unencrypted files."),
    
    ("15. Generador de Contratos de Servicios", "15. Professional Service Agreement Generator"),
    ("Redacta borradores editables de contratos de servicios con cláusulas fundamentales.", "Drafts customizable professional service agreements with essential protective clauses."),
    ("Al formalizar acuerdos con clientes, consultores o proveedores independientes.", "When onboarding new clients, retaining freelance contractors, or starting consulting engagements."),
    ("Estructura cláusulas de alcance, entregables, pagos, confidencialidad y resolución.", "Structures clauses covering scope of work, milestones, payment schedules, IP, and termination."),
    ("Identificación de partes, descripción del servicio, montos, plazos y condiciones.", "Full legal party names, service descriptions, milestones, fee amounts, and jurisdictions."),
    ("Borrador contractual completo editable y descargable.", "Complete, editable service contract document ready for review and signing."),
    ("Haz revisar siempre el borrador con un abogado antes de firmar para adecuarlo a tu legislación.", "Have legal counsel verify agreement terms to ensure compliance with local contract law."),
    
    ("16. Generador de Cotizaciones", "16. Quote & Estimate Generator"),
    ("Prepara cotizaciones comerciales estructuradas con cálculo de impuestos y descuentos.", "Prepares formal commercial estimates with itemized tax and discount calculations."),
    ("Al enviar propuestas comerciales a prospectos que requieren detalle formal de costos.", "When submitting proposals to prospects requiring detailed scope and financial breakdowns."),
    ("Calcula subtotales, descuentos, impuestos y genera documentos imprimibles.", "Calculates subtotal, discounts, sales tax, and renders print-ready branded estimates."),
    ("Datos de tu empresa, datos del cliente, lista de ítems, precios y validez.", "Company identity, client details, line items, billable rates, and expiration date."),
    ("Cotización en PDF con diseño profesional listo para compartir.", "Polished PDF proposal ready to send to prospective clients."),
    ("Especifica claramente qué incluye y qué NO incluye el presupuesto para evitar malentendidos.", "Explicitly delineate scope inclusions and exclusions to prevent misunderstandings."),
    
    ("17. Chroma · Generador de Paletas Corporativas", "17. Chroma — Brand Color Palette Generator"),
    ("Construye paletas de colores coherentes y accesibles para la identidad de tu negocio.", "Creates cohesive, accessible color palettes for business identity and web design."),
    ("Al definir la imagen de marca, rediseñar tu web o crear piezas gráficas.", "When creating brand guidelines, designing digital interfaces, or developing social templates."),
    ("Aplica teoría del color (armonías análogas, tríadas, complementarias) y verifica contraste.", "Applies color theory harmonies (triadic, analogous, complementary) and audits contrast."),
    ("Color base en formato hexadecimal o selector visual.", "Primary brand color input via HEX code or color picker."),
    ("Paleta completa de colores con valores HEX, RGB y análisis de contraste WCAG.", "Complete color palette with HEX/RGB codes and WCAG AA accessibility compliance ratings."),
    ("Verifica que los textos sobre fondos de color cumplan con un contraste mínimo de 4.5:1.", "Ensure body text maintains a minimum 4.5:1 contrast ratio against backgrounds for legibility."),
    
    ("18. Generador de Políticas de Devolución", "18. Return & Refund Policy Generator"),
    ("Redacta políticas claras de cambios y devoluciones para comercio online y físico.", "Drafts transparent return, exchange, and refund policies for retail and ecommerce."),
    ("Al lanzar una tienda online o actualizar las condiciones comerciales de tu tienda física.", "When launching an online shop or updating customer service policies in retail stores."),
    ("Adapta el texto según el tipo de producto (físico, moda, tecnología, perecedero o digital).", "Customizes terms based on vertical (physical goods, fashion, electronics, food, or digital)."),
    ("Datos del comercio, plazos de devolución, condiciones del producto y métodos de reembolso.", "Store details, return timeframes, product conditions, and refund settlement methods."),
    ("Política de devolución completa lista para publicar en tu sitio web.", "Complete, formatted return policy ready to publish on your website footer."),
    ("Una política de devolución clara genera confianza y reduce las disputas y reclamos con clientes.", "A transparent return policy increases checkout conversion and minimizes chargeback disputes."),
    
    ("19. LegalForge · Generador de Políticas y Términos", "19. Terms & Privacy Policy Generator"),
    ("Genera textos legales esenciales: Términos y Condiciones, Privacidad y Cookies.", "Generates core website compliance disclosures: Terms of Service, Privacy, and Cookies."),
    ("Al publicar cualquier sitio web, aplicación o plataforma que recopile datos de usuarios.", "When launching any website, landing page, or online shop collecting user inquiries."),
    ("Crea plantillas estructuradas con obligaciones del usuario, limitación de responsabilidad y privacidad.", "Builds structured disclosures covering user rights, liability limitations, and data privacy."),
    ("Nombre de la empresa, URL del sitio, país de operación y prácticas de datos.", "Company legal name, site URL, governing state/country, and analytics/cookies practices."),
    ("Documentos legales listos para insertar en las páginas institucionales de tu web.", "Compliance documents ready to link from your website footer and checkout pages."),
    ("Asegúrate de que la política de privacidad describa fielmente cómo tratas los datos reales.", "Ensure your privacy disclosures accurately reflect actual trackers and marketing pixels used."),
    
    ("20. ObjeciónPro · Guiones para Manejo de Objeciones", "20. Sales Objection Handling Scripts"),
    ("Proporciona respuestas estructuradas y probadas ante las objeciones más comunes en ventas.", "Provides proven, structured talk tracks to navigate difficult sales objections."),
    ("Durante llamadas de ventas, reuniones comerciales o capacitaciones de equipo.", "During live sales calls, discovery meetings, and team sales enablement training."),
    ("Ofrece argumentarios basados en empatía, reformulación y preguntas de diagnóstico.", "Provides responses rooted in empathetic validation, re-framing, and diagnostic questions."),
    ("Categoría de objeción (precio, tiempo, competencia, desconfianza, decisión).", "Objection category (price, timing, competition, trust, or decision authority)."),
    ("Guiones sugeridos, análisis de por qué funciona cada respuesta y preguntas de avance.", "Actionable talk tracks, psychological rationale, and recommended follow-up questions."),
    ("Nunca contradigas directamente al cliente; valida su preocupación antes de reformular el valor.", "Never argue directly with a prospect; validate their concern first before shifting perspective."),
    
    ("21. Organizador de Matriz de Contenidos", "21. Content Matrix & Editorial Planner"),
    ("Estructura tu estrategia de contenidos alineando pilares, formatos, canales y fechas.", "Structures your marketing content strategy across strategic pillars, formats, and channels."),
    ("Al planificar el calendario editorial de redes sociales, blog o campañas de email.", "When organizing monthly editorial schedules for social media, blogs, or newsletters."),
    ("Organiza publicaciones por etapa del embudo (ToFU, MoFU, BoFU) y canal de distribución.", "Categorizes content ideas by funnel stage (Awareness, Consideration, Conversion) and channel."),
    ("Pilares temáticos, formatos de contenido, canales objetivo y fechas de publicación.", "Content themes, formats (video, graphic, article), platforms, and publishing dates."),
    ("Matriz visual interactiva y calendario editorial exportable.", "Interactive visual matrix board and exportable CSV editorial calendar."),
    ("Prioriza la consistencia sobre el volumen: es mejor publicar 3 piezas sólidas por semana que 7 apresuradas.", "Prioritize consistency and depth over volume: three high-value posts outperform daily filler."),
    
    ("22. Simulador TCO · Físico vs. Nube", "22. Cloud vs. On-Premises TCO Simulator"),
    ("Compara el Costo Total de Propiedad entre infraestructura de servidores local y servicios cloud.", "Compares multi-year Total Cost of Ownership between on-premises servers and cloud services."),
    ("Al decidir si renovar servidores físicos o migrar sistemas a la nube (AWS, Azure, GCP).", "When deciding whether to replace physical hardware or migrate business workloads to the cloud."),
    ("Calcula costos acumulados a 3 y 5 años incluyendo hardware, energía, mantenimiento y cloud.", "Projects 3-year and 5-year cumulative costs including CAPEX, power, maintenance, and cloud fees."),
    ("Costo de servidor físico, consumo eléctrico, internet, soporte versus costo mensual cloud.", "Physical server purchase price, electricity, cooling, and IT maintenance vs. monthly cloud billing."),
    ("Gráfica comparativa de TCO, punto de equilibrio y análisis de ahorro acumulado.", "TCO comparison curves, economic break-even point, and executive financial summary."),
    ("Recuerda que la nube ofrece alta disponibilidad y copias de seguridad automáticas que en físico tienen costo extra.", "Remember cloud pricing includes built-in redundancy and offsite backups that carry hidden on-prem costs."),
    
    ("23. CRM y Pipeline Comercial", "23. SMB CRM & Sales Pipeline"),
    ("Centraliza contactos, negocios y etapas de venta para dar seguimiento comercial riguroso.", "Centralizes contacts, deals, and pipeline stages for disciplined sales management."),
    ("En la gestión diaria de prospectos, cotizaciones en negociación y seguimiento de clientes.", "For day-to-day lead management, quote follow-ups, and customer relationship tracking."),
    ("Visualiza las oportunidades en un tablero Kanban con cálculo de pipeline ponderado.", "Visualizes sales opportunities across a visual board with weighted pipeline forecasting."),
    ("Datos de contacto, nombre de la oportunidad, valor estimado, etapa y fecha de próxima acción.", "Contact details, opportunity name, estimated deal value, stage, and next action date."),
    ("Tablero Kanban de ventas, base de contactos y métricas de conversión comercial.", "Interactive sales pipeline board, contact directory, and conversion metrics."),
    ("Mantén siempre una 'próxima acción' con fecha concreta para cada oportunidad activa.", "Always set a concrete 'next action' and deadline on every active deal to maintain momentum."),
    
    ("24. Flujo de Caja y Cobranzas", "24. Cash Flow & Receivables Tracker"),
    ("Monitorea entradas, salidas, vencimientos y saldo operativo de tesorería.", "Monitors cash inflows, outflows, invoice due dates, and operating liquidity balances."),
    ("Para el control semanal de liquidez, seguimiento de cuentas por cobrar y pagos a proveedores.", "For weekly liquidity monitoring, accounts receivable collection, and vendor payment scheduling."),
    ("Registra cobros y pagos con estados (pendiente/realizado) y proyecta el saldo de caja.", "Tracks receipts and disbursements with settlement statuses and projects net cash balances."),
    ("Monto, tipo de movimiento, categoría, fecha de vencimiento y estado de pago.", "Transaction amount, inflow/outflow type, category, due date, and payment status."),
    ("Saldo actual proyectado, resumen de ingresos y gastos por categoría y tabla de vencimientos.", "Projected cash balance, category expense summaries, and overdue receivables list."),
    ("Anticípate a los meses de baja liquidez cobrando anticipos y acordando plazos con proveedores.", "Forecast low-liquidity cycles early by collecting project retainers and structuring payment terms."),
    
    ("25. Inventario, Proveedores y Compras", "25. Inventory, Suppliers & Purchasing"),
    ("Controla existencias de productos, costos, umbrales mínimos y pedidos de reposición.", "Tracks product stock levels, unit costs, minimum reorder thresholds, and vendor orders."),
    ("Para negocios comerciales, talleres y tiendas que gestionan inventario físico.", "For retailers, wholesalers, and service businesses managing physical product inventory."),
    ("Registra compras para aumentar stock y salidas manuales, alertando ante stock crítico.", "Applies purchase orders to restock inventory and generates instant alerts for low-stock items."),
    ("SKU, nombre del producto, costo unitario, precio de venta, stock actual y stock mínimo.", "SKU, item name, unit cost, retail price, current stock count, and minimum reorder point."),
    ("Catálogo valorizado de inventario, alertas de reposición y directorio de proveedores.", "Valued stock directory, low-inventory alert list, and supplier contact directory."),
    ("Establece niveles de stock mínimo basados en los días que tarda tu proveedor en reponer.", "Set minimum reorder points based on realistic supplier lead times plus safety buffers."),
    
    ("26. Tareas y Proyectos Operativos", "26. Operational Tasks & Projects"),
    ("Organiza proyectos de clientes, asigna responsables y gestiona entregables en equipo.", "Organizes client projects, assigns team responsibilities, and tracks deliverables."),
    ("Para coordinar servicios, proyectos de clientes, lanzamientos y tareas operativas.", "To coordinate client deliverables, marketing launches, and operational team workflows."),
    ("Gestiona tareas en un tablero Kanban con filtros por proyecto, prioridad y responsable.", "Manages tasks across a visual Kanban board with project, priority, and assignee filters."),
    ("Nombre del proyecto, cliente, fecha de entrega; tareas con responsable y prioridad.", "Project name, client, target due date; tasks with designated owners and priority ratings."),
    ("Tablero Kanban de tareas, control de vencimientos y lista de proyectos activos.", "Kanban task board, overdue milestone tracking, and active project dashboard."),
    ("Limita el trabajo en curso (WIP): terminar tareas antes de empezar nuevas aumenta la velocidad de entrega.", "Limit Work-in-Progress (WIP): finishing tasks before starting new ones accelerates turnaround times.")
]

# Apply to user guide
guide_file = EN_DIR / "user-guide.html"
guide_content = guide_file.read_text(encoding="utf-8")
for old_s, new_s in GUIDE_REPLACEMENTS:
    guide_content = guide_content.replace(old_s, new_s)
guide_file.write_text(guide_content, encoding="utf-8")
(EN_DIR / "guia-uso-22-apps.html").write_text(guide_content, encoding="utf-8")
print("User guide deep translation completed!")

# ==============================================================================
# 2. AUDIT AND REFINE EN/INDEX.HTML
# ==============================================================================
index_file = EN_DIR / "index.html"
index_content = index_file.read_text(encoding="utf-8")

# Fix any lingering Spanish names in aria-labels or tool links
INDEX_CLEANUPS = [
    ('aria-label="Add Generador de Contraseñas para Pymes to favorites"', 'aria-label="Add Password Generator for Small Teams to favorites"'),
    ('aria-label="Add Comparador de Campañas to favorites"', 'aria-label="Add Ad Campaign Comparator to favorites"'),
    ('aria-label="Add Inventario, Proveedores y Compras to favorites"', 'aria-label="Add Inventory, Suppliers & Purchase Orders to favorites"'),
    ('aria-label="Add Calculadora de Descuentos to favorites"', 'aria-label="Add Discount & Margin Calculator to favorites"'),
    ('aria-label="Add Calculadora de Precios con IGV to favorites"', 'aria-label="Add Sales Pricing & Tax Calculator to favorites"'),
    ('aria-label="Add Calculadora de Sobrecostos Laborales to favorites"', 'aria-label="Add Labor Cost & Payroll Burden Calculator to favorites"'),
    ('aria-label="Add Calculadora de Préstamos to favorites"', 'aria-label="Add Loan & Amortization Calculator to favorites"'),
    ('aria-label="Add Políticas de Devolución to favorites"', 'aria-label="Add Return & Refund Policy Generator to favorites"'),
    ('aria-label="Add Políticas y Términos to favorites"', 'aria-label="Add Terms of Service & Privacy Policy Generator to favorites"'),
    ('aria-label="Add Guiones para Objeciones to favorites"', 'aria-label="Add Sales Objection Handling Scripts to favorites"'),
    ('aria-label="Add Matriz de Contenidos to favorites"', 'aria-label="Add Content Matrix & Editorial Planner to favorites"'),
    ('aria-label="Add Creador de Facturas Proforma to favorites"', 'aria-label="Add Proforma Invoice Generator to favorites"'),
    ('aria-label="Add Generador de Cotizaciones to favorites"', 'aria-label="Add Quote & Estimate Generator to favorites"'),
    ('aria-label="Add Firma de Correo en HTML to favorites"', 'aria-label="Add HTML Email Signature Generator to favorites"'),
    ('aria-label="Add Paletas Corporativas to favorites"', 'aria-label="Add Brand Color Palette Generator to favorites"'),
    ('aria-label="Add Flujo de Caja y Cobranzas to favorites"', 'aria-label="Add Cash Flow & Receivables Tracker to favorites"'),
    ('aria-label="Add Tareas y Proyectos Operativos to favorites"', 'aria-label="Add Operational Tasks & Project Tracker to favorites"'),
    ('aria-label="Add Calculadora de Flete Local to favorites"', 'aria-label="Add Local Shipping & Freight Calculator to favorites"'),
    ('aria-label="Add Enlaces y QR para WhatsApp to favorites"', 'aria-label="Add QR Code & WhatsApp Link Generator to favorites"'),
    ('aria-label="Add Optimizador de Imágenes WebP to favorites"', 'aria-label="Add WebP Image Converter & Optimizer to favorites"'),
    ('aria-label="Add Consola de Campañas UTM to favorites"', 'aria-label="Add UTM Campaign Builder Console to favorites"'),
    ('aria-label="Add Simulador TCO: Físico vs Nube to favorites"', 'aria-label="Add Cloud vs. On-Premises TCO Simulator to favorites"'),
    ('aria-label="Add Auditor SEO Básico to favorites"', 'aria-label="Add Basic SEO Auditor to favorites"'),
    ('aria-label="Add Analizador de Titulares to favorites"', 'aria-label="Add Headline Analyzer to favorites"'),
    ('aria-label="Add Generador de Contratos de Servicios to favorites"', 'aria-label="Add Service Agreement Generator to favorites"'),
    ('aria-label="Add CRM y Pipeline Comercial to favorites"', 'aria-label="Add SMB CRM & Sales Pipeline to favorites"'),
]

for old_s, new_s in INDEX_CLEANUPS:
    index_content = index_content.replace(old_s, new_s)

# Update internal href links on cards to point to clean English tool files in /en/
CARD_LINK_MAPPINGS = [
    ("/herramientas/marketing/analizador-titulares/", "./headline-analyzer.html"),
    ("/herramientas/marketing/auditor-seo-basico/", "./basic-seo-auditor.html"),
    ("/herramientas/finanzas/calculadora-descuentos-promociones/", "./discount-promotions-calculator.html"),
    ("/herramientas/operaciones/calculadora-flete-envio-local/", "./local-shipping-calculator.html"),
    ("/herramientas/finanzas/calculadora-precios-venta-igv/", "./sales-pricing-tax-calculator.html"),
    ("/herramientas/finanzas/calculadora-prestamos-amortizaciones/", "./loan-amortization-calculator.html"),
    ("/herramientas/finanzas/calculadora-sobrecostos-laborales/", "./labor-cost-calculator.html"),
    ("/herramientas/marketing/comparador-campanas-avanzado/", "./ad-campaign-comparator.html"),
    ("/herramientas/marketing/consola-campanas/", "./utm-campaign-console.html"),
    ("/herramientas/productividad/conversor-optimizador-imagenes/", "./image-converter-optimizer.html"),
    ("/herramientas/ventas/creador-facturas-proforma/", "./proforma-invoice-generator.html"),
    ("/herramientas/productividad/firma-correo-html/", "./html-email-signature.html"),
    ("/herramientas/ventas/generador-codigos-qr/", "./qr-code-generator.html"),
    ("/herramientas/ventas/generador-cotizaciones/", "./quote-estimate-generator.html"),
    ("/herramientas/productividad/generador-paletas-corporativas/", "./brand-palette-generator.html"),
    ("/herramientas/legal/generador-politicas-devolucion/", "./return-refund-policy-generator.html"),
    ("/herramientas/legal/generador-politicas-terminos/", "./terms-privacy-generator.html"),
    ("/herramientas/ventas/guiones-manejo-objeciones/", "./objection-handling-scripts.html"),
    ("/herramientas/marketing/organizador-matriz-contenidos/", "./content-matrix-planner.html"),
    ("/herramientas/operaciones/simulador-tco-fisico-nube/", "./cloud-vs-onprem-tco.html"),
    ("/herramientas/productividad/generador-contrasenas-pymes/", "./password-generator.html"),
    ("/herramientas/legal/generador-contratos-servicios/", "./service-contract-generator.html"),
    ("/herramientas/ventas/crm-pymes/", "./smb-crm.html"),
    ("/herramientas/finanzas/flujo-caja-pymes/", "./cash-flow-tracker.html"),
    ("/herramientas/operaciones/inventario-compras-pymes/", "./inventory-purchase-orders.html"),
    ("/herramientas/productividad/tareas-proyectos-pymes/", "./task-project-tracker.html"),
]

for old_link, new_link in CARD_LINK_MAPPINGS:
    index_content = index_content.replace(f'href="{old_link}"', f'href="{new_link}"')

index_file.write_text(index_content, encoding="utf-8")
print("en/index.html deep cleanup and link mapping completed!")
