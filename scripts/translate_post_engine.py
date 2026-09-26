import os
import sys
import re
import json
import time
import copy
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup, NavigableString, Comment

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(ROOT_DIR, 'scripts', 'translation_cache.json')
SLUG_MAP_FILE = os.path.join(ROOT_DIR, 'scripts', 'posts_slug_map.json')

_cache = {}
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            _cache = json.load(f)
    except Exception:
        _cache = {}

with open(SLUG_MAP_FILE, 'r', encoding='utf-8') as f:
    SLUG_MAP = json.load(f)

# Reverse map
REV_SLUG_MAP = {v: k for k, v in SLUG_MAP.items()}

# Tool mapping (Spanish filename / slug to English filename)
TOOL_MAP = {
    'analizador-titulares.html': 'headline-analyzer.html',
    'auditor-seo-basico.html': 'basic-on-page-seo-auditor.html',
    'calculadora-descuentos-promociones.html': 'discount-promotion-calculator.html',
    'calculadora-flete-envio-local.html': 'local-shipping-rate-calculator.html',
    'calculadora-precios-venta-igv.html': 'pricing-calculator.html',
    'calculadora-prestamos-amortizaciones.html': 'loan-amortization-calculator.html',
    'calculadora-sobrecostos-laborales.html': 'payroll-cost-calculator.html',
    'comparador-campanas-avanzado.html': 'advanced-campaign-comparator.html',
    'consola-campanas.html': 'campaign-utm-console.html',
    'conversor-optimizador-imagenes.html': 'image-webp-optimizer.html',
    'creador-facturas-proforma.html': 'proforma-invoice-maker.html',
    'crm-pymes.html': 'sales-crm-pipeline.html',
    'firma-correo-html.html': 'html-email-signature-generator.html',
    'flujo-caja-pymes.html': 'cash-flow-simulator.html',
    'generador-codigos-qr.html': 'qr-code-whatsapp-generator.html',
    'generador-contrasenas-pymes.html': 'secure-password-generator.html',
    'generador-contratos-servicios.html': 'service-contract-generator.html',
    'generador-cotizaciones.html': 'quote-generator.html',
    'generador-paletas-corporativas.html': 'brand-palette-generator.html',
    'generador-politicas-devolucion.html': 'refund-return-policy-generator.html',
    'generador-politicas-terminos.html': 'terms-privacy-policy-generator.html',
    'guia-uso-22-apps.html': 'user-guide.html',
    'guiones-manejo-objeciones.html': 'sales-objection-scripts.html',
    'inventario-compras-pymes.html': 'inventory-purchasing-manager.html',
    'organizador-matriz-contenidos.html': 'content-matrix-planner.html',
    'simulador-tco-fisico-nube.html': 'cloud-vs-onprem-tco-calculator.html',
    'tareas-proyectos-pymes.html': 'team-task-project-tracker.html'
}

def save_cache():
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(_cache, f, ensure_ascii=False)

def translate_api(text, src='es', dest='en'):
    text_clean = text.strip()
    if not text_clean or len(text_clean) <= 1 or text_clean.isnumeric():
        return text
    
    cache_key = f"{src}->{dest}:{text_clean}"
    if cache_key in _cache:
        translated = _cache[cache_key]
        leading_space = text[:len(text) - len(text.lstrip())]
        trailing_space = text[len(text.rstrip()):]
        return leading_space + translated + trailing_space

    # If text is too long, split by double newlines or chunks
    if len(text_clean) > 1800:
        parts = text_clean.split("\n\n")
        translated_parts = [translate_api(p, src, dest) for p in parts]
        res = "\n\n".join(translated_parts)
        _cache[cache_key] = res
        return res

    url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q=" + urllib.parse.quote(text_clean)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                translated = "".join([segment[0] for segment in data[0] if segment[0]])
                _cache[cache_key] = translated
                leading_space = text[:len(text) - len(text.lstrip())]
                trailing_space = text[len(text.rstrip()):]
                return leading_space + translated + trailing_space
        except Exception as e:
            time.sleep(1 + attempt * 2)
            
    return text

def translate_element_content(tag, soup):
    """Recursively translates an HTML element while preserving inline tags."""
    if not tag.find_all(True):
        txt = tag.string
        if txt and txt.strip():
            tag.string.replace_with(translate_api(str(txt)))
        return

    inline_tags = {'a', 'strong', 'b', 'em', 'i', 'code', 'span', 'small', 'mark', 'kbd'}
    children = list(tag.children)
    
    # If it contains block children (e.g., div inside div, li inside ul, table inside div), don't collapse
    has_block_children = any(getattr(c, 'name', None) not in inline_tags and getattr(c, 'name', None) is not None for c in children)
    if has_block_children:
        for child in children:
            if hasattr(child, 'find_all'):
                translate_element_content(child, soup)
        return

    # Translate inline children
    tokens = {}
    counter = 0
    tokenized_str = ""
    for child in children:
        if isinstance(child, str):
            tokenized_str += str(child)
        elif getattr(child, 'name', None) in inline_tags:
            token = f"[[T{counter}]]"
            translate_element_content(child, soup)
            tokens[token] = str(child)
            tokenized_str += token
            counter += 1
        else:
            tokenized_str += str(child)
            
    translated_str = translate_api(tokenized_str)
    
    for token, child_html in tokens.items():
        pattern = re.escape(token).replace(r'\[\[', r'\[\s*\[').replace(r'\]\]', r'\]\s*\]')
        translated_str = re.sub(pattern, child_html, translated_str)
        
    try:
        new_soup = BeautifulSoup(f"<div>{translated_str}</div>", 'html.parser')
        tag.clear()
        for item in list(new_soup.div.contents):
            tag.append(item)
    except Exception:
        pass

