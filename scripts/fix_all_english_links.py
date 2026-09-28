#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reescribe y sincroniza todos los enlaces internos dentro del ecosistema en inglés (/en/).
Garantiza que ningún enlace en /en/ apunte a rutas en español, evitando que el usuario
sea devuelto a la versión en español al hacer clic en pestañas, categorías, artículos o herramientas.
Restaura además el selector de idioma para que apunte con total precisión a la versión en español.
"""

import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EN_DIR = ROOT / "en"

CATEGORY_MAP_EN = {
    "automatizacion-ia": "AI Automation & Productivity",
    "comunicacion-equipos": "Team Communication & Collaboration",
    "crm": "CRM & Customer Management",
    "facturacion-contabilidad": "Invoicing & Accounting",
    "gestion-proyectos": "Project & Task Management",
    "software-por-sector": "Industry-Specific Software",
}

special_en_to_es = {
    "about-us": "sobre-nosotros",
    "tools": "herramientas",
    "user-guide": "herramientas/guia-uso",
    "blog": "blog",
}

def log(msg):
    print(f"[LINK-FIXER] {msg}", flush=True)

def make_sleek_switcher(target_url, is_en=True):
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

def fix_links():
    slug_map = json.loads((ROOT / "scripts" / "posts_slug_map.json").read_text(encoding="utf-8"))
    en_to_es = {v: k for k, v in slug_map.items()}
    
    # Lista de archivos en inglés a procesar
    en_files = list((DIST / "en").rglob("*.html")) + list(EN_DIR.rglob("*.html"))
    seen = set()
    targets = []
    for f in en_files:
        if f not in seen and f.is_file():
            seen.add(f)
            targets.append(f)
            
    log(f"Reescribiendo enlaces internos en {len(targets)} archivos HTML en inglés...")
    
    updated_files = 0
    for html_file in targets:
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            original = content
            
            # 1. Navbar y enlaces generales del sistema
            content = content.replace('href="/blog/"', 'href="/en/blog/"')
            content = content.replace('href="/blog"', 'href="/en/blog/"')
            content = content.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
            content = content.replace('href="/sobre-nosotros"', 'href="/en/about-us/"')
            content = content.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')
            content = content.replace('href="/directorio-herramientas"', 'href="/en/tools/"')
            content = content.replace('href="/herramientas/"', 'href="/en/tools/"')
            content = content.replace('href="/software-por-sector/"', 'href="/en/category/software-por-sector/"')
            content = content.replace('href="/software-por-sector"', 'href="/en/category/software-por-sector/"')
            
            # Enlace Free Tools en el header si quedó con href="/en/"
            content = re.sub(
                r'href="/en/"\s+class="menu-link">Free Tools',
                'href="/en/tools/" class="menu-link">Free Tools',
                content
            )
            
            # 2. Categorías
            for cat_slug in CATEGORY_MAP_EN:
                content = content.replace(f'href="/category/{cat_slug}/"', f'href="/en/category/{cat_slug}/"')
                content = content.replace(f'href="/category/{cat_slug}"', f'href="/en/category/{cat_slug}/"')
                
            # 3. Slugs de artículos
            for es_slug, en_slug in slug_map.items():
                content = content.replace(f'href="/{es_slug}/"', f'href="/en/{en_slug}/"')
                content = content.replace(f'href="/{es_slug}"', f'href="/en/{en_slug}/"')
                
            # 4. Enlaces de herramientas individuales en /en/index.html o páginas en inglés
            content = content.replace('href="/herramientas-ia-automatizar-tareas/"', 'href="/en/ai-tools-automate-business-tasks/"')
            content = content.replace('href="/herramientas-profesores-particulares/"', 'href="/en/language-school-management-software/"')
            
            # 5. Enlaces en footer
            content = content.replace('href="/aviso-legal/"', 'href="/en/legal-notice/"')
            content = content.replace('href="/descargo-de-responsabilidad/"', 'href="/en/disclaimer/"')
            content = content.replace('href="/politica-de-privacidad/"', 'href="/en/privacy-policy/"')
            content = content.replace('href="/terminos-y-condiciones/"', 'href="/en/terms-and-conditions/"')
            content = content.replace('href="/contacto/"', 'href="/en/contact/"')
            content = content.replace('href="/metodologia-de-resenas/"', 'href="/en/review-methodology/"')
            content = content.replace('href="/politica-de-cookies/"', 'href="/en/cookie-policy/"')

            # 6. RESTAURAR EL SELECTOR DE IDIOMA PARA QUE APUNTE CON PRECISIÓN A ESPAÑOL
            if "menu-item-lang-switcher" in content:
                tag_start = content.find("menu-item-lang-switcher")
                li_start = content.rfind("<li", 0, tag_start)
                li_end = content.find("</li>", tag_start)
                if li_start != -1 and li_end != -1:
                    li_end += 5
                    parts = html_file.parts
                    slug = ""
                    if "en" in parts:
                        idx = parts.index("en")
                        if len(parts) > idx + 2:
                            slug = parts[idx + 1]
                    
                    if slug in en_to_es:
                        target_url = f"/{en_to_es[slug]}/"
                    elif slug in special_en_to_es:
                        target_url = f"/{special_en_to_es[slug]}/"
                    elif slug == "blog":
                        target_url = "/blog/"
                    elif slug == "category" and len(parts) > idx + 3:
                        target_url = f"/category/{parts[idx + 2]}/"
                    else:
                        target_url = "/"
                        
                    content = content[:li_start] + make_sleek_switcher(target_url, is_en=True) + content[li_end:]

            if content != original:
                html_file.write_text(content, encoding="utf-8")
                updated_files += 1
        except Exception as e:
            log(f"Error procesando {html_file.name}: {e}")
            
    log(f"Se corrigieron y enlazaron a inglés las rutas de {updated_files} archivos HTML.")

if __name__ == "__main__":
    fix_links()
