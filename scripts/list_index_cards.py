from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
html = (ROOT / "index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

articles = soup.find_all("article")
print(f"Total articles found: {len(articles)}")

for i, a in enumerate(articles, 1):
    cat = a.find("span", class_=lambda c: c and "uppercase" in c)
    cat_text = cat.get_text(strip=True) if cat else "No cat"
    h3 = a.find("h3")
    title = h3.get_text(strip=True) if h3 else "No title"
    p = a.find("p")
    desc = p.get_text(strip=True) if p else "No desc"
    link = a.find("a")
    href = link.get("href") if link else "No href"
    print(f"{i}. [{cat_text}] {title}")
    print(f"   Desc: {desc}")
    print(f"   Link: {href}")
