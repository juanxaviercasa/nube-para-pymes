import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

print("=== 1. AUDIT OF LANGUAGE TOGGLES IN SPANISH TOOLS ===")
for html_file in ROOT.glob("*.html"):
    if html_file.name in ["guia-uso-22-apps.html", "index.html"]:
        continue
    txt = html_file.read_text(encoding="utf-8", errors="ignore")
    # find hreflang and toggle
    alts = re.findall(r'<link[^>]*hreflang=["\']en["\'][^>]*href=["\']([^"\']+)["\']', txt)
    toggles = re.findall(r'<a[^>]*class=["\'][^"\']*np-lang-toggle[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', txt)
    if not alts or not toggles:
        print(f"Spanish tool {html_file.name}: alts={alts}, toggles={toggles}")
    elif alts and toggles and alts[0] != toggles[0] and ('/en/' + alts[0].split('/')[-1]) != toggles[0]:
        print(f"Spanish tool {html_file.name}: alt={alts[0]} vs toggle={toggles[0]}")

print("\n=== 2. AUDIT OF LANGUAGE TOGGLES IN ENGLISH TOOLS ===")
for en_html in EN_DIR.glob("*.html"):
    if en_html.name in ["user-guide.html", "index.html"]:
        continue
    txt = en_html.read_text(encoding="utf-8", errors="ignore")
    alts = re.findall(r'<link[^>]*hreflang=["\']es["\'][^>]*href=["\']([^"\']+)["\']', txt)
    toggles = re.findall(r'<a[^>]*class=["\'][^"\']*np-lang-toggle[^"\']*["\'][^>]*href=["\']([^"\']+)["\']', txt)
    if not toggles:
        print(f"English file {en_html.name}: NO toggle found!")
    else:
        # Check if the toggle target actually exists
        target = toggles[0]
        # check target
        # e.g. /calculadora-precios-venta-igv.html or /herramientas/...
        clean_target = target.lstrip('/')
        exists = (ROOT / clean_target).exists() or (ROOT / (clean_target + '/index.html')).exists()
        if not exists:
            print(f"English file {en_html.name}: toggle points to NON-EXISTENT target '{target}'")

print("\n=== 3. AUDIT OF DUPLICATE TOOLS IN EN/ ===")
en_files = [f.name for f in EN_DIR.glob("*.html")]
for f in sorted(en_files):
    if (ROOT / f).exists() and f not in ["index.html"]:
        print(f"Duplicate Spanish-named file exists inside en/: {f}")

print("\n=== 4. AUDIT OF LINKS IN EN/TOOLS/INDEX.HTML ===")
en_tools_index = EN_DIR / "tools" / "index.html"
if en_tools_index.exists():
    txt = en_tools_index.read_text(encoding="utf-8", errors="ignore")
    card_links = re.findall(r'<a[^>]*href=["\']([^"\']+)["\'][^>]*class=["\'][^"\']*(?:tool-card|btn|card)[^"\']*["\']', txt)
    all_links = set(re.findall(r'href=["\']([^"\'#]+)["\']', txt))
    broken = []
    for l in all_links:
        if l.startswith("http") or l.startswith("mailto:"):
            continue
        clean_l = l.lstrip('/')
        # Check if exists in ROOT or in EN_DIR or in DIST
        exists_in_root = (ROOT / clean_l).exists() or (ROOT / (clean_l + '/index.html')).exists() or (ROOT / (clean_l + '.html')).exists()
        exists_in_en = (EN_DIR / clean_l).exists() or (ROOT / clean_l).exists()
        if not exists_in_root:
            broken.append(l)
    print(f"Total links in en/tools/index.html: {len(all_links)}")
    print(f"Links pointing to missing files: {broken[:15]}")
