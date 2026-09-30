"""Single source of truth for published Spanish/English page pairs."""
import json
from pathlib import Path
from urllib.parse import urlsplit
from fix_multilingual_issues import TOOLS_MAP

ROOT = Path(__file__).resolve().parents[1]
INFORMATION_PAGES = {
    'politica-de-privacidad': ('privacy-policy', 'Privacy Policy'),
    'sobre-nosotros': ('about-us', 'About Us'),
    'metodologia-de-resenas': ('review-methodology', 'Review Methodology'),
    'contacto': ('contact', 'Contact'),
    'terminos-y-condiciones': ('terms-and-conditions', 'Terms and Conditions'),
    'politica-de-cookies': ('cookie-policy', 'Cookie Policy'),
    'descargo-de-responsabilidad': ('disclaimer', 'Disclaimer'),
    'aviso-legal': ('legal-notice', 'Legal Notice'),
}

def route_for(file, root):
    value = '/' + file.relative_to(root).as_posix()
    return value[:-10] if value.endswith('index.html') else value

def route_pairs(dist):
    existing = {route_for(file, dist) for file in dist.rglob('index.html')}
    pairs = {'/': '/en/', '/herramientas/': '/en/tools/',
             '/herramientas/guia-uso/': '/en/user-guide/'}
    for es, (en, _) in INFORMATION_PAGES.items():
        pairs[f'/{es}/'] = f'/en/{en}/'
    posts = json.loads((ROOT / 'scripts/posts_slug_map.json').read_text(encoding='utf-8'))
    pairs.update({f'/{es}/': f'/en/{en}/' for es, en in posts.items()})
    for tool in TOOLS_MAP.values():
        pairs[f'/herramientas/{tool["cat"]}/{tool["slug"]}/'] = f'/en/{tool["en_slug"]}/'
    # Preserve the complete pagination path, not just the final directory name.
    for route in sorted(existing):
        if route.startswith(('/en/blog/', '/en/category/', '/en/author/', '/en/tag/')) or route[4:8].isdigit():
            es = route[3:]
            if es in existing:
                pairs[es] = route
    return pairs

def aliases(pairs):
    result = {'/directorio-herramientas/': '/herramientas/',
              '/herramientas-gratis/': '/herramientas/',
              '/en/herramientas/': '/en/tools/',
              '/en/tools/en/index.html': '/en/tools/',
              '/en/tools/en/': '/en/tools/',
              '/herramientas/en/index.html': '/en/tools/',
              '/herramientas/en/': '/en/tools/',
              '/en/guia-uso/': '/en/user-guide/',
              '/en/user-guide.html': '/en/user-guide/',
              '/guia-uso/': '/herramientas/guia-uso/',
              '/guia-uso-22-apps.html': '/herramientas/guia-uso/'}
    result.update({
        '/author/': '/author/xaviercabello/',
        '/crm/': '/category/crm/',
        '/software-segun-numero-empleados/': '/elegir-software-segun-numero-empleados/',
        '/herramientas/guia-uso/en/user-guide.html': '/en/user-guide/',
        '/herramientas/guia-uso/GUIA_DESPLIEGUE_HOSTING.md': '/herramientas/guia-uso/',
        '/en/cash-flow-simulator.html': '/en/cash-flow-tracker/',
        '/en/cloud-vs-onprem-tco-calculator.html': '/en/cloud-vs-onprem-tco-simulator/',
        '/en/inventory-purchasing-manager.html': '/en/inventory-purchasing/',
        '/en/payroll-cost-calculator.html': '/en/labor-cost-payroll-burden-calculator/',
        '/en/proforma-invoice-maker.html': '/en/proforma-invoice-generator/',
        '/en/sales-crm-pipeline.html': '/en/smb-crm/',
        '/en/sales-objection-scripts.html': '/en/objection-handling-scripts/',
        '/en/service-contract-generator.html': '/en/service-contracts-generator/',
        '/en/team-task-project-tracker.html': '/en/tasks-projects-tracker/',
        '/en/guia-uso-22-apps.html': '/en/user-guide/',
        '/herramientas/auditor-basico-de-seo-on-page/': '/herramientas/marketing/auditor-seo-basico/',
        '/herramientas/calculadora-de-precios-de-venta-con-igv/': '/herramientas/finanzas/calculadora-precios-venta-igv/',
        '/software-por-sector/': '/category/software-por-sector/',
    })
    for es, en in pairs.items():
        if es not in ('/', '/herramientas/') and not es.startswith(('/category/', '/blog/', '/herramientas/')):
            result['/en' + es] = en
    for tool in TOOLS_MAP.values():
        es = f'/herramientas/{tool["cat"]}/{tool["slug"]}/'
        en = f'/en/{tool["en_slug"]}/'
        for prefix in ('/', '/herramientas/'):
            result[prefix + tool['src']] = es
            result[prefix + tool['slug'] + '/'] = es
        for prefix in ('/en/', '/en/tools/'):
            result[prefix + tool['src']] = en
            result[prefix + tool['en_src']] = en
            result[prefix + tool['slug'] + '/'] = en
            result[prefix + tool['en_slug'] + '/'] = en
        result['/en' + es] = en
    return {k: v for k, v in result.items() if k != v}

def canonical_path(path, alias_map):
    if path in alias_map:
        return alias_map[path]
    if path.endswith('/index.html'):
        path = path[:-10]
    if not Path(path).suffix and not path.endswith('/'):
        path += '/'
    return alias_map.get(path, path)
