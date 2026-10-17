"""Shared, bilingual tool chrome. Kept outside React's application root."""
import html
import re
from urllib.parse import urlencode
from site_routes import ROOT, TOOLS_MAP

VERSION = '20261017-3'


def enhance(text, tool, english=False, prefix='/herramientas/'):
    text = re.sub(r'<script\b[^>]*data-npp-regional(?:-ui)?[^>]*></script>\s*', '', text)
    regional = (f'<script src="{prefix}js/regional-settings.js?v={VERSION}" data-npp-regional></script>\n'
                f'<script defer src="{prefix}js/regional-ui.js?v={VERSION}" data-npp-regional-ui></script>\n')
    text = re.sub(r'(<head\b[^>]*>)\s*', lambda m: m[1] + '\n' + regional, text, count=1)
    text = re.sub(r'demo-experience\.js\?v=[^"\x27]+', f'demo-experience.js?v={VERSION}', text)
    text = re.sub(r'<script\b[^>]*data-npp-site-theme[^>]*></script>\s*', '', text)
    text = re.sub(r'(<head\b[^>]*>)\s*', lambda m: m[1] + f'\n<script src="{prefix}js/site-theme.js?v={VERSION}" data-npp-site-theme></script>\n', text, count=1)
    text = re.sub(r'<!-- \[TODOLIMA_PARTNER_BANNER_START\] -->[\s\S]*?<!-- \[TODOLIMA_PARTNER_BANNER_END\] -->\s*', '', text)
    text = re.sub(r'<!-- NPP_TOOL_(?:NAV|BRIDGE)_START -->[\s\S]*?<!-- NPP_TOOL_(?:NAV|BRIDGE)_END -->\s*', '', text)
    text = re.sub(r'<(?:link|script)\b[^>]*data-npp-tool-experience[^>]*>(?:</script>)?\s*', '', text)
    assets = (f'<link rel="stylesheet" href="{prefix}css/tool-experience.css?v={VERSION}" data-npp-tool-experience>\n'
              f'<script defer src="{prefix}js/tool-experience.js?v={VERSION}" data-npp-tool-experience></script>\n')
    text = text.replace('</head>', assets + '</head>', 1)
    query = urlencode(dict(utm_source='nubeparapymes', utm_medium='referral', utm_campaign='ecosistema', utm_content='herramienta-' + tool['slug']))
    url = html.escape('https://todolima.com/para-negocios?' + query, quote=True)
    portal = '/en/tools/' if english else '/herramientas/'
    home = '/en/' if english else '/'
    nav = f'''<!-- NPP_TOOL_NAV_START -->
<nav class="npp-tool-nav" aria-label="{'Site navigation' if english else 'Navegación del sitio'}">
<div class="npp-tool-nav-inner"><a class="npp-tool-back" href="{portal}"><span aria-hidden="true">←</span> {'Tools' if english else 'Herramientas'}</a>
<div class="npp-tool-nav-links"><a href="{home}">{'Home' if english else 'Inicio'}</a><button type="button" data-npp-theme-toggle aria-pressed="false">{'Dark' if english else 'Oscuro'}</button><a class="npp-tool-business" href="{url}">{'Your business in TodoLima' if english else 'Tu negocio en TodoLima'} <span aria-hidden="true">↗</span></a></div></div>
</nav><!-- NPP_TOOL_NAV_END -->\n'''
    text = re.sub(r'(<body\b[^>]*>)\s*', lambda m: m[1] + '\n' + nav, text, count=1)
    title = 'Make your business easier to find in Lima' if english else 'Haz que tu negocio sea más fácil de encontrar en Lima'
    desc = ('Present your services, location and contact details in TodoLima. Request a review or publication of your business listing.' if english else 'Presenta tus servicios, ubicación y formas de contacto en TodoLima. Solicita la revisión o publicación de tu ficha comercial.')
    label = 'Request a review in TodoLima' if english else 'Solicitar revisión en TodoLima'
    bridge = f'''<!-- NPP_TOOL_BRIDGE_START -->
<aside class="npp-tool-bridge" aria-labelledby="npp-business-title">
<div class="npp-tool-bridge-copy"><span class="npp-tool-eyebrow">{'Next step for your business' if english else 'El siguiente paso para tu negocio'} · TodoLima.com</span>
<h2 id="npp-business-title">{title}</h2><p>{desc}</p></div>
<a class="npp-tool-bridge-action" href="{url}" data-ecosystem-destination="todolima">{label} <span aria-hidden="true">→</span></a>
</aside><!-- NPP_TOOL_BRIDGE_END -->\n'''
    footer = re.search(r'<footer\b[^>]*class="[^"]*\bnp-global-footer\b[^\"]*"[^>]*>', text)
    if not footer:
        raise ValueError(f"Missing global footer for {tool['slug']}")
    text = text[:footer.start()] + bridge + text[footer.start():]
    return text


def update_sources():
    for file in (ROOT / 'index.html', ROOT / 'en/index.html'):
        text = file.read_text(encoding='utf-8')
        text = re.sub(r'<script\b[^>]*data-npp-regional(?:-ui)?[^>]*></script>\s*', '', text)
        text = re.sub(r'(<head\b[^>]*>)\s*', lambda m: m[1] + f'\n<script src="/js/regional-settings.js?v={VERSION}" data-npp-regional></script>\n<script defer src="/js/regional-ui.js?v={VERSION}" data-npp-regional-ui></script>\n', text, count=1)
        text = re.sub(r'<script\b[^>]*data-npp-site-theme[^>]*></script>\s*', '', text)
        text = re.sub(r'(<head\b[^>]*>)\s*', lambda m: m[1] + f'\n<script src="/js/site-theme.js?v={VERSION}" data-npp-site-theme></script>\n', text, count=1)
        file.write_text(text, encoding='utf-8')
    for tool in TOOLS_MAP.values():
        for file, english, prefix in [(ROOT / tool['src'], False, './'), (ROOT / 'en' / (tool['en_slug'] + '.html'), True, '../')]:
            text = file.read_text(encoding='utf-8')
            file.write_text(enhance(text, tool, english, prefix), encoding='utf-8')


if __name__ == '__main__':
    update_sources()
