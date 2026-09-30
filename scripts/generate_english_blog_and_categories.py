#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador del Blog y Categorías en Inglés para Nube para Pymes (/en/blog/ y /en/category/)
Crea las páginas completas y paginadas en inglés para que la navegación en inglés
sea 100% autosuficiente y nunca devuelva al usuario a páginas en español.
"""

import re
import json
import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from functools import lru_cache

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
EN_DIR = ROOT / "en"

POSTS_PER_PAGE = 10

CATEGORY_MAP_EN = {
    "automatizacion-ia": "AI Automation & Productivity",
    "comunicacion-equipos": "Team Communication & Collaboration",
    "crm": "CRM & Customer Management",
    "facturacion-contabilidad": "Invoicing & Accounting",
    "gestion-proyectos": "Project & Task Management",
    "software-por-sector": "Industry-Specific Software",
}

def log(msg):
    print(f"[EN-ARCHIVES] {msg}", flush=True)

@lru_cache(maxsize=1)
def load_english_posts():
    slug_map = json.loads((ROOT / "scripts" / "posts_slug_map.json").read_text(encoding="utf-8"))
    catalog = json.loads((ROOT / "scripts" / "posts_catalog.json").read_text(encoding="utf-8"))
    
    # Mapeo por slug en español
    catalog_by_es = {item["slug"]: item for item in catalog}
    
    posts_data = []
    for es_slug, en_slug in slug_map.items():
        cat_info = catalog_by_es.get(es_slug, {})
        en_post_path = DIST / "en" / en_slug / "index.html"
        
        title = en_slug.replace("-", " ").title()
        desc = ""
        category_slug = "automatizacion-ia"
        date_str = "02/08/2026"
        img_src = "/wp-content/uploads/2026/07/facturacion-electronica-freelancers.webp"
        
        # Extraer metadatos reales del post inglés si existe
        if en_post_path.exists():
            soup = BeautifulSoup(en_post_path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
            h1 = soup.find("h1")
            if h1 and h1.get_text(strip=True):
                title = h1.get_text(strip=True)
            meta_desc = soup.find("meta", {"name": "description"})
            if meta_desc and meta_desc.get("content"):
                desc = meta_desc["content"]
            
            # Buscar categoría en clases o links
            article = soup.find('article')
            article_classes = article.get('class', []) if article else []
            for cat_k in CATEGORY_MAP_EN:
                if f"category-{cat_k}" in article_classes:
                    category_slug = cat_k
                    break
            
            # Imagen destacada
            img = soup.find("img", class_="wp-post-image")
            if img and img.get("src"):
                img_src = img["src"]
        
        if not desc:
            desc = f"{title}: Review features, limits, pricing, and use cases before choosing an option for your business."
            
        posts_data.append({
            "es_slug": es_slug,
            "en_slug": en_slug,
            "title": title,
            "desc": desc,
            "category_slug": category_slug,
            "category_name": CATEGORY_MAP_EN.get(category_slug, "Business Software"),
            "img_src": img_src,
            "date": date_str
        })
        
    return posts_data

def make_en_article_card(p, idx):
    post_id = 700 + idx
    return f'''<article class="post-{post_id} post type-post status-publish format-standard has-post-thumbnail hentry category-{p["category_slug"]} ast-grid-common-col ast-full-width ast-article-post remove-featured-img-padding" id="post-{post_id}" itemtype="https://schema.org/CreativeWork" itemscope="itemscope">
\t<div class="ast-post-format- blog-layout-4 ast-article-inner">
\t\t<div class="post-content ast-grid-common-col">
\t\t\t<div class="ast-blog-featured-section post-thumb ast-blog-single-element">
\t\t\t\t<div class="post-thumb-img-content post-thumb">
\t\t\t\t\t<a href="/en/{p["en_slug"]}/" aria-label="Read: {p["title"]}">
\t\t\t\t\t\t<img width="1024" height="572" src="{p["img_src"]}" loading="lazy" class="attachment-large size-large wp-post-image" alt="{p["title"]}" decoding="async" style="aspect-ratio:16/9;width:100%;object-fit:cover;">
\t\t\t\t\t</a>
\t\t\t\t</div>
\t\t\t</div>
\t\t\t<span class="ast-blog-single-element ast-taxonomy-container cat-links default">
\t\t\t\t<a href="/en/category/{p["category_slug"]}/" rel="category tag">{p["category_name"]}</a>
\t\t\t</span>
\t\t\t<h2 class="entry-title ast-blog-single-element" itemprop="headline">
\t\t\t\t<a href="/en/{p["en_slug"]}/" rel="bookmark">{p["title"]}</a>
\t\t\t</h2>
\t\t\t<header class="entry-header ast-blog-single-element ast-blog-meta-container">
\t\t\t\t<div class="entry-meta">
\t\t\t\t\t<span class="posted-by vcard author" itemtype="https://schema.org/Person" itemscope="itemscope" itemprop="author">
\t\t\t\t\t\t<a title="View author profile" href="/en/about-us/" rel="author" class="url fn n" itemprop="url">
\t\t\t\t\t\t\t<span class="author-name" itemprop="name">Juan Xavier Cabello</span>
\t\t\t\t\t\t</a>
\t\t\t\t\t</span>
\t\t\t\t\t / <span class="posted-on"><span class="published" itemprop="datePublished"> {p["date"]} </span></span>
\t\t\t\t</div>
\t\t\t</header>
\t\t\t<div class="ast-excerpt-container ast-blog-single-element">
\t\t\t\t<p>{p["desc"]}</p>
\t\t\t</div>
\t\t\t<div class="entry-content clear" itemprop="text"></div>
\t\t</div>
\t</div>
</article>'''

def make_en_pagination(current_page, total_pages, base_url="/en/blog/"):
    if total_pages <= 1:
        return ""
        
    items = []
    if current_page > 1:
        prev_url = f"{base_url}" if current_page == 2 else f"{base_url}page/{current_page - 1}/"
        items.append(f'<a class="prev page-numbers" href="{prev_url}"><span class="ast-left-arrow" aria-hidden="true">&larr;</span> Previous</a>')
        
    for p in range(1, total_pages + 1):
        if p == current_page:
            items.append(f'<span aria-current="page" class="page-numbers current">{p}</span>')
        else:
            p_url = f"{base_url}" if p == 1 else f"{base_url}page/{p}/"
            items.append(f'<a class="page-numbers" href="{p_url}">{p}</a>')
            
    if current_page < total_pages:
        next_url = f"{base_url}page/{current_page + 1}/"
        items.append(f'<a class="next page-numbers" href="{next_url}">Next <span class="ast-right-arrow" aria-hidden="true">&rarr;</span></a>')
        
    links_html = "\n".join(items)
    return f'''<div class="ast-pagination">
\t<nav class="navigation pagination" aria-label="Posts pagination">
\t\t<div class="nav-links">
{links_html}
\t\t</div>
\t</nav>
</div>'''

def generate_english_blog():
    log("Generando Blog en inglés (/en/blog/ y paginación)...")
    base_template_path = DIST / "blog" / "index.html"
    if not base_template_path.exists():
        log("ERROR: No se encontró dist/blog/index.html")
        return
        
    template = base_template_path.read_text(encoding="utf-8")
    posts = load_english_posts()
    total_posts = len(posts)
    total_pages = (total_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
    
    # Preparar el header en inglés para la plantilla base
    template = template.replace('lang="es"', 'lang="en"')
    template = template.replace('<title>Blog - Nube para Pymes</title>', '<title>Blog — SMB Cloud: Guides, Reviews & Free Tools</title>')
    template = template.replace('href="/blog/"', 'href="/en/blog/"')
    template = template.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    template = template.replace('href="/herramientas/"', 'href="/en/tools/"')
    template = template.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')
    template = template.replace('href="/en/" class="menu-link">Free Tools', 'href="/en/tools/" class="menu-link">Free Tools')
    
    # Reemplazar categorías en navbar
    for cat_slug, cat_en_name in CATEGORY_MAP_EN.items():
        template = template.replace(f'href="/category/{cat_slug}/"', f'href="/en/category/{cat_slug}/"')
        
    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * POSTS_PER_PAGE
        end_idx = min(start_idx + POSTS_PER_PAGE, total_posts)
        page_posts = posts[start_idx:end_idx]
        
        cards_html = "\n".join([make_en_article_card(p, start_idx + i) for i, p in enumerate(page_posts)])
        pagination_html = make_en_pagination(page_num, total_pages, "/en/blog/")
        
        # En el template, reemplazar los artículos
        content = re.sub(
            r'(<div class="ast-row">)[\s\S]*?(</div>\s*</main>)',
            rf'\g<1>\n{cards_html}\n\g<2>',
            template
        )
        
        # Reemplazar la paginación
        content = re.sub(
            r'<div class="ast-pagination">[\s\S]*?</nav>\s*</div>',
            pagination_html,
            content
        )
        
        # Canonical y switcher para esta página
        if page_num == 1:
            canonical_url = "https://nubeparapymes.online/en/blog/"
            es_counterpart = "/blog/"
            out_dir = DIST / "en" / "blog"
            root_out_dir = EN_DIR / "blog"
        else:
            canonical_url = f"https://nubeparapymes.online/en/blog/page/{page_num}/"
            es_counterpart = f"/blog/page/{page_num}/"
            out_dir = DIST / "en" / "blog" / "page" / str(page_num)
            root_out_dir = EN_DIR / "blog" / "page" / str(page_num)
            
        content = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical_url}" />', content)
        
        # Switcher de idioma en navbar apuntando al equivalente en español
        globe = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
        sleek_switcher = f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{es_counterpart}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Cambiar a versión en español" aria-label="Cambiar a versión en español">
    {globe}
    <span style="color:#f97316;font-weight:700;">EN</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">ES</span>
  </a>
</li>'''
        content = re.sub(r'<li[^>]*class=["\'][^"\']*menu-item-lang-switcher[^"\']*["\'][^>]*>[\s\S]*?</li>', sleek_switcher, content)
        
        # Escribir archivos
        out_dir.mkdir(parents=True, exist_ok=True)
        root_out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(content, encoding="utf-8")
        (root_out_dir / "index.html").write_text(content, encoding="utf-8")
        
    log(f"Blog en inglés generado exitosamente ({total_pages} páginas).")

def generate_english_categories():
    log("Generando archivos de categorías en inglés (/en/category/[slug]/)...")
    base_template_path = DIST / "blog" / "index.html"
    template = base_template_path.read_text(encoding="utf-8")
    posts = load_english_posts()
    
    # Preparar el header en inglés
    template = template.replace('lang="es"', 'lang="en"')
    template = template.replace('href="/blog/"', 'href="/en/blog/"')
    template = template.replace('href="/sobre-nosotros/"', 'href="/en/about-us/"')
    template = template.replace('href="/herramientas/"', 'href="/en/tools/"')
    template = template.replace('href="/directorio-herramientas/"', 'href="/en/tools/"')
    
    for cat_slug, cat_en_name in CATEGORY_MAP_EN.items():
        template = template.replace(f'href="/category/{cat_slug}/"', f'href="/en/category/{cat_slug}/"')
        
    for cat_slug, cat_en_name in CATEGORY_MAP_EN.items():
        cat_posts = [p for p in posts if p["category_slug"] == cat_slug]
        if not cat_posts:
            # Fallback si no tiene posts directos: incluir los primeros 6 posts
            cat_posts = posts[:6]
            
        total_cat_posts = len(cat_posts)
        total_cat_pages = (total_cat_posts + POSTS_PER_PAGE - 1) // POSTS_PER_PAGE
        
        for p_num in range(1, total_cat_pages + 1):
            s_idx = (p_num - 1) * POSTS_PER_PAGE
            e_idx = min(s_idx + POSTS_PER_PAGE, total_cat_posts)
            page_posts = cat_posts[s_idx:e_idx]
            
            cards_html = "\n".join([make_en_article_card(p, s_idx + i) for i, p in enumerate(page_posts)])
            pagination_html = make_en_pagination(p_num, total_cat_pages, f"/en/category/{cat_slug}/")
            
            content = re.sub(
                r'(<div class="ast-row">)[\s\S]*?(</div>\s*</main>)',
                rf'\g<1>\n{cards_html}\n\g<2>',
                template
            )
            content = re.sub(
                r'<div class="ast-pagination">[\s\S]*?</nav>\s*</div>',
                pagination_html,
                content
            )
            
            title_tag = f"<title>{cat_en_name} — Guides & Software Reviews | SMB Cloud</title>"
            content = re.sub(r'<title>.*?</title>', title_tag, content)
            
            if p_num == 1:
                canonical = f"https://nubeparapymes.online/en/category/{cat_slug}/"
                es_equiv = f"/category/{cat_slug}/"
                out_dir = DIST / "en" / "category" / cat_slug
                root_out_dir = EN_DIR / "category" / cat_slug
            else:
                canonical = f"https://nubeparapymes.online/en/category/{cat_slug}/page/{p_num}/"
                es_equiv = f"/category/{cat_slug}/page/{p_num}/"
                out_dir = DIST / "en" / "category" / cat_slug / "page" / str(p_num)
                root_out_dir = EN_DIR / "category" / cat_slug / "page" / str(p_num)
                
            content = re.sub(r'<link rel="canonical"[^>]*>', f'<link rel="canonical" href="{canonical}" />', content)
            
            globe = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
            sleek_switcher = f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{es_equiv}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Cambiar a versión en español" aria-label="Cambiar a versión en español">
    {globe}
    <span style="color:#f97316;font-weight:700;">EN</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">ES</span>
  </a>
</li>'''
            content = re.sub(r'<li[^>]*class=["\'][^"\']*menu-item-lang-switcher[^"\']*["\'][^>]*>[\s\S]*?</li>', sleek_switcher, content)
            
            out_dir.mkdir(parents=True, exist_ok=True)
            root_out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(content, encoding="utf-8")
            (root_out_dir / "index.html").write_text(content, encoding="utf-8")
            
    log("Categorías en inglés generadas exitosamente.")

def main():
    generate_english_blog()
    generate_english_categories()

if __name__ == "__main__":
    main()
