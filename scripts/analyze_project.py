import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

html_files = [f for f in ROOT.glob("*.html")]

print(f"Total root HTML files found: {len(html_files)}")
print("=" * 60)

for f in sorted(html_files):
    content = f.read_text(encoding="utf-8", errors="ignore")
    title_m = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    title = title_m.group(1).strip() if title_m else "NO TITLE"
    
    desc_m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
    if not desc_m:
        desc_m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', content, re.IGNORECASE)
    desc = desc_m.group(1).strip() if desc_m else "NO DESCRIPTION"
    
    links = set(re.findall(r'href=["\']([^"\']+)["\']', content))
    internal_html = [l for l in links if l.endswith(".html") or "/herramientas/" in l]
    
    print(f"File: {f.name}")
    print(f"  Title: {title}")
    print(f"  Description: {desc[:80]}...")
    print(f"  Size: {len(content)} chars")
    print(f"  Internal Links sample: {internal_html[:5]}")
    print("-" * 60)
