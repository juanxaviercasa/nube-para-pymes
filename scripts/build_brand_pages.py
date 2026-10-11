"""Build honest, bilingual about/contact pages for the static Cloudflare site."""
import json
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]


def build(dist):
    privacy_file = dist / 'politica-de-privacidad/index.html'
    privacy = BeautifulSoup(privacy_file.read_text(encoding='utf-8'), 'html.parser')
    container = privacy.select_one('.entry-content')
    for node in container.find_all(string=True):
        if 'Formulario de contacto:' in str(node):
            node.replace_with('Formulario de contacto: nombre, correo electrónico, tipo de consulta y mensaje; negocio y enlace relacionado son opcionales. Utilizamos estos datos para entender y responder a tu consulta.')
        elif '13 de julio de 2026' in str(node):
            node.replace_with(str(node).replace('13 de julio de 2026', '11 de octubre de 2026'))
    if not container.select_one('#procesamiento-contacto'):
        container.append(BeautifulSoup('<section id="procesamiento-contacto"><h2>Procesamiento de las consultas</h2><p>El formulario utiliza Cloudflare Workers para tramitar el envío y Cloudflare Turnstile para verificar solicitudes y reducir el abuso. Cloudflare procesa también datos técnicos, como la dirección IP, para esa verificación. El mensaje se entrega a un buzón del proyecto administrado en Gmail (Google), desde el que respondemos.</p><p>El envío no te suscribe a publicidad ni guarda la consulta en una base de datos del sitio. Conservamos el mensaje en el correo para atenderlo. Puedes solicitar su eliminación escribiendo a <a href="mailto:contacto@nubeparapymes.online">contacto@nubeparapymes.online</a>.</p></section>', 'html.parser'))
    privacy_file.write_text(str(privacy), encoding='utf-8')
    for es, en, kind in [('sobre-nosotros', 'about-us', 'about'), ('contacto', 'contact', 'contact')]:
        template = (dist / es / 'index.html').read_text(encoding='utf-8')
        for lang, route, title, description in [
            ('es', es, 'Sobre nosotros' if kind == 'about' else 'Contacto',
             'Guías y herramientas para elegir software y organizar una pyme.' if kind == 'about' else 'Cuéntanos qué necesita tu pyme: software, herramientas, una corrección o apoyo digital.'),
            ('en', 'en/' + en, 'About us' if kind == 'about' else 'Contact',
             'Guides and tools to choose software and organize a small business.' if kind == 'about' else 'Tell us what your business needs: software, tools, an editorial correction or digital support.')]:
            soup = BeautifulSoup(template, 'html.parser')
            soup.html['lang'] = lang
            soup.body['class'] = list(soup.body.get('class', [])) + ['npp-info-page']
            content = soup.select_one('.entry-content')
            content.clear()
            markup = (ROOT / 'content/brand' / f'{kind}-{lang}.html').read_text(encoding='utf-8')
            content.append(BeautifulSoup(markup, 'html.parser'))
            for tag in soup.select('.entry-header, .post-thumb, #secondary, script[type="application/ld+json"]'):
                tag.decompose()
            soup.title.string = title + ' | Nube para Pymes'
            for selector, value in [('meta[name="description"]', description), ('meta[property="og:description"]', description), ('meta[property="og:title"]', title + ' | Nube para Pymes'), ('meta[name="twitter:title"]', title + ' | Nube para Pymes'), ('meta[name="twitter:description"]', description)]:
                tag = soup.select_one(selector)
                if tag:
                    tag['content'] = value
            soup.head.append(BeautifulSoup('<link rel="stylesheet" href="/assets/brand-pages.css?v=20261011"/>', 'html.parser'))
            if kind == 'contact':
                soup.body.append(BeautifulSoup('<script src="/assets/contact.js?v=20261011-2" async></script>', 'html.parser'))
            schema = soup.new_tag('script', type='application/ld+json')
            schema.string = json.dumps({'@context': 'https://schema.org', '@type': 'AboutPage' if kind == 'about' else 'ContactPage', 'name': title, 'url': 'https://nubeparapymes.online/' + route + '/', 'inLanguage': lang, 'description': description}, ensure_ascii=False)
            soup.head.append(schema)
            target = dist / route / 'index.html'
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(soup), encoding='utf-8')
    (dist / 'assets').mkdir(exist_ok=True)
    for name in ['brand-pages.css', 'contact.js']:
        shutil.copy2(ROOT / 'assets' / name, dist / 'assets' / name)

