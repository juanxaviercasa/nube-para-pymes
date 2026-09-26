from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

SLUG_MAP = {
    "analizador-titulares.html": "headline-analyzer.html",
    "auditor-seo-basico.html": "basic-on-page-seo-auditor.html",
    "calculadora-descuentos-promociones.html": "discount-promotions-calculator.html",
    "calculadora-flete-envio-local.html": "local-shipping-calculator.html",
    "calculadora-precios-venta-igv.html": "sales-pricing-tax-calculator.html",
    "calculadora-prestamos-amortizaciones.html": "loan-amortization-calculator.html",
    "calculadora-sobrecostos-laborales.html": "labor-cost-payroll-burden-calculator.html",
    "comparador-campanas-avanzado.html": "advanced-campaign-comparator.html",
    "consola-campanas.html": "campaign-utm-console.html",
    "conversor-optimizador-imagenes.html": "image-converter-optimizer.html",
    "creador-facturas-proforma.html": "proforma-invoice-generator.html",
    "crm-pymes.html": "smb-crm.html",
    "firma-correo-html.html": "html-email-signature.html",
    "flujo-caja-pymes.html": "cash-flow-tracker.html",
    "generador-codigos-qr.html": "qr-code-generator.html",
    "generador-contrasenas-pymes.html": "smb-password-generator.html",
    "generador-contratos-servicios.html": "service-contracts-generator.html",
    "generador-cotizaciones.html": "quote-estimate-generator.html",
    "generador-paletas-corporativas.html": "brand-palette-generator.html",
    "generador-politicas-devolucion.html": "return-policy-generator.html",
    "generador-politicas-terminos.html": "terms-privacy-generator.html",
    "guiones-manejo-objeciones.html": "objection-handling-scripts.html",
    "inventario-compras-pymes.html": "inventory-purchasing.html",
    "organizador-matriz-contenidos.html": "content-matrix-planner.html",
    "simulador-tco-fisico-nube.html": "cloud-vs-onprem-tco-simulator.html",
    "tareas-proyectos-pymes.html": "tasks-projects-tracker.html"
}

print("Verifying JS element parity between root and en/ tools...")
discrepancies = []

for es_file, en_file in SLUG_MAP.items():
    es_path = ROOT / es_file
    en_path = EN_DIR / en_file
    if not es_path.exists() or not en_path.exists():
        discrepancies.append(f"Missing file pair: {es_file} or {en_file}")
        continue
        
    es_txt = es_path.read_text(encoding="utf-8", errors="ignore")
    en_txt = en_path.read_text(encoding="utf-8", errors="ignore")
    
    # Check all element IDs
    es_ids = set(re.findall(r'\bid=["\']([a-zA-Z0-9_\-]+)["\']', es_txt))
    en_ids = set(re.findall(r'\bid=["\']([a-zA-Z0-9_\-]+)["\']', en_txt))
    
    missing_ids_in_en = es_ids - en_ids
    if missing_ids_in_en:
        discrepancies.append(f"In {en_file}, missing IDs present in {es_file}: {missing_ids_in_en}")
        
    # Check external/internal script src filenames
    es_scripts = set(p.split("?")[0].split("/")[-1] for p in re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', es_txt))
    en_scripts = set(p.split("?")[0].split("/")[-1] for p in re.findall(r'<script[^>]*src=["\']([^"\']+)["\']', en_txt))
    
    diff_scripts = es_scripts - en_scripts
    if diff_scripts:
        discrepancies.append(f"In {en_file}, missing script tags present in {es_file}: {diff_scripts}")

print(f"\n--- JS PARITY AUDIT SUMMARY ---")
print(f"Total tool pairs checked: {len(SLUG_MAP)}")
print(f"Total parity discrepancies found: {len(discrepancies)}")
if discrepancies:
    for d in discrepancies[:10]:
        print(f"  DISCREPANCY: {d}")
else:
    print("SUCCESS: 100% of DOM IDs and script tags match perfectly across all 26 tools!")
