import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JS_DIR = ROOT / "js"

print("=== CHECKING ROUTER CONFIGURATION ACROSS ALL JS BUNDLES ===")
for js_file in sorted(JS_DIR.glob("*.js")):
    content = js_file.read_text(encoding="utf-8", errors="ignore")
    if "BrowserRouter" in content or "createBrowserRouter" in content:
        routes = re.findall(r'path:\s*["\']([^"\']+)["\']', content)
        not_found = re.findall(r'NotFound', content)
        print(f"{js_file.name}: paths={routes}, NotFound count={len(not_found)}")
