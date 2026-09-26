import http.server
import socketserver
import threading
import urllib.request
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PORT = 8765

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):
        pass # Suppress server console noise

httpd = socketserver.TCPServer(("127.0.0.1", PORT), CustomHandler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
time.sleep(0.5)

endpoints_to_test = [
    ("/", "NubeParaPymes"),
    ("/index.html", "NubeParaPymes"),
    ("/en/", "NubeParaPymes"),
    ("/en/index.html", "SMB Cloud"),
    ("/guia-uso-22-apps.html", "Guía completa de uso"),
    ("/en/user-guide.html", "Complete User Guide"),
    ("/analizador-titulares.html", "NP_HELP_CONFIG"),
    ("/en/headline-analyzer.html", "Headline Analyzer"),
    ("/en/analizador-titulares.html", "Headline Analyzer"),
    ("/creador-facturas-proforma.html", "PROFORMA"),
    ("/en/proforma-invoice-generator.html", "Proforma Invoice Generator"),
    ("/crm-pymes.html", "CRM"),
    ("/en/smb-crm.html", "SMB CRM"),
    ("/calculadora-descuentos-promociones.html", "NP_HELP_CONFIG"),
    ("/en/discount-promotions-calculator.html", "Discount & Promotions Calculator"),
    ("/calculadora-precios-venta-igv.html", "NP_HELP_CONFIG"),
    ("/en/sales-pricing-tax-calculator.html", "Sales Pricing & Tax Calculator"),
    ("/js/ayuda-apps.js", "np-lang-switch-floating"),
    ("/css/ayuda-apps.css", "np-lang-switch-floating")
]

print(f"Testing live HTTP server at http://127.0.0.1:{PORT}...")
results = []
all_ok = True

for path, expected_needle in endpoints_to_test:
    url = f"http://127.0.0.1:{PORT}{path}"
    try:
        req = urllib.request.urlopen(url, timeout=3)
        status = req.getcode()
        body = req.read().decode("utf-8", errors="ignore")
        if status == 200 and expected_needle in body:
            results.append((path, status, "PASS"))
        else:
            all_ok = False
            results.append((path, status, f"FAIL (Needle '{expected_needle}' missing)"))
    except Exception as e:
        all_ok = False
        results.append((path, 500, f"FAIL ({e})"))

httpd.shutdown()
httpd.server_close()

print("\n--- LIVE HTTP TEST RESULTS ---")
for path, status, res in results:
    print(f"  {status} {path} -> {res}")

if all_ok:
    print("\nSUCCESS: All endpoints returned HTTP 200 and expected content!")
else:
    print("\nFAIL: Some endpoints failed.")
