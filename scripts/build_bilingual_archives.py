"""Build English archives from the exact post selection of Spanish archives.

Matching only article bodies avoids confusing navbar category links with the
category of the current article. Pagination and dates stay identical in ES/EN.
"""
import html
import re
from pathlib import Path
from generate_english_blog_and_categories import load_english_posts, make_en_article_card, CATEGORY_MAP_EN
from generate_all_paginations import load_all_posts, build_archive_series

TAGS = {
    'automatizacion': 'Automation', 'comunicacion': 'Communication',
    'crm': 'CRM', 'digitalizacion': 'Digitization', 'facturacion': 'Invoicing',
    'gestion-de-proyectos': 'Project Management', 'ia': 'AI',
    'productividad': 'Productivity', 'software-por-sector': 'Industry Software',
    'abogados': 'Lawyers', 'academias': 'Academies', 'academias-online': 'Online Academies',
    'agencias-creativas': 'Creative Agencies', 'agencias-de-marketing': 'Marketing Agencies',
    'apps-gratuitas': 'Free Apps', 'atencion-al-cliente': 'Customer Service',
    'automatizacion-ia': 'AI Automation', 'clinicas': 'Clinics', 'comparativas': 'Comparisons',
    'computacion-en-la-nube': 'Cloud Computing', 'contabilidad': 'Accounting',
    'control-de-gastos': 'Expense Tracking', 'control-de-horarios': 'Time Tracking',
    'crm-gratis': 'Free CRM', 'crm-para-pymes': 'CRM for Small Businesses',
    'educacion': 'Education', 'encuestas': 'Surveys', 'equipos-remotos': 'Remote Teams',
    'facturacion-contabilidad': 'Invoicing & Accounting', 'facturacion-electronica': 'Electronic Invoicing',
    'firma-electronica': 'Electronic Signatures', 'gestion-de-citas': 'Appointment Scheduling',
    'gestion-de-clientes': 'Customer Management', 'gestion-de-tareas': 'Task Management',
    'gimnasios': 'Fitness Studios', 'guia-de-compra': 'Buying Guide', 'guia-practica': 'Practical Guide',
    'herramientas-gratuitas': 'Free Tools', 'independientes': 'Independent Professionals',
    'inmobiliarias': 'Real Estate', 'inteligencia-artificial': 'Artificial Intelligence',
    'inventario': 'Inventory', 'latinoamerica': 'Latin America', 'matematicas': 'Mathematics',
    'migracion-de-datos': 'Data Migration', 'nomina': 'Payroll', 'presupuesto': 'Budget',
    'profesores-particulares': 'Private Tutors', 'punto-de-venta': 'Point of Sale',
    'redes-sociales': 'Social Media', 'reportes': 'Reports', 'reservas': 'Bookings',
    'restaurantes': 'Restaurants', 'reuniones': 'Meetings', 'tiendas-online': 'Online Stores',
    'trabajo-administrativo': 'Administrative Work', 'videollamadas': 'Video Calls',
}

def build(dist):
    _, posts = load_all_posts()
    # The old export links to monthly archives but never exported their pages.
    for year, month in sorted({(p['dt'].year, p['dt'].month) for p in posts}):
        route = f'/{year}/{month:02d}/'
        selection = [p for p in posts if (p['dt'].year, p['dt'].month) == (year, month)]
        build_archive_series(route, dist / 'blog/index.html', route, selection, [dist / route.lstrip('/')])
    # Complete all category archives, including categories omitted by the old builder.
    for slug in CATEGORY_MAP_EN:
        selection = [p for p in posts if slug in p['cat_slugs']]
        if selection:
            build_archive_series(slug, dist / 'category' / slug / 'index.html', f'/category/{slug}/', selection, [dist / 'category' / slug])
    translated = {p['es_slug']: p for p in load_english_posts()}
    files = []
    for base in ('blog', 'author', 'category', 'tag'):
        files.extend((dist / base).rglob('index.html'))
    for year in sorted({str(p['dt'].year) for p in posts}):
        files.extend((dist / year).rglob('index.html'))
    for source in files:
        rel = source.relative_to(dist)
        parts = rel.parts
        title = 'Blog'
        if parts[0] == 'category':
            title = CATEGORY_MAP_EN.get(parts[1], parts[1].replace('-', ' ').title())
        elif parts[0] == 'tag':
            title = TAGS.get(parts[1], parts[1].replace('-', ' ').title())
        elif parts[0] == 'author':
            title = 'Articles by Juan Xavier Cabello'
        elif parts[0].isdigit():
            title = f'Article archive: {parts[0]}-{parts[1]}'
        text = source.read_text(encoding='utf-8')
        def card(match):
            block = match[0]
            for slug, post in translated.items():
                if f'href="/{slug}/"' in block:
                    copy = dict(post)
                    date = re.search(r'itemprop="datePublished"[^>]*>\s*([^<]+)', block)
                    if date:
                        copy['date'] = date[1].strip()
                    return make_en_article_card(copy, list(translated).index(slug))
            raise ValueError(f'Archive article has no translation: {source}')
        text = re.sub(r'<article\b[^>]*>[\s\S]*?</article>', card, text)
        text = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)} | SMB Cloud</title>', text)
        text = re.sub(r'(<h1\b[^>]*>)[\s\S]*?</h1>', lambda m: m[1] + html.escape(title) + '</h1>', text)
        text = text.replace('lang="es"', 'lang="en"')
        target = dist / 'en' / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    print(f'[I18N] Generated {len(files)} English archive pages from matching Spanish selections.', flush=True)
