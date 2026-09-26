import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from en_help_configs import EN_CONFIGS

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"
EN_DIR.mkdir(exist_ok=True)

# General replacements applicable to all tools
GLOBAL_REPLACEMENTS = [
    # Global footers
    ("NubeParaPymes · Herramienta local y gratuita.", "SMB Cloud · Free local tool."),
    ("Aviso: los resultados son orientativos y se generan localmente. Verifica los datos, las fuentes y las normas aplicables antes de tomar decisiones comerciales, financieras, legales, laborales o tributarias.", "Notice: Results are generated locally for informational purposes. Verify all figures, tax rates, and legal requirements with a licensed professional before making commercial, financial, or legal decisions."),
    (">Portal de apps<", ">Tools Portal<"),
    (">Sitio principal<", ">Main Website<"),
    ("Diseñado y Desarrollado por", "Designed & Developed by"),
    
    # Common navigation
    ('aria-label="Volver al portal principal"', 'aria-label="Back to main portal"'),
    ('aria-label="Navegación de herramientas"', 'aria-label="Tools navigation"'),
    ('>Portal<', '>Portal<'),
    ('>Cotizaciones<', '>Quotes<'),
    ('>Caja<', '>Cash Flow<'),
    ('>Inventario<', '>Inventory<'),
    ('>Tareas<', '>Tasks<'),
    ('>Guía de uso<', '>User Guide<'),
    
    # Common actions & buttons
    (">Guardar<", ">Save<"),
    (">Limpiar<", ">Clear<"),
    (">Cancelar<", ">Cancel<"),
    (">Eliminar<", ">Delete<"),
    (">Eliminar todos<", ">Delete All<"),
    (">Eliminar todo<", ">Delete All<"),
    (">Descargar<", ">Download<"),
    (">Copiar<", ">Copy<"),
    (">Compartir<", ">Share<"),
    (">Exportar<", ">Export<"),
    (">Importar<", ">Import<"),
    (">Cerrar<", ">Close<"),
    (">Atrás<", ">Back<"),
    (">Siguiente<", ">Next<"),
    (">Editar<", ">Edit<"),
    (">Actualizar<", ">Update<"),
    (">Filtrar<", ">Filter<"),
    (">Buscar<", ">Search<"),
    
    # Common UI phrases
    ("Los datos se guardan en este navegador.", "Data is stored locally in this browser."),
    ("Centro operativo local", "Local Operations Center"),
    ("Sin asignar", "Unassigned"),
    ("Sin datos", "No data"),
]

