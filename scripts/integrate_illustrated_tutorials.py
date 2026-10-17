"""Build-time links to verified illustrated tutorials; no runtime fetch."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from site_routes import route_pairs

ROOT = Path(__file__).resolve().parents[1]

def write_html(file, soup):
    text = re.sub(r"</svg>[ \t]+\n", "</svg>\n", str(soup))
    # Preserve the canonical alternate format used by the bilingual build.
    for tag in soup.select('link[rel="alternate"][hreflang][href]'):
        stable = '<link rel="alternate" hreflang="' + html.escape(tag['hreflang'], quote=True) + '" href="' + html.escape(tag['href'], quote=True) + '"/>'
        text = text.replace(str(tag), stable)
    file.write_text(text, encoding='utf-8')

def integrate(dist):
    data = json.loads((ROOT / 'content/todolima-tutorials.json').read_text(encoding='utf-8'))
    pairs = route_pairs(dist)
    tools = data['tools']
    seen = set()
    for tool in tools:
        slug = tool['slug']
        if slug in seen:
            raise ValueError(f'Duplicate tutorial {slug}')
        seen.add(slug)
        target = tool['tutorialUrl']
        parsed = urlsplit(target)
        if parsed.scheme != 'https' or parsed.netloc != 'todolima.com' or parsed.path != f'/herramientas/{slug}':
            raise ValueError(f'Invalid tutorial URL: {target}')
        route = urlsplit(tool['toolUrl']).path
        for route, english in [(route, False), (pairs[route], True)]:
            file = dist / route.strip('/') / 'index.html'
            soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
            for old in soup.select('[data-npp-illustrated-tutorial], #np-illustrated-tutorial-config'):
                old.decompose()
            title = 'Learn with screenshots' if english else 'Aprende con capturas paso a paso'
            label = 'View illustrated tutorial in Spanish' if english else 'Ver tutorial ilustrado en Todo Lima'
            note = ('Open the Spanish guide in a new tab and keep this tool open to follow each step.' if english else 'Abre la guía en otra pestaña y mantén esta herramienta abierta para practicar cada paso.')
            block = BeautifulSoup(f'<aside class="npp-illustrated-tutorial" data-npp-illustrated-tutorial="{slug}" aria-label="{title}"><div><p class="npp-tutorial-eyebrow">Todo Lima · {len(tool["steps"])} '+('illustrated steps' if english else 'pasos ilustrados')+f'</p><h2>{title}</h2><p>{note}</p></div><a href="{html.escape(target, quote=True)}" target="_blank" rel="noopener noreferrer">{label} <span aria-hidden="true">↗</span><span class="npp-tutorial-sr">'+(' (opens in a new tab)' if english else ' (abre en otra pestaña)')+'</span></a></aside>', 'html.parser').aside
            # Outside React roots: survives app rendering and remains available without JS.
            app = soup.select_one('#root')
            if app:
                app.insert_before(block)
            else:
                nav = soup.select_one('.np-global-nav')
                if nav: nav.insert_after(block)
                else: soup.body.insert(0, block)
            css = soup.new_tag('link', rel='stylesheet', href='/herramientas/css/tutoriales-ilustrados.css')
            soup.head.append(css)
            config = soup.new_tag('script', id='np-illustrated-tutorial-config')
            config.string = 'window.NP_ILLUSTRATED_TUTORIAL=' + json.dumps({'url': target, 'label': label}, ensure_ascii=False) + ';'
            soup.head.append(config)
            write_html(file, soup)
        # Card links in both portals; only tools with a verified tutorial receive one.
        for portal, app_route, english in [('herramientas/index.html', urlsplit(tool['toolUrl']).path, False), ('en/tools/index.html', pairs[urlsplit(tool['toolUrl']).path], True)]:
            file = dist / portal
            soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
            launch = soup.find('a', href=app_route)
            if launch is None: raise ValueError(f'Missing portal card: {slug} in {portal}')
            if not soup.select_one(f'[data-npp-tutorial-card="{slug}"]'):
                link = soup.new_tag('a', href=target, target='_blank', rel='noopener noreferrer')
                link['data-npp-tutorial-card'] = slug
                link['class'] = 'npp-tutorial-card-link'
                link.string = 'Illustrated tutorial (Spanish) ↗' if english else 'Tutorial con capturas ↗'
                launch.insert_after(link)
                if not soup.select_one('link[href="/herramientas/css/tutoriales-ilustrados.css"]'):
                    soup.head.append(soup.new_tag('link', rel='stylesheet', href='/herramientas/css/tutoriales-ilustrados.css'))
                write_html(file, soup)
    for portal, english in [('herramientas/index.html', False), ('en/tools/index.html', True)]:
        file = dist / portal
        soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        for old in soup.select('#np-tutorial-portal-config, script[data-npp-tutorial-portal]'):
            old.decompose()
        config = soup.new_tag('script', id='np-tutorial-portal-config')
        entries = []
        for tool in tools:
            route = urlsplit(tool['toolUrl']).path
            entries.append({'route': pairs[route] if english else route, 'slug': tool['slug'], 'url': tool['tutorialUrl']})
        config.string = 'window.NP_TUTORIAL_PORTAL=' + json.dumps({'english': english, 'tools': entries}, ensure_ascii=False) + ';'
        soup.head.append(config)
        script = soup.new_tag('script', src='/herramientas/js/tutoriales-ilustrados.js')
        script['defer'] = ''
        script['data-npp-tutorial-portal'] = 'true'
        soup.head.append(script)
        write_html(file, soup)
    print(f'Illustrated tutorials: {len(tools)} tools integrated in Spanish and English.')
