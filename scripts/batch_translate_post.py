import os
import sys
import re
import json
import time
import copy
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup, NavigableString

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

CATEGORY_TRANSLATIONS = {
    'Automatización y productividad con IA': 'Automation & AI Productivity',
    'Comunicación y colaboración': 'Communication & Collaboration',
    'CRM y gestión de clientes': 'CRM & Customer Management',
    'Facturación y contabilidad': 'Invoicing & Accounting',
    'Gestión de proyectos y tareas': 'Project & Task Management',
    'Software por sector específico': 'Industry-Specific Software',
    'Categorías': 'Categories',
    'Sobre Nosotros': 'About Us',
    'Herramientas Gratis': 'Free Tools',
    'Herramientas': 'Tools',
    'Entradas relacionadas': 'Related Articles',
    'Anterior': 'Previous',
    'Siguiente': 'Next'
}

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

def translate_batch(texts, src='es', dest='en'):
    results = [None] * len(texts)
    to_query_indices = []
    to_query_texts = []
    
    for i, t in enumerate(texts):
        t_clean = t.strip()
        if not t_clean or len(t_clean) <= 1 or t_clean.isnumeric():
            results[i] = t
            continue
        key = f"{src}->{dest}:{t_clean}"
        if key in _cache:
            leading = t[:len(t) - len(t.lstrip())]
            trailing = t[len(t.rstrip()):]
            results[i] = leading + _cache[key] + trailing
        elif t_clean in CATEGORY_TRANSLATIONS:
            trans = CATEGORY_TRANSLATIONS[t_clean]
            _cache[key] = trans
            leading = t[:len(t) - len(t.lstrip())]
            trailing = t[len(t.rstrip()):]
            results[i] = leading + trans + trailing
        else:
            to_query_indices.append(i)
            to_query_texts.append(t_clean)
            
    if not to_query_texts:
        return results
        
    chunks = []
    current_chunk = []
    current_len = 0
    
    for idx, text in zip(to_query_indices, to_query_texts):
        if current_len + len(text) + 20 > 2200 and current_chunk:
            chunks.append(current_chunk)
            current_chunk = [(idx, text)]
            current_len = len(text)
        else:
            current_chunk.append((idx, text))
            current_len += len(text) + 20
    if current_chunk:
        chunks.append(current_chunk)
        
    delimiter = "\n\n[[SPLIT]]\n\n"
    
    for chunk in chunks:
        indices = [item[0] for item in chunk]
        chunk_texts = [item[1] for item in chunk]
        combined = delimiter.join(chunk_texts)
        
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q=" + urllib.parse.quote(combined)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        
        success = False
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=12) as resp:
                    data = json.loads(resp.read().decode('utf-8'))
                    full_trans = "".join([s[0] for s in data[0] if s[0]])
                    
                parts = full_trans.split("[[SPLIT]]")
                parts = [p.strip() for p in parts]
                
                if len(parts) == len(chunk_texts):
                    for idx, orig_text, trans_text in zip(indices, chunk_texts, parts):
                        _cache[f"{src}->{dest}:{orig_text}"] = trans_text
                        orig_full = texts[idx]
                        leading = orig_full[:len(orig_full) - len(orig_full.lstrip())]
                        trailing = orig_full[len(orig_full.rstrip()):]
                        results[idx] = leading + trans_text + trailing
                    success = True
                    break
                else:
                    break
            except Exception:
                time.sleep(1 + attempt * 2)
                
        if not success:
            for idx, orig_text in zip(indices, chunk_texts):
                single_url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={src}&tl={dest}&dt=t&q=" + urllib.parse.quote(orig_text)
                single_req = urllib.request.Request(single_url, headers={'User-Agent': 'Mozilla/5.0'})
                try:
                    with urllib.request.urlopen(single_req, timeout=8) as resp:
                        s_data = json.loads(resp.read().decode('utf-8'))
                        s_trans = "".join([s[0] for s in s_data[0] if s[0]])
                    _cache[f"{src}->{dest}:{orig_text}"] = s_trans
                    orig_full = texts[idx]
                    leading = orig_full[:len(orig_full) - len(orig_full.lstrip())]
                    trailing = orig_full[len(orig_full.rstrip()):]
                    results[idx] = leading + s_trans + trailing
                except Exception:
                    results[idx] = texts[idx]
                    
    save_cache()
    return results

