#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador Maestro de Paginación para Nube para Pymes
Resuelve los errores 404 al navegar a la página 2, 3, etc. del blog,
del autor, de las categorías y de las etiquetas, generando páginas estáticas HTML
completas, con SEO canónico, rel prev/next y marcado de navegación Astra/WordPress.
"""

import os
import re
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
WP_EXPORT = ROOT / "nubepymesexport"

POSTS_PER_PAGE = 10
SITE_URL = "https://nubeparapymes.online"

def log(msg):
    print(f"[PAGINATION] {msg}", flush=True)

def load_all_posts():
    log("Cargando catálogo y metadatos de los 70 artículos...")
    catalog_path = ROOT / "scripts" / "posts_catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError("No se encontró posts_catalog.json")
    
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    
    # Mapeo de categorías y etiquetas desde wp-json si existen
    cats_map = {}
    cat_dir = DIST / "wp-json" / "wp/v2" / "categories"
    if cat_dir.exists():
        for f in cat_dir.iterdir():
            if f.is_file() and f.name.isdigit():
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    cats_map[d["id"]] = d["slug"]
                except Exception:
                    pass

    tags_map = {}
    tag_dir = DIST / "wp-json" / "wp/v2" / "tags"
    if tag_dir.exists():
        for f in tag_dir.iterdir():
            if f.is_file() and f.name.isdigit():
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    tags_map[d["id"]] = d["slug"]
                except Exception:
                    pass

    # Fechas y metadatos WP
    wp_meta = {}
    wp_posts_dir = DIST / "wp-json" / "wp/v2" / "posts"
    if wp_posts_dir.exists():
        for f in wp_posts_dir.iterdir():
            if f.is_file() and f.name.isdigit():
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                    wp_meta[d["slug"]] = d
                except Exception:
                    pass

    # IDs de la página 1 del blog para conservar el orden original de WordPress
    blog_file = DIST / "blog" / "index.html"
    page1_ids = []
    if blog_file.exists():
        btxt = blog_file.read_text(encoding="utf-8", errors="ignore")
        page1_ids = [int(x) for x in re.findall(r'<article[^>]+id="post-(\d+)"', btxt)]

    posts = []
    for item in catalog:
        slug = item["slug"]
        post_dir = DIST / slug
        if not post_dir.exists():
            continue
        idx = post_dir / "index.html"
        if not idx.exists():
            continue
        txt = idx.read_text(encoding="utf-8", errors="ignore")

        # ID
        art_m = re.search(r'<article[^>]+id="post-(\d+)"', txt)
        post_id = int(art_m.group(1)) if art_m else None

        # Date
        date_m = re.search(r'itemprop="datePublished"[^>]*>\s*([^<]+)\s*</span>', txt)
        date_str = date_m.group(1).strip() if date_m else "01/08/2026"

        wp_d = wp_meta.get(slug, {})
        if wp_d:
            wp_iso = wp_d.get("date", "2026-08-01T12:00:00")
            dt = datetime.fromisoformat(wp_iso)
            if not post_id:
                post_id = wp_d.get("id", 1400)
            cat_ids = wp_d.get("categories", [])
            tag_ids = wp_d.get("tags", [])
            cat_slugs = set(cats_map.get(cid, str(cid)) for cid in cat_ids)
            tag_slugs = set(tags_map.get(tid, str(tid)) for tid in tag_ids)
        else:
            try:
                dt = datetime.strptime(date_str, "%d/%m/%Y")
            except Exception:
                dt = datetime(2026, 8, 1)
            if not post_id:
                post_id = 1400
            cat_slugs = set()
            tag_slugs = set()

        # Extraer categorías y etiquetas desde clases del html si faltan
        found_cats = re.findall(r'category-([a-z0-9-]+)', txt)
        cat_slugs.update(found_cats)
        found_tags = re.findall(r'tag-([a-z0-9-]+)', txt)
        tag_slugs.update(found_tags)

        # Title
        title_m = re.search(r'<h1[^>]*class="entry-title[^"]*"[^>]*>(.*?)</h1>', txt, re.DOTALL)
        title = title_m.group(1).strip() if title_m else item.get("h1", slug)
        title_clean = re.sub(r'<[^>]+>', '', title).strip()

        # Excerpt
        desc_m = re.search(r'<meta name="description" content="([^"]+)"', txt)
        excerpt = desc_m.group(1).strip() if desc_m else item.get("meta_description", "")

        # Category links
        cat_m = re.search(r'<span class="ast-taxonomy-container cat-links[^"]*">(.*?)</span>', txt, re.DOTALL)
        cat_html = cat_m.group(1).strip() if cat_m else '<a href="/category/software-por-sector/" rel="category tag">Software por sector</a>'

        cat_classes = " ".join(f"category-{c}" for c in sorted(cat_slugs))
        tag_classes = " ".join(f"tag-{t}" for t in sorted(tag_slugs))
        all_tax_classes = f"{cat_classes} {tag_classes}".strip()

        # Featured Image
        img_m = re.search(r'<img[^>]+wp-post-image[^>]+>', txt)
        if img_m:
            img_tag = img_m.group(0)
            if 'loading=' not in img_tag:
                img_tag = img_tag.replace('class="', 'loading="lazy" class="')
        else:
            img_tag = f'<img width="1024" height="572" src="/wp-content/uploads/2026/07/{slug}.webp" class="attachment-large size-large wp-post-image" alt="{title_clean}" itemprop="image" decoding="async" loading="lazy">'

        posts.append({
            "slug": slug,
            "id": post_id,
            "dt": dt,
            "date_str": date_str,
            "title": title_clean,
            "excerpt": excerpt,
            "cat_html": cat_html,
            "tax_classes": all_tax_classes,
            "cat_slugs": cat_slugs,
            "tag_slugs": tag_slugs,
            "img_tag": img_tag
        })

    # Ordenar blog: primero los de page 1 en su orden exacto, luego el resto por fecha desc
    page1_posts = [p for p in posts if p["id"] in page1_ids]
    page1_posts.sort(key=lambda p: page1_ids.index(p["id"]))

    other_posts = [p for p in posts if p["id"] not in page1_ids]
    other_posts.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)

    ordered_blog_posts = page1_posts + other_posts
    log(f"Cargados {len(ordered_blog_posts)} artículos ordenados.")
    return ordered_blog_posts, posts

def render_article_card(p):
    return f"""<article class="post-{p['id']} post type-post status-publish format-standard has-post-thumbnail hentry {p['tax_classes']} ast-grid-common-col ast-full-width ast-article-post remove-featured-img-padding" id="post-{p['id']}" itemtype="https://schema.org/CreativeWork" itemscope="itemscope">
		<div class="ast-post-format- blog-layout-4 ast-article-inner">
	<div class="post-content ast-grid-common-col">
		<div class="ast-blog-featured-section post-thumb ast-blog-single-element"><div class="post-thumb-img-content post-thumb"><a href="/{p['slug']}/" aria-label="Leer: {p['title']}">{p['img_tag']}</a></div></div><span class="ast-blog-single-element ast-taxonomy-container cat-links default">{p['cat_html']}</span><h2 class="entry-title ast-blog-single-element" itemprop="headline"><a href="/{p['slug']}/" rel="bookmark">{p['title']}</a></h2>		<header class="entry-header ast-blog-single-element ast-blog-meta-container">
			<div class="entry-meta"><span class="posted-by vcard author" itemtype="https://schema.org/Person" itemscope="itemscope" itemprop="author">			<a title="Ver todas las entradas de Nube para Pymes" href="/author/xaviercabello/" rel="author" class="url fn n" itemprop="url">
				<span class="author-name" itemprop="name">
				Nube para Pymes			</span>
			</a>
		</span>

		 / <span class="posted-on"><span class="published" itemprop="datePublished"> {p['date_str']} </span></span></div>		</header><!-- .entry-header -->
					<div class="ast-excerpt-container ast-blog-single-element">
				<p>{p['excerpt']}</p>
			</div>
				<div class="entry-content clear" itemprop="text">
					</div><!-- .entry-content .clear -->
	</div><!-- .post-content -->