# Tool-specific string replacements dictionary
TOOL_SPECIFIC_REPLACEMENTS = {
    "analizador-titulares": [
        ("Motor analítico de titulares", "Headline Analytics Engine"),
        ("Analizador de <span class=\"text-signal\">Titulares</span>", "Headline <span class=\"text-signal\">Analyzer</span>"),
        ("Puntaje en vivo, huella emocional NLP, previsualización pixel-perfect y test A/B bayesiano para decidir con datos.", "Live scoring, NLP emotional footprint, pixel-perfect search preview, and Bayesian A/B testing."),
        (">Analizador<", ">Analyzer<"),
        (">Prueba A/B<", ">A/B Test<"),
        ("Escribe tu titular", "Enter your headline"),
        ("Ej: 7 secretos definitivos para escribir titulares irresistibles", "e.g. 7 proven strategies to write high-converting headlines"),
        ("Palabra poderosa", "Power word"),
        ("Palabra débil / relleno", "Weak / filler word"),
        ("Prueba:", "Try:"),
        ("7 secretos definitivos para escribir mejor", "7 proven tips to write compelling copy"),
        ("La guía gratis para duplicar tus clientes.", "The free blueprint to double your sales pipeline."),
        ("Evita este error urgente antes de que sea tarde", "Avoid this critical mistake before it costs you deals"),
        ("Puntuación general", "Overall Score"),
        ("Estructura y legibilidad", "Structure & Readability"),
        ("Huella emocional", "Emotional Resonance"),
        ("Potencial viral", "Viral Potential"),
        ("Previsualización en Google", "Google Search Preview"),
        ("Escritorio", "Desktop"),
        ("Móvil", "Mobile"),
        ("Tu titular aparecerá aquí", "Your headline will appear here"),
        ("Escribe una meta descripción para ver cómo se mostrará junto a tu titular en los resultados.", "Enter a meta description to see how it displays alongside your headline in search results."),
        ("Límite visible:", "Visible limit:"),
        ("caracteres.", "characters."),
        ("Copiar informe", "Copy Report"),
        ("Análisis heurístico y PNL local · Estadística bayesiana orientadora", "Local NLP heuristic analysis · Bayesian guidance")
    ],
    "auditor-seo-basico": [
        ("Auditor Básico de SEO On-Page", "Basic On-Page SEO Auditor"),
        ("Analiza etiquetas, encabezados, imágenes y señales on-page para mejorar el posicionamiento de tu sitio.", "Analyze tags, headings, images, and on-page signals to improve search engine rankings."),
        ("Auditar URL", "Audit URL"),
        ("Ingresar Manualmente", "Manual Entry"),
        ("URL de la página", "Webpage URL"),
        ("Analizar página", "Analyze Page"),
        ("Título SEO (Title Tag)", "SEO Title Tag"),
        ("Meta descripción", "Meta Description"),
        ("Encabezado H1", "H1 Heading"),
        ("Contenido del artículo o página", "Body Content or Article"),
        ("Palabra clave objetivo", "Target Keyword"),
        ("Ejecutar auditoría", "Run Audit"),
        ("Salud SEO general", "Overall SEO Health"),
        ("Recomendaciones prioritarias", "Priority Recommendations"),
        ("Vista previa en buscadores", "Search Engine Preview"),
        ("Historial de auditorías", "Audit History"),
        ("Guardar auditoría", "Save Audit"),
        ("Exportar reporte", "Export Report")
    ],
    "calculadora-descuentos-promociones": [
        ("Calculadora de Descuentos y Promociones", "Discounts & Promotions Calculator"),
        ("Simula promociones, calcula márgenes y descubre el punto de equilibrio de tus ofertas comerciales.", "Simulate promotions, calculate profit margins, and discover the break-even point for your offers."),
        ("Descuento Simple", "Simple Discount"),
        ("Margen y Recargo", "Margin & Markup"),
        ("Venta en Combo", "Bundle Pricing"),
        ("Campaña Flash", "Flash Sale"),
        ("Precio original", "Original Price"),
        ("Porcentaje de descuento", "Discount Percentage"),
        ("Precio final con descuento", "Final Discounted Price"),
        ("Ahorro del cliente", "Customer Savings"),
        ("Margen bruto resultante", "Resulting Gross Margin"),
        ("Unidades adicionales necesarias para mantener ganancia", "Additional units required to maintain net profit"),
        ("Punto de equilibrio promocional", "Promotional Break-Even"),
        ("Calcular", "Calculate"),
        ("Simular escenario", "Simulate Scenario")
    ],
    "calculadora-flete-envio-local": [
        ("Calculadora de Flete y Envío Local", "Local Shipping & Freight Calculator"),
        ("Cotiza costos de despacho local considerando peso real, peso volumétrico, vehículo y paradas.", "Calculate local delivery rates based on actual weight, dimensional volume, vehicle class, and drop-offs."),
        ("Dimensiones del paquete", "Package Dimensions"),
        ("Largo (cm)", "Length (cm/in)"),
        ("Ancho (cm)", "Width (cm/in)"),
        ("Alto (cm)", "Height (cm/in)"),
        ("Peso real (kg)", "Actual Weight (kg/lb)"),
        ("Tipo de vehículo", "Vehicle Type"),
        ("Motocicleta", "Motorcycle / Courier"),
        ("Automóvil / Sedán", "Sedan / Car"),
        ("Furgoneta / Van", "Van / Light Truck"),
        ("Camión de carga", "Cargo Truck"),
        ("Zona de destino", "Delivery Zone"),
        ("Paradas adicionales", "Additional Stops"),
        ("Tarifa base", "Base Rate"),
        ("Recargo volumétrico", "Dimensional Surcharge"),
        ("Costo total estimado", "Estimated Total Cost"),
        ("Generar manifiesto de envío", "Generate Shipping Manifest")
    ],
    "calculadora-precios-venta-igv": [
        ("Calculadora de Precios de Venta con IGV", "Sales Pricing & Tax Calculator"),
        ("Fija precios rentables, calcula márgenes y desglosa el impuesto sobre las ventas (Sales Tax / GST).", "Set profitable retail prices, calculate margins, and isolate sales tax / GST."),
        ("Costo unitario del producto o servicio", "Unit Cost of Product or Service"),
        ("Margen neto deseado (%)", "Target Net Margin (%)"),
        ("Tasa de impuesto (IGV / Sales Tax / GST)", "Tax Rate (Sales Tax / GST %)"),
        ("Precio antes de impuestos (Neto)", "Pre-Tax Selling Price (Net)"),
        ("Monto de impuesto", "Sales Tax / GST Amount"),
        ("Precio final al consumidor", "Final Customer Retail Price"),
        ("Ganancia neta en dinero", "Net Profit Amount"),
        ("Margen sobre costo (Markup)", "Markup on Cost"),
        ("Desglose detallado", "Itemized Breakdown"),
        ("Descargar desglose", "Download Breakdown")
    ],
    "calculadora-prestamos-amortizaciones": [
        ("Calculadora de Préstamos y Amortizaciones", "Loan & Amortization Calculator"),
        ("Proyecta cuotas mensuales, tabla completa de pagos y ahorro de intereses con abonos extraordinarios.", "Project monthly repayments, full amortization schedules, and interest savings with extra payments."),
        ("Monto del préstamo", "Loan Principal Amount"),
        ("Tasa de interés anual (%)", "Annual Interest Rate (%)"),
        ("Plazo (meses)", "Loan Term (Months)"),
        ("Sistema de amortización", "Amortization Method"),
        ("Francés (Cuota constante)", "Fixed Payment (Standard Amortization)"),
        ("Alemán (Amortización constante)", "Equal Principal Repayment"),
        ("Cuota mensual estimada", "Estimated Monthly Payment"),
        ("Intereses totales", "Total Interest Paid"),
        ("Costo total del crédito", "Total Cost of Loan"),
        ("Tabla de amortización", "Amortization Schedule"),
        ("Abono extraordinario", "Extra Lump-Sum Payment"),
        ("Ahorro estimado en intereses", "Estimated Interest Savings"),
        ("Reducción de plazo", "Term Reduction")
    ],
    "calculadora-sobrecostos-laborales": [
        ("Calculadora de Sobrecostos Laborales", "Labor Cost & Payroll Burden Calculator"),
        ("Estima el costo total del empleador por trabajador considerando beneficios de ley, aportes y provisiones.", "Estimate the true employer cost per employee including statutory benefits, taxes, and provisions."),
        ("Moneda de cálculo", "Calculation Currency"),
        ("Agregar colaborador", "Add Employee"),
        ("Nombre del empleado", "Employee Name"),
        ("Cargo / Puesto", "Job Title / Role"),
        ("Departamento", "Department"),
        ("Salario base mensual", "Monthly Base Wage"),
        ("Aportes del empleador", "Employer Contributions & Taxes"),
        ("Provisiones anuales", "Annual Accruals & Benefits"),
        ("Costo mensual total", "Total Monthly Employer Cost"),
        ("Costo anual total", "Total Annual Employer Cost"),
        ("Factor de sobrecosto laboral", "Payroll Burden Factor"),
        ("Descargar reporte de nómina", "Download Payroll Report")
    ],
    "comparador-campanas-avanzado": [
        ("Comparador Avanzado de Campañas", "Ad Campaign Performance Comparator"),
        ("Compara el rendimiento y retorno de inversión entre plataformas de anuncios (Meta, Google, LinkedIn).", "Compare performance and ROI across advertising platforms (Meta, Google Ads, LinkedIn)."),
        ("Nueva campaña", "New Campaign"),
        ("Plataforma publicitaria", "Advertising Platform"),
        ("Presupuesto invertido", "Ad Spend Budget"),
        ("Impresiones", "Impressions"),
        ("Clics obtenidos", "Clicks"),
        ("Conversiones / Ventas", "Conversions / Sales"),
        ("Ingresos generados", "Revenue Generated"),
        ("Retorno de la inversión (ROAS)", "Return on Ad Spend (ROAS)"),
        ("Costo por clic (CPC)", "Cost Per Click (CPC)"),
        ("Costo por adquisición (CPA)", "Cost Per Acquisition (CPA)"),
        ("Tasa de clics (CTR)", "Click-Through Rate (CTR)"),
        ("Tasa de conversión", "Conversion Rate"),
        ("Comparativa lado a lado", "Side-by-Side Comparison"),
        ("Mejor canal en ROAS", "Top Performing Channel (ROAS)")
    ],
    "consola-campanas": [
        ("Constructor UTM — Consola de Campañas", "UTM Campaign Builder Console"),
        ("Organiza, estandariza y genera enlaces de seguimiento UTM para medir tus fuentes de tráfico.", "Organize, standardize, and generate UTM tracking links to measure digital acquisition channels."),
        ("URL de destino *", "Destination Landing Page URL *"),
        ("Fuente de tráfico (utm_source) *", "Traffic Source (utm_source) *"),
        ("Medio de campaña (utm_medium) *", "Campaign Medium (utm_medium) *"),
        ("Nombre de campaña (utm_campaign) *", "Campaign Name (utm_campaign) *"),
        ("Contenido de anuncio (utm_content)", "Ad Content (utm_content)"),
        ("Término de búsqueda (utm_term)", "Search Term (utm_term)"),
        ("Generar enlace UTM", "Generate UTM Link"),
        ("Enlace final generado", "Generated Tracking URL"),
        ("Copiar enlace", "Copy Tracking URL"),
        ("Probar enlace", "Test Link in New Tab"),
        ("Historial de enlaces", "Campaign Links Library")
    ],
    "conversor-optimizador-imagenes": [
        ("WebP Forge — Conversor y optimizador de imágenes", "WebP Forge — Image Converter & Optimizer"),
        ("Reduce el peso de imágenes en tu navegador sin subirlas a ningún servidor. 100% privado y rápido.", "Compress images locally in your browser with zero server uploads. 100% private, instant, and secure."),
        ("Arrastra tus imágenes aquí o haz clic para seleccionar", "Drag and drop your images here or click to browse"),
        ("Formato de salida", "Output Format"),
        ("Calidad de compresión", "Compression Quality"),
        ("Ancho máximo (px)", "Max Width (px)"),
        ("Optimizar y Convertir", "Optimize & Convert"),
        ("Ahorro de espacio", "Storage Savings"),
        ("Descargar imagen optimizada", "Download Optimized Image"),
        ("Descargar todas (ZIP)", "Download All (ZIP)")
    ],
    "creador-facturas-proforma": [
        ("Creador de Facturas Proforma", "Proforma Invoice Generator"),
        ("Prepara cotizaciones formales y facturas proforma con el logotipo y datos de tu empresa.", "Draft formal quotes and proforma invoices with your company logo and contact details."),
        ("Datos del Emisor", "Business Details"),
        ("Nombre comercial o empresa", "Company or Trade Name"),
        ("Identificación fiscal (RUC/CIF/RFC/ABN/EIN)", "Tax ID / ABN / EIN / VAT"),
        ("Dirección", "Business Address"),
        ("Datos del Cliente", "Client Details"),
        ("Nombre del cliente", "Client Name"),
        ("Correo electrónico", "Client Email"),
        ("Número de proforma", "Proforma Number"),
        ("Fecha de emisión", "Date of Issue"),
        ("Fecha de validez", "Valid Until"),
        ("Moneda", "Currency"),
        ("Descripción del ítem", "Item Description"),
        ("Cantidad", "Qty"),
        ("Precio unitario", "Unit Price"),
        ("Subtotal", "Subtotal"),
        ("Impuestos", "Tax"),
        ("Total General", "Grand Total"),
        ("Términos y condiciones de pago", "Payment Terms & Bank Details"),
        ("Descargar Proforma en PDF", "Download Proforma PDF")
    ],
    "crm-pymes": [
        ("CRM y Pipeline Comercial", "CRM & Sales Pipeline"),
        ("Clientes, oportunidades y seguimientos en un solo lugar.", "Contacts, opportunities, and follow-ups in one place."),
        ("Centro operativo local", "Local Operations Center"),
        ("Los datos se guardan en este navegador. Usa el botón <strong>Respaldo JSON</strong> para exportar una copia.", "Data is stored locally in this browser. Use the <strong>JSON Backup</strong> button to export a copy."),
        ("Guía de uso", "User Guide"),
        ("Contactos", "Contacts"),
        ("empresas y personas", "companies & individuals"),
        ("Oportunidades abiertas", "Open Opportunities"),
        ("en seguimiento", "in active pipeline"),
        ("Pipeline ponderado", "Weighted Pipeline"),
        ("valor × probabilidad", "value × probability"),
        ("Seguimientos vencidos", "Overdue Follow-ups"),
        ("requieren atención", "require action"),
        ("Nuevo contacto", "New Contact"),
        ("Nombre o empresa *", "Name or Company *"),
        ("Persona de contacto", "Contact Person"),
        ("Teléfono", "Phone"),
        ("Correo", "Email"),
        ("Notas", "Notes"),
        ("Guardar contacto", "Save Contact"),
        ("Nueva oportunidad", "New Opportunity"),
        ("Oportunidad *", "Opportunity *"),
        ("Ej. Implementación web", "e.g. Website redesign"),
        ("Contacto", "Contact"),
        ("Valor estimado", "Estimated Value"),
        ("Etapa", "Stage"),
        ("Probabilidad (%)", "Win Probability (%)"),
        ("Próxima acción", "Next Action Date"),
        ("Qué sigue", "Next Step Description"),
        ("Llamar para validar alcance", "Call to confirm proposal scope"),
        ("Agregar oportunidad", "Add Opportunity"),
        ("Pipeline comercial", "Sales Pipeline"),
        ("Actualiza las etapas directamente en cada tarjeta.", "Update deal stages directly on each card."),
        ("Buscar oportunidad o contacto", "Search opportunities or contacts..."),
        ("Base local de clientes y prospectos.", "Local database of clients and leads.")
    ],
    "firma-correo-html": [
        ("Firma de Correo HTML", "HTML Email Signature Generator"),
        ("Diseña firmas de correo elegantes y profesionales para Gmail, Outlook y Apple Mail.", "Create sleek, professional email signatures compatible with Gmail, Outlook, and Apple Mail."),
        ("Nombre completo", "Full Name"),
        ("Cargo o profesión", "Job Title / Role"),
        ("Empresa o marca", "Company / Brand"),
        ("Teléfono o móvil", "Phone / Mobile"),
        ("Sitio web", "Website URL"),
        ("Dirección", "Office Address"),
        ("URL de foto o logo", "Logo or Photo URL"),
        ("URL del banner (imagen)", "Promotional Banner Image URL"),
        ("Enlace del banner", "Banner Click-Through URL"),
        ("Color principal", "Primary Accent Color"),
        ("Vista previa en vivo", "Live Signature Preview"),
        ("Copiar firma seleccionada", "Copy Selected Signature"),
        ("Copiar código HTML", "Copy Raw HTML Code")
    ],
    "flujo-caja-pymes": [
        ("Flujo de Caja y Cobranzas", "Cash Flow & Receivables Tracker"),
        ("Ingresos, egresos y control de liquidez operativa.", "Income, expenses, and operational liquidity management."),
        ("Registra ingresos, egresos, vencimientos y estados de pago para observar el saldo operativo y anticipar faltantes.", "Record income, expenses, due dates, and settlement status to monitor operating balances and prevent liquidity shortfalls."),
        ("Nuevo movimiento", "New Transaction"),
        ("Tipo de movimiento", "Transaction Type"),
        ("Ingreso (Cobro)", "Inflow (Income)"),
        ("Egreso (Pago)", "Outflow (Expense)"),
        ("Monto *", "Amount *"),
        ("Fecha de vencimiento", "Due Date"),
        ("Fecha de pago", "Payment Date"),
        ("Estado de pago", "Payment Status"),
        ("Pendiente", "Pending"),
        ("Cobrado / Pagado", "Settled / Paid"),
        ("Vencido", "Overdue"),
        ("Saldo actual proyectado", "Projected Net Balance"),
        ("Total ingresos pendientes", "Pending Receivables"),
        ("Total pagos pendientes", "Pending Payables"),
        ("Guardar movimiento", "Save Transaction")
    ],
    "generador-codigos-qr": [
        ("Código QR directo", "Direct QR Code Generator"),
        ("Enlaces y códigos QR para WhatsApp", "QR Codes and Direct Links for WhatsApp"),
        ("Crea links directos y códigos QR escaneables con mensajes predefinidos.", "Create direct links and scannable QR codes with pre-filled messages."),
        ("Número de WhatsApp", "WhatsApp Phone Number"),
        ("Número sin código de país", "Phone number with country code"),
        ("Mensaje predefinido", "Pre-filled Message"),
        ("Hola, me gustaría recibir más información sobre...", "Hi! I would like to get more information about..."),
        ("Parámetros de rastreo (UTM)", "Campaign Tracking Parameters (UTM)"),
        ("Estilo del QR", "QR Code Style"),
        ("Clásico", "Classic"),
        ("Moderno", "Modern"),
        ("Icono de chat al centro", "Center Chat Icon"),
        ("Generar Código QR", "Generate QR Code"),
        ("Descargar imagen PNG", "Download PNG Image")
    ],
    "generador-contrasenas-pymes": [
        ("SecuKey — Generador de Contraseñas para Pymes", "SecuKey — Password Generator for Small Teams"),
        ("Crea contraseñas seguras, robustas y de alta entropía para proteger las cuentas de tu negocio.", "Generate strong, high-entropy passwords to secure your team accounts and business services."),
        ("Longitud de la contraseña", "Password Length"),
        ("Incluir letras mayúsculas (A-Z)", "Include uppercase letters (A-Z)"),
        ("Incluir letras minúsculas (a-z)", "Include lowercase letters (a-z)"),
        ("Incluir números (0-9)", "Include numbers (0-9)"),
        ("Incluir símbolos especiales (!@#$)", "Include special symbols (!@#$)"),
        ("Excluir caracteres ambiguos (l, 1, O, 0)", "Exclude ambiguous characters (l, 1, O, 0)"),
        ("Generar contraseña segura", "Generate Secure Password"),
        ("Fuerza de la contraseña", "Password Strength"),
        ("Copiar contraseña", "Copy Password"),
        ("Generación por lotes", "Batch Password Generation")
    ],
    "generador-contratos-servicios": [
        ("Generador de Contratos de Prestación de Servicios", "Professional Service Agreement Generator"),
        ("Genera contratos de servicios profesionales sin esfuerzo.", "Draft professional service agreements effortlessly."),
        ("Borrador editable con cláusulas de entregables, pagos, propiedad intelectual y confidencialidad.", "Customizable agreement draft with deliverables, payment milestones, IP rights, and confidentiality."),
        ("Datos del Proveedor / Prestador", "Service Provider Details"),
        ("Datos del Cliente / Contratante", "Client Details"),
        ("Descripción del servicio", "Scope of Work & Services"),
        ("Entregables específicos", "Specific Deliverables"),
        ("Monto de honorarios", "Professional Fees"),
        ("Forma de pago", "Payment Schedule"),
        ("Fecha de inicio", "Effective Start Date"),
        ("Fecha de terminación", "Completion Date"),
        ("Jurisdicción aplicable", "Governing Jurisdiction"),
        ("Generar borrador de contrato", "Generate Agreement Draft"),
        ("Descargar documento", "Download Contract Document")
    ],
    "generador-cotizaciones": [
        ("Generador de Cotizaciones", "Quote & Estimate Generator"),
        ("Arma propuestas comerciales estructuradas y envíalas en formato PDF con la identidad de tu marca.", "Build structured commercial estimates with custom branding and export ready-to-send PDFs."),
        ("Nombre de la Empresa Emisora", "Company / Sender Name"),
        ("RUC / Identificador", "Tax ID / ABN / EIN / Company Reg"),
        ("Teléfono / WhatsApp", "Phone / WhatsApp"),
        ("Correo del Cliente", "Client Email"),
        ("N.º de Cotización", "Quote / Estimate Number"),
        ("Fecha de Emisión", "Issue Date"),
        ("Validez de la oferta", "Quote Validity"),
        ("Subir logotipo (procesado localmente)", "Upload Company Logo (Processed Locally)"),
        ("Agregar ítem", "Add Item"),
        ("Plantilla Clásica", "Classic Template"),
        ("Plantilla Moderna", "Modern Template"),
        ("Descargar Cotización (PDF)", "Download Estimate (PDF)")
    ],
    "generador-paletas-corporativas": [
        ("Chroma — Generador de Paletas Corporativas", "Chroma — Brand Color Palette Generator"),
        ("Paletas que definen marcas, no solo pantallas.", "Color palettes that define brands, not just screens."),
        ("Color Base (HEX)", "Base Brand Color (HEX)"),
        ("Nombra tu paleta (ej. Marca Fintech)", "Name your palette (e.g. Fintech Brand)"),
        ("Armonías cromáticas", "Color Harmonies"),
        ("Análogos — 30 º", "Analogous — 30°"),
        ("Tétrada — 90 º", "Tetradic — 90°"),
        ("Tríada — 120 º", "Triadic — 120°"),
        ("Complementario", "Complementary"),
        ("Monocromático", "Monochromatic"),
        ("Aleatorio", "Random Color"),
        ("Verificación de Contraste WCAG", "WCAG Contrast Checker"),
        ("Guardar en galería", "Save to Library"),
        ("Descargar PDF", "Download Color Spec Sheet")
    ],
    "generador-politicas-devolucion": [
        ("Generador de Políticas de Devolución", "Return & Refund Policy Generator"),
        ("Políticas de devolución claras en segundos", "Clear return & refund policies in seconds"),
        ("Redacta textos transparentes sobre garantías, cambios y reembolsos según tu modelo comercial.", "Draft clear terms for product returns, warranties, and refunds tailored to your business model."),
        ("Ropa y Moda", "Apparel & Fashion"),
        ("Electrónica", "Consumer Electronics"),
        ("Servicios Digitales", "Digital Products & Software"),
        ("Alimentos", "Food & Perishable Goods"),
        ("Plazo para devoluciones", "Return Window"),
        ("14 días", "14 days"),
        ("30 días", "30 days"),
        ("60 días", "60 days"),
        ("Condiciones del producto devuelto", "Eligible Product Conditions"),
        ("En empaque original y sin uso", "Unused in original packaging"),
        ("Método de reembolso", "Refund Mechanism"),
        ("Reembolso al método de pago original", "Refund to original payment method"),
        ("Crédito en tienda o cambio", "Store credit or exchange"),
        ("Generar política", "Generate Policy Text"),
        ("Copiar al portapapeles", "Copy Policy Text")
    ],
    "generador-politicas-terminos": [
        ("LegalForge — Generador de Políticas y Términos", "LegalForge — Terms & Privacy Policy Generator"),
        ("Crea los documentos legales obligatorios para tu presencia web o comercio electrónico.", "Generate essential legal disclosures and terms for your website or ecommerce store."),
        ("Términos y Condiciones", "Terms of Service"),
        ("Política de Privacidad", "Privacy Policy"),
        ("Política de Cookies", "Cookie Policy"),
        ("Nombre de la empresa", "Legal Business Name"),
        ("URL del sitio web", "Website URL"),
        ("País / Jurisdicción", "Country / Governing State"),
        ("Identificación fiscal (opcional)", "Tax ID / ABN / EIN (Optional)"),
        ("Domicilio fiscal (opcional)", "Registered Address (Optional)"),
        ("Correo de contacto legal", "Legal Contact Email"),
        ("¿Recopilas pagos online?", "Do you process payments online?"),
        ("¿Utilizas cookies analíticas?", "Do you use analytics cookies?"),
        ("Generar documento legal", "Generate Legal Document"),
        ("Copiar texto", "Copy Document Text")
    ],
    "guiones-manejo-objeciones": [
        ("Guiones para Manejo de Objeciones", "Sales Objection Handling Scripts"),
        ("Los mejores scripts para manejar cualquier objeción.", "The proven scripts to overcome any sales objection."),
        ("Encuentra qué decir y por qué funciona, practica el tono en voz alta y presenta sin distracciones con el Modo Zen.", "Know exactly what to say, practice your delivery aloud, and close with confidence using Zen Mode."),
        ("Base de datos de respuestas de ventas", "Sales Talk Track Library"),
        ("Scripts disponibles", "Scripts Available"),
        ("Tipos de objeción", "Objection Categories"),
        ("Objeción de Precio", "Price Objections"),
        ("Objeción de Tiempo", "Timing Objections"),
        ("Objeción de Confianza", "Trust & Credibility Objections"),
        ("Objeción de Competencia", "Competitor Objections"),
        ("Objeción de Autoridad", "Decision-Maker Objections"),
        ("Explorador", "Script Explorer"),
        ("Modo Conversación", "Conversation Mode"),
        ("Modo Zen", "Zen Mode"),
        ("Aportar script", "Contribute Script"),
        ("Por qué funciona esta respuesta", "Why This Framework Works"),
        ("Pregunta de seguimiento recomendada", "Recommended Follow-Up Question"),
        ("Copiar guion", "Copy Script")
    ],
    "inventario-compras-pymes": [
        ("Inventario, Proveedores y Compras", "Inventory, Suppliers & Purchasing"),
        ("Control de existencias, costos, compras y alertas de reposición.", "Track stock levels, unit costs, supplier orders, and reorder alerts."),
        ("Productos en catálogo", "Catalog Products"),
        ("Valor total del inventario", "Total Inventory Valuation"),
        ("Alertas de stock bajo", "Low-Stock Alerts"),
        ("Proveedores activos", "Active Suppliers"),
        ("Nuevo producto", "New Product"),
        ("SKU *", "SKU *"),
        ("Producto *", "Product Name *"),
        ("Costo unitario", "Unit Cost"),
        ("Precio de venta", "Retail Selling Price"),
        ("Stock inicial", "Starting Stock"),
        ("Stock mínimo", "Minimum Reorder Level"),
        ("Guardar producto", "Save Product"),
        ("Nuevo proveedor", "New Supplier"),
        ("Proveedor o empresa *", "Supplier Company *"),
        ("Contacto", "Contact Person"),
        ("Teléfono", "Phone"),
        ("Correo", "Email"),
        ("Plazo de pago (días)", "Payment Terms (Days)"),
        ("Guardar proveedor", "Save Supplier"),
        ("Registrar compra / reposición", "Record Restock Purchase"),
        ("Cantidad comprada", "Units Purchased"),
        ("Aplicar compra al stock", "Add to Inventory Stock")
    ],
    "organizador-matriz-contenidos": [
        ("Organizador de Matriz de Contenidos", "Content Matrix & Editorial Planner"),
        ("Planifica, organiza y estructura tus contenidos de redes sociales y blog en un tablero interactivo.", "Plan, organize, and structure your social media and blog content across an interactive matrix."),
        ("Pilares de Contenido", "Content Pillars"),
        ("Etapas del Funnel", "Funnel Stages"),
        ("Atracción (ToFU)", "Top of Funnel (Awareness)"),
        ("Consideración (MoFU)", "Middle of Funnel (Consideration)"),
        ("Conversión (BoFU)", "Bottom of Funnel (Conversion)"),
        ("Fidelización", "Retention & Advocacy"),
        ("Nueva idea de contenido", "New Content Idea"),
        ("Título de la publicación", "Post Headline / Topic"),
        ("Canal de publicación", "Publishing Channel"),
        ("Formato de contenido", "Format (Video, Carousel, Article)"),
        ("Fecha programada", "Scheduled Date"),
        ("Estado de producción", "Production Status"),
        ("Idea", "Idea"),
        ("En redacción", "In Drafting"),
        ("Listo para publicar", "Ready to Publish"),
        ("Publicado", "Published"),
        ("Vista Semanal", "Week View"),
        ("Vista Mensual", "Month View"),
        ("Exportar calendario (CSV)", "Export Calendar (CSV)")
    ],
    "simulador-tco-fisico-nube": [
        ("Simulador TCO — Físico vs. Nube", "Cloud vs. On-Premises TCO Simulator"),
        ("Simulador Empresa de Infraestructura TI", "IT Infrastructure TCO Simulator"),
        ("Compara el costo total de propiedad a 3 y 5 años entre servidores físicos en oficina y nube pública.", "Compare 3-year and 5-year Total Cost of Ownership between on-premises servers and public cloud services."),
        ("Horizonte de evaluación", "Evaluation Horizon"),
        ("3 Años", "3 Years"),
        ("5 Años", "5 Years"),
        ("Servidor Físico (On-Premises)", "On-Premises Physical Server"),
        ("Costo inicial de hardware", "Initial Hardware CAPEX"),
        ("Consumo eléctrico mensual", "Monthly Electricity & Cooling"),
        ("Conectividad e Internet dedicado", "Dedicated Bandwidth / Internet"),
        ("Mantenimiento y soporte técnico anual", "Annual Maintenance & Support"),
        ("Infraestructura en la Nube (Cloud)", "Cloud Infrastructure (AWS/Azure/GCP)"),
        ("Costo mensual de cómputo en la nube", "Monthly Cloud Hosting"),
        ("Almacenamiento y respaldo mensual", "Monthly Storage & Backup"),
        ("TCO Acumulado Servidor Físico", "Cumulative On-Premises TCO"),
        ("TCO Acumulado Nube", "Cumulative Cloud TCO"),
        ("Punto de equilibrio económico", "Financial Break-Even Point"),
        ("Diferencia neta estimada", "Estimated Net Difference"),
        ("Descargar informe ejecutivo", "Download Executive Summary")
    ],
    "tareas-proyectos-pymes": [
        ("Tareas y Proyectos Operativos", "Operational Tasks & Projects"),
        ("Planificación de entregables, responsables y seguimiento de ejecución.", "Project planning, task assignments, and milestone tracking."),
        ("Proyectos activos", "Active Projects"),
        ("Tareas pendientes", "Pending Tasks"),
        ("Tareas en curso", "In Progress Tasks"),
        ("Tareas completadas", "Completed Tasks"),
        ("Nuevo proyecto", "New Project"),
        ("Nombre del proyecto *", "Project Title *"),
        ("Cliente / Área", "Client / Department"),
        ("Entrega prevista", "Target Due Date"),
        ("Objetivo y notas", "Objective & Notes"),
        ("Crear proyecto", "Create Project"),
        ("Nueva tarea operativa", "New Operational Task"),
        ("Tarea *", "Task Title *"),
        ("Proyecto asociado", "Associated Project"),
        ("Responsable asignado", "Assignee"),
        ("Prioridad", "Priority"),
        ("Baja", "Low"),
        ("Media", "Medium"),
        ("Alta", "High"),
        ("Urgente", "Urgent"),
        ("Fecha límite", "Deadline"),
        ("Añadir tarea", "Add Task"),
        ("Tablero Kanban", "Kanban Board"),
        ("Por hacer", "To Do"),
        ("En curso", "In Progress"),
        ("Bloqueado", "Blocked"),
        ("Terminado", "Done")
    ]
}