def tokenize_tag(tag):
    if not tag.find_all(True):
        return tag.get_text(), {}
        
    inline_tags = {'a', 'strong', 'b', 'em', 'i', 'code', 'span', 'small', 'mark', 'kbd'}
    children = list(tag.children)
    
    has_block = any(getattr(c, 'name', None) not in inline_tags and getattr(c, 'name', None) is not None for c in children)
    if has_block:
        return None, None
        
    tokens = {}
    counter = 0
    tokenized = ""
    for child in children:
        if isinstance(child, str):
            tokenized += str(child)
        elif getattr(child, 'name', None) in inline_tags:
            token = f"[[T{counter}]]"
            tokens[token] = child
            tokenized += token
            counter += 1
        else:
            tokenized += str(child)
            
    return tokenized, tokens

def untokenize_and_replace(tag, translated_text, tokens, inline_translations):
    if tokens is None or not tokens:
        tag.string = translated_text
        return
        
    res = translated_text
    for token, child_tag in tokens.items():
        child_copy = copy.copy(child_tag)
        orig_inline_text = child_tag.get_text()
        trans_inline_text = inline_translations.get(orig_inline_text, orig_inline_text)
        child_copy.string = trans_inline_text
        
        pattern = re.escape(token).replace(r'\[\[', r'\[\s*\[').replace(r'\]\]', r'\]\s*\]')
        res = re.sub(pattern, str(child_copy), res)
        
    try:
        new_soup = BeautifulSoup(f"<div>{res}</div>", 'html.parser')
        tag.clear()
        for item in list(new_soup.div.contents):
            tag.append(item)
    except Exception:
        tag.string = translated_text

def adapt_links(soup, spanish_slug, english_slug):
    for a in soup.find_all('a', href=True):
        href = a['href']
        
        for sp_tool, en_tool in TOOL_MAP.items():
            if sp_tool in href or f"/{sp_tool[:-5]}" in href:
                a['href'] = f"/en/{en_tool}"
                break
                
        for sp_s, en_s in SLUG_MAP.items():
            if f"/{sp_s}/" in href or href.endswith(f"/{sp_s}"):
                a['href'] = f"/en/{en_s}/"
                break
                
        if href in ['/', '/index.html', 'https://nubeparapymes.online/']:
            a['href'] = '/en/'
        elif href in ['/herramientas/', '/herramientas/index.html', '/herramientas-gratis/']:
            a['href'] = '/en/'

