#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Actualizador ultrarrápido y seguro de selectores de idioma (sin regex backtracking).
Reemplaza el elemento menu-item-lang-switcher por el selector píldora estilizado.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EN_DIR = ROOT / "en"

slug_map_file = ROOT / "scripts" / "posts_slug_map.json"
es_to_en = json.loads(slug_map_file.read_text(encoding="utf-8")) if slug_map_file.exists() else {}
en_to_es = {v: k for k, v in es_to_en.items()}

special_en_to_es = {
    "about-us": "sobre-nosotros",
    "tools": "herramientas",
    "user-guide": "herramientas/guia-uso",
    "blog": "blog",
}
special_es_to_en = {
    "sobre-nosotros": "about-us",
    "herramientas": "tools",
    "directorio-herramientas": "tools",
    "blog": "blog",
}

def make_sleek_switcher(target_url, is_en=False):
    globe = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    if is_en:
        return f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{target_url}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Cambiar a versión en español" aria-label="Cambiar a versión en español">
    {globe}
    <span style="color:#f97316;font-weight:700;">EN</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">ES</span>
  </a>
</li>'''
    else:
        return f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{target_url}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Switch to English version" aria-label="Switch to English version">
    {globe}
    <span style="color:#f97316;font-weight:700;">ES</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">EN</span>
  </a>
</li>'''

def update_all():
    targets = list(DIST.rglob("*.html")) + list(EN_DIR.rglob("*.html"))
    seen = set()
    count = 0

    for html_file in targets:
        if html_file in seen or not html_file.is_file():
            continue
        seen.add(html_file)
        
        rel_str = str(html_file).replace("\\", "/")
        if "/herramientas/" in rel_str and not rel_str.endswith("herramientas/index.html") and not rel_str.endswith("herramientas/guia-uso/index.html"):
            continue
            
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            tag_start = content.find("menu-item-lang-switcher")
            if tag_start == -1:
                continue
                
            li_start = content.rfind("<li", 0, tag_start)
            if li_start == -1:
                continue
                
            li_end = content.find("</li>", tag_start)
            if li_end == -1:
                continue
            li_end += 5
            
            is_en = "/en/" in rel_str or rel_str.endswith("/en/index.html") or "/en" in html_file.parts
            
            # Determinar slug
            parts = html_file.parts
            slug = ""
            if "en" in parts:
                idx = parts.index("en")
                if len(parts) > idx + 2:
                    slug = parts[idx + 1]
            elif "dist" in parts:
                idx = parts.index("dist")
                if len(parts) > idx + 2:
                    slug = parts[idx + 1]
                    
            if is_en:
                if slug in en_to_es:
                    target_url = f"/{en_to_es[slug]}/"
                elif slug in special_en_to_es:
                    target_url = f"/{special_en_to_es[slug]}/"
                elif slug == "blog":
                    target_url = "/blog/"
                else:
                    target_url = "/"
            else:
                if slug in es_to_en:
                    target_url = f"/en/{es_to_en[slug]}/"
                elif slug in special_es_to_en:
                    target_url = f"/en/{special_es_to_en[slug]}/"
                elif slug == "blog":
                    target_url = "/en/blog/"
                else:
                    target_url = "/en/"
                    
            new_switcher = make_sleek_switcher(target_url, is_en)
            new_content = content[:li_start] + new_switcher + content[li_end:]
            
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                count += 1
        except Exception:
            pass

    print(f"Selector rápido actualizado en {count} archivos.")

if __name__ == "__main__":
    update_all()
