"""Normalize the final artifact, after all legacy generators have finished.

All URL decisions come from site_routes; no guessed '/en/' destinations.
Only dist is modified. The build fails if a declared translation is absent.
"""
import html
import json
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlsplit
from pathlib import Path
from site_routes import ROOT, INFORMATION_PAGES, TOOLS_MAP, route_pairs, aliases, route_for, canonical_path
from build_information_pages import build as build_information_pages
from build_en_index import translate_portal
from localize_widgets import build as build_widgets
from build_bilingual_archives import TAGS
from static_wordpress_assets import prepare as prepare_wp_assets, normalize as normalize_wp_assets

HOST = 'https://nubeparapymes.online'
LABELS = {
    'Política de Privacidad': 'Privacy Policy', 'Sobre Nosotros': 'About Us',
    'Metodología de Reseñas': 'Review Methodology', 'Contacto': 'Contact',
    'Términos y Condiciones': 'Terms and Conditions', 'Política de Cookies': 'Cookie Policy',
    'Descargo de Responsabilidad': 'Disclaimer', 'Aviso Legal': 'Legal Notice',
    'Herramientas Gratis': 'Free Tools', 'Categorías': 'Categories',
    'Automatización e IA': 'AI & Automation', 'Automatización & IA': 'AI & Automation',
    'Comunicación de Equipos': 'Team Communication', 'Comunicación y Equipos': 'Team Communication',
    'Facturación y Contabilidad': 'Invoicing & Accounting', 'Gestión de Proyectos': 'Project Management',
    'Software por Sector': 'Industry Software', 'Buscar...': 'Search...',
    'Buscar…': 'Search…', 'Buscar': 'Search', 'Saltar al contenido': 'Skip to content',
    'Página anterior': 'Previous page', 'Página siguiente': 'Next page',
    'Anterior': 'Previous', 'Siguiente': 'Next',
    'Ir al contenido': 'Skip to content', 'Menú principal': 'Main menu',
    'Automatización y productividad con IA': 'AI Automation & Productivity',
    'Comunicación y colaboración': 'Communication & Collaboration',
    'CRM y gestión de clientes': 'CRM & Customer Management',
    'Facturación y contabilidad': 'Invoicing & Accounting',
    'Gestión de proyectos y tareas': 'Project & Task Management',
    'Software por sector específico': 'Industry-Specific Software',
    'agosto 2026': 'August 2026', 'julio 2026': 'July 2026',
    'Entradas recientes': 'Recent posts', 'Comentarios recientes': 'Recent comments',
    'Archivos': 'Archives', 'Deja un comentario': 'Leave a comment',
    'Cancelar respuesta': 'Cancel reply', 'Deja una respuesta': 'Leave a reply',
    'Tu dirección de correo electrónico no será publicada. Los campos obligatorios están marcados con': 'Your email address will not be published. Required fields are marked with',
    'Comentario': 'Comment', 'Nombre': 'Name', 'Correo electrónico': 'Email',
    'Web': 'Website', 'Publicar el comentario': 'Post comment',
    'Búsqueda rápida en el sitio': 'Quick site search',
    'Escribe para buscar artículos, páginas...': 'Search articles and pages...',
    'Limpiar búsqueda': 'Clear search', 'Cerrar (Esc)': 'Close (Esc)',
    'Escribe una palabra clave para buscar en todo el contenido estático.': 'Enter a keyword to search the website.',
    'Navegar': 'Navigate', 'Seleccionar': 'Select', 'Cerrar': 'Close',
}

def attr(tag, name):
    match = re.search(r'\b' + re.escape(name) + r'\s*=\s*([\"\x27])(.*?)\1', tag, re.S | re.I)
    return html.unescape(match[2]) if match else ''

def set_attr(tag, name, value):
    encoded = html.escape(value, quote=True)
    pattern = r'(\b' + re.escape(name) + r'\s*=\s*)([\"\x27])(.*?)\2'
    if re.search(pattern, tag, re.S | re.I):
        return re.sub(pattern, lambda m: m[1] + '"' + encoded + '"', tag, count=1, flags=re.S | re.I)
    return tag[:-1] + f' {name}="{encoded}">'

def redirect_page(target, is_en):
    title = 'Page moved' if is_en else 'Página trasladada'
    return f'<!doctype html><html lang="{"en" if is_en else "es"}"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="{HOST}{target}"><meta name="robots" content="noindex"><title>{title}</title></head><body><a href="{target}">{title}</a></body></html>'