</div> <!-- .blog-layout-4 -->
	</article><!-- #post-## -->"""

def generate_pagination_html(current_page, total_pages, base_url):
    def page_url(n):
        return base_url if n == 1 else f"{base_url}page/{n}/"

    lines = [
        '<div class="ast-pagination"><nav class="navigation pagination" aria-label="Paginaci&oacute;n de entradas">',
        '\t<div class="nav-links">'
    ]

    # Botón Anterior
    if current_page > 1:
        prev_u = page_url(current_page - 1)
        lines.append(f'<a class="prev page-numbers" href="{prev_u}"><span class="ast-left-arrow" aria-hidden="true">&larr;</span> Anterior</a>')

    if total_pages <= 5:
        # Paginación corta: mostrar todas las páginas
        for n in range(1, total_pages + 1):
            if n == current_page:
                lines.append(f'<span aria-current="page" class="page-numbers current">{n}</span>')
            else:
                lines.append(f'<a class="page-numbers" href="{page_url(n)}">{n}</a>')
    else:
        # Paginación con elipsis (estilo WordPress)
        # Siempre incluir 1
        if current_page == 1:
            lines.append('<span aria-current="page" class="page-numbers current">1</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(2)}">2</a>')
            lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages)}">{total_pages}</a>')
        elif current_page == 2:
            lines.append(f'<a class="page-numbers" href="{page_url(1)}">1</a>')
            lines.append('<span aria-current="page" class="page-numbers current">2</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(3)}">3</a>')
            lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages)}">{total_pages}</a>')
        elif current_page == total_pages - 1:
            lines.append(f'<a class="page-numbers" href="{page_url(1)}">1</a>')
            lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages - 2)}">{total_pages - 2}</a>')
            lines.append(f'<span aria-current="page" class="page-numbers current">{current_page}</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages)}">{total_pages}</a>')
        elif current_page == total_pages:
            lines.append(f'<a class="page-numbers" href="{page_url(1)}">1</a>')
            lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages - 1)}">{total_pages - 1}</a>')
            lines.append(f'<span aria-current="page" class="page-numbers current">{total_pages}</span>')
        else:
            lines.append(f'<a class="page-numbers" href="{page_url(1)}">1</a>')
            if current_page > 3:
                lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(current_page - 1)}">{current_page - 1}</a>')
            lines.append(f'<span aria-current="page" class="page-numbers current">{current_page}</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(current_page + 1)}">{current_page + 1}</a>')
            if current_page < total_pages - 2:
                lines.append('<span class="page-numbers dots">&hellip;</span>')
            lines.append(f'<a class="page-numbers" href="{page_url(total_pages)}">{total_pages}</a>')

    # Botón Siguiente
    if current_page < total_pages:
        next_u = page_url(current_page + 1)
        lines.append(f'<a class="next page-numbers" href="{next_u}">Siguiente <span class="ast-right-arrow" aria-hidden="true">&rarr;</span></a>')

    lines.append('</div>\n\t\t</nav></div>')
    return "\n".join(lines)

