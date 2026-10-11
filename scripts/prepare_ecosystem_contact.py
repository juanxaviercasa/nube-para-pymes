"""Prepare the two companion sites using each site's existing shell and branding."""
from pathlib import Path
import json
import shutil
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
sites = json.loads((ROOT / 'cloudflare/sites.json').read_text(encoding='utf8'))

def prepare_mundos(target):
    config = sites['mundos-simulados']
    markup = BeautifulSoup((ROOT / 'content/brand/contact-es.html').read_text(encoding='utf8'), 'html.parser')
    markup.h1.string = 'Exploremos tu próxima pregunta.'
    markup.select_one('.npp-lead').string = 'Propón un escenario, comparte una corrección con sus fuentes o cuéntanos cómo quieres utilizar nuestras simulaciones.'
    for link in markup.select('a[href^="mailto:"]'):
        link['href'] = 'mailto:contacto@mundossimulados.online'
        link.string = 'contacto@mundossimulados.online'
    markup.form['data-contact-email'] = 'contacto@mundossimulados.online'
    topics = markup.select_one('.npp-topics')
    topics.clear()
    help_text = {
        'escenario':'Describe la pregunta, las condiciones iniciales y qué te gustaría explorar.',
        'correccion':'Incluye el enlace del artículo, el dato que debe revisarse y una fuente verificable.',
        'herramientas':'Indica la simulación, el dispositivo y los pasos que producen el problema.',
        'educacion':'Cuéntanos la edad del alumnado, el contexto y cómo quieres utilizar el contenido.',
        'colaboracion':'Describe tu propuesta, tu experiencia y el alcance de la colaboración.',
        'otra':'Cuéntanos el contexto de tu consulta y cómo podemos ayudarte.'}
    for value, label in config['categories'].items():
        fragment = BeautifulSoup('<label class="npp-topic"><input type="radio" name="category" required/><span><strong></strong><small></small></span></label>', 'html.parser')
        fragment.input['value'] = value
        fragment.input['data-help'] = help_text[value]
        fragment.strong.string = label
        fragment.small.string = help_text[value]
        topics.append(fragment)
    aside = markup.select_one('.npp-contact-aside')
    aside.clear()
    aside.append(BeautifulSoup('<section class="npp-card"><h2>Una conversación con contexto</h2><p>Respondemos al correo que indiques. Las propuestas y correcciones pasan por revisión editorial; enviar un mensaje no publica ni modifica contenido automáticamente.</p></section><section class="npp-card"><h2>Antes de enviar</h2><p>Consulta nuestros <a href="/escenarios/">escenarios</a> y acompaña las correcciones con fuentes. No envíes datos privados de estudiantes ni contraseñas.</p></section>', 'html.parser'))
    shell = BeautifulSoup((target / 'index.html').read_text(encoding='utf8'), 'html.parser')
    content = shell.select_one('.entry-content')
    content.clear(); content.append(markup)
    for node in shell.select('.entry-header, .post-thumb, #secondary, script[type="application/ld+json"]'):
        node.decompose()
    shell.body['class'] = ['npp-info-page']
    shell.title.string = 'Contacto | Mundos Simulados'
    for node in shell.select('meta[property="og:title"], meta[name="twitter:title"]'):
        node['content'] = 'Contacto | Mundos Simulados'
    for node in shell.select('link[rel="canonical"], meta[property="og:url"]'):
        node['href' if node.name == 'link' else 'content'] = 'https://mundossimulados.online/contacto/'
    for node in shell.select('[src], [href]'):
        for attr in ('src','href'):
            value = node.get(attr, '')
            if value.startswith('./'):
                node[attr] = '/' + value[2:]
    shell.head.append(BeautifulSoup('<link rel="stylesheet" href="/assets/contact-brand.css"/>', 'html.parser'))
    shell.body.append(BeautifulSoup('<script src="/assets/contact.js" defer></script>', 'html.parser'))
    (target / 'contacto').mkdir(exist_ok=True)
    (target / 'contacto/index.html').write_text(str(shell), encoding='utf8')
    (target / 'assets').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'assets/contact.js', target / 'assets/contact.js')
    css = (ROOT / 'assets/brand-pages.css').read_text(encoding='utf8')
    css += '''
.npp-info-page{background:var(--ms-bg-deep,#f3f6fa)!important}
.npp-info-page .npp-brand :is(h1,h2,h3,p,label,legend,span,strong,small){color:var(--ms-text-main,#13243b)!important}
.npp-info-page .npp-card,.npp-info-page .npp-contact-form,.npp-info-page .npp-topic{background:var(--ms-bg-card,#fff)!important;border-color:var(--ms-border,#cfdae6)!important}
.npp-info-page .npp-topic:has(input:checked){box-shadow:inset 0 0 0 2px var(--ms-cyan-neon,#075e6b)}
.npp-info-page .npp-brand a{color:var(--ms-cyan-neon,#075e6b)!important}
.npp-info-page .npp-contact-form :is(input,textarea){background:var(--ms-bg-card,#fff)!important;color:var(--ms-text-main,#13243b)!important}
.npp-info-page .npp-brand .npp-button{background:#075e6b!important;border-color:#075e6b!important;color:#fff!important}
'''
    (target / 'assets/contact-brand.css').write_text(css, encoding='utf8')
    (target / 'cloudflare').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'cloudflare/contact-worker.mjs',target / 'cloudflare/contact-worker.mjs')
    (target / 'cloudflare/contact-site.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf8')
    privacy_path = target / 'politica-de-privacidad/index.html'
    privacy = BeautifulSoup(privacy_path.read_text(encoding='utf8'), 'html.parser')
    if not privacy.select_one('#consultas-contacto'):
        privacy.select_one('.entry-content').append(BeautifulSoup('<section id="consultas-contacto"><h2>Consultas del formulario</h2><p>Recogemos tu nombre, correo, tipo de consulta y mensaje, y opcionalmente tu organización y un enlace. Cloudflare Workers procesa el envío y Turnstile verifica solicitudes utilizando datos técnicos como la dirección IP. La consulta se entrega al buzón de Mundos Simulados en Gmail para responderte; no se guarda en una base de datos del sitio ni te suscribe a publicidad. Puedes solicitar su eliminación escribiendo a contacto@mundossimulados.online.</p></section>', 'html.parser'))
        privacy_path.write_text(str(privacy),encoding='utf8')
    sitemap_path = target / 'sitemap.xml'
    sitemap = sitemap_path.read_text(encoding='utf8')
    if 'https://mundossimulados.online/contacto/' not in sitemap:
        sitemap_path.write_text(sitemap.replace('</urlset>', '<url><loc>https://mundossimulados.online/contacto/</loc></url>\n</urlset>'),encoding='utf8')
    import re
    for page in target.rglob('index.html'):
        if any(part.startswith('.') for part in page.relative_to(target).parts):
            continue
        text = page.read_text(encoding='utf8')
        if '/contacto/"' not in text and 'mailto:contacto@mundossimulados.online' in text:
            text = re.sub(r'(<a\b[^>]*href="mailto:contacto@mundossimulados.online")', '<a href="/contacto/">Formulario de contacto</a> · \\1',text,count=1)
            page.write_text(text,encoding='utf8')

