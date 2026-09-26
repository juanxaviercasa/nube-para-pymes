import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

# Complete dictionary of deep tool UI replacements
DEEP_REPLACEMENTS = {
    "guiones-manejo-objeciones.html": [
        ("Base de datos de respuestas de ventas", "Sales Objection Response Database"),
        ("Los mejores scripts para manejar cualquier objeción.", "Proven scripts to overcome any sales objection."),
        ("Encuentra qué decir y por qué funciona, practica el tono en voz alta, recupera el árbol de decisión y presenta sin distracciones con el Modo Zen.",
         "Know what to say and why it works, practice your tone aloud, navigate decision trees, and present distraction-free in Zen Mode."),
        ("Scripts disponibles", "Scripts Available"),
        ("Tipos de objeción", "Objection Types"),
        ("Perfiles de cliente", "Buyer Personas"),
        ("Aportar script", "Contribute Script"),
        ("Explorador", "Explorer"),
        ("Modo Conversación", "Conversation Mode"),
        ("Categoría", "Category"),
        ("Errores de guion (0)", "Script Flags (0)"),
        ("Modo Zen", "Zen Mode"),
        ("Qué decir", "What to Say"),
        ("Por qué funciona", "Why It Works"),
        ("Cliente Analítico", "Analytical Buyer"),
        ("Cliente Decidido", "Decisive Buyer"),
        ("Cliente Exigente", "Demanding Buyer"),
        ("Cliente Cauteloso", "Cautious Buyer"),
        ("Es muy caro", "It's Too Expensive"),
        ("Aislar la objeción real", "Isolate the True Objection"),
        ("Guardar en favoritos", "Save to Favorites"),
        ("No tengo tiempo ahora", "I Don't Have Time Right Now"),
        ("Tengo que consultarlo con mi socio", "I Need to Consult with My Partner"),
        ("Ya trabajamos con otra empresa", "We Already Work with Another Vendor"),
        ("Envíame un correo y lo reviso", "Send Me an Email and I'll Review"),
        ("El próximo trimestre lo vemos", "Let's Revisit Next Quarter"),
        ("No veo claro el retorno", "I Don't See a Clear ROI"),
        ("Tu competencia cobra menos", "Your Competitor Charges Less"),
        ("Nunca he oído hablar de ustedes", "I've Never Heard of Your Company"),
        ("No estamos buscando nada ahora", "We're Not Looking for Anything Right Now"),
        ("Cuando dices que es caro, ¿es que no ves el valor todavía, o es un tema de que no encaja en el presupuesto de este mes? Te lo pregunto porque para cada caso tengo una salida distinta.",
         "When you say it's expensive, is it that you don't see the full value yet, or is it strictly a cash flow timing issue for this quarter? I ask because I have different solutions for each."),
        ("Separa la objeción de valor de la de presupuesto. Sin este diagnóstico, terminas rebajando el precio cuando el problema real era otro.",
         "Separates value perception from budget timing. Without this diagnostic question, you risk discounting prematurely when price wasn't the actual blocker.")
    ],

    "creador-facturas-proforma.html": [
        ("Catálogo", "Catalog"),
        ("Respaldo", "Backup"),
        ("Datos del Emisor", "Business Details"),
        ("Subir Logotipo", "Upload Logo"),
        ("Nombre / Empresa", "Company / Business Name"),
        ("Mi Empresa SAC", "My Company LLC"),
        ("RUC / Identificación", "Tax ID / ABN / EIN"),
        ("Teléfono", "Phone"),
        ("Correo", "Email"),
        ("Datos del Cliente", "Client Details"),
        ("Nombre / Razón Social", "Client Name / Business Name"),
        ("Cliente SAC", "Acme Client Corp"),
        ("Dirección Fiscal", "Billing Address"),
        ("Condiciones y Moneda", "Terms & Currency"),
        ("N.º de Proforma", "Proforma Number"),
        ("Fecha de Emisión", "Issue Date"),
        ("Fecha de Vencimiento", "Due Date"),
        ("Moneda", "Currency"),
        ("Conceptos / Productos", "Line Items & Deliverables"),
        ("Agregar Concepto", "Add Line Item"),
        ("Descripción del producto o servicio", "Description of product or service"),
        ("Cantidad", "Qty"),
        ("Precio Unit.", "Unit Price"),
        ("Subtotal", "Subtotal"),
        ("Impuestos (IGV)", "Tax (Sales Tax / GST)"),
        ("Total General", "Grand Total"),
        ("Total a Pagar", "Total Amount Due"),
        ("Términos y condiciones de pago", "Payment Terms & Bank Details"),
        ("Descargar Proforma en PDF", "Download Proforma PDF"),
        ("Imprimir", "Print Document"),
        ("Nueva Proforma", "New Proforma"),
        ("Exportar JSON", "Export JSON"),
        ("Importar JSON", "Import JSON")
    ],

    "generador-cotizaciones.html": [
        ("Modo Oscuro", "Dark Mode"),
        ("Subir logotipo (procesado localmente)", "Upload Logo (Processed Locally)"),
        ("Agregar ítem", "Add Item"),
        ("Plantilla Clásica", "Classic Template"),
        ("Plantilla Moderna", "Modern Template"),
        ("Nombre de la Empresa Emisora", "Company / Sender Name"),
        ("RUC / Identificador", "Tax ID / ABN / EIN"),
        ("Teléfono / WhatsApp", "Phone / WhatsApp"),
        ("Correo del Cliente", "Client Email"),
        ("N.º de Cotización", "Quote / Estimate Number"),
        ("Fecha de Emisión", "Issue Date"),
        ("Validez de la oferta", "Quote Validity"),
        ("15 días", "15 days"),
        ("30 días", "30 days"),
        ("Datos del Cliente", "Client Information"),
        ("Nombre del Cliente o Empresa", "Client or Company Name"),
        ("Dirección del Cliente", "Client Address"),
        ("Conceptos a Cotizar", "Quoted Items & Services"),
        ("Descripción", "Description"),
        ("Precio Unitario", "Unit Price"),
        ("Descuento (%)", "Discount (%)"),
        ("Subtotal", "Subtotal"),
        ("Impuesto (IGV / IVA)", "Sales Tax / GST"),
        ("Total Cotizado", "Total Quoted Amount"),
        ("Condiciones comerciales y formas de pago", "Terms & Payment Instructions"),
        ("Descargar Cotización (PDF)", "Download Estimate (PDF)"),
        ("Guardar Borrador", "Save Draft")
    ],

    "calculadora-descuentos-promociones.html": [
        ("Descuento Simple", "Simple Discount"),
        ("Margen y Recargo", "Margin & Markup"),
        ("Venta en Combo", "Bundle Pricing"),
        ("Campaña Flash", "Flash Sale"),
        ("Precio original", "Original Price"),
        ("Porcentaje de descuento", "Discount Percentage"),
        ("Precio final con descuento", "Final Discounted Price"),
        ("Ahorro del cliente", "Customer Savings"),
        ("Margen bruto resultante", "Resulting Gross Margin"),
        ("Unidades adicionales necesarias para mantener ganancia", "Additional units needed to maintain profit"),
        ("Punto de equilibrio promocional", "Promotional Break-Even"),
        ("Calcular", "Calculate"),
        ("Simular escenario", "Simulate Scenario"),
        ("Costo unitario", "Unit Cost"),
        ("Precio de venta", "Selling Price"),
        ("Margen deseado", "Target Margin"),
        ("Recargo sobre costo (Markup)", "Markup on Cost"),
        ("Ganancia unitaria", "Profit per Unit"),
        ("Producto 1", "Product 1"),
        ("Producto 2", "Product 2"),
        ("Producto 3", "Product 3"),
        ("Suma individual", "Individual Sum"),
        ("Precio del combo", "Bundle Price"),
        ("Ahorro en combo", "Bundle Savings")
    ],

    "calculadora-precios-venta-igv.html": [
        ("Costo unitario del producto o servicio", "Unit Cost of Product or Service"),
        ("Margen neto deseado (%)", "Target Net Margin (%)"),
        ("Tasa de impuesto (IGV / Sales Tax / GST)", "Tax Rate (Sales Tax / GST %)"),
        ("Precio antes de impuestos (Neto)", "Pre-Tax Selling Price (Net)"),
        ("Monto de impuesto", "Sales Tax / GST Amount"),
        ("Precio final al consumidor", "Final Customer Retail Price"),
        ("Ganancia neta en dinero", "Net Profit Amount"),
        ("Margen sobre costo (Markup)", "Markup on Cost"),
        ("Desglose detallado", "Itemized Breakdown"),
        ("Descargar desglose", "Download Breakdown"),
        ("Calcular Precio", "Calculate Price"),
        ("Escenario A", "Scenario A"),
        ("Escenario B", "Scenario B"),
        ("Comparativa de márgenes", "Margin Comparison")
    ],

    "generador-politicas-terminos.html": [
        ("Limpiar formulario", "Clear Form"),
        ("Formulario", "Form"),
        ("Vista previa", "Preview"),
        ("Corporativo", "Corporate"),
        ("Información web", "Web Information"),
        ("Tienda online", "Online Store"),
        ("Comercio electrónico", "E-commerce"),
        ("Continuar", "Continue"),
        ("Nombre de la empresa", "Company Legal Name"),
        ("URL del sitio web", "Website URL"),
        ("País", "Country / State Jurisdiction"),
        ("Identificación fiscal(opcional)", "Tax ID / ABN / EIN (Optional)"),
        ("Domicilio fiscal(opcional)", "Registered Address (Optional)"),
        ("Correo de contacto legal", "Legal Contact Email"),
        ("Generar documento legal", "Generate Legal Document"),
        ("Copiar texto", "Copy Document Text"),
        ("Descargar TXT", "Download TXT")
    ],

    "generador-paletas-corporativas.html": [
        ("Descargar PDF", "Download PDF"),
        ("Aleatorio", "Random"),
        ("Análogos — 30 º", "Analogous — 30°"),
        ("Tétrada — 90 º", "Tetradic — 90°"),
        ("Tríada — 120 º", "Triadic — 120°"),
        ("Guardar en galería", "Save to Library"),
        ("Color Base (HEX)", "Base Brand Color (HEX)"),
        ("Nombra tu paleta (ej. Marca Fintech)", "Name your palette (e.g. Fintech Brand)"),
        ("Armonías cromáticas", "Color Harmonies"),
        ("Verificación de Contraste WCAG", "WCAG Contrast Checker"),
        ("Contraste texto normal", "Normal Text Contrast"),
        ("Contraste texto grande", "Large Text Contrast"),
        ("Cumple WCAG AA", "Passes WCAG AA"),
        ("Cumple WCAG AAA", "Passes WCAG AAA")
    ],

    "simulador-tco-fisico-nube.html": [
        ("Guardar Escenario", "Save Scenario"),
        ("Compartir", "Share"),
        ("Informe en PDF", "PDF Report"),
        ("Simulador", "Simulator"),
        ("Comparador (0)", "Comparator (0)"),
        ("Cantidad nodos", "Node Count"),
        ("Hardware inicial $USD", "Initial Hardware ($USD)"),
        ("Energía / mes $USD", "Power / Month ($USD)"),
        ("Internet / mes $USD", "Internet / Month ($USD)"),
        ("Mantenimiento / año $USD", "Maintenance / Year ($USD)"),
        ("Licencias / año $USD", "Licensing / Year ($USD)"),
        ("Nombre del nodo", "Node Name"),
        ("Nombre de la instancia", "Instance Name"),
        ("Costo mensual Cloud $USD", "Monthly Cloud Cost ($USD)"),
        ("Almacenamiento Cloud $USD", "Cloud Storage ($USD)"),
        ("TCO Servidor Físico", "On-Premises Server TCO"),
        ("TCO Nube Pública", "Public Cloud TCO"),
        ("Punto de equilibrio", "Break-Even Horizon")
    ],

    "organizador-matriz-contenidos.html": [
        ("Sugerir reciclaje", "Suggest Repurposing"),
        ("Nueva idea", "New Idea"),
        ("Semana", "Week"),
        ("Mes", "Month"),
        ("Hoy", "Today"),
        ("Pilares de contenido", "Content Pillars"),
        ("Etapa del funnel", "Funnel Stage"),
        ("Atracción (ToFU)", "Top of Funnel (Awareness)"),
        ("Consideración (MoFU)", "Middle of Funnel (Consideration)"),
        ("Conversión (BoFU)", "Bottom of Funnel (Conversion)"),
        ("Fidelización", "Retention & Advocacy"),
        ("Canal", "Channel"),
        ("Formato", "Format"),
        ("Fecha de publicación", "Publish Date"),
        ("Estado", "Status"),
        ("Idea", "Idea"),
        ("En redacción", "In Drafting"),
        ("Listo para publicar", "Ready to Publish"),
        ("Publicado", "Published")
    ],

    "generador-politicas-devolucion.html": [
        ("Ropa y Moda", "Apparel & Fashion"),
        ("Tallas, prendas y accesorios", "Sizes, clothing, and accessories"),
        ("Electrónica", "Consumer Electronics"),
        ("Gadgets y dispositivos", "Gadgets and tech devices"),
        ("Servicios Digitales", "Digital Services"),
        ("Software, cursos, licencias", "Software, courses, and licenses"),
        ("Alimentos", "Food & Beverage"),
        ("Productos perecederos", "Perishable goods"),
        ("Generar política", "Generate Policy"),
        ("Plazo para devoluciones", "Return Timeframe"),
        ("14 días", "14 days"),
        ("30 días", "30 days"),
        ("60 días", "60 days"),
        ("Condiciones del producto", "Product Conditions"),
        ("En empaque original", "In original packaging"),
        ("Sin usar", "Unused condition"),
        ("Reembolso al método original", "Refund to original payment method"),
        ("Crédito en tienda", "Store credit or exchange"),
        ("Copiar texto", "Copy Policy Text")
    ],

    "generador-contratos-servicios.html": [
        ("Genera contratos de servicios profesionales sin esfuerzo.", "Draft professional service agreements effortlessly."),
        ("Datos del Proveedor", "Service Provider Details"),
        ("Datos del Cliente", "Client Details"),
        ("Descripción del servicio", "Scope of Work & Services"),
        ("Entregables", "Deliverables"),
        ("Honorarios", "Fees & Invoicing"),
        ("Forma de pago", "Payment Terms"),
        ("Fecha de inicio", "Effective Start Date"),
        ("Fecha de término", "Completion Date"),
        ("Generar contrato", "Generate Agreement"),
        ("Descargar PDF", "Download PDF")
    ],

    "generador-contrasenas-pymes.html": [
        ("Guía de ciberseguridad", "Cybersecurity Guide"),
        ("Generador", "Generator"),
        ("Importar Bóveda", "Import Vault"),
        ("Kit de Emergencia", "Emergency Kit"),
        ("Generar contraseña segura", "Generate Secure Password"),
        ("Minúsculas", "Lowercase (a-z)"),
        ("Mayúsculas", "Uppercase (A-Z)"),
        ("Números", "Numbers (0-9)"),
        ("Símbolos", "Symbols (!@#$)"),
        ("Longitud", "Length"),
        ("Fuerza:", "Strength:"),
        ("Copiar", "Copy"),
        ("Nueva clave", "New Key")
    ],

    "generador-codigos-qr.html": [
        ("Parámetros de rastreo (UTM)", "Campaign Tracking Parameters (UTM)"),
        ("Clásico", "Classic"),
        ("Moderno", "Modern"),
        ("Icono de chat al centro", "Center Chat Icon"),
        ("Número de WhatsApp", "WhatsApp Number"),
        ("Número sin código de país", "Phone number with country code"),
        ("Mensaje predefinido", "Pre-filled Message"),
        ("Hola, me gustaría recibir más información sobre...", "Hi! I'd like more information about..."),
        ("Generar Código QR", "Generate QR Code"),
        ("Descargar imagen PNG", "Download PNG Image")
    ],

    "calculadora-prestamos-amortizaciones.html": [
        ("Monto del préstamo", "Loan Amount"),
        ("Tasa de interés anual (%)", "Annual Interest Rate (%)"),
        ("Plazo (meses)", "Loan Term (Months)"),
        ("Cuota mensual", "Monthly Payment"),
        ("Total intereses", "Total Interest"),
        ("Costo total", "Total Loan Cost"),
        ("Abono extraordinario", "Extra Payment"),
        ("Tabla de amortización", "Amortization Table"),
        ("Mes", "Month"),
        ("Cuota", "Payment"),
        ("Interés", "Interest"),
        ("Capital", "Principal"),
        ("Saldo pendiente", "Remaining Balance")
    ],

    "calculadora-sobrecostos-laborales.html": [
        ("Moneda", "Currency"),
        ("Agregar empleado", "Add Employee"),
        ("Salario base", "Base Wage"),
        ("Aportes del empleador", "Employer Taxes & Contributions"),
        ("Beneficios y provisiones", "Statutory Benefits & Accruals"),
        ("Costo mensual total", "Total Monthly Cost"),
        ("Costo anual total", "Total Annual Cost"),
        ("Descargar reporte", "Download Report")
    ],

    "calculadora-flete-envio-local.html": [
        ("Largo (cm)", "Length (cm)"),
        ("Ancho (cm)", "Width (cm)"),
        ("Alto (cm)", "Height (cm)"),
        ("Peso real (kg)", "Actual Weight (kg)"),
        ("Tipo de vehículo", "Vehicle Type"),
        ("Zona de entrega", "Delivery Zone"),
        ("Paradas adicionales", "Additional Stops"),
        ("Costo total estimado", "Estimated Total Cost"),
        ("Generar manifiesto", "Generate Manifest")
    ],

    "comparador-campanas-avanzado.html": [
        ("Nueva campaña", "New Campaign"),
        ("Plataforma", "Platform"),
        ("Presupuesto", "Budget Spend"),
        ("Impresiones", "Impressions"),
        ("Clics", "Clicks"),
        ("Conversiones", "Conversions"),
        ("Ingresos", "Revenue"),
        ("Comparativa", "Comparison"),
        ("Exportar reporte", "Export Report")
    ],

    "consola-campanas.html": [
        ("URL de destino", "Landing Page URL"),
        ("Fuente de tráfico", "Traffic Source"),
        ("Medio de campaña", "Campaign Medium"),
        ("Nombre de campaña", "Campaign Name"),
        ("Generar enlace UTM", "Generate UTM Link"),
        ("Copiar enlace", "Copy Link")
    ],

    "conversor-optimizador-imagenes.html": [
        ("Formato de salida", "Output Format"),
        ("Calidad de compresión", "Compression Quality"),
        ("Ancho máximo", "Max Width"),
        ("Optimizar y Convertir", "Optimize & Convert"),
        ("Descargar imagen", "Download Image"),
        ("Descargar todas (ZIP)", "Download All (ZIP)")
    ],

    "firma-correo-html.html": [
        ("Nombre completo", "Full Name"),
        ("Cargo o profesión", "Role / Job Title"),
        ("Empresa o marca", "Company / Brand"),
        ("Teléfono", "Phone"),
        ("Sitio web", "Website"),
        ("Dirección", "Address"),
        ("URL de foto o logo", "Photo / Logo URL"),
        ("URL del banner (imagen)", "Banner Image URL"),
        ("Enlace del banner", "Banner Link URL"),
        ("Copiar firma", "Copy Signature"),
        ("Copiar código HTML", "Copy HTML Code")
    ]
}

def apply_deep_replacements():
    count = 0
    # Process both the original name and english slug in en/
    from en_help_configs import EN_CONFIGS
    
    for tool_id, reps in DEEP_REPLACEMENTS.items():
        base_name = tool_id.replace(".html", "")
        cfg = EN_CONFIGS.get(base_name, {})
        en_slug = cfg.get("en_slug", base_name)
        
        target_files = [EN_DIR / tool_id, EN_DIR / f"{en_slug}.html"]
        for tf in target_files:
            if not tf.exists():
                continue
            text = tf.read_text(encoding="utf-8")
            for es, en in reps:
                text = text.replace(es, en)
            tf.write_text(text, encoding="utf-8")
            count += 1
            
    print(f"Deep tool replacements applied across {count} files in en/!")

apply_deep_replacements()