print(f"Total tools configured: {len(TOOL_SPECIFIC_REPLACEMENTS)}")

def translate_html_file(file_name):
    src_file = ROOT / file_name
    if not src_file.exists():
        print(f"Warning: {file_name} does not exist.")
        return
    
    content = src_file.read_text(encoding="utf-8")
    tool_key = file_name.replace(".html", "")
    cfg = EN_CONFIGS.get(tool_key, {})
    
    # 1. HTML lang
    content = re.sub(r'<html\s+lang=["\']es["\']', '<html lang="en"', content)
    
    # 2. Path updates for static assets
    content = content.replace('src="./js/', 'src="../js/')
    content = content.replace('href="./css/', 'href="../css/')
    content = content.replace('href="./assets/', 'href="../assets/')
    content = content.replace('src="./assets/', 'src="../assets/')
    content = content.replace('href="./guia-uso-22-apps.html"', 'href="./user-guide.html"')
    content = content.replace('href="./guia-uso-22-apps.html#', 'href="./user-guide.html#')
    content = content.replace('href="./index.html"', 'href="./index.html"')
    
    # Clean up any leftover browser extension artifacts
    content = re.sub(r'<script\s+src=["\']chrome-extension://[^"\']+["\'][^>]*></script>', '', content)
    
    # 3. Update Title & Meta Description
    en_title = cfg.get("title", f"{tool_key} — SMB Cloud")
    en_desc = cfg.get("description", "Free browser tool for small businesses.")
    
    # Replace or add title
    if "<title>" in content:
        content = re.sub(r'<title>.*?</title>', f'<title>{en_title}</title>', content, flags=re.DOTALL)
    else:
        content = content.replace('<head>', f'<head>\n  <title>{en_title}</title>')
        
    # Replace or add meta description
    if 'name="description"' in content:
        content = re.sub(r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']>', f'<meta name="description" content="{en_desc}">', content)
    elif 'content="' in content and 'name="description"' in content:
        content = re.sub(r'<meta\s+content=["\'][^"\']*["\']\s+name=["\']description["\']>', f'<meta name="description" content="{en_desc}">', content)
    else:
        content = content.replace('</title>', f'</title>\n  <meta name="description" content="{en_desc}">')
        
    # 4. Replace window.NP_HELP_CONFIG
    if cfg:
        help_obj = {
            "id": tool_key,
            "name": cfg["name"],
            "purpose": cfg["purpose"],
            "quick": cfg["quick"],
            "tip": cfg["tip"],
            "guide": f"./user-guide.html#{cfg['anchor']}",
            "steps": [{"title": s[1], "text": s[2], "selector": [s[0]]} for s in cfg["steps"]]
        }
        help_json = json.dumps(help_obj, ensure_ascii=False)
        help_replacement = f'window.NP_HELP_CONFIG={help_json};'
        content = re.sub(r'window\.NP_HELP_CONFIG\s*=\s*\{.*?\};', help_replacement, content, flags=re.DOTALL)
        
    # 5. Update data-app-name
    if cfg.get("name"):
        content = re.sub(r'data-app-name=["\'][^"\']+["\']', f'data-app-name="{cfg["name"]}"', content)
        
    # 6. Global Replacements
    for old_s, new_s in GLOBAL_REPLACEMENTS:
        content = content.replace(old_s, new_s)
        
    # 7. Tool-Specific Replacements
    specifics = TOOL_SPECIFIC_REPLACEMENTS.get(tool_key, [])
    for old_s, new_s in specifics:
        content = content.replace(old_s, new_s)
        
    # Write both original filename and english slug filename inside en/
    dest_original = EN_DIR / file_name
    dest_original.write_text(content, encoding="utf-8")
    
    en_slug = cfg.get("en_slug", tool_key)
    dest_slug = EN_DIR / f"{en_slug}.html"
    dest_slug.write_text(content, encoding="utf-8")
    
    print(f"  Processed {file_name} -> en/{file_name} and en/{en_slug}.html")

for t in TOOL_SPECIFIC_REPLACEMENTS.keys():
    translate_html_file(f"{t}.html")

print("\nAll 26 tools translated and generated in en/ successfully!")
