"""Build-time links to verified illustrated tutorials; no runtime fetch."""
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from site_routes import route_pairs
from fix_multilingual_issues import TOOLS_MAP
from help_configs import CONFIGS

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
    for portal, english in [('herramientas/index.html', False), ('en/tools/index.html', True)]:
        file = dist / portal
        soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
        for old in soup.select('#np-tutorial-portal-config, script[data-npp-tutorial-portal], [data-npp-tutorial-card]'):
            old.decompose()
        if not soup.select_one('link[href*="tutoriales-ilustrados.css"]'):
            soup.head.append(soup.new_tag('link', rel='stylesheet', href='/herramientas/css/tutoriales-ilustrados.css'))
        config = soup.new_tag('script', id='np-tutorial-portal-config')
        entries = []
        illustrated = {tool['slug']: tool for tool in tools}
        for slug, tool in TOOLS_MAP.items():
            route = f"/herramientas/{tool['cat']}/{tool['slug']}/"
            full_route = pairs[route] if english else route
            tutorial = illustrated.get(slug)
            url = tutorial['tutorialUrl'] if tutorial else ('/en/user-guide/' if english else '/herramientas/guia-uso/') + '#' + CONFIGS.get(slug, {'anchor': {'inventario-compras-pymes':'25-inventario-proveedores-y-compras','tareas-proyectos-pymes':'26-tareas-y-proyectos-operativos'}.get(slug,slug)})['anchor']
            if english and not tutorial:
                # English help uses the translated guide's actual tool section.
                anchors = {'comparador-campanas-avanzado':'8-advanced-ad-campaign-comparator','consola-campanas':'9-campaign-utm-console','organizador-matriz-contenidos':'21-content-matrix-planner','calculadora-descuentos-promociones':'3-discount-promotions-calculator','guiones-manejo-objeciones':'20-objectionpro-sales-objection-scripts','simulador-tco-fisico-nube':'22-tco-simulator-on-premise-vs-cloud','inventario-compras-pymes':'25-inventory-supplier-purchasing','firma-correo-html':'12-html-email-signature-generator','generador-contrasenas-pymes':'14-secukey-smb-password-generator','tareas-proyectos-pymes':'26-operations-tasks-projects'}
                url = '/en/user-guide/#' + anchors[slug]
            if not tutorial:
                guide_path, anchor = url.split('#', 1)
                guide = BeautifulSoup((dist / guide_path.strip('/') / 'index.html').read_text(encoding='utf-8'), 'html.parser')
                if guide.find(id=anchor) is None: raise ValueError(f'Missing tutorial section: {url}')
            entries.append({'route': full_route, 'slug': slug, 'url': url, 'illustrated': bool(tutorial)})
            launch = soup.find('a', href=full_route)
            card = launch.find_parent('article') if launch else None
            if card is not None:
                link = soup.new_tag('a', href=url)
                link['data-npp-tutorial-card'] = slug
                link['class'] = 'npp-tutorial-card-link'
                if tutorial: link['target'] = '_blank'; link['rel'] = 'noopener noreferrer'
                link.string = 'View tutorial' if english else 'Ver tutorial'
                card.append(link)
        config.string = 'window.NP_TUTORIAL_PORTAL=' + json.dumps({'english': english, 'tools': entries}, ensure_ascii=False) + ';'
        soup.head.append(config)
        script = soup.new_tag('script', src='/herramientas/js/tutoriales-ilustrados.js')
        script['defer'] = ''
        script['data-npp-tutorial-portal'] = 'true'
        soup.head.append(script)
        write_html(file, soup)
    # Refresh shared visual assets in existing browsers after this repair.
    affected = {'/herramientas/', '/en/tools/'}
    for tool in TOOLS_MAP.values():
        route = f"/herramientas/{tool['cat']}/{tool['slug']}/"
        affected.update((route, pairs[route]))
    for route in affected:
        file = dist / route.strip('/') / 'index.html'
        text = file.read_text(encoding='utf-8')
        text = re.sub(r'((?:src|href)=["\'])([^"\']*(?:tool-experience\.css|regional-settings\.css|regional-ui\.js|tutoriales-ilustrados\.(?:css|js)|generador-paletas-corporativas\.js))(?:\?[^"\']*)?(["\'])', lambda m: m[1] + m[2] + '?v=20261017-visual-2' + m[3], text)
        file.write_text(text, encoding='utf-8')
    print(f'Illustrated tutorials: {len(tools)} tools integrated in Spanish and English.')
