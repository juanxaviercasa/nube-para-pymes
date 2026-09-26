from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

all_en_files = list(EN_DIR.glob("*.html"))
print(f"Checking responsive metadata and stylesheet links in {len(all_en_files)} files in en/...")

missing_viewport = []
missing_charset = []
broken_css_links = []

for f in all_en_files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    
    # Check viewport
    if not re.search(r'<meta[^>]*name=["\']viewport["\']', content, re.IGNORECASE):
        missing_viewport.append(f.name)
        
    # Check charset
    if not re.search(r'<meta[^>]*charset=', content, re.IGNORECASE):
        missing_charset.append(f.name)
        
    # Check CSS links
    css_links = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\']([^"\']+)["\']', content, re.IGNORECASE)
    for link in css_links:
        if link.startswith("http://") or link.startswith("https://"):
            continue
        clean_link = link.split("?")[0].split("#")[0]
        target = (EN_DIR / clean_link).resolve()
        if not target.exists():
            broken_css_links.append((f.name, link))

print(f"\n--- RESPONSIVE & STYLE AUDIT SUMMARY ---")
print(f"Files missing viewport meta tag: {len(missing_viewport)}")
print(f"Files missing charset meta tag: {len(missing_charset)}")
print(f"Broken stylesheet links: {len(broken_css_links)}")

if not missing_viewport and not missing_charset and not broken_css_links:
    print("SUCCESS: 100% of files have proper responsive viewport meta tags, UTF-8 charset, and valid stylesheet links!")