def build_archive_series(name, template_file, base_url, posts_list, target_dirs):
    """
    Construye las páginas paginadas a partir de una plantilla dada.
    """
    total_posts = len(posts_list)
    total_pages = ((total_posts - 1) // POSTS_PER_PAGE) + 1
    log(f"Procesando {name}: {total_posts} entradas -> {total_pages} páginas (Base: {base_url})")

    if not template_file.exists():
        log(f"ADVERTENCIA: Plantilla no encontrada: {template_file}")
        return

    template_txt = template_file.read_text(encoding="utf-8", errors="ignore")

    # Localizar sección de artículos
    ast_row_tag = '<div class="ast-row">'
    row_idx = template_txt.find(ast_row_tag)
    main_end_tag = '</main><!-- #main -->'
    main_idx = template_txt.find(main_end_tag)

    if row_idx == -1 or main_idx == -1:
        log(f"ERROR: No se encontraron los delimitadores ast-row en {template_file}")
        return

    head_part = template_txt[:row_idx + len(ast_row_tag)]
    tail_part = template_txt[main_idx:]

    for page_num in range(1, total_pages + 1):
        start_idx = (page_num - 1) * POSTS_PER_PAGE
        end_idx = start_idx + POSTS_PER_PAGE
        page_posts = posts_list[start_idx:end_idx]

        # Artículos HTML
        articles_html = "\n".join(render_article_card(p) for p in page_posts)

        # Paginación HTML
        pagination_html = generate_pagination_html(page_num, total_pages, base_url)

        # Modificar head_part para la página actual
        current_head = head_part
        current_tail = tail_part

        # 1. Título
        if page_num > 1:
            title_pat = r'<title>(.*?)</title>'
            m = re.search(title_pat, current_head)
            if m:
                base_title = m.group(1).split(" - Página")[0]
                new_title = f"{base_title} - Página {page_num} de {total_pages}"
                current_head = re.sub(title_pat, f"<title>{new_title}</title>", current_head)

        # 2. Canonical
        canon_pat = r'<link rel="canonical" href="([^"]*)"\s*/?>'
        curr_canon = f"{SITE_URL}{base_url}" if page_num == 1 else f"{SITE_URL}{base_url}page/{page_num}/"
        current_head = re.sub(canon_pat, f'<link rel="canonical" href="{curr_canon}" />', current_head)

        # 3. OG URL
        og_pat = r'<meta property="og:url" content="([^"]*)"\s*/?>'
        current_head = re.sub(og_pat, f'<meta property="og:url" content="{curr_canon}" />', current_head)

        # 4. Prev / Next links
        # Remover prev/next existentes
        current_head = re.sub(r'<link rel="(prev|next)" href="[^"]*"\s*/?>\n?', '', current_head)
        prev_next_tags = []
        if page_num > 1:
            p_prev = base_url if page_num == 2 else f"{base_url}page/{page_num - 1}/"
            prev_next_tags.append(f'<link rel="prev" href="{p_prev}">')
        if page_num < total_pages:
            prev_next_tags.append(f'<link rel="next" href="{base_url}page/{page_num + 1}/">')

        if prev_next_tags:
            insert_str = "\n".join(prev_next_tags) + "\n"
            current_head = current_head.replace('</head>', f'{insert_str}</head>')

        # 5. Sustituir paginación en tail_part
        # Reemplazar <div class="ast-pagination">...</div>
        current_tail = re.sub(
            r'<div class="ast-pagination">.*?</div>\s*</div>',
            pagination_html + '\n\t</div>',
            current_tail,
            flags=re.DOTALL
        )

        full_html = current_head + "\n" + articles_html + "\n</div>\t\t\t" + current_tail

        # Guardar archivo en todos los directorios destino
        for tdir in target_dirs:
            if page_num == 1:
                target_file = tdir / "index.html"
            else:
                target_file = tdir / "page" / str(page_num) / "index.html"

            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(full_html, encoding="utf-8")

    log(f"Finalizado {name}: {total_pages} páginas generadas en {len(target_dirs)} destinos.")

def main():
    log("Iniciando generación de páginas de blog y taxonomías...")
    blog_ordered_posts, all_posts = load_all_posts()

    # 1. Blog General (/blog/)
    build_archive_series(
        name="Blog General",
        template_file=DIST / "blog" / "index.html",
        base_url="/blog/",
        posts_list=blog_ordered_posts,
        target_dirs=[
            DIST / "blog",
            WP_EXPORT / "blog",
            ROOT / "blog"
        ]
    )

    # 2. Autor Xavier Cabello (/author/xaviercabello/)
    author_posts = sorted(all_posts, key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Autor Xavier Cabello",
        template_file=DIST / "author" / "xaviercabello" / "index.html",
        base_url="/author/xaviercabello/",
        posts_list=author_posts,
        target_dirs=[
            DIST / "author" / "xaviercabello",
            WP_EXPORT / "author" / "xaviercabello",
            ROOT / "author" / "xaviercabello"
        ]
    )

    # 3. Categoría: software-por-sector
    cat_software = [p for p in all_posts if "software-por-sector" in p["cat_slugs"]]
    cat_software.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Categoría Software por Sector",
        template_file=DIST / "category" / "software-por-sector" / "index.html",
        base_url="/category/software-por-sector/",
        posts_list=cat_software,
        target_dirs=[
            DIST / "category" / "software-por-sector",
            WP_EXPORT / "category" / "software-por-sector",
            ROOT / "category" / "software-por-sector"
        ]
    )

    # 4. Categoría: gestion-proyectos
    cat_proyectos = [p for p in all_posts if "gestion-proyectos" in p["cat_slugs"]]
    cat_proyectos.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Categoría Gestión de Proyectos",
        template_file=DIST / "category" / "gestion-proyectos" / "index.html",
        base_url="/category/gestion-proyectos/",
        posts_list=cat_proyectos,
        target_dirs=[
            DIST / "category" / "gestion-proyectos",
            WP_EXPORT / "category" / "gestion-proyectos",
            ROOT / "category" / "gestion-proyectos"
        ]
    )

    # 5. Categoría: automatizacion-ia
    cat_ia = [p for p in all_posts if "automatizacion-ia" in p["cat_slugs"]]
    cat_ia.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Categoría Automatización con IA",
        template_file=DIST / "category" / "automatizacion-ia" / "index.html",
        base_url="/category/automatizacion-ia/",
        posts_list=cat_ia,
        target_dirs=[
            DIST / "category" / "automatizacion-ia",
            WP_EXPORT / "category" / "automatizacion-ia",
            ROOT / "category" / "automatizacion-ia"
        ]
    )

    # 6. Etiqueta: software-por-sector
    tag_software = [p for p in all_posts if "software-por-sector" in p["tag_slugs"]]
    tag_software.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Etiqueta Software por Sector",
        template_file=DIST / "tag" / "software-por-sector" / "index.html",
        base_url="/tag/software-por-sector/",
        posts_list=tag_software,
        target_dirs=[
            DIST / "tag" / "software-por-sector",
            WP_EXPORT / "tag" / "software-por-sector",
            ROOT / "tag" / "software-por-sector"
        ]
    )

    # 7. Etiqueta: gestion-de-proyectos
    tag_proyectos = [p for p in all_posts if "gestion-de-proyectos" in p["tag_slugs"]]
    tag_proyectos.sort(key=lambda p: (p["dt"], p["id"]), reverse=True)
    build_archive_series(
        name="Etiqueta Gestión de Proyectos",
        template_file=DIST / "tag" / "gestion-de-proyectos" / "index.html",
        base_url="/tag/gestion-de-proyectos/",
        posts_list=tag_proyectos,
        target_dirs=[
            DIST / "tag" / "gestion-de-proyectos",
            WP_EXPORT / "tag" / "gestion-de-proyectos",
            ROOT / "tag" / "gestion-de-proyectos"
        ]
    )

    log("¡Todas las páginas paginadas del blog y taxonomías han sido generadas con éxito!")

if __name__ == "__main__":
    main()
