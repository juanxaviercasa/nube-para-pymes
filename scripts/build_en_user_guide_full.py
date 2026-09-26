import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

content = """<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Complete user guide for the 26 free browser-based business tools of NubeParaPymes.">
  <title>User Guide · NubeParaPymes</title>
  <style>
    :root { color-scheme: dark; --bg:#071426; --panel:#0d2037; --line:#28415c; --text:#edf4ff; --muted:#aabbd0; --accent:#ff7a18; --link:#7db8ff; }
    * { box-sizing:border-box; }
    body { margin:0; background:var(--bg); color:var(--text); font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; line-height:1.65; }
    header { border-bottom:1px solid var(--line); background:#091a2e; }
    .top { max-width:1160px; margin:auto; padding:18px 24px; display:flex; justify-content:space-between; gap:16px; align-items:center; }
    .brand { color:var(--text); font-weight:800; text-decoration:none; letter-spacing:.01em; }
    .nav-links { display:flex; align-items:center; gap:16px; }
    .lang-toggle { font-size:.85rem; font-weight:600; padding:4px 10px; border-radius:6px; border:1px solid var(--line); background:#132d4b; color:#fff; text-decoration:none; }
    .lang-toggle:hover { border-color:var(--accent); color:var(--accent); }
    .back { color:var(--link); text-decoration:none; font-size:.95rem; }
    main { max-width:1160px; margin:0 auto; padding:42px 24px 72px; }
    article { background:rgba(13,32,55,.72); border:1px solid var(--line); border-radius:18px; padding:34px clamp(22px,5vw,64px); box-shadow:0 18px 60px rgba(0,0,0,.2); }
    h1,h2,h3 { line-height:1.2; color:#fff; margin-top:1.65em; }
    h1 { margin-top:0; font-size:clamp(2rem,4vw,3.2rem); }
    h2 { border-bottom:1px solid var(--line); padding-bottom:.4em; font-size:clamp(1.45rem,2.4vw,2rem); }
    h3 { color:#dceaff; font-size:1.2rem; }
    p,li { color:var(--muted); }
    strong { color:#fff; }
    a { color:var(--link); }
    blockquote { margin:1.5em 0; padding:1em 1.2em; border-left:4px solid var(--accent); background:rgba(255,122,24,.09); border-radius:0 10px 10px 0; }
    blockquote p { margin:.1em 0; color:#e8eef7; }
    code { padding:.15em .35em; border-radius:5px; background:#06101e; color:#ffd5af; }
    pre { overflow:auto; padding:16px; border-radius:10px; background:#06101e; }
    pre code { padding:0; }
    table { width:100%; border-collapse:collapse; display:block; overflow-x:auto; margin:1.4em 0; }
    th,td { text-align:left; vertical-align:top; padding:10px 12px; border:1px solid var(--line); min-width:120px; }
    th { color:#fff; background:#132d4b; }
    td { color:var(--muted); }
    hr { border:0; border-top:1px solid var(--line); margin:2.4em 0; }
    footer { max-width:1160px; margin:0 auto; padding:0 24px 36px; color:var(--muted); font-size:.9rem; }
  </style>
</head>
<body>
  <header>
    <div class="top">
      <a class="brand" href="./index.html">NubeParaPymes</a>
      <div class="nav-links">
        <a class="lang-toggle" href="../guia-uso-22-apps.html">ES</a>
        <a class="back" href="./index.html">← Back to Directory</a>
      </div>
    </div>
  </header>
  <main>
    <article>
      <h1 id="complete-user-guide-to-nubeparapymes">Complete User Guide for NubeParaPymes</h1>
      
      <h2 id="introduction">Introduction</h2>
      <p>NubeParaPymes brings together <strong>26 free, browser-based business tools</strong> to streamline marketing, sales, operations, finance, documentation, and operational planning for small and medium-sized enterprises (SMBs). Every application runs entirely on your device and keeps data stored locally when equipped with history or persistent storage. No account registration, email submission, or paid subscription is required to use any published feature.</p>
      <p>The English directory portal is accessible at <a href="./index.html">NubeParaPymes English Portal</a>. Each application opens via an independent standalone HTML file in the directory, following the pattern <code>./app-slug.html</code>.</p>
      <blockquote>
        <p><strong>General Best Practices:</strong> Input sample data to test calculations before processing mission-critical business data. Double check numbers, currency rates, and units. Download or export your important reports and keep local backup JSON files when available. The financial, labor, and legal drafting calculators are intended as practical estimation instruments; results should always be reviewed alongside applicable regional regulations, contracts, and qualified professional advice.</p>
      </blockquote>

      <h2 id="table-of-applications">Directory of Business Tools</h2>
      <table>
        <thead>
          <tr>
            <th style="text-align: right;">#</th>
            <th>Application</th>
            <th>Primary Business Purpose</th>
            <th>Access</th>
          </tr>
        </thead>
        <tbody>
          <tr><td style="text-align: right;">1</td><td>Headline Analyzer</td><td>Evaluate and optimize marketing headlines</td><td><a href="./headline-analyzer.html">Open</a></td></tr>
          <tr><td style="text-align: right;">2</td><td>Basic On-Page SEO Auditor</td><td>Audit page metadata, headings, and SEO health</td><td><a href="./basic-on-page-seo-auditor.html">Open</a></td></tr>
          <tr><td style="text-align: right;">3</td><td>Discount & Promotions Calculator</td><td>Simulate prices, profit margins, and promotional campaigns</td><td><a href="./discount-promotions-calculator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">4</td><td>Local Freight & Shipping Calculator</td><td>Calculate delivery rates, volumetric weights, and multi-stop routes</td><td><a href="./local-shipping-calculator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">5</td><td>Sales Pricing & Tax Calculator</td><td>Calculate selling prices, net margins, and Sales Tax / GST</td><td><a href="./sales-pricing-tax-calculator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">6</td><td>Loan & Amortization Calculator</td><td>Compare business loan amortizations and extra payments</td><td><a href="./loan-amortization-calculator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">7</td><td>Labor Cost & Payroll Burden Calculator</td><td>Calculate total employer payroll burden, benefits, and true wage costs</td><td><a href="./labor-cost-payroll-burden-calculator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">8</td><td>Advanced Ad Campaign Comparator</td><td>Benchmark ad campaigns across Meta, Google, TikTok, and LinkedIn</td><td><a href="./advanced-campaign-comparator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">9</td><td>Campaign UTM Console</td><td>Build UTM tracking parameters and organize marketing funnels</td><td><a href="./campaign-utm-console.html">Open</a></td></tr>
          <tr><td style="text-align: right;">10</td><td>WebP Forge</td><td>Convert, resize, and optimize images into WebP/JPEG locally</td><td><a href="./image-converter-optimizer.html">Open</a></td></tr>
          <tr><td style="text-align: right;">11</td><td>Proforma Invoice Generator</td><td>Create and download professional commercial proforma invoices</td><td><a href="./proforma-invoice-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">12</td><td>HTML Email Signature Generator</td><td>Design a responsive corporate HTML email signature</td><td><a href="./html-email-signature.html">Open</a></td></tr>
          <tr><td style="text-align: right;">13</td><td>QR Code Generator</td><td>Create QR codes for URLs, WiFi, and direct WhatsApp links</td><td><a href="./qr-code-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">14</td><td>SecuKey</td><td>Generate cryptographically secure passwords and 2FA simulation</td><td><a href="./smb-password-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">15</td><td>Service Contract Generator</td><td>Draft service contracts and professional client agreements</td><td><a href="./service-contracts-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">16</td><td>Quote & Estimate Generator</td><td>Prepare multi-currency client estimates and commercial quotes</td><td><a href="./quote-estimate-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">17</td><td>Chroma</td><td>Generate accessible brand palettes and extract image colors</td><td><a href="./brand-palette-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">18</td><td>Return Policy Generator</td><td>Draft clear return and refund policies for retail & ecommerce</td><td><a href="./return-policy-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">19</td><td>LegalForge</td><td>Generate custom website privacy policies and terms of service</td><td><a href="./terms-privacy-generator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">20</td><td>ObjectionPro</td><td>Master sales objection scripts with buyer personas & flashcards</td><td><a href="./objection-handling-scripts.html">Open</a></td></tr>
          <tr><td style="text-align: right;">21</td><td>Content Matrix Planner</td><td>Plan, calendarize, and balance social media publications</td><td><a href="./content-matrix-planner.html">Open</a></td></tr>
          <tr><td style="text-align: right;">22</td><td>TCO Simulator: On-Premise vs Cloud</td><td>Compare 36-month total cost of ownership (Physical servers vs Cloud)</td><td><a href="./cloud-vs-onprem-tco-simulator.html">Open</a></td></tr>
          <tr><td style="text-align: right;">23</td><td>SMB CRM & Sales Pipeline</td><td>Manage leads, deals, contacts, pipeline stages, and follow-ups</td><td><a href="./smb-crm.html">Open</a></td></tr>
          <tr><td style="text-align: right;">24</td><td>Cash Flow & Accounts Receivable</td><td>Track cash inflows, outflows, receivables, and operational runway</td><td><a href="./cash-flow-tracker.html">Open</a></td></tr>
          <tr><td style="text-align: right;">25</td><td>Inventory & Supplier Purchasing</td><td>Control stock levels, reorder thresholds, supplier orders, and SKUs</td><td><a href="./inventory-purchasing.html">Open</a></td></tr>
          <tr><td style="text-align: right;">26</td><td>Operations Tasks & Projects</td><td>Coordinate client deliverables, kanban boards, and project deadlines</td><td><a href="./tasks-projects-tracker.html">Open</a></td></tr>
        </tbody>
      </table>
      <hr>

      <h2 id="1-headline-analyzer">1. Headline Analyzer</h2>
      <h3>What it does</h3>
      <p>Evaluates marketing headlines and subject lines using heuristic scoring across clarity, emotional resonance, tone, and engagement. Features heuristic suggestions, sentiment classification, SERP and social media previews, A/B comparison testing, and local history.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter your proposed headline along with the target keyword or contextual niche.</li>
        <li>Review your overall score, word count, emotional balance, and clarity suggestions.</li>
        <li>Refine your wording and re-analyze to view score improvements.</li>
        <li>Use the A/B comparison tab to benchmark two variations side by side.</li>
        <li>Check the SERP and social snippet previews to verify truncation limits.</li>
        <li>Copy or export your analysis report.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Do not simply chase an arbitrary high score. Ensure the headline remains truthful, authentic, and aligned with your brand voice without overpromising.</p>

      <h2 id="2-basic-on-page-seo-auditor">2. Basic On-Page SEO Auditor</h2>
      <h3>What it does</h3>
      <p>Audits essential on-page SEO signals including title tags, meta descriptions, canonical URLs, Open Graph tags, heading structure (H1-H6), keyword density, image alt attributes, and social previews.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter your webpage URL or paste your HTML content and metadata manually.</li>
        <li>Run the audit to review your health score and priority issue alerts.</li>
        <li>Check the SERP snippet preview to ensure your title and description fit within pixel limits.</li>
        <li>Inspect keyword frequency and heading hierarchy.</li>
        <li>Work through the actionable checklist to resolve missing alt tags or thin content.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>This tool serves as an editorial pre-flight checklist. It complements, but does not replace, comprehensive technical crawling, core web vitals testing, or Google Search Console verification.</p>

      <h2 id="3-discount-promotions-calculator">3. Discount & Promotions Calculator</h2>
      <h3>What it does</h3>
      <p>Enables businesses to model promotional pricing, profit margins, sales break-even points, bundled kit discounts, customer lifetime value (CLV), persuasive sales copy, and flash sale strategies.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Select your operational scenario: single item discount, margin impact, volume break-even, product combo, or CLV.</li>
        <li>Input the original retail price, unit cost, discount percentage, and anticipated volume.</li>
        <li>Analyze the net profit margin and the additional units required to break even.</li>
        <li>In the Combo Builder, combine up to three products to determine the safe maximum bundled discount.</li>
        <li>In the CLV module, calculate expected customer lifetime value to justify acquisition offers.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Always verify that your unit cost includes all variable expenses (packaging, merchant transaction fees, and shipping). Never confuse markup on cost with gross margin on sales.</p>

      <h2 id="4-local-freight-shipping-calculator">4. Local Freight & Shipping Calculator</h2>
      <h3>What it does</h3>
      <p>Calculates commercial freight and courier shipping quotes based on package dimensions, actual weight, volumetric divisor, suggested vehicle type, mileage zones, and route stops.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Input package length, width, height, and actual scale weight.</li>
        <li>Select vehicle category (motorcycle courier, delivery van, or cargo truck).</li>
        <li>Add pickup and delivery stopovers across local delivery zones.</li>
        <li>Review billable weight (comparing actual vs. volumetric weight), base tariffs, surcharges, and total quote.</li>
        <li>Save the quote to your local history and generate a shipping manifest or package label.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Confirm the volumetric divisor used by your primary carrier (typically 5,000 cm³/kg or 139 in³/lb). Account for special access, loading dock wait times, and fragile goods handling.</p>

      <h2 id="5-sales-pricing-tax-calculator">5. Sales Pricing & Tax Calculator</h2>
      <h3>What it does</h3>
      <p>Calculates optimal selling prices, gross margins, markups, and applicable sales tax or GST (such as 10% Australian GST or US state sales tax). Supports forward pricing and reverse calculation from tax-inclusive retail totals.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter your total direct acquisition or production cost.</li>
        <li>Input your desired target net margin percentage or markup.</li>
        <li>Set your regional Sales Tax / GST percentage (e.g., 10% GST or state tax).</li>
        <li>Review pre-tax wholesale price, tax amount, and final customer retail price.</li>
        <li>Switch to Reverse Calculation mode if you have a fixed target retail price and need to determine allowable costs.</li>
        <li>Export the commercial breakdown to PDF.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Ensure that tax rates reflect your local jurisdiction and tax regime. Use this tool for commercial margin simulation and consult your certified CPA for statutory filing.</p>

      <h2 id="6-loan-amortization-calculator">6. Loan & Amortization Calculator</h2>
      <h3>What it does</h3>
      <p>Calculates periodic loan payments, total interest costs, and full amortization tables. Allows modeling of grace periods (interest-only or capitalization) and early principal prepayments.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter principal loan amount, annual interest rate, and repayment term.</li>
        <li>Select amortization frequency (monthly, bi-weekly, or quarterly).</li>
        <li>Configure grace periods if applicable (interest-only or principal deferral).</li>
        <li>Review payment amounts, total interest, and amortization schedule.</li>
        <li>Simulate one-time or recurring extra principal prepayments to observe interest savings and term reduction.</li>
        <li>Compare Scenario A vs. Scenario B side by side.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Verify whether your lender quotes nominal APR or effective interest rates, and check for origination fees, closing costs, or mandatory credit insurance.</p>

      <h2 id="7-labor-cost-payroll-burden-calculator">7. Labor Cost & Payroll Burden Calculator</h2>
      <h3>What it does</h3>
      <p>Calculates true employer labor costs beyond gross wages, including payroll taxes, statutory health benefits, pension contributions, paid time off provisions, and mandatory insurance across multi-employee rosters.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Select your currency and default reporting period (monthly or annual).</li>
        <li>Add staff members with their gross salary, job title, and department.</li>
        <li>Configure statutory employer burden rates (social security, Medicare/health, workers comp, superannuation / 401(k) matching).</li>
        <li>Review the total employer cost, net take-home estimates, and department cost distribution.</li>
        <li>Export a breakdown report in PDF.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Statutory payroll requirements vary significantly by country and state/province. Maintain separate budget estimations from formal accounting payroll runs.</p>

      <h2 id="8-advanced-ad-campaign-comparator">8. Advanced Ad Campaign Comparator</h2>
      <h3>What it does</h3>
      <p>Compares performance metrics across digital advertising platforms (Meta Ads, Google Ads, TikTok Ads, LinkedIn Ads). Evaluates spend, impressions, clicks, CPC, CTR, conversion rates, CPA, revenue, and ROAS.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Add a campaign scenario and select the advertising channel.</li>
        <li>Enter ad spend, reach, impressions, clicks, conversions, and generated revenue.</li>
        <li>Review calculated KPIs: CPC, CTR, Conversion Rate, CPA, and ROAS.</li>
        <li>Compare campaigns side by side on the visual scatter and bar charts.</li>
        <li>Export your benchmark comparison report to CSV or PDF.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Standardize conversion attribution windows across platforms before comparing ROAS directly. Consistent timeframes and conversion definitions are critical.</p>

      <h2 id="9-campaign-utm-console">9. Campaign UTM Console</h2>
      <h3>What it does</h3>
      <p>Generates clean, standardized Google Analytics UTM tracking URLs. Features campaign naming conventions, preset source/medium templates, an ROI simulation calculator, and campaign folder storage.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter the target destination webpage URL.</li>
        <li>Specify <code>utm_source</code>, <code>utm_medium</code>, and <code>utm_campaign</code> (plus optional <code>utm_term</code> and <code>utm_content</code>).</li>
        <li>Use preset buttons (e.g., Google Search, Meta Ad, Newsletter) to ensure standardized lowercase naming.</li>
        <li>Copy the generated tracking link and test it in a private browser window.</li>
        <li>Save campaigns into local folders and use the ROI simulator to forecast required conversion rates.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Always use lowercase characters and hyphens instead of spaces or special characters. Consistent naming prevents fragmented reporting in Google Analytics 4.</p>

      <h2 id="10-webp-forge-image-converter-optimizer">10. WebP Forge — Image Converter & Optimizer</h2>
      <h3>What it does</h3>
      <p>Converts and compresses image files (PNG, JPG, SVG, WebP) directly in your browser using HTML5 Canvas. Supports batch conversion, dimensions resizing, custom quality control, watermarking, and ZIP download.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Drag and drop images into the upload area or click to select files.</li>
        <li>Choose target format (WebP or JPEG), compression quality (1-100%), and maximum width/height constraints.</li>
        <li>Optionally enable a text watermark and position it across your batch.</li>
        <li>Click Process to convert your images instantly without server uploads.</li>
        <li>Inspect original vs. compressed file size savings and download individual images or a packaged ZIP file.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Keep your original high-resolution master assets safely stored. For web display, 75-85% WebP quality typically reduces image payload by 60-80% without noticeable visual artifacts.</p>

      <h2 id="11-proforma-invoice-generator">11. Proforma Invoice Generator</h2>
      <h3>What it does</h3>
      <p>Generates professional, printable commercial proforma invoices and receipts. Supports custom corporate branding, company logos, itemized line items, multi-currency conversion, sales tax/GST, payment instructions, and PDF export.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Fill in your business details and upload your company logo.</li>
        <li>Enter buyer/client details, proforma invoice number, and issue/due dates.</li>
        <li>Select primary currency and optional secondary currency with exchange rate.</li>
        <li>Add itemized goods or services with descriptions, quantities, unit prices, and discounts.</li>
        <li>Specify payment methods (bank wire details, ACH, PayPal, or payment links).</li>
        <li>Choose your invoice visual template, preview the document, and click Download PDF.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>A proforma invoice is a commercial pre-shipment quotation and binding commercial commitment, but it is not a formal fiscal tax invoice. Ensure clear notation of commercial validity terms.</p>

      <h2 id="12-html-email-signature-generator">12. HTML Email Signature Generator</h2>
      <h3>What it does</h3>
      <p>Creates clean, professional, cross-client compatible HTML email signatures. Includes styling controls, contact details, social media icons, profile avatars, legal disclaimers, and one-click copy to clipboard.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter your full name, title, department, company name, phone numbers, and website.</li>
        <li>Add social profile links (LinkedIn, Twitter/X, Instagram, YouTube).</li>
        <li>Provide a publicly hosted image URL for your profile photo or company logo.</li>
        <li>Adjust brand accent colors, font family, and layout orientation.</li>
        <li>Preview the signature across desktop and mobile layouts.</li>
        <li>Click "Copy Signature" or "Copy HTML Code" and paste into Gmail, Outlook, Apple Mail, or Thunderbird.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Host your logo images on a reliable, public HTTPS server. Avoid overly large banners that may trigger email spam filters or distort on mobile screens.</p>

      <h2 id="13-qr-code-generator">13. QR Code Generator</h2>
      <h3>What it does</h3>
      <p>Generates high-resolution QR codes locally for URLs, plain text, vCard contact cards, WiFi network credentials, and direct WhatsApp chat links with pre-filled messages. Allows PNG download and custom styling.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Select content type: URL, Plain Text, Contact vCard, WiFi, or WhatsApp.</li>
        <li>Enter the required destination details. For WhatsApp, select country code and enter phone number.</li>
        <li>Adjust QR error correction level and foreground/background colors.</li>
        <li>Preview the real-time generated QR code.</li>
        <li>Download the QR image in high-resolution PNG format.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Always maintain high contrast (dark pixels on light background). Test scan the physical code with both iOS and Android camera apps before printing bulk marketing collateral.</p>

      <h2 id="14-secukey-smb-password-generator">14. SecuKey — SMB Password Generator</h2>
      <h3>What it does</h3>
      <p>Generates cryptographically secure, random passwords and passphrases using browser <code>crypto.getRandomValues</code>. Includes character set toggles, entropy scoring, corporate policy presets, and a 2FA TOTP algorithm simulator.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Select desired character length (16+ characters recommended for business accounts).</li>
        <li>Toggle uppercase, lowercase, digits, and special characters.</li>
        <li>Enable "Exclude Ambiguous" (e.g. 0, O, 1, l, I) if passwords must be typed manually.</li>
        <li>Click Generate and inspect password entropy and crack-time resistance.</li>
        <li>Click Copy to Clipboard and store immediately in your team's password manager.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Never share passwords across unencrypted email or chat. Use this generator to create distinct credentials for every corporate system and store them in an enterprise password manager.</p>

      <h2 id="15-service-contract-generator">15. Service Contract Generator</h2>
      <h3>What it does</h3>
      <p>Drafts comprehensive professional service agreements, scopes of work (SOW), and freelance client contracts. Covers contractor/client identities, deliverables, payment terms, milestones, confidentiality, IP ownership, and dispute resolution.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter jurisdiction, city/state, contract date, and legal party details.</li>
        <li>Define the detailed scope of services, deliverables, and timeline milestones.</li>
        <li>Specify fee structure (fixed price, hourly rate, or milestone installments) and payment schedules.</li>
        <li>Review clauses covering intellectual property rights, non-disclosure, and termination conditions.</li>
        <li>Preview the full agreement text and download as an editable document or print-ready PDF.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>This generator provides standard commercial templates. Have all substantial contracts reviewed by regional legal counsel to ensure compliance with local contract law.</p>

      <h2 id="16-quote-estimate-generator">16. Quote & Estimate Generator</h2>
      <h3>What it does</h3>
      <p>Creates itemized client price estimates and commercial quotes. Supports company branding, multi-currency pricing, line item discounts, tax calculations, customer catalog, and PDF download.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Fill in company details, client contact information, and estimate reference number.</li>
        <li>Set issue date and quote validity expiration date.</li>
        <li>Add products or service lines with descriptions, quantities, unit prices, and line discounts.</li>
        <li>Save frequent line items to your local catalog for rapid one-click re-use.</li>
        <li>Review subtotal, tax rate, and grand total.</li>
        <li>Preview the layout and download your client-ready PDF quote.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Always state an explicit validity expiration date (e.g. "Valid for 30 days") to protect against sudden supplier price increases or currency fluctuations.</p>

      <h2 id="17-chroma-corporate-palette-generator">17. Chroma — Corporate Palette Generator</h2>
      <h3>What it does</h3>
      <p>Generates balanced corporate brand color palettes based on color theory (monochromatic, analogous, complementary, triadic, tetradic). Features image color palette extraction, HEX/RGB/HSL conversion, and WCAG accessibility contrast checking.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter or pick a primary brand HEX color.</li>
        <li>Select harmony model (complementary, analogous, triadic, etc.) or adjust palette hue angles.</li>
        <li>Review derived accent, surface, text, and highlight colors.</li>
        <li>Check the built-in WCAG contrast ratios to verify text readability standards.</li>
        <li>Alternatively, upload a brand photograph to automatically extract its dominant color scheme.</li>
        <li>Copy individual color codes or export the CSS variables palette.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Ensure that primary text colors against your brand background achieve at least WCAG AA compliance (4.5:1 contrast ratio) for optimal readability.</p>

      <h2 id="18-return-policy-generator">18. Return Policy Generator</h2>
      <h3>What it does</h3>
      <p>Generates tailored return and refund policies for retail, ecommerce, and digital service businesses. Outlines return windows, product condition criteria, non-returnable items, restocking fees, and refund processing procedures.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Select your business sector (fashion, electronics, digital goods, perishable goods, or consulting).</li>
        <li>Define return timeframe (e.g., 14, 30, or 60 days from delivery).</li>
        <li>Specify who bears return shipping costs and whether restocking fees apply.</li>
        <li>Select accepted refund formats (original payment method, store credit, or exchange only).</li>
        <li>Generate and review the full policy document.</li>
        <li>Copy the text or download it for publication on your website footer and checkout flow.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Ensure your published policy adheres to statutory consumer rights in your target markets (e.g., Australian Consumer Law or US state consumer protection guidelines).</p>

      <h2 id="19-legalforge-terms-privacy-generator">19. LegalForge — Terms & Privacy Generator</h2>
      <h3>What it does</h3>
      <p>Drafts foundational website legal documentation including Privacy Policies, Terms of Service, Cookie Notices, and Disclaimer statements based on site functionality and data collection activities.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Enter company legal name, website URL, contact email, and regional jurisdiction.</li>
        <li>Select website type: corporate brochure, lead generation blog, SaaS platform, or ecommerce store.</li>
        <li>Specify data collection practices: contact forms, email newsletters, analytics tracking, or user registrations.</li>
        <li>Review generated sections detailing data retention, third-party disclosure, user rights, and cookie use.</li>
        <li>Download the generated documents and integrate into your website's legal pages.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Accurately reflect the third-party trackers (Google Analytics, Meta Pixel, etc.) actually operating on your website. Periodically update your policies whenever tracking technology changes.</p>

      <h2 id="20-objectionpro-sales-objection-scripts">20. ObjectionPro — Sales Objection Scripts</h2>
      <h3>What it does</h3>
      <p>Provides an interactive library of tested sales objection handling scripts, psychology breakdowns, buyer persona profiles, and flashcard practice modes to train sales teams and founders.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Browse objection categories: "Price/Budget", "Need to Think", "Competitor Comparison", "No Authority", or "Bad Timing".</li>
        <li>Filter by buyer persona: Analytical, Skeptical, Impulsive, or Busy Executive.</li>
        <li>Study suggested response frameworks (e.g., Isolate & Validate, Anchor Value, or Flip the Script).</li>
        <li>Save frequently encountered objections to your favorites.</li>
        <li>Enter Zen Practice Mode to review flashcards without distraction.</li>
        <li>Add custom internal scripts to build a shared team sales playbook.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Use scripts as conversational frameworks rather than rigid monologues. Listen carefully, validate customer concerns, and focus on delivering measurable business value.</p>

      <h2 id="21-content-matrix-planner">21. Content Matrix Planner</h2>
      <h3>What it does</h3>
      <p>Provides a weekly editorial calendar and multi-channel content planner. Organize posts across Instagram, LinkedIn, Facebook, X, TikTok, and YouTube with platform balance metrics, format tracking, and local history.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Navigate through calendar weeks using Previous, Today, and Next controls.</li>
        <li>Click a day to add a content card with title, platform, format (reel, carousel, text post, video), and status.</li>
        <li>Review weekly publication health scores and platform distribution percentages.</li>
        <li>Filter views by individual platform to spot publishing gaps.</li>
        <li>Use Undo and Redo controls to manage edits, with automatic local persistence.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Maintain a balanced mix of educational, social proof, and direct commercial content. The planner organizes publication schedules but does not auto-post to social APIs.</p>

      <h2 id="22-tco-simulator-on-premise-vs-cloud">22. TCO Simulator: On-Premise vs Cloud</h2>
      <h3>What it does</h3>
      <p>Models 36-month Total Cost of Ownership comparing on-premise physical servers against cloud infrastructure (AWS, Azure, GCP). Evaluates hardware capex, power, cooling, internet, maintenance, licenses, and cloud egress fees.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Configure physical cluster: number of nodes, server hardware capex, monthly power/cooling, admin maintenance, and residual salvage value.</li>
        <li>Configure cloud deployment: instances count, provider benchmark, monthly subscription, and estimated data egress.</li>
        <li>Select growth scenario: conservative, moderate, or aggressive scale.</li>
        <li>Inspect 3-year cumulative cost charts, breakeven inflection month, and heuristic recommendations.</li>
        <li>Export the comparative financial summary report.</li>
      </ol>
      <h3>Best Practices</h3>
      <p>Factor in indirect costs such as migration engineering, disaster recovery, security audits, and specialized staff training when planning infrastructure transitions.</p>

      <h2 id="23-smb-crm-sales-pipeline">23. SMB CRM & Sales Pipeline</h2>
      <h3>What it does</h3>
      <p>Tracks corporate leads, contacts, commercial opportunities, deal values, pipeline stages, and follow-up tasks directly in your browser without recurring SaaS subscription fees.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Add companies and contacts with phone numbers, emails, and notes.</li>
        <li>Create a deal opportunity, assign an estimated deal value, and select its pipeline stage (Lead, Qualified, Proposal, Negotiation, Won, Lost).</li>
        <li>Set a clear next action and scheduled follow-up deadline.</li>
        <li>Drag or update deal stages across the Kanban pipeline and monitor overdue follow-ups.</li>
        <li>Export your CRM data to JSON or CSV for secure local backup.</li>
      </ol>

      <h2 id="24-cash-flow-accounts-receivable">24. Cash Flow & Accounts Receivable</h2>
      <h3>What it does</h3>
      <p>Records business revenue, operational expenses, payment maturities, and accounts receivable to calculate current cash balance and forecast upcoming cash runway.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Record income and expenditure entries with amount, category, and due date.</li>
        <li>Link transactions to specific customers or vendors.</li>
        <li>Mark entries as Pending or Paid upon funds settlement.</li>
        <li>Inspect visual category charts and projected operational cash balances.</li>
        <li>Export financial summaries for operational budgeting.</li>
      </ol>

      <h2 id="25-inventory-supplier-purchasing">25. Inventory & Supplier Purchasing</h2>
      <h3>What it does</h3>
      <p>Tracks product catalog, SKUs, unit costs, retail prices, current warehouse stock, minimum reorder alerts, and supplier purchase orders.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Add products with SKU codes, unit purchase costs, selling prices, and minimum stock threshold levels.</li>
        <li>Record supplier contacts and default lead times.</li>
        <li>Log incoming stock replenishment purchases to automatically increase inventory levels.</li>
        <li>Log manual sales shipments and address low-stock visual alerts promptly.</li>
        <li>Export inventory rosters and replenishment orders.</li>
      </ol>

      <h2 id="26-operations-tasks-projects">26. Operations Tasks & Projects</h2>
      <h3>What it does</h3>
      <p>Transforms client commitments into structured projects, task assignments, priority levels, and deliverable deadlines across Kanban and list views.</p>
      <h3>How to use it</h3>
      <ol>
        <li>Create a project defining client, deliverable objective, and target completion date.</li>
        <li>Add tasks with assigned team members, priority level (Low, Medium, High, Urgent), and deadline.</li>
        <li>Move tasks across status columns: Backlog, In Progress, Blocked, or Completed.</li>
        <li>Review completion percentages and overdue task alerts to ensure timely operational delivery.</li>
      </ol>

      <h2 id="recommended-workflow">Recommended Multi-App Workflow</h2>
      <p>Small businesses can combine these 26 modular tools into a streamlined daily workflow:</p>
      <ol>
        <li><strong>Commercial & Pricing Strategy:</strong> Use the <strong>Sales Pricing Calculator</strong>, <strong>Discount & Promotions Calculator</strong>, and <strong>Quote Generator</strong> to establish profitable price floors and produce client estimates.</li>
        <li><strong>Digital Presence & Outreach:</strong> Craft impactful copy with the <strong>Headline Analyzer</strong>, audit your landing pages with the <strong>On-Page SEO Auditor</strong>, build tracked marketing campaigns with the <strong>UTM Console</strong>, and organize publishing schedules with the <strong>Content Matrix Planner</strong>.</li>
        <li><strong>Operations & Administration:</strong> Issue professional <strong>Proforma Invoices</strong>, compute logistics with the <strong>Freight Calculator</strong>, track personnel expenses with the <strong>Labor Cost Calculator</strong>, and evaluate IT systems with the <strong>TCO Simulator</strong>.</li>
        <li><strong>Sales Pipeline & Cash Operations:</strong> Track inbound deals with the <strong>SMB CRM</strong>, monitor operational liquidity with the <strong>Cash Flow Tracker</strong>, manage stock with <strong>Inventory & Purchasing</strong>, and execute client deliverables with <strong>Operations Tasks & Projects</strong>.</li>
        <li><strong>Legal & Compliance Documentation:</strong> Safeguard commercial relationships with the <strong>Service Contract Generator</strong>, <strong>LegalForge</strong>, and the <strong>Return Policy Generator</strong>.</li>
      </ol>

      <h2 id="privacy-storage-backups">Privacy, Local Storage & Data Backups</h2>
      <p>All 26 applications are engineered with privacy by design. Data entered into calculators, CRM pipelines, inventory rosters, and financial trackers is processed client-side and saved exclusively in your browser's <code>localStorage</code>.</p>
      <p>Clearing browser cookies and cache, using private/incognito browsing windows, or changing devices will reset local data. When working with critical records, use the built-in <strong>JSON/CSV/PDF Export</strong> features regularly to preserve offline backups.</p>

      <h2 id="troubleshooting">Quick Troubleshooting</h2>
      <table>
        <thead>
          <tr>
            <th>Observed Symptom</th>
            <th>Recommended Solution</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>404 Error when opening a tool</td>
            <td>Verify that the URL ends in <code>.html</code> and that the file path corresponds to the <code>/en/</code> directory structure.</td>
          </tr>
          <tr>
            <td>Page shows only blank background</td>
            <td>Hard refresh with <code>Ctrl + F5</code> (or <code>Cmd + Shift + R</code>) to clear cached assets; ensure JavaScript is enabled.</td>
          </tr>
          <tr>
            <td>Special characters or accent errors</td>
            <td>Ensure your browser and local server support standard UTF-8 encoding (specified via <code>&lt;meta charset="UTF-8"&gt;</code>).</td>
          </tr>
          <tr>
            <td>CSS styling is missing</td>
            <td>Confirm that relative asset paths resolve correctly to <code>../css/</code> and <code>../assets/</code>.</td>
          </tr>
          <tr>
            <td>Saved tool data is missing</td>
            <td>Check whether you switched browsers, opened in private/incognito mode, or recently cleared site cookies and data.</td>
          </tr>
          <tr>
            <td>PDF or ZIP download does not start</td>
            <td>Allow browser file downloads in your browser security settings; all file generation happens client-side in JavaScript.</td>
          </tr>
        </tbody>
      </table>

      <h2 id="project-credits">Project Credits</h2>
      <hr>
      <p><strong>NubeParaPymes · Free, browser-based business productivity tools for small and medium businesses.</strong></p>
      <p><em>Built and maintained for production deployment.</em></p>
    </article>
  </main>
  <footer>
    User Guide for 26 Business Tools · NubeParaPymes · Designed and Developed by <a href="https://juan.cabellorosas.com" target="_blank" rel="noopener" style="font-weight:700;color:inherit;text-decoration:underline;">Xavier Cabello</a>
  </footer>
</body>
</html>
"""

# Write to both en/user-guide.html and en/guia-uso-22-apps.html
(EN_DIR / "user-guide.html").write_text(content, encoding="utf-8")
(EN_DIR / "guia-uso-22-apps.html").write_text(content, encoding="utf-8")
print("Successfully generated en/user-guide.html and en/guia-uso-22-apps.html!")
