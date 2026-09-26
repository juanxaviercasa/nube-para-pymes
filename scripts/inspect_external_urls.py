from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
EN_DIR = ROOT / "en"

all_html = list(ROOT.glob("*.html")) + list(EN_DIR.glob("*.html"))
external_urls = set()

for html_file in all_html:
    content = html_file.read_text(encoding="utf-8", errors="ignore")
    matches = re.findall(r'(?:src|href)=["\'](https?://[^"\']+)["\']', content)
    for m in matches:
        external_urls.add(m)

print(f"External URLs ({len(external_urls)}):")
for u in sorted(external_urls):
    print(f"  {u}")
