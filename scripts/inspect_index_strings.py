from pathlib import Path
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

print("Title:", soup.title.string if soup.title else None)
print("Meta desc:", soup.find("meta", {"name": "description"}))
print("H1:", soup.find("h1").get_text(strip=True) if soup.find("h1") else None)
print("H2s:", [h.get_text(strip=True) for h in soup.find_all("h2")])
print("H3s count:", len(soup.find_all("h3")))
print("Sample H3s:", [h.get_text(strip=True) for h in soup.find_all("h3")[:5]])