def translate_full_post(spanish_slug, english_slug):
    t0 = time.time()
    src_file = os.path.join(ROOT_DIR, 'dist', spanish_slug, 'index.html')
    if not os.path.exists(src_file):
        src_file = os.path.join(ROOT_DIR, 'nubepymesexport', spanish_slug, 'index.html')
    if not os.path.exists(src_file):
        print(f"[ERROR] Source not found: {spanish_slug}", flush=True)
        return False
        
    with open(src_file, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    soup = BeautifulSoup(html, 'html.parser')
    
    if soup.html:
        soup.html['lang'] = 'en'
        
    title_str = ""
    if soup.title and soup.title.string:
        title_str = re.sub(r'\s*[-–—|]\s*Nube para Pymes.*$', '', soup.title.string.strip(), flags=re.IGNORECASE)
        
    desc_str = ""
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_str = meta_desc['content'].strip()
        
    schema_script = soup.find('script', type='application/ld+json')
    schema_headline = ""
    schema_desc = ""
    schema_keywords = ""
    schema_obj = None
    if schema_script and schema_script.string:
        try:
            schema_obj = json.loads(schema_script.string)
            def find_blog_posting(node):
                nonlocal schema_headline, schema_desc, schema_keywords
                if isinstance(node, dict):
                    if node.get('@type') in ['BlogPosting', 'Article', 'NewsArticle']:
                        schema_headline = node.get('headline', '')
                        schema_desc = node.get('description', '')
                        schema_keywords = node.get('keywords', '')
                    for v in node.values():
                        find_blog_posting(v)
                elif isinstance(node, list):
                    for item in node:
                        find_blog_posting(item)
            find_blog_posting(schema_obj)
        except Exception:
            schema_obj = None

    # Collect ALL headings and content blocks across the entire page
    content_blocks = []
    inline_strings_to_translate = set()
    
    # 1. All H1 elements (banner and article)
    for h1 in soup.find_all('h1'):
        tok, tok_dict = tokenize_tag(h1)
        if tok and tok.strip():
            content_blocks.append((h1, tok, tok_dict))
            for child in tok_dict.values():
                inline_strings_to_translate.add(child.get_text())

    # 2. Entry banner meta
    banner = soup.find('section', class_=re.compile(r'entry-banner'))
    if banner:
        for span in banner.find_all('span'):
            if span.string and ('Por ' in span.string or 'Publicado' in span.string):
                span.string = span.string.replace('Por ', 'By ').replace('Publicado el ', 'Published on ')

    # 3. Article content
    article = soup.find('article')
    if article:
        for meta_elem in article.find_all('span', class_=re.compile(r'author|date|comments|category')):
            tok, tok_dict = tokenize_tag(meta_elem)
            if tok:
                content_blocks.append((meta_elem, tok, tok_dict))
                
        entry = article.find('div', class_='entry-content')
        if entry:
            tags = entry.find_all(['h2', 'h3', 'h4', 'h5', 'p', 'li', 'th', 'td', 'blockquote', 'figcaption', 'strong'])
            for tag in tags:
                # If strong is inside a schema-faq, translate it
                if tag.name == 'strong' and 'schema-faq-question' not in tag.get('class', []):
                    continue
                tok, tok_dict = tokenize_tag(tag)
                if tok is not None and tok.strip():
                    content_blocks.append((tag, tok, tok_dict))
                    if tok_dict:
                        for child in tok_dict.values():
                            inline_strings_to_translate.add(child.get_text())
                            
    # 4. Navigation previous/next post links
    post_nav = soup.find('nav', class_=re.compile(r'post-navigation'))
    if post_nav:
        for p in post_nav.find_all('p'):
            tok, tok_dict = tokenize_tag(p)
            if tok and tok.strip():
                content_blocks.append((p, tok, tok_dict))
        for span in post_nav.find_all('span', class_=re.compile(r'ast-post-nav')):
            if 'Anterior' in span.text:
                span.string = span.text.replace('Anterior', 'Previous')
            elif 'Siguiente' in span.text:
                span.string = span.text.replace('Siguiente', 'Next')

    # 5. Related posts section
    rel_section = soup.find('div', class_=re.compile(r'ast-single-related-posts-container'))
    if rel_section:
        rel_title = rel_section.find('h2', class_=re.compile(r'ast-related-posts-title'))
        if rel_title:
            rel_title.string = 'Related Articles'
        for h3 in rel_section.find_all('h3', class_=re.compile(r'entry-title')):
            tok, tok_dict = tokenize_tag(h3)
            if tok and tok.strip():
                content_blocks.append((h3, tok, tok_dict))
        for p in rel_section.find_all('p', class_=re.compile(r'ast-related-post-excerpt')):
            tok, tok_dict = tokenize_tag(p)
            if tok and tok.strip():
                content_blocks.append((p, tok, tok_dict))

    all_texts = [title_str, desc_str, schema_headline, schema_desc, schema_keywords]
    meta_count = len(all_texts)
    
    block_indices = []
    for tag, tok, tok_dict in content_blocks:
        block_indices.append(len(all_texts))
        all_texts.append(tok)
        
    inline_list = list(inline_strings_to_translate)
    inline_start_idx = len(all_texts)
    all_texts.extend(inline_list)
    
    translated_all = translate_batch(all_texts, src='es', dest='en')
    
    t_title = translated_all[0]
    t_desc = translated_all[1]
    t_schema_head = translated_all[2]
    t_schema_desc = translated_all[3]
    t_schema_keywords = translated_all[4]
    
    inline_trans_map = {}
    for i, orig_s in enumerate(inline_list):
        inline_trans_map[orig_s] = translated_all[inline_start_idx + i]
        
    for i, (tag, tok, tok_dict) in enumerate(content_blocks):
        trans_block_text = translated_all[block_indices[i]]
        untokenize_and_replace(tag, trans_block_text, tok_dict, inline_trans_map)
        
    if soup.title:
        soup.title.string = f"{t_title} — Nube para Pymes"
    if meta_desc:
        meta_desc['content'] = t_desc
        
    og_locale = soup.find('meta', property='og:locale')
    if og_locale: og_locale['content'] = 'en_US'
    og_title = soup.find('meta', property='og:title')
    if og_title: og_title['content'] = t_title
    og_desc = soup.find('meta', property='og:description')
    if og_desc: og_desc['content'] = t_desc
    og_url = soup.find('meta', property='og:url')
    if og_url: og_url['content'] = f"https://nubeparapymes.online/en/{english_slug}/"
        
    tw_title = soup.find('meta', attrs={'name': 'twitter:title'})
    if tw_title: tw_title['content'] = t_title
    tw_desc = soup.find('meta', attrs={'name': 'twitter:description'})
    if tw_desc: tw_desc['content'] = t_desc
        
    canonical = soup.find('link', rel='canonical')
    if canonical: canonical['href'] = f"https://nubeparapymes.online/en/{english_slug}/"
        
    for alt in soup.find_all('link', rel='alternate', hreflang=True):
        alt.decompose()
        
    if soup.head:
        soup.head.append(soup.new_tag('link', rel='alternate', hreflang='es', href=f"https://nubeparapymes.online/{spanish_slug}/"))
        soup.head.append(soup.new_tag('link', rel='alternate', hreflang='en', href=f"https://nubeparapymes.online/en/{english_slug}/"))
        soup.head.append(soup.new_tag('link', rel='alternate', hreflang='x-default', href=f"https://nubeparapymes.online/{spanish_slug}/"))

    if schema_obj and schema_script:
        def mutate_schema(node):
            if isinstance(node, dict):
                if 'inLanguage' in node and node['inLanguage'] == 'es':
                    node['inLanguage'] = 'en'
                if node.get('@type') in ['BlogPosting', 'Article', 'NewsArticle']:
                    if t_schema_head: node['headline'] = t_schema_head
                    if t_schema_desc: node['description'] = t_schema_desc
                    if t_schema_keywords: node['keywords'] = t_schema_keywords
                if 'name' in node and isinstance(node['name'], str) and node.get('@type') != 'Organization':
                    if t_title: node['name'] = t_title
                if 'url' in node and isinstance(node['url'], str):
                    node['url'] = node['url'].replace(f"/{spanish_slug}/", f"/en/{english_slug}/")
                if '@id' in node and isinstance(node['@id'], str):
                    node['@id'] = node['@id'].replace(f"/{spanish_slug}/", f"/en/{english_slug}/")
                for v in node.values():
                    mutate_schema(v)
            elif isinstance(node, list):
                for it in node:
                    mutate_schema(it)
        mutate_schema(schema_obj)
        schema_script.string = json.dumps(schema_obj, ensure_ascii=False)

    # Header navigation translation
    header = soup.find('header')
    if header:
        for a in header.find_all(['a', 'span']):
            txt = a.text.strip()
            if txt in CATEGORY_TRANSLATIONS:
                a.string = CATEGORY_TRANSLATIONS[txt]
            elif txt in ['Inicio', 'Home']:
                a.string = 'Home'
                if a.name == 'a': a['href'] = '/en/'
            elif txt in ['Herramientas', 'Tools', 'Herramientas Gratis']:
                a.string = 'Tools'
                if a.name == 'a': a['href'] = '/en/'
            elif txt in ['Blog']:
                a.string = 'Blog'
            elif txt in ['Contacto', 'Contact']:
                a.string = 'Contact'
            elif txt in ['Sobre Nosotros', 'About Us']:
                a.string = 'About Us'
                
        inp = header.find('input', type='search')
        if inp:
            inp['placeholder'] = 'Search...'
            inp['aria-label'] = 'Search'

    # Adapt links
    adapt_links(soup, spanish_slug, english_slug)
    
    # Inject floating language switcher
    lang_switcher_html = f"""
    <aside class="np-lang-switch-floating" style="position:fixed;bottom:24px;right:24px;z-index:99999;background:rgba(15,23,42,0.92);backdrop-filter:blur(8px);color:#ffffff;border:1px solid #334155;border-radius:9999px;padding:8px 16px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.3);font-family:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:13px;display:flex;align-items:center;gap:10px;">
      <a href="/{spanish_slug}/" style="color:#94a3b8;text-decoration:none;font-weight:600;transition:color 0.2s;" title="Versión en español">ES</a>
      <span style="color:#475569;font-weight:300;">|</span>
      <span style="color:#2dd4bf;font-weight:700;">EN</span>
    </aside>
    """
    if soup.body:
        soup.body.append(BeautifulSoup(lang_switcher_html, 'html.parser'))

    # Footer
    footer = soup.find('footer')
    if footer:
        for p in footer.find_all(['p', 'span']):
            if 'Todos los derechos reservados' in p.text:
                p.string = p.text.replace('Todos los derechos reservados', 'All rights reserved').replace('Diseñado y Desarrollado por', 'Designed and Developed by')

    rendered_html = str(soup)
    for base in [os.path.join(ROOT_DIR, 'en'), os.path.join(ROOT_DIR, 'dist', 'en')]:
        target_dir = os.path.join(base, english_slug)
        os.makedirs(target_dir, exist_ok=True)
        with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(rendered_html)
            
        if spanish_slug != english_slug:
            stub_dir = os.path.join(base, spanish_slug)
            os.makedirs(stub_dir, exist_ok=True)
            stub_html = f"""<!DOCTYPE html>
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
            with open(os.path.join(stub_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(stub_html)
            
    elapsed = time.time() - t0
    print(f"[SUCCESS] {spanish_slug} -> en/{english_slug}/ ({len(content_blocks)} blocks in {elapsed:.2f}s)", flush=True)
    return True

if __name__ == '__main__':
    translate_full_post('alternativas-gratuitas-asana', 'free-asana-alternatives')
