from pathlib import Path
from bs4 import BeautifulSoup

html = Path("guia-uso-22-apps.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

h2s = [h.get_text(strip=True) for h in soup.find_all("h2")]
print(f"Total H2s: {len(h2s)}")
for i, h in enumerate(h2s):
    print(f"  {i+1}. {h}")
