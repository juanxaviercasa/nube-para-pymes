from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
en_index = ROOT / "en" / "index.html"
txt = en_index.read_text(encoding="utf-8")
links = set(re.findall(r'href=["\']([^"\'#]+)["\']', txt))
print("Total links in en/index.html:", len(links))

spanish_links = [l for l in links if not l.startswith("/en/") and not l.startswith("http") and not l.startswith("mailto:") and not l.startswith("#")]
print("\nNon-English links in en/index.html:")
for l in sorted(spanish_links):
    print("  ", l)
