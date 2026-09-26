# English Help Configs & Metadata for all 26 Tools
# Adapted for US and Australian Small & Medium Businesses

EN_CONFIGS = {
    "analizador-titulares": {
        "en_slug": "headline-analyzer",
        "name": "Headline Analyzer",
        "title": "Headline Analyzer — Free Title & CTR Optimization Tool",
        "description": "Evaluate clarity, power words, sentiment, and SEO strength of your headlines. Maximize clicks for ads, articles, and landing pages with local NLP.",
        "purpose": "Evaluate clarity, power words, emotional tone, and appeal of headlines to improve click-through rates across ads, articles, pages, and social media posts.",
        "anchor": "1-headline-analyzer",
        "quick": [
            "Enter your headline and optionally your target keyword.",
            "Run the analysis and review your score, emotional tone, readability, and recommendations.",
            "Compare A/B variations side-by-side and copy or export the detailed report."
        ],
        "tip": "Don't just chase a high score: ensure the headline accurately represents your offer and connects directly with your audience.",
        "steps": [
            ("h1", "Define the Objective", "Understand what the headline promises and who it is written for."),
            ("textarea,input[type=text]", "Write Your Headline", "Enter a working headline and re-analyze after each iteration."),
            ("button", "Analyze and Compare", "Use the score breakdown and A/B comparison tools to test alternatives.")
        ]
    },
    "auditor-seo-basico": {
        "en_slug": "basic-seo-auditor",
        "name": "Basic On-Page SEO Auditor",
        "title": "Basic On-Page SEO Auditor — Meta Tags & Content Checklist",
        "description": "Audit on-page SEO signals including titles, descriptions, H1 tags, content density, and search snippet previews directly in your browser.",
        "purpose": "Review editorial on-page signals — title tags, meta descriptions, H1 headers, content depth, and snippet previews — to generate actionable SEO improvements.",
        "anchor": "2-basic-seo-on-page-auditor",
        "quick": [
            "Enter your URL or fill in your page details manually.",
            "Run the audit to review SEO health scores, recommendations, and search previews.",
            "Save the audit report to your history and re-run after making updates to track progress."
        ],
        "tip": "An on-page audit addresses content factors; pair it with Google Search Console and technical server diagnostics for complete indexing health.",
        "steps": [
            ("input[type=url],input", "Enter Webpage Details", "Provide a live URL or manually enter title, description, H1, and body content."),
            ("textarea,input", "Complete SEO Elements", "Ensure content accurately reflects the target page and search intent."),
            ("button", "Run Audit", "Execute the audit, review prioritized recommendations, and save to local history.")
        ]
    },
    "calculadora-descuentos-promociones": {
        "en_slug": "discount-promotions-calculator",
        "name": "Discounts & Promotions Calculator",
        "title": "Discounts & Promotions Calculator — Margins & Break-Even Simulator",
        "description": "Calculate promotional discounts, profit margins, break-even sales volume, product bundles, and flash sale ROI for small businesses.",
        "purpose": "Simulate discounts, gross margins, break-even thresholds, bundles, customer lifetime value (CLV), and flash sales to make data-backed commercial decisions.",
        "anchor": "3-discounts-and-promotions-calculator",
        "quick": [
            "Select the scenario matching your pricing decision.",
            "Enter base price, unit cost, discount percentage, target volume, and related parameters.",
            "Compare net profitability before launching your promotional offer."
        ],
        "tip": "Distinguish between gross profit margin on sales and markup on cost, and avoid premature rounding during calculation.",
        "steps": [
            ("[role=tab],button", "Select Scenario", "Switch between simple discount, margin simulation, bundle pricing, CLV, or flash sale."),
            ("input", "Input Figures", "Enter base price, unit costs, sales units, and discount rates."),
            ("button", "Review Profitability", "Examine net profit, final price, and margin before launching.")
        ]
    },
    "calculadora-flete-envio-local": {
        "en_slug": "local-shipping-calculator",
        "name": "Local Shipping & Freight Calculator",
        "title": "Local Shipping & Delivery Calculator — Dimensional Weight & Rates",
        "description": "Calculate local delivery rates, compare actual vs. dimensional weight, plan multi-stop courier routes, and generate shipment manifests.",
        "purpose": "Estimate local delivery costs based on package dimensions, weight, vehicle type, delivery zones, and multiple stops, and prepare a shipment manifest.",
        "anchor": "4-local-shipping-and-freight-calculator",
        "quick": [
            "Enter package dimensions, actual weight, and vehicle type.",
            "Add delivery stops and choose target zones.",
            "Review rates, surcharges, and total, then export the delivery manifest once finalized."
        ],
        "tip": "Verify dimensional weight rules, vehicle access limits, wait times, insurance coverage, and special handling fees with your courier.",
        "steps": [
            ("input", "Describe Package", "Enter length, width, height, and gross weight using consistent measurement units."),
            ("button,select", "Define Route & Vehicle", "Select vehicle class, delivery zone, and delivery drop-off points."),
            ("button", "Calculate & Export", "Check total delivery cost and generate the manifest or shipping label.")
        ]
    },
    "calculadora-precios-venta-igv": {
        "en_slug": "sales-pricing-tax-calculator",
        "name": "Sales Pricing & Tax Calculator",
        "title": "Sales Pricing & Tax Calculator — Margin, Markup & Sales Tax / GST",
        "description": "Calculate retail selling prices, net profit margins, and sales tax / GST. Compare pricing scenarios and download itemized breakdowns.",
        "purpose": "Convert product unit cost, desired net margin, and applicable sales tax or GST into a profitable selling price with full tax breakdowns.",
        "anchor": "5-sales-pricing-and-tax-calculator",
        "quick": [
            "Enter the unit cost of your product or service.",
            "Specify your target profit margin and confirm the applicable Sales Tax / GST percentage.",
            "Compare pricing scenarios, save results locally, or download the itemized price breakdown."
        ],
        "tip": "Confirm statutory sales tax or GST rates applicable to your jurisdiction (e.g. US state tax, Australian 10% GST). This simulation does not replace professional tax advice.",
        "steps": [
            ("input", "Input Cost & Desired Margin", "Enter product cost, target profit percentage, and sales tax / GST rate."),
            ("button", "Compare Scenarios", "Adjust values dynamically to observe changes in final customer price and net revenue."),
            ("button", "Save & Export Breakdown", "Save your pricing model or download a clean PDF summary.")
        ]
    },
    "calculadora-prestamos-amortizaciones": {
        "en_slug": "loan-amortization-calculator",
        "name": "Loan & Amortization Calculator",
        "title": "Loan & Amortization Calculator — Repayment Schedules & Extra Payments",
        "description": "Calculate business loan payments, generate full amortization schedules, simulate lump-sum extra payments, and calculate interest savings.",
        "purpose": "Calculate monthly loan payments, total interest paid, and full amortization schedules, while simulating early extra payments and credit terms.",
        "anchor": "6-loan-and-amortization-calculator",
        "quick": [
            "Enter loan amount, annual interest rate, and term length.",
            "Select grace period or payment frequency and review the detailed amortization schedule.",
            "Simulate lump-sum extra payments to see interest savings and term reductions."
        ],
        "tip": "Verify whether your lender quotes nominal APR or effective annual rates, and account for origination fees, closing costs, and required insurance.",
        "steps": [
            ("input", "Define Loan Parameters", "Enter principal amount, interest rate, and repayment term."),
            ("select,input", "Configure Schedule", "Select payment frequency, grace periods, or interest-only terms."),
            ("button", "Analyze Savings", "Review monthly payments, total interest expense, and early extra payoff benefits.")
        ]
    },
    "calculadora-sobrecostos-laborales": {
        "en_slug": "labor-cost-calculator",
        "name": "Labor Cost & Payroll Burden Calculator",
        "title": "Labor Cost & Payroll Burden Calculator — True Employee Expense",
        "description": "Calculate total employer cost per employee including base wages, statutory benefits, payroll taxes, workers comp, and annual provisions.",
        "purpose": "Estimate the true employer cost of hiring staff per employee, department, and pay period, factoring in mandatory benefits, statutory taxes, and provisions.",
        "anchor": "7-labor-cost-and-payroll-burden-calculator",
        "quick": [
            "Set your currency and payroll parameters.",
            "Add team members with job titles, departments, and base compensation.",
            "Review true employer cost breakdowns, filter by department, and export the payroll report."
        ],
        "tip": "Adjust statutory percentages for payroll taxes (e.g., FICA/Medicare in US, Superannuation in AU). Use for operational budgeting, not as a legal payroll settlement slip.",
        "steps": [
            ("input,button", "Configure Settings", "Select currency, statutory contribution rates, and burden assumptions."),
            ("input", "Add Team Roster", "Record employee names, titles, departments, and gross salaries."),
            ("button", "Analyze & Export", "Filter by department, toggle monthly/annual views, and download the report.")
        ]
    },
    "comparador-campanas-avanzado": {
        "en_slug": "ad-campaign-comparator",
        "name": "Ad Campaign Performance Comparator",
        "title": "Ad Campaign Performance Comparator — ROI, ROAS, CPA & CTR",
        "description": "Compare marketing campaigns across Meta, Google Ads, TikTok, and LinkedIn. Analyze budget, conversions, CPA, ROAS, and profit side-by-side.",
        "purpose": "Compare advertising campaigns and investment scenarios side-by-side to assess ad spend, revenue, return on investment (ROAS/ROI), and cross-channel efficiency.",
        "anchor": "8-ad-campaign-performance-comparator",
        "quick": [
            "Create or select advertising campaign scenarios.",
            "Enter ad spend, clicks, conversion volume, and resulting revenue.",
            "Compare channels side-by-side and export performance comparisons for client or internal reporting."
        ],
        "tip": "Standardize your reporting timeframes; a channel generating higher gross revenue may carry a lower net profit or higher acquisition cost (CPA).",
        "steps": [
            ("button,[role=tab]", "Select Platform", "Choose a channel (Google, Meta, LinkedIn) or create a custom scenario."),
            ("input", "Input Campaign Metrics", "Enter spend, impressions, clicks, conversions, and revenue."),
            ("button", "Compare Metrics", "Evaluate ROAS, CPA, and profit margins to optimize marketing budget allocation.")
        ]
    },
    "consola-campanas": {
        "en_slug": "utm-campaign-console",
        "name": "UTM Campaign Builder Console",
        "title": "UTM Campaign Builder Console — Clean Tracking URLs & Tagging",
        "description": "Build, standardize, and organize UTM tracking URLs for Google Analytics 4 and marketing tools. Maintain consistent campaign naming conventions.",
        "purpose": "Organize marketing campaigns, generate error-free UTM tracking links, and maintain consistent naming conventions across all digital acquisition channels.",
        "anchor": "9-utm-campaign-builder-console",
        "quick": [
            "Enter landing page URL, source, medium, campaign name, content, and term.",
            "Generate clean UTM links with automatic URL validation and lowercase formatting.",
            "Save or copy links directly into your ads, email campaigns, and social posts."
        ],
        "tip": "Use lowercase characters and hyphens consistently; avoid placing personally identifiable information (PII) inside visible URL query parameters.",
        "steps": [
            ("input", "Define Campaign Context", "Enter destination URL, traffic source, medium, and campaign identifier."),
            ("button", "Generate UTM Link", "Click to generate the formatted tracking URL."),
            ("button", "Copy & Test Destination", "Copy your link and verify that the destination URL loads properly.")
        ]
    },
    "conversor-optimizador-imagenes": {
        "en_slug": "image-converter-optimizer",
        "name": "WebP Forge — Image Converter & Optimizer",
        "title": "WebP Forge — Free Browser Image Converter & WebP Optimizer",
        "description": "Convert PNG, JPEG, and WebP images locally in your browser. Compress file sizes, adjust quality, resize dimensions, and boost webpage speed.",
        "purpose": "Convert and optimize images for the web locally in the browser, reducing file size and adjusting formats to accelerate page load times.",
        "anchor": "10-webp-forge-image-converter-and-optimizer",
        "quick": [
            "Drag and drop or select images from your computer.",
            "Select target format (WebP, PNG, JPG), compression quality, and maximum dimensions.",
            "Preview compression savings and download the optimized images."
        ],
        "tip": "Keep original high-res masters safely archived, and ensure compression retains sufficient sharpness for your intended display scale.",
        "steps": [
            ("input[type=file]", "Upload Images", "Select images from your device; processing is 100% local and private."),
            ("input,select", "Adjust Compression", "Set target format, compression level, and dimension constraints."),
            ("button", "Download Optimized Files", "Review file size savings and download optimized assets.")
        ]
    },
    "creador-facturas-proforma": {
        "en_slug": "proforma-invoice-generator",
        "name": "Proforma Invoice Generator",
        "title": "Proforma Invoice Generator — Create & Export Proforma Invoices",
        "description": "Generate professional proforma invoices with company branding, client details, line items, taxes, and payment instructions. Download print-ready PDFs.",
        "purpose": "Prepare professional proforma invoices locally with business identity, client information, line items, quantities, taxes, and totals for instant export.",
        "anchor": "11-proforma-invoice-generator",
        "quick": [
            "Enter company details, client contact information, invoice number, and date.",
            "Add product/service items with quantities, unit prices, and applicable taxes.",
            "Review subtotals and click Download to generate a print-ready proforma invoice."
        ],
        "tip": "A proforma invoice is a preliminary commercial quote and agreement, not an official tax invoice. Review jurisdictional requirements before final billing.",
        "steps": [
            ("input,textarea", "Enter Header Details", "Add seller details, client info, proforma number, and payment terms."),
            ("input,button", "Add Line Items", "Add goods or services with quantities, rates, and tax percentages."),
            ("button", "Review & Download", "Verify calculated totals and download or print the proforma invoice.")
        ]
    },
    "crm-pymes": {
        "en_slug": "smb-crm",
        "name": "SMB CRM & Sales Pipeline",
        "title": "SMB CRM & Sales Pipeline — Lightweight Local-First Sales Manager",
        "description": "Track client contacts, manage sales opportunities through a customizable visual pipeline, calculate weighted revenue, and never miss a follow-up.",
        "purpose": "Centralize contacts, deals, commercial pipeline stages, and next actions to organize sales follow-ups and close more business without subscriptions.",
        "anchor": "12-smb-crm-and-sales-pipeline",
        "quick": [
            "Add new customer companies and contact persons.",
            "Create deals with deal value, stage, win probability, and next follow-up date.",
            "Move deals across pipeline columns and monitor overdue follow-ups."
        ],
        "tip": "Assign an upcoming action and target date to every active deal to maintain deal momentum across your pipeline.",
        "steps": [
            ("#contact-form", "Add New Contact", "Save company name, contact person, phone, email, and notes."),
            ("#opportunity-form", "Create Deal Opportunity", "Assign deal value, stage, win probability, and next follow-up action."),
            ("#pipeline", "Manage Visual Pipeline", "Update stages directly on deal cards and prioritize overdue follow-ups.")
        ]
    },
    "firma-correo-html": {
        "en_slug": "html-email-signature",
        "name": "HTML Email Signature Generator",
        "title": "HTML Email Signature Generator — Professional Email Signatures",
        "description": "Design sleek, responsive HTML email signatures for your team. Compatible with Gmail, Outlook, Apple Mail, and mobile email clients.",
        "purpose": "Design cohesive, responsive email signatures featuring corporate branding, contact channels, social links, and clean HTML ready for any email client.",
        "anchor": "13-html-email-signature-generator",
        "quick": [
            "Fill in full name, title, company name, and contact details.",
            "Customize brand colors, logo URL, banner graphics, and social links.",
            "Preview rendering and copy or download the HTML signature code."
        ],
        "tip": "Include only essential business channels and test across desktop and mobile email clients before rolling out to your organization.",
        "steps": [
            ("input,textarea", "Enter Contact Information", "Provide your professional credentials, title, phone, and website."),
            ("input[type=color],input", "Brand Visual Styling", "Adjust theme accent colors, profile picture, logo, and social links."),
            ("button", "Copy HTML Signature", "Preview the live signature and copy the formatted signature or HTML.")
        ]
    },
    "flujo-caja-pymes": {
        "en_slug": "cash-flow-tracker",
        "name": "Cash Flow & Receivables Tracker",
        "title": "Cash Flow & Receivables Tracker — Forecast Liquidity & Invoices",
        "description": "Track operational cash inflows, outflows, receivables, and payables. Monitor net cash balance and forecast small business liquidity.",
        "purpose": "Record cash inflows, outflows, invoice due dates, and settlement status to monitor operating balances and prevent liquidity shortfalls.",
        "anchor": "14-cash-flow-and-receivables-tracker",
        "quick": [
            "Record each cash transaction with type (inflow/outflow), amount, category, and date.",
            "Associate records with specific clients or vendors.",
            "Mark items as paid or collected upon actual settlement.",
            "Review category summaries to maintain liquidity control."
        ],
        "tip": "Consistent daily or weekly entry ensures accurate cash forecasts; do not confuse managerial cash flow with accrual fiscal accounting.",
        "steps": [
            ("input,select", "Record Transactions", "Log transaction type, amount, category, client/vendor, and payment status."),
            ("table,article", "Review Liquidity Summary", "Examine current cash balance, overdue receivables, and upcoming payables."),
            ("button", "Maintain Cash Records", "Update payment statuses and export JSON backups regularly.")
        ]
    },
    "generador-codigos-qr": {
        "en_slug": "qr-code-generator",
        "name": "QR Code & WhatsApp Direct Generator",
        "title": "QR Code & WhatsApp Direct Generator — Free Scannable Codes",
        "description": "Generate scannable QR codes for websites, WhatsApp direct messages, WiFi credentials, and plain text. Download high-resolution PNGs.",
        "purpose": "Generate scannable QR codes for web links, pre-filled WhatsApp messages, contact cards, and text, with customization and direct image downloads.",
        "anchor": "15-qr-code-and-whatsapp-direct-generator",
        "quick": [
            "Select content type: Web URL, WhatsApp direct chat, or custom text.",
            "Input destination URL or phone number with international country code.",
            "Generate, test by scanning with a smartphone, and download high-resolution graphics."
        ],
        "tip": "A QR code cannot fix a broken link: always scan-test the live code on multiple devices before sending to print.",
        "steps": [
            ("button,[role=tab]", "Select Code Type", "Choose Web URL, WhatsApp chat link, or text message."),
            ("input,textarea", "Enter Destination Data", "Fill in link or phone number with country prefix."),
            ("button,canvas", "Generate & Download", "Review rendering, test scan with your camera, and save the image.")
        ]
    },
    "generador-contrasenas-pymes": {
        "en_slug": "password-generator",
        "name": "SecuKey — Password Generator for Small Teams",
        "title": "SecuKey — Secure Password Generator & Entropy Checker",
        "description": "Generate strong, randomized passwords and passphrases locally in your browser. Evaluate entropy, customize characters, and secure team accounts.",
        "purpose": "Generate strong, cryptographically secure passwords and passphrases locally with customizable length, symbols, and entropy scoring.",
        "anchor": "16-secukey-password-generator-for-small-teams",
        "quick": [
            "Select desired password length and character sets (uppercase, lowercase, numbers, symbols).",
            "Generate single or batch passwords with live entropy ratings.",
            "Copy securely and store immediately in an encrypted team password manager."
        ],
        "tip": "Never reuse passwords across critical business services; a generator creates keys but should always be paired with a dedicated password manager.",
        "steps": [
            ("input", "Configure Complexity", "Set length (recommended 16+ characters) and character sets."),
            ("button", "Generate Strong Password", "Click to generate a fresh cryptographically random key."),
            ("button", "Copy Securely", "Copy to clipboard, store in your vault, and clear clipboard history.")
        ]
    },
    "generador-contratos-servicios": {
        "en_slug": "service-contract-generator",
        "name": "Service Agreement Generator",
        "title": "Service Agreement Generator — Contractor & Consulting Contracts",
        "description": "Draft customizable independent contractor and professional service agreements. Define deliverables, payment terms, IP rights, and confidentiality.",
        "purpose": "Generate customizable professional service contracts and contractor agreements covering scope of work, deliverables, payment milestones, IP, and confidentiality.",
        "anchor": "17-service-agreement-generator",
        "quick": [
            "Input client and service provider legal entities.",
            "Detail scope of work, project milestones, payment schedules, and turnaround times.",
            "Generate, review, and download the draft contract for legal signing."
        ],
        "tip": "This tool provides an operational commercial draft; always have contracts reviewed by licensed legal counsel to comply with your governing jurisdiction.",
        "steps": [
            ("input,textarea", "Party Identification", "Enter full legal names, company registration numbers, addresses, and contacts."),
            ("input,textarea", "Scope & Payment Terms", "Detail deliverables, revision limits, fees, payment schedule, and deadlines."),
            ("button", "Generate & Review", "Review clauses, adjust wording, and export for formal signing.")
        ]
    },
    "generador-cotizaciones": {
        "en_slug": "quote-estimate-generator",
        "name": "Quote & Estimate Generator",
        "title": "Quote & Estimate Generator — Professional Estimates in PDF",
        "description": "Build branded client quotes, estimates, and proposals. Support multi-currency, tax rates, line items, and terms. Export print-ready PDFs.",
        "purpose": "Build professional multi-currency commercial estimates with custom business branding, line items, discounts, taxes, validity terms, and PDF export.",
        "anchor": "18-quote-and-estimate-generator",
        "quick": [
            "Enter business details, client info, estimate number, and currency.",
            "Add line items with descriptions, quantities, unit prices, and discounts.",
            "Review subtotals, specify validity period and payment terms, and download the PDF."
        ],
        "tip": "Clearly state proposal expiration dates, payment milestones, scope boundaries, and applicable taxes to avoid misunderstandings with clients.",
        "steps": [
            ("input,textarea", "Complete Header", "Input business identity, client details, estimate date, and currency."),
            ("input,button", "Add Deliverables", "Add line items, billable rates, quantities, and discount rates."),
            ("button", "Export Client Quote", "Review final summary and export a polished PDF estimate.")
        ]
    },
    "generador-paletas-corporativas": {
        "en_slug": "brand-palette-generator",
        "name": "Brand Color Palette Generator",
        "title": "Chroma — Brand Color Palette Generator & Contrast Checker",
        "description": "Generate harmonious color schemes for brand identity, logos, and web UI. Check WCAG contrast compliance and copy HEX, RGB, and CSS codes.",
        "purpose": "Create harmonious, accessible brand color palettes with harmonic rules, WCAG contrast verification, and exportable HEX, RGB, and CSS tokens.",
        "anchor": "19-chroma-brand-color-palette-generator",
        "quick": [
            "Pick or input your primary brand base color in HEX format.",
            "Explore color harmonies (analogous, triadic, complementary, monochromatic).",
            "Verify text-to-background contrast and copy color tokens for your design system."
        ],
        "tip": "Ensure your primary text and button combinations pass WCAG AA contrast standards (minimum 4.5:1 ratio) on both light and dark backgrounds.",
        "steps": [
            ("input[type=color],input", "Set Primary Brand Color", "Input your core brand HEX color or explore presets."),
            ("button", "Generate Harmonies", "Generate complementary, triadic, and analogous color shades."),
            ("button", "Check Contrast & Copy Tokens", "Verify legibility scores and copy color values for web and print.")
        ]
    },
    "generador-politicas-devolucion": {
        "en_slug": "return-refund-policy-generator",
        "name": "Return & Refund Policy Generator",
        "title": "Return & Refund Policy Generator — Ecommerce & Retail Policies",
        "description": "Create customized return, refund, and exchange policies for your ecommerce store or retail business. Tailored for physical and digital goods.",
        "purpose": "Draft customized return and refund policies specifying return windows, eligible item conditions, exchange processes, refund methods, and support channels.",
        "anchor": "20-return-and-refund-policy-generator",
        "quick": [
            "Select your business model: physical goods, apparel, electronics, or digital services.",
            "Define return window (e.g. 14, 30 days), shipping responsibility, and refund mechanisms.",
            "Generate, review, and download the finished policy for your website or storefront."
        ],
        "tip": "Ensure your published return policy complies with consumer protection laws in your operating states or countries (such as statutory guarantees in Australia).",
        "steps": [
            ("input,textarea", "Business & Product Type", "Select your catalog type and input contact and business details."),
            ("input,button", "Define Return Rules", "Configure return eligibility, inspection rules, restocking fees, and refunds."),
            ("button", "Generate & Publish", "Review policy wording and copy or download for your website footer.")
        ]
    },
    "generador-politicas-terminos": {
        "en_slug": "terms-privacy-generator",
        "name": "Terms of Service & Privacy Policy Generator",
        "title": "Terms of Service & Privacy Policy Generator — LegalForge",
        "description": "Generate standard Terms of Service, Privacy Policies, and Cookie Notices for websites, online shops, and SaaS applications.",
        "purpose": "Generate comprehensive draft Terms of Service, Privacy Policies, and Cookie Notices tailored to small business websites and online stores.",
        "anchor": "21-terms-of-service-and-privacy-policy-generator",
        "quick": [
            "Select document type: Terms of Service, Privacy Policy, or Cookie Notice.",
            "Enter business legal name, website URL, jurisdiction, and user data practices.",
            "Generate, review, and adapt the policy template before embedding on your site."
        ],
        "tip": "Privacy disclosures must accurately reflect your actual data collection, analytics trackers, and cookies. Have terms verified by legal counsel.",
        "steps": [
            ("button,[role=tab]", "Select Document Type", "Choose Terms of Service, Privacy Policy, or Cookie Disclosure."),
            ("input,textarea", "Input Business Context", "Provide legal company name, jurisdiction, website URL, and data handling practices."),
            ("button", "Generate & Review Draft", "Download or copy the generated legal policy for your site footer.")
        ]
    },
    "guiones-manejo-objeciones": {
        "en_slug": "objection-handling-scripts",
        "name": "Sales Objection Handling Scripts",
        "title": "Sales Objection Handling Scripts — Responses for Price & Trust",
        "description": "Master customer objections on price, timing, competitor comparisons, and trust. Access structured sales talk tracks and practice in Zen Mode.",
        "purpose": "Equip sales professionals and founders with proven talk tracks and frameworks to handle buyer objections regarding pricing, timing, competitors, and trust.",
        "anchor": "22-sales-objection-handling-scripts",
        "quick": [
            "Select an objection category: Price, Timing, Competition, Trust, or Authority.",
            "Review proven talk tracks, psychological rationale, and suggested follow-up questions.",
            "Practice aloud, adapt to your customer context, or use Zen Mode for distraction-free sales calls."
        ],
        "tip": "Objection handling is an empathetic conversation, not an argument: validate the client's concern first before re-framing value.",
        "steps": [
            ("button,[role=tab]", "Select Objection Scenario", "Browse objection categories to find the scenario matching your deal."),
            ("input,textarea", "Review Response Framework", "Analyze why the script works and adapt phrasing to your specific service."),
            ("button", "Practice & Save Custom Scripts", "Practice responses and save high-performing talk tracks for your team.")
        ]
    },
    "inventario-compras-pymes": {
        "en_slug": "inventory-purchase-orders",
        "name": "Inventory, Suppliers & Purchase Orders",
        "title": "Inventory, Suppliers & Purchase Orders — Local Stock Manager",
        "description": "Manage product catalog, stock levels, unit costs, reorder thresholds, supplier contacts, and purchase orders directly in your browser.",
        "purpose": "Track product inventory levels, unit costs, selling prices, minimum stock thresholds, supplier records, and stock restocking orders locally.",
        "anchor": "23-inventory-suppliers-and-purchase-orders",
        "quick": [
            "Add products with SKU, unit cost, selling price, and minimum stock threshold.",
            "Register vendor suppliers with lead times and payment terms.",
            "Apply replenishment purchase orders to automatically increase stock levels.",
            "Monitor low-stock alerts to reorder inventory before running out."
        ],
        "tip": "Conduct periodic physical stock counts to reconcile local browser records with actual on-shelf warehouse inventory.",
        "steps": [
            ("input,select", "Add Products & Suppliers", "Record SKUs, item descriptions, costs, and supplier directories."),
            ("button", "Receive Purchase Orders", "Apply incoming inventory shipments to update stock counts automatically."),
            ("table,article", "Review Stock & Alerts", "Monitor items falling below minimum inventory thresholds.")
        ]
    },
    "organizador-matriz-contenidos": {
        "en_slug": "content-matrix-planner",
        "name": "Content Matrix & Editorial Planner",
        "title": "Content Matrix & Editorial Planner — Social Media & Blog Calendar",
        "description": "Organize marketing content across editorial pillars, funnel stages, distribution channels, and publishing dates with an interactive matrix.",
        "purpose": "Plan and organize marketing content across content pillars, buyer journey stages, formats, channels, and dates into an actionable editorial calendar.",
        "anchor": "24-content-matrix-and-editorial-planner",
        "quick": [
            "Define your core content pillars, target audiences, and campaign goals.",
            "Add content ideas with format (video, carousel, article), channel, and publish date.",
            "Filter, rearrange, and export your content calendar to keep social publishing consistent."
        ],
        "tip": "Map each content piece to a specific audience stage (awareness, consideration, decision); a packed calendar must drive clear commercial goals.",
        "steps": [
            ("input,textarea", "Define Content Pillars", "Establish strategic themes, audience segments, and publishing objectives."),
            ("input,button", "Add Content Entries", "Log post ideas, formats, target platforms, and scheduled dates."),
            ("button", "Filter & Export Calendar", "Organize weekly/monthly schedules and export the editorial matrix.")
        ]
    },
    "simulador-tco-fisico-nube": {
        "en_slug": "cloud-vs-onprem-tco",
        "name": "Cloud vs. On-Premises TCO Simulator",
        "title": "Cloud vs. On-Premises TCO Simulator — Total Cost of Ownership",
        "description": "Compare 3-year and 5-year Total Cost of Ownership between physical on-premises servers and cloud infrastructure (AWS, Azure, GCP).",
        "purpose": "Compare the multi-year Total Cost of Ownership (TCO) between on-premises physical servers and cloud services, factoring in hardware, energy, IT labor, and growth.",
        "anchor": "25-cloud-vs-on-premises-tco-simulator",
        "quick": [
            "Set planning horizon (3 to 5 years), active user count, and anticipated data growth.",
            "Enter initial server hardware, maintenance, cooling, energy, and backup costs.",
            "Enter monthly cloud hosting, egress bandwidth, and managed service estimates.",
            "Compare cumulative TCO, break-even timeline, and export the financial executive summary."
        ],
        "tip": "Factor in server replacement cycles, downtime risk, software licensing, and IT maintenance hours; monthly cloud fees must be compared against all physical overhead.",
        "steps": [
            ("input", "Define Infrastructure Scope", "Set timeline horizon, compute workloads, and anticipated annual growth."),
            ("input", "Input Costs", "Enter CAPEX hardware, electricity, cooling, maintenance vs. OPEX cloud costs."),
            ("button", "Review Financial Comparison", "Analyze break-even curves, cumulative cost differences, and download reports.")
        ]
    },
    "tareas-proyectos-pymes": {
        "en_slug": "task-project-tracker",
        "name": "Operational Tasks & Project Tracker",
        "title": "Operational Tasks & Project Tracker — Visual Team Kanban Board",
        "description": "Track small business projects, operational tasks, team assignees, priority levels, and delivery deadlines on a local-first visual board.",
        "purpose": "Organize commercial commitments and internal operations into projects, actionable tasks, team assignees, priorities, and deadlines on an operational board.",
        "anchor": "26-operational-tasks-and-project-tracker",
        "quick": [
            "Create a project with client name, scope objective, and target delivery date.",
            "Add actionable tasks with designated team assignee, priority level, and deadline.",
            "Move tasks across Kanban columns: To Do, In Progress, Blocked, and Completed.",
            "Review overdue milestones to maintain operational control."
        ],
        "tip": "Break large projects into tasks with realistic 1-to-3-day deadlines and clear single owners to avoid operational bottlenecks.",
        "steps": [
            ("input,select", "Create Project", "Set project title, client/area, objective notes, and target completion date."),
            ("input,button", "Add Tasks", "Create specific tasks with assignees, priority levels, and due dates."),
            ("article,button", "Track Kanban Workflow", "Advance tasks through workflow stages and resolve overdue items.")
        ]
    }
}