def prepare_todo(target):
    import re
    config = sites['todo-lima']
    file = target / 'components/ContactForm.js'
    source = file.read_text(encoding='utf8')
    source = source.replace("import {useState} from 'react';", "import {useEffect} from 'react';")
    start = source.index("  const [status")
    end = source.index('  const inputClass')
    source = source[:start] + '''  useEffect(() => {
    const script = document.createElement('script');
    script.src = '/contact.js?v=20261011';
    document.body.append(script);
    return () => script.remove();
  }, []);
''' + source[end:]
    start = source.index('  async function submit(')
    end = source.index('  return <section', start)
    source = source[:start] + source[end:]
    source = source.replace('<form onSubmit={submit}', '<form id="npp-contact-form" action="/api/contact" method="post" data-language="es" data-contact-email="contacto@todolima.com"')
    source = source.replace('name="topic"', 'name="category"')
    source = source.replace('<textarea name="message"', '<textarea id="contact-message" aria-describedby="contact-message-help" name="message"')
    source = source.replace('name="pageUrl"', 'name="reference"')
    source = source.replace('<span className="block text-xs text-slate-500">Entre', '<span id="contact-message-help" className="block text-xs text-slate-500">Entre')
    source = source.replace('<button type="submit" disabled={status === \'sending\'}', '<div id="npp-turnstile"/><button id="npp-submit-btn" type="submit" disabled')
    source = source.replace("{status === 'sending' ? 'Enviando…' : 'Enviar consulta'}", 'Enviar consulta')
    source = re.sub(r'<p role=\{status[\s\S]*?\{notice\}</p>', '<p id="npp-form-msg" role="status" aria-live="polite" tabIndex={-1} className="text-sm break-words">Preparando el envío…</p><noscript>Escríbenos a contacto@todolima.com.</noscript>',source)
    file.write_text(source,encoding='utf8')
    shutil.copy2(ROOT / 'assets/contact.js', target / 'public/contact.js')
    (target / 'cloudflare').mkdir(exist_ok=True)
    shutil.copy2(ROOT / 'cloudflare/contact-worker.mjs',target / 'cloudflare/contact-worker.mjs')
    (target / 'cloudflare/contact-site.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf8')
    # The Worker route replaces the old token-based Pages endpoint.
    (target / 'functions/api/contacto.js').write_text("export function onRequest(){return Response.json({error:'Usa /api/contact.'},{status:410,headers:{'Cache-Control':'no-store'}});}\n",encoding='utf8')

if __name__ == '__main__':
    import sys
    (prepare_todo if len(sys.argv) > 2 and sys.argv[2] == 'todo' else prepare_mundos)(Path(sys.argv[1]))