def build_english_portal(dist):
    # Use the translated, server-rendered portal with its English controller.
    # The Spanish React bundle would replace this DOM with Spanish on mount.
    text = translate_portal((ROOT / 'index.html').read_text(encoding='utf-8'))
    text = re.sub(r'<script\b[^>]*src="[^\"]*/js/index\.js[^\"]*"[^>]*></script>', '<script defer src="/js/en-index.js"></script>', text)
    text = text.replace('../assets/', '/assets/').replace('../css/', '/css/').replace('../js/', '/js/')
    text = re.sub(r'<script\b[^>]*src="[^\"]*portal-lang-switcher\.js[^\"]*"[^>]*></script>', '', text)
    text = text.replace('id="tour-modal"', 'id="tour-modal" hidden')
    text = text.replace('href="./en/index.html"', 'href="/herramientas/"')
    text = re.sub(r'(<a\b[^>]*class="[^\"]*np-lang-toggle[^\"]*"[^>]*>)[\s\S]*?</a>', lambda m: set_attr(m[1], 'href', '/herramientas/') + '<span>EN</span> | <span>ES</span></a>', text)
    # Static footer language links also need to be identified as switches.
    text = re.sub(r'<a\b[^>]*href="/herramientas/"[^>]*>English</a>', '<a class="np-footer-lang" href="/herramientas/">Español</a>', text)
    text = text.replace('>Español</span>', '>English</span>')
    for tool in TOOLS_MAP.values():
        for old in ('./' + tool['src'], tool['src']):
            text = text.replace(f'href="{old}"', f'href="/en/{tool["en_slug"]}/"')
    text = text.replace('href="./user-guide.html"', 'href="/en/user-guide/"')
    (dist / 'en/tools/index.html').write_text(text, encoding='utf-8')

def build_legacy_portal_stubs(dist):
    # Keep a physical fallback: production may normalize /index.html before
    # evaluating a hosting provider's redirect rules.
    for path in ('en/tools/en', 'herramientas/en'):
        destination = dist / path / 'index.html'
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(redirect_page('/en/tools/', True), encoding='utf-8')