def adapt_post_links(soup, spanish_slug, english_slug):
    """Updates internal links, tool links, and post links."""
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        # Tools linking
        for sp_tool, en_tool in TOOL_MAP.items():
            if sp_tool in href or f"/{sp_tool[:-5]}" in href:
                a['href'] = f"/en/{en_tool}"
                break
                
        # Other blog posts linking
        for sp_s, en_s in SLUG_MAP.items():
            if f"/{sp_s}/" in href or href.endswith(f"/{sp_s}"):
                a['href'] = f"/en/{en_s}/"
                break
                
        # Home / Herramientas root links
        if href in ['/', '/index.html', 'https://nubeparapymes.online/']:
            a['href'] = '/en/'
        elif href in ['/herramientas/', '/herramientas/index.html']:
            a['href'] = '/en/'

def translate_post(spanish_slug, english_slug):
    src_file = os.path.join(ROOT_DIR, 'dist', spanish_slug, 'index.html')
    if not os.path.exists(src_file):
        src_file = os.path.join(ROOT_DIR, 'nubepymesexport', spanish_slug, 'index.html')
    if not os.path.exists(src_file):
        print(f"[ERROR] Source post not found: {spanish_slug}")
        return False
        
    with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()
        
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Update <html lang="en">
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'en'
        
    # 2. Translate Title
    if soup.title and soup.title.string:
        clean_t = soup.title.string.strip()
        # Remove Spanish brand suffixes if any
        clean_t = re.sub(r'\s*[-–—|]\s*Nube para Pymes.*$', '', clean_t, flags=re.IGNORECASE)
        trans_t = translate_api(clean_t)
        soup.title.string = f"{trans_t} — Nube para Pymes"
        
    # 3. Meta description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        meta_desc['content'] = translate_api(meta_desc['content'])
        
    # 4. OpenGraph tags
    og_locale = soup.find('meta', property='og:locale')
    if og_locale:
        og_locale['content'] = 'en_US'
        
    og_title = soup.find('meta', property='og:title')
    if og_title and og_title.get('content'):
        og_title['content'] = translate_api(og_title['content'])
        
    og_desc = soup.find('meta', property='og:description')
    if og_desc and og_desc.get('content'):
        og_desc['content'] = translate_api(og_desc['content'])
        
    og_url = soup.find('meta', property='og:url')
    if og_url:
        og_url['content'] = f"https://nubeparapymes.online/en/{english_slug}/"
        
    tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if tw_title and tw_title.get('content'):
        tw_title['content'] = translate_api(tw_title['content'])
        
    tw_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if tw_desc and tw_desc.get('content'):
        tw_desc['content'] = translate_api(tw_desc['content'])
        
    # 5. Canonical & Hreflang
    canonical = soup.find('link', rel='canonical')
    if canonical:
        canonical['href'] = f"https://nubeparapymes.online/en/{english_slug}/"
        
    # Add hreflangs if not present
    for existing_alt in soup.find_all('link', rel='alternate', hreflang=True):
        existing_alt.decompose()
        
    head = soup.find('head')
    if head:
        alt_es = soup.new_tag('link', rel='alternate', hreflang='es', href=f"https://nubeparapymes.online/{spanish_slug}/")
        alt_en = soup.new_tag('link', rel='alternate', hreflang='en', href=f"https://nubeparapymes.online/en/{english_slug}/")
        alt_def = soup.new_tag('link', rel='alternate', hreflang='x-default', href=f"https://nubeparapymes.online/{spanish_slug}/")
        head.append(alt_es)
        head.append(alt_en)
        head.append(alt_def)
        
    # 6. JSON-LD Schema
    for script in soup.find_all('script', type='application/ld+json'):
        if script.string:
            try:
                schema = json.loads(script.string)
                
                def update_schema_node(node):
                    if isinstance(node, dict):
                        if 'inLanguage' in node and node['inLanguage'] == 'es':
                            node['inLanguage'] = 'en'
                        if '@type' in node and node['@type'] in ['BlogPosting', 'Article', 'NewsArticle']:
                            if 'headline' in node and isinstance(node['headline'], str):
                                node['headline'] = translate_api(node['headline'])
                            if 'description' in node and isinstance(node['description'], str):
                                node['description'] = translate_api(node['description'])
                            if 'keywords' in node and isinstance(node['keywords'], str):
                                node['keywords'] = translate_api(node['keywords'])
                        if 'name' in node and isinstance(node['name'], str) and node.get('@type') != 'Organization':
                            node['name'] = translate_api(node['name'])
                        if 'url' in node and isinstance(node['url'], str):
                            node['url'] = node['url'].replace(f"/{spanish_slug}/", f"/en/{english_slug}/")
                        if '@id' in node and isinstance(node['@id'], str):
                            node['@id'] = node['@id'].replace(f"/{spanish_slug}/", f"/en/{english_slug}/")
                        for k, v in node.items():
                            update_schema_node(v)
                    elif isinstance(node, list):
                        for item in node:
                            update_schema_node(item)
                            
                update_schema_node(schema)
                script.string = json.dumps(schema, ensure_ascii=False)
            except Exception:
                pass
                
    # 7. Navigation Bar
    header = soup.find('header')
    if header:
        for nav_item in header.find_all(['a', 'span', 'button']):
            txt = nav_item.text.strip()
            if txt in ['Inicio', 'Home']:
                nav_item.string = 'Home'
                if nav_item.name == 'a':
                    nav_item['href'] = '/en/'
            elif txt in ['Herramientas', 'Tools', 'Portal']:
                nav_item.string = 'Tools'
                if nav_item.name == 'a':
                    nav_item['href'] = '/en/'
            elif txt in ['Blog']:
                nav_item.string = 'Blog'
            elif txt in ['Contacto', 'Contact']:
                nav_item.string = 'Contact'
                
        # Update search placeholder
        search_input = header.find('input', type='search')
        if search_input:
            search_input['placeholder'] = 'Search...'
            search_input['aria-label'] = 'Search'

    # 8. Article content translation
    article = soup.find('article')
    if article:
        # H1
        h1 = article.find('h1')
        if h1:
            translate_element_content(h1, soup)
            
        # Meta info (author, date, read time)
        for meta_elem in article.find_all('span', class_=re.compile(r'author|date|comments|category')):
            translate_element_content(meta_elem, soup)
            
        # Entry content
        entry_content = article.find('div', class_='entry-content')
        if entry_content:
            # Blocks to translate
            content_tags = entry_content.find_all(['h2', 'h3', 'h4', 'h5', 'p', 'li', 'th', 'td', 'blockquote', 'figcaption'])
            for tag in content_tags:
                translate_element_content(tag, soup)
                
    # 9. Adapt internal links
    adapt_post_links(soup, spanish_slug, english_slug)
    
    # 10. Add Floating Language Switcher
    lang_switcher_html = f"""
    <aside class="np-lang-switch-floating" style="position:fixed;bottom:24px;right:24px;z-index:99999;background:rgba(15,23,42,0.92);backdrop-filter:blur(8px);color:#ffffff;border:1px solid #334155;border-radius:9999px;padding:8px 16px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.3);font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;display:flex;align-items:center;gap:10px;">
      <a href="/{spanish_slug}/" style="color:#94a3b8;text-decoration:none;font-weight:600;transition:color 0.2s;" title="Cambiar a español">ES</a>
      <span style="color:#475569;font-weight:300;">|</span>
      <span style="color:#2dd4bf;font-weight:700;">EN</span>
    </aside>
    """
    body = soup.find('body')
    if body:
        switcher_soup = BeautifulSoup(lang_switcher_html, 'html.parser')
        body.append(switcher_soup)
        
    # 11. Normalize Footer
    footer = soup.find('footer')
    if footer:
        for p in footer.find_all(['p', 'span']):
            txt = p.text.strip()
            if 'Todos los derechos reservados' in txt:
                p.string = p.text.replace('Todos los derechos reservados', 'All rights reserved').replace('Diseñado y Desarrollado por', 'Designed and Developed by')
                
    # 12. Save Translated Post in root `en/<english_slug>/index.html` AND `dist/en/<english_slug>/index.html`
    out_dirs = [
        os.path.join(ROOT_DIR, 'en', english_slug),
        os.path.join(ROOT_DIR, 'dist', 'en', english_slug)
    ]
    for out_d in out_dirs:
        os.makedirs(out_d, exist_ok=True)
        out_file = os.path.join(out_d, 'index.html')
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
            
    # 13. Create redirect stub in `en/<spanish_slug>/index.html`
    redirect_dirs = [
        os.path.join(ROOT_DIR, 'en', spanish_slug),
        os.path.join(ROOT_DIR, 'dist', 'en', spanish_slug)
    ]
    stub_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="refresh" content="0; url=/en/{english_slug}/">
  <link rel="canonical" href="https://nubeparapymes.online/en/{english_slug}/">
  <title>Redirecting to {english_slug} — Nube para Pymes</title>
  <script>window.location.replace("/en/{english_slug}/");</script>
</head>
<body>
  <p>Redirecting to <a href="/en/{english_slug}/">{english_slug}</a>...</p>
</body>
</html>
"""
    for r_d in redirect_dirs:
        os.makedirs(r_d, exist_ok=True)
        with open(os.path.join(r_d, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(stub_content)
            
    save_cache()
    print(f"[OK] Translated {spanish_slug} -> en/{english_slug}/")
    return True

if __name__ == '__main__':
    # Test on one post
    translate_post('alternativas-gratuitas-asana', 'free-asana-alternatives')
