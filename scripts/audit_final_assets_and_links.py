import os
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

print("Auditing all assets and links across root and en/...")

files_to_audit = list(ROOT.glob("*.html")) + list(EN_DIR.glob("*.html"))
print(f"Total HTML files to audit: {len(files_to_audit)}")

broken_assets = []
broken_internal_links = []
external_urls = set()

for html_file in files_to_audit:
    content = html_file.read_text(encoding="utf-8", errors="ignore")
    is_in_en = (html_file.parent == EN_DIR)
    
    # Check script src, link href (css), img src
    asset_matches = re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
    for ref in asset_matches:
        # Ignore anchors, mailto, tel, javascript
        if ref.startswith("#") or ref.startswith("mailto:") or ref.startswith("tel:") or ref.startswith("javascript:") or ref.startswith("data:"):
            continue
            
        parsed = urlparse(ref)
        if parsed.scheme in ["http", "https"]:
            external_urls.add(ref)
            continue
            
        # Clean query strings and hashes
        clean_ref = ref.split("?")[0].split("#")[0]
        if not clean_ref:
            continue
            
        # Resolve path
        if clean_ref.startswith("/"):
            # absolute from root
            target = ROOT / clean_ref.lstrip("/")
        elif is_in_en:
            target = (EN_DIR / clean_ref).resolve()
        else:
            target = (ROOT / clean_ref).resolve()
            
        if not target.exists():
            # Check if it's an asset or an HTML page
            if any(clean_ref.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".jpeg", ".webp", ".svg", ".ico", ".json", ".woff", ".woff2"]):
                broken_assets.append((html_file.name, ref, str(target)))
            elif clean_ref.endswith(".html") or not "." in Path(clean_ref).name:
                broken_internal_links.append((html_file.name, ref, str(target)))

print(f"\n--- ASSET & LINK AUDIT SUMMARY ---")
print(f"Total external URLs referenced: {len(external_urls)}")
print(f"Broken local assets (CSS, JS, Images): {len(broken_assets)}")
print(f"Broken internal HTML links: {len(broken_internal_links)}")

if broken_assets:
    print("\nBroken Assets:")
    for src, ref, tgt in broken_assets[:15]:
        print(f"  In {src}: {ref} -> {tgt}")

if broken_internal_links:
    print("\nBroken Internal Links:")
    for src, ref, tgt in broken_internal_links[:15]:
        print(f"  In {src}: {ref} -> {tgt}")

if not broken_assets and not broken_internal_links:
    print("\nSUCCESS: 0 broken assets and 0 broken internal links found across all files!")
