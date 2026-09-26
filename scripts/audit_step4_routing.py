from pathlib import Path
import re
import os

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

errors = []

# 1. Root index.html check
root_index = (ROOT / "index.html").read_text(encoding="utf-8")
if 'href="./en/index.html"' not in root_index:
    errors.append("Root index.html missing link to ./en/index.html")
if 'Idioma / Language:' not in root_index:
    errors.append("Root index.html missing footer language indicator")

# 2. EN index.html check
en_index = (EN_DIR / "index.html").read_text(encoding="utf-8")
if 'href="../index.html"' not in en_index:
    errors.append("EN index.html missing link to ../index.html")
if 'Language / Idioma:' not in en_index:
    errors.append("EN index.html missing footer language indicator")

# Check all tool links in en/index.html stay inside en/
tool_links = re.findall(r'<a[^>]*href=["\']([^"\']+\.html)["\']', en_index)
for link in tool_links:
    if link.startswith("../") and not link.endswith("index.html"):
        errors.append(f"EN index.html has link leaking out to root: {link}")
    elif not link.startswith("http") and not link.startswith("../"):
        # verify file exists in en/
        clean_link = link.replace("./", "").split("#")[0].split("?")[0]
        if not (EN_DIR / clean_link).exists():
            errors.append(f"EN index.html links to missing file in en/: {link}")

# 3. User guides check
root_guide = (ROOT / "guia-uso-22-apps.html").read_text(encoding="utf-8")
if 'href="./en/user-guide.html"' not in root_guide:
    errors.append("Root guia-uso-22-apps.html missing link to ./en/user-guide.html")

en_guide = (EN_DIR / "user-guide.html").read_text(encoding="utf-8")
if 'href="../guia-uso-22-apps.html"' not in en_guide:
    errors.append("EN user-guide.html missing link to ../guia-uso-22-apps.html")

# 4. Root tools check
root_tools = [p for p in ROOT.glob("*.html") if p.name not in ["index.html", "guia-uso-22-apps.html"]]
for rt in root_tools:
    txt = rt.read_text(encoding="utf-8", errors="ignore")
    en_links = re.findall(r'href=["\'](\./en/[^"\']+\.html)["\']', txt)
    if not en_links:
        errors.append(f"Root tool {rt.name} missing footer link to English version")
    else:
        for el in en_links:
            target = ROOT / el.replace("./", "")
            if not target.exists():
                errors.append(f"Root tool {rt.name} links to missing English target: {el}")

# 5. EN tools check
en_tools = [p for p in EN_DIR.glob("*.html") if p.name not in ["index.html", "user-guide.html", "guia-uso-22-apps.html"]]
for et in en_tools:
    txt = et.read_text(encoding="utf-8", errors="ignore")
    es_links = re.findall(r'href=["\'](\.\./[^"\']+\.html)["\']', txt)
    if not es_links:
        errors.append(f"EN tool {et.name} missing footer link to Spanish version")
    else:
        for sl in es_links:
            target = ROOT / sl.replace("../", "")
            if not target.exists():
                errors.append(f"EN tool {et.name} links to missing Spanish target: {sl}")

# 6. CSS & JS check
ayuda_css = (ROOT / "css" / "ayuda-apps.css").read_text(encoding="utf-8")
if ".np-lang-switch-floating" not in ayuda_css:
    errors.append("css/ayuda-apps.css missing .np-lang-switch-floating")

ayuda_js = (ROOT / "js" / "ayuda-apps.js").read_text(encoding="utf-8")
if "np-lang-switch-floating" not in ayuda_js:
    errors.append("js/ayuda-apps.js missing floating language switcher code")

print(f"Audit completed with {len(errors)} issues.")
if errors:
    for e in errors[:15]:
        print(f"  ERROR: {e}")
else:
    print("ALL ROUTING & LANGUAGE SWITCHER CHECKS PASSED PERFECTLY (100% OK)!")
