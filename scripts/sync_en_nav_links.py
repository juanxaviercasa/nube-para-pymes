from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent

def fix_en_links():
    targets = [ROOT / "en", ROOT / "dist" / "en"]
    count = 0
    for target in targets:
        if not target.exists():
            continue
        for f in target.rglob("*.html"):
            txt = f.read_text(encoding="utf-8", errors="ignore")
            orig = txt
            txt = txt.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
            txt = txt.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')
            txt = txt.replace('href="/herramientas/"', 'href="/en/tools/"')
            txt = txt.replace('href="/en/" class="menu-link">Free Tools', 'href="/en/tools/" class="menu-link">Free Tools')
            txt = txt.replace('href="/en/" class="menu-link" >Free Tools', 'href="/en/tools/" class="menu-link">Free Tools')
            
            # Clean up any leftover geo-lang-detect
            txt = re.sub(r'<script[^>]*geo-lang-detect[^>]*></script>', '', txt)
            # Clean up any leftover floating badges
            txt = re.sub(r'<aside[^>]*class=["\']np-lang-switch-floating["\'][^>]*>[\s\S]*?</aside>', '', txt)
            
            if txt != orig:
                f.write_text(txt, encoding="utf-8")
                count += 1
    print(f"Normalized internal English navigation links across {count} HTML files.")

if __name__ == "__main__":
    fix_en_links()
