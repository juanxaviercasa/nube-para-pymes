"""Contextual links with separate business-listing and digital-service journeys."""
import html
import re
from urllib.parse import urlencode
from pathlib import Path
from site_routes import route_pairs

LISTING_ARTICLES = {
    'punto-de-venta-restaurantes', 'software-reservas-clinicas',
    'gestion-despachos-abogados', 'crm-para-inmobiliarias',
    'software-gimnasios-estudios', 'facturar-independiente-peru',
    'herramientas-profesores-particulares', 'geo-para-pymes-respuestas-inteligencia-artificial',
}
DIGITAL_ARTICLES = {
    'crm-integrado-whatsapp-business', 'crm-con-whatsapp-integrado',
    'seo-geo-para-pymes-visibilidad-ia', 'digitalizar-procesos-negocio-pequeno',
    'automatizacion-ia-pymes-criterios-decision', 'crm-con-ia-para-pymes-que-automatizar',
}
SCENARIOS = {
    'automatizacion-ia-pymes-criterios-decision': ('robots-con-derechos-laborales', 'Robots y derechos laborales', 'Robots and labour rights'),
    'crm-con-ia-para-pymes-que-automatizar': ('resurreccion-digital-avatares', 'Avatares digitales y sus límites', 'Digital avatars and their limits'),
    'digitalizar-procesos-negocio-pequeno': ('realidad-virtual-indistinguible', 'Los límites de una realidad virtual indistinguible', 'The limits of indistinguishable virtual reality'),
}

def tagged_url(host, path, content):
    return f'https://{host}{path}?' + urlencode({'utm_source': 'nubeparapymes', 'utm_medium': 'referral', 'utm_campaign': 'ecosistema', 'utm_content': content})

def card(slug, digital, english=False):
    path = '/auditoria' if digital else '/para-negocios'
    title = ('Apply this to your business in Lima' if english else 'Lleva este paso a tu negocio en Lima')
    if digital:
        desc = ('Discuss your website, enquiry handling or automation needs with Todo Lima. Define the scope and a quote before choosing a solution.' if english else 'Consulta con Todo Lima sobre tu sitio web, la organización de consultas o la automatización de atención. Define el alcance y solicita un presupuesto antes de elegir una solución.')
        label = 'Discuss a digital review' if english else 'Consultar una revisión digital'
    else:
        desc = ('If you own or represent a business in Lima, ask Todo Lima to review or publish its listing so visitors can find its services and contact details.' if english else 'Si eres titular o representante de un negocio en Lima, solicita a Todo Lima la revisión o publicación de su ficha para presentar servicios, ubicación y formas de contacto.')
        label = 'Request a business listing review' if english else 'Solicitar revisión de mi ficha'
    url = html.escape(tagged_url('todolima.com', path, slug), quote=True)
    secondary = ''
    if slug in SCENARIOS:
        scenario, es_label, en_label = SCENARIOS[slug]
        scenario_url = html.escape(tagged_url('mundossimulados.online', f'/{scenario}/', slug), quote=True)
        lead = 'Related scenario in Mundos Simulados' if english else 'Escenario complementario en Mundos Simulados'
        secondary = f'<p class="npp-ecosystem-reading">{lead}: <a href="{scenario_url}" data-ecosystem-destination="mundossimulados">{en_label if english else es_label}</a>. {"A thought experiment, not a prediction." if english else "Un ejercicio de reflexión, no una predicción."}</p>'
    return f'''<!-- [ECOSYSTEM_BRIDGE_START] -->
<aside class="npp-ecosystem-bridge" aria-label="{title}" style="margin:2rem 0;padding:1.4rem;border:1px solid #cbd5e1;border-left:4px solid #0284c7;border-radius:12px;background:#f8fafc;color:#0f172a">
<h2 style="font-size:1.2rem">{title}</h2><p>{desc}</p>
<a href="{url}" data-ecosystem-destination="todolima" style="display:inline-block;padding:.65rem 1rem;background:#0369a1;color:white;border-radius:8px;text-decoration:none">{label} →</a>{secondary}
</aside><!-- [ECOSYSTEM_BRIDGE_END] -->'''

def integrate_ecosystem(dist: Path):
    pairs = route_pairs(dist)
    count = 0
    for slug in sorted(LISTING_ARTICLES | DIGITAL_ARTICLES):
        es_route = f'/{slug}/'
        for route, english in [(es_route, False), (pairs.get(es_route), True)]:
            if not route:
                continue
            file = dist / route.strip('/') / 'index.html'
            if not file.exists():
                continue
            text = file.read_text(encoding='utf-8')
            text = re.sub(r'<!-- \[(?:TODOLIMA_BRIDGE|ECOSYSTEM_BRIDGE)_START\] -->[\s\S]*?<!-- \[(?:TODOLIMA_BRIDGE|ECOSYSTEM_BRIDGE)_END\] -->\s*', '', text)
            marker = '</div><!-- .entry-content .clear -->'
            anchor = marker if marker in text else '</article>'
            if anchor not in text:
                raise ValueError(f'No article anchor for {route}')
            text = text.replace(anchor, card(slug, slug in DIGITAL_ARTICLES, english) + '\n' + anchor, 1)
            file.write_text(text, encoding='utf-8')
            count += 1
    # Existing tool banners promised a listing but linked to the home page.
    for file in dist.rglob('*.html'):
        text = file.read_text(encoding='utf-8')
        def banner(match):
            return match[0].replace('Publica tu ficha comercial gratis y capta clientes directos en los 43 distritos de la capital.', 'Solicita la revisión de tu ficha y presenta ubicación, servicios y formas de contacto. La inclusión no garantiza consultas ni ventas.').replace('Publicar mi Negocio en Todo Lima →', 'Solicitar revisión de mi ficha →').replace('href="https://todolima.com"', 'href="' + html.escape(tagged_url('todolima.com', '/para-negocios', 'herramienta-' + file.parent.name), quote=True) + '"')
        updated = re.sub(r'<!-- \[TODOLIMA_PARTNER_BANNER_START\] -->[\s\S]*?<!-- \[TODOLIMA_PARTNER_BANNER_END\] -->', banner, text)
        if updated != text:
            file.write_text(updated, encoding='utf-8')
    print(f'[ECOSYSTEM] {count} contextual business bridges; canonical business-listing banner targets.')

if __name__ == '__main__':
    integrate_ecosystem(Path(__file__).resolve().parents[1] / 'dist')
