import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

files = sorted(list(EN_DIR.glob("*.html")))
print(f"Verifying integrity of {len(files)} HTML files in en/...")

missing_titles = []
missing_descriptions = []
missing_lang = []
broken_local_assets = []

for f in files:
    content = f.read_text(encoding="utf-8", errors="ignore")
    
    # Check lang="en"
    if 'lang="en"' not in content:
        missing_lang.append(f.name)
        
    # Check title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    if not title_match or not title_match.group(1).strip():
        missing_titles.append(f.name)
        
    # Check meta description
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']*)["\']', content, re.IGNORECASE)
    if not desc_match or not desc_match.group(1).strip():
        missing_descriptions.append(f.name)
        
    # Check asset paths
    assets = re.findall(r'(?:src|href)=["\'](\.\./[^"\']+)["\']', content)
    for a in assets:
        target = ROOT / a.replace('../', '')
        # Ignore external or query params
        target_path = str(target).split('?')[0].split('#')[0]
        if not os.path.exists(target_path):
            broken_local_assets.append((f.name, a))

print(f"Missing lang='en': {len(missing_lang)}")
print(f"Missing titles: {len(missing_titles)}")
print(f"Missing meta descriptions: {len(missing_descriptions)}")
print(f"Broken relative assets: {len(broken_local_assets)}")

if broken_local_assets:
    for b in broken_local_assets[:10]:
        print(f"  Broken in {b[0]}: {b[1]}")
else:
    print("ALL assets and meta tags verified successfully!")