def finalize(dist):
    from build_tool_translations import build as build_tool_translations
    build_tool_translations(dist)
    wp_assets = prepare_wp_assets(dist)
    build_widgets(ROOT, dist)
    for name in ('en-index.js', 'directory-experience.js'):
        for directory in (dist / 'js', dist / 'herramientas/js'):
            shutil.copyfile(ROOT / 'js' / name, directory / name)
    build_information_pages(dist)
    print('[I18N] Information pages ready', flush=True)
    build_english_portal(dist)
    print('[I18N] English portal ready', flush=True)
    # Real directory pages avoid Cloudflare's implicit .html -> extensionless
    # redirect fighting an explicit extensionless -> .html redirect.
    for name in [t['en_slug'] for t in TOOLS_MAP.values()] + ['user-guide']:
        source = ROOT / 'en' / (name + '.html')
        if not source.is_file():
            raise FileNotFoundError(f'Missing English tool: {source}')
        target = dist / 'en' / name / 'index.html'
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
    build_legacy_portal_stubs(dist)
    pairs = route_pairs(dist)
    alias_map = aliases(pairs)
    reverse = {en: es for es, en in pairs.items()}
    english_flat_files = {file.name for file in (ROOT / 'en').glob('*.html')}
    post_titles = {}
    catalog = json.loads((ROOT / 'scripts/posts_catalog.json').read_text(encoding='utf-8'))
    def translated_title(post):
        destination = pairs.get('/' + post['slug'] + '/')
        if not destination:
            return
        source = (ROOT / destination.lstrip('/') / 'index.html').read_text(encoding='utf-8')
        heading = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', source)
        if heading:
            title = html.unescape(re.sub(r'<[^>]+>', '', heading[1])).strip()
            for old in (post.get('title'), post.get('h1')):
                if old:
                    post_titles[html.unescape(old).strip()] = title
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(translated_title, catalog))
    existing_pages = {route_for(file, dist) for file in dist.rglob('index.html')}
    for es, en in pairs.items():
        for route in (es, en):
            if route not in existing_pages:
                raise FileNotFoundError(f'Missing paired page: {route}')
    data = {'pairs': pairs, 'aliases': alias_map}
    (dist / 'language-routes.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    manager = 'window.NPP_ROUTES = ' + json.dumps(data, ensure_ascii=False) + ';\n'
    manager += (ROOT / 'js/language-navigation.js').read_text(encoding='utf-8')
    (dist / 'wp-static-arquitect-assets/npp-lang-manager.js').write_text(manager, encoding='utf-8')

    english_search = []
    sitemap_urls = []
    def normalize_page(item):
        index, file = item
        if index % 100 == 0:
            print(f'[I18N] Normalizing page {index}', flush=True)
        route = route_for(file, dist)
        text = file.read_text(encoding='utf-8')
        if route in alias_map:
            file.write_text(redirect_page(alias_map[route], route.startswith('/en/')), encoding='utf-8')
            return
        if 'http-equiv="refresh"' in text.lower():
            return
        is_en = route.startswith('/en/')
        text = normalize_wp_assets(text, is_en, wp_assets)
        if route.startswith('/en/tag/'):
            slug = route.split('/')[3]
            if slug in TAGS:
                title = html.escape(TAGS[slug])
                text = re.sub(r'<title>.*?</title>', f'<title>{title} | SMB Cloud</title>', text)
                text = re.sub(r'(<h1\b[^>]*>)[\s\S]*?</h1>', lambda m: m[1] + title + '</h1>', text)
        opposite = reverse.get(route) if is_en else pairs.get(route)
        def local_url(value, switch=False):
            if not value or value.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:')):
                return value
            url = urlsplit(urljoin(HOST + route, value))
            if url.netloc not in ('nubeparapymes.online', 'apps.nubeparapymes.online', 'dev-nube-para-pymes.pantheonsite.io'):
                return value
            target = canonical_path(url.path, alias_map)
            if url.netloc == 'apps.nubeparapymes.online' and target == '/':
                target = '/herramientas/'
            # Relative links from the old flat English tools must be resolved
            # against /en/, not the new directory containing each tool.
            name = Path(url.path).name
            if is_en and name in english_flat_files and name != 'index.html':
                target = canonical_path('/en/' + name, alias_map)
            if switch and opposite:
                target = opposite
            elif is_en:
                target = pairs.get(target, target)
            return target + ('?' + url.query if url.query else '') + ('#' + url.fragment if url.fragment else '')

        def anchor(match):
            opening, inside = match[1], match[2]
            href = attr(opening, 'href')
            classes = attr(opening, 'class')
            switch = any(c in classes.split() for c in ('np-lang-toggle', 'np-footer-lang')) or attr(opening, 'id') in ('np-nav-lang-switcher', 'np-footer-lang-switcher')
            if href:
                opening = set_attr(opening, 'href', local_url(href, switch))
            if is_en and '<img' not in inside:
                old_title = html.unescape(re.sub(r'<[^>]+>', '', inside)).strip()
                if old_title in post_titles:
                    inside = html.escape(post_titles[old_title])
            return opening + inside + '</a>'
        # Never perform text/markup substitutions inside application JavaScript.
        chunks = re.split(r'(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->)', text, flags=re.I)
        for i in range(0, len(chunks), 2):
            chunk = re.sub(r'(<a\b[^>]*>)([\s\S]*?)</a>', anchor, chunks[i], flags=re.I)
            if is_en:
                def translate_node(m):
                    value = html.unescape(m[1])
                    stripped = value.strip()
                    return '>' + (value.replace(stripped, LABELS[stripped]) if stripped in LABELS else m[1]) + '<'
                chunk = re.sub(r'>([^<>]+)<', translate_node, chunk)
                def translate_attribute(m):
                    value = html.unescape(m[3])
                    return m[1] + '="' + html.escape(LABELS[value], quote=True) + '"' if value in LABELS else m[0]
                chunk = re.sub(r'\b(placeholder|aria-label|title)=(["\x27])(.*?)\2', translate_attribute, chunk)
            chunks[i] = chunk
        text = ''.join(chunks)
        if is_en:
            text = text.replace('Todos los derechos reservados', 'All rights reserved').replace('Diseñado y Desarrollado por', 'Designed &amp; Developed by')
        # Add a header switch to older editorial templates that have none.
        if opposite and 'menu-item-lang-switcher' not in text and 'id="ast-hf-menu-1"' in text:
            label = 'EN | ES' if is_en else 'ES | EN'
            switch = f'<li class="menu-item menu-item-lang-switcher"><a class="np-lang-toggle menu-link" href="{opposite}">{label}</a></li>'
            text = re.sub(r'(<ul\b[^>]*id="ast-hf-menu-[12]"[^>]*>)', lambda m: m[1] + switch, text)
        # WordPress comment submissions cannot work on a static host. Keep any
        # existing comments, and give visitors a working contact destination.
        contact_url = '/en/contact/' if is_en else '/contacto/'
        contact_label = 'Send us your question or feedback' if is_en else 'Envíanos tu pregunta o comentario'
        text = re.sub(r'<form\b[^>]*action=["\x27][^"\x27]*wp-comments-post\.php["\x27][^>]*>[\s\S]*?</form>', f'<p><a href="{contact_url}">{contact_label}</a></p>', text, flags=re.I)
        text = re.sub(r'<html\b([^>]*?)\blang="[^"]*"', lambda m: '<html' + m[1] + f'lang="{"en" if is_en else "es"}"', text, count=1)
        # Replace stale or fabricated alternates, including category pagination.
        text = re.sub(r'<link\b[^>]*\bhreflang=[^>]*>', '', text, flags=re.I)
        text = re.sub(r'<link\b[^>]*\brel=["\x27]canonical["\x27][^>]*>', '', text, flags=re.I)
        meta = f'<link rel="canonical" href="{HOST}{route}">\n'
        if opposite:
            es, en = (opposite, route) if is_en else (route, opposite)
            for lang, dest in [('es', es), ('en', en), ('x-default', es)]:
                meta += f'<link rel="alternate" hreflang="{lang}" href="{HOST}{dest}">\n'
        text = text.replace('</head>', meta + '</head>', 1)
        text = re.sub(r'<script\b[^>]*src=["\x27][^"\x27]*npp-lang-manager\.js[^"\x27]*["\x27][^>]*>\s*</script>', '', text, flags=re.I)
        text = text.replace('</head>', '<script defer src="/wp-static-arquitect-assets/npp-lang-manager.js?v=routes-v2"></script></head>', 1)
        # Nested English tool assets originally used ../js and ../css.
        if is_en:
            tool_slug = route.strip('/').split('/')[-1]
            if tool_slug in {tool['en_slug'] for tool in TOOLS_MAP.values()}:
                text = re.sub(r'<script\b[^>]*src="/en/translations/[^\"]+"[^>]*>\s*</script>', '', text)
                text = text.replace('</head>', f'<script defer src="/en/translations/{tool_slug}.js"></script></head>', 1)
            text = re.sub(r'((?:src|href)=["\x27])(?:\.\./)+(js|css|assets)/', r'\1/\2/', text)
            text = text.replace('/search-client.js', '/search-client-en.js').replace('/supabase-comments.js', '/supabase-comments-en.js')
            if route in reverse and not route.startswith(('/en/blog/', '/en/category/', '/en/tag/', '/en/author/')) and not route[4:8].isdigit():
                heading = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', text) or re.search(r'<title>(.*?)</title>', text)
                description = re.search(r'<meta\b[^>]*name=["\x27]description["\x27][^>]*>', text)
                english_search.append({'title': html.unescape(re.sub(r'<[^>]*>', '', heading[1])).strip() if heading else route,
                                       'url': route, 'excerpt': attr(description[0], 'content') if description else '', 'type': 'page'})
        file.write_text(text, encoding='utf-8')
        if route != '/404.html' and '/wp-' not in route and 'noindex' not in text:
            sitemap_urls.append(route)
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(normalize_page, enumerate(dist.rglob('*.html'))))
    english_search.sort(key=lambda item: item['url'])
    (dist / 'en/search-index.json').write_text(json.dumps(english_search, ensure_ascii=False), encoding='utf-8')

    # The only remaining shared bundle is Spanish; make its generated hrefs
    # independent of the URL at which it is mounted.
    for file in (dist / 'js/index.js', dist / 'herramientas/js/index.js'):
        text = file.read_text(encoding='utf-8').replace('./en/index.html', '/en/tools/').replace('./guia-uso-22-apps.html', '/herramientas/guia-uso/')
        for tool in TOOLS_MAP.values():
            text = text.replace('./' + tool['src'], f'/herramientas/{tool["cat"]}/{tool["slug"]}/')
        file.write_text(text, encoding='utf-8')

    # Exact legacy aliases precede existing rules; no catch-all redirects.
    redirects = {}
    for line in (dist / '_redirects').read_text(encoding='utf-8').splitlines():
        fields = line.split()
        if len(fields) != 3 or fields[0].startswith('#'):
            continue
        source, target, status = fields
        if status not in ('301', '302', '303', '307', '308', '200'):
            continue
        source_norm = canonical_path(source, {})
        target_norm = canonical_path(target, alias_map)
        if source_norm == target_norm:
            continue
        redirects[source] = (target_norm, status)
    for source, target in alias_map.items():
        redirects[source] = (target, '301')
        if source.endswith('/'):
            redirects[source.rstrip('/')] = (target, '301')
    (dist / '_redirects').write_text('# Generated legacy aliases; real pages serve both languages.\n' + '\n'.join(f'{s}    {t}    {status}' for s, (t, status) in redirects.items()) + '\n', encoding='utf-8')
    # Publish only canonical pages in the sitemap, in both languages.
    urls = sitemap_urls
    (dist / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(f'<url><loc>{HOST}{html.escape(url)}</loc></url>' for url in sorted(set(urls))) + '\n</urlset>\n', encoding='utf-8')
    print(f'[I18N] Finalized {len(pairs)} bilingual page pairs and {len(redirects)} legacy redirects.', flush=True)

if __name__ == '__main__':
    finalize(ROOT / 'dist')
