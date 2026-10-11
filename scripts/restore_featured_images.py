"""Restore each article's original artwork, including all archive cards."""
import hashlib
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ARTICLE = re.compile(r'<article\b[^>]*>[\s\S]*?</article>', re.I)
IMAGE = re.compile(r'<img\b[^>]*\bclass=["\'][^"\']*\bwp-post-image\b[^"\']*["\'][^>]*>', re.I)
HEADING = re.compile(r'<h[12]\b[^>]*class=["\'][^"\']*entry-title[^"\']*["\'][^>]*>([\s\S]*?)</h[12]>', re.I)


def restore(dist):
    manifest = json.loads((ROOT / 'content/featured-images.json').read_text(encoding='utf-8'))
    translated = json.loads((ROOT / 'scripts/posts_slug_map.json').read_text(encoding='utf-8'))
    routes = {'/' + slug + '/': slug for slug in manifest}
    routes.update({'/en/' + translated[slug] + '/': slug for slug in manifest})
    catalog = {e['slug']: e for e in json.loads((ROOT / 'scripts/posts_catalog.json').read_text(encoding='utf-8'))}
    image_data = {}
    for slug, record in manifest.items():
        path = dist / record['path'].lstrip('/')
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise ValueError('Original artwork missing or changed: ' + slug)
        with Image.open(path) as image:
            width, height = image.size
        responsive = []
        for thumbnail in path.parent.glob(path.stem + '-*.webp'):
            size = re.search(r'-(\d+)x\d+\.webp$', thumbnail.name)
            if size and int(size[1]) < width:
                responsive.append((int(size[1]), '/' + thumbnail.relative_to(dist).as_posix()))
        responsive.append((width, record['path']))
        image_data[slug] = (width, height, ', '.join(f'{url} {w}w' for w, url in sorted(responsive)))
    changed = 0
    images = 0
    for file in dist.rglob('*.html'):
        content = file.read_text(encoding='utf-8')
        route = '/' + file.relative_to(dist).as_posix()
        route = route[:-10] if route.endswith('index.html') else route
        page_slug = routes.get(route)

        def article(match):
            nonlocal images
            block = match[0]
            heading = HEADING.search(block)
            primary = 'ast-article-single' in block.split('>', 1)[0]
            slug = page_slug if primary else None
            if not slug and heading:
                link = re.search(r'<a\b[^>]*href=["\']([^"\']+)', heading[1])
                if link:
                    path = urlsplit(html.unescape(link[1])).path
                    slug = routes.get(path if path.endswith('/') else path + '/')
            if not slug:
                for href in re.findall(r'<a\b[^>]*href=["\']([^"\']+)', block):
                    path = urlsplit(html.unescape(href)).path
                    slug = routes.get(path if path.endswith('/') else path + '/')
                    if slug:
                        break
            if not slug:
                return block
            title = html.unescape(re.sub('<[^>]+>', '', heading[1])).strip() if heading else catalog[slug]['h1']
            width, height, srcset = image_data[slug]

            def image_tag(image_match):
                nonlocal images
                tag = BeautifulSoup(image_match[0], 'html.parser').img
                tag['src'] = manifest[slug]['path']
                tag['alt'] = title
                tag['width'], tag['height'] = str(width), str(height)
                tag['srcset'] = srcset
                tag['sizes'] = '(max-width: 600px) 100vw, (max-width: 1000px) 50vw, 520px' if not page_slug else '(max-width: 900px) 100vw, 900px'
                for name in ['data-src', 'data-lazy-src', 'data-srcset', 'data-lazy-srcset']:
                    if name in tag.attrs:
                        tag[name] = srcset if 'srcset' in name else manifest[slug]['path']
                images += 1
                return str(tag)
            if primary and not re.search(r'<img\b', block):
                featured = f'<figure class="post-thumb"><img class="wp-post-image" src="{manifest[slug]["path"]}" alt="" decoding="async" /></figure>'
                featured = IMAGE.sub(image_tag, featured, count=1)
                if '</header>' in block:
                    return re.sub(r'(</header>)', lambda m: m[0] + featured, block, count=1)
                return re.sub(r'(<div\b[^>]*class=["\'][^"\']*entry-content[^"\']*["\'][^>]*>)', lambda m: m[0] + featured, block, count=1)
            if primary:
                return re.sub(r'<img\b[^>]*>', image_tag, block, count=1, flags=re.I)
            return IMAGE.sub(image_tag, block, count=1)

        updated = ARTICLE.sub(article, content)
        if page_slug:
            source = manifest[page_slug]['path']
            def meta(match):
                tag = BeautifulSoup(match[0], 'html.parser').meta
                if tag.get('property') in ('og:image', 'og:image:secure_url') or tag.get('name') == 'twitter:image':
                    tag['content'] = 'https://nubeparapymes.online' + source
                    return str(tag)
                if tag.get('property') in ('og:image:width', 'og:image:height'):
                    tag['content'] = str(image_data[page_slug][0 if tag['property'].endswith('width') else 1])
                    return str(tag)
                return match[0]
            updated = re.sub(r'<meta\b[^>]*>', meta, updated, flags=re.I)

            def structured(match):
                try:
                    data = json.loads(match[2])
                except ValueError:
                    return match[0]
                def visit(node):
                    if isinstance(node, list):
                        for child in node: visit(child)
                    elif isinstance(node, dict):
                        types = node.get('@type', [])
                        if isinstance(types, str): types = [types]
                        if any(t in types for t in ('Article', 'BlogPosting')):
                            node['image'] = 'https://nubeparapymes.online' + source
                        if 'ImageObject' in types and '/wp-content/uploads/' in node.get('url', '') and 'logo' not in node.get('url', '').lower():
                            node.update(url='https://nubeparapymes.online' + source, contentUrl='https://nubeparapymes.online' + source, width=image_data[page_slug][0], height=image_data[page_slug][1])
                        for child in node.values(): visit(child)
                visit(data)
                return match[1] + json.dumps(data, ensure_ascii=False).replace('</', '<\\/') + match[3]
            updated = re.sub(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)([\s\S]*?)(</script>)', structured, updated, flags=re.I)
        if updated != content:
            updated = re.sub(r'[ \t]+$', '', updated, flags=re.M)
            file.write_text(updated, encoding='utf-8')
            changed += 1
    print(f'[ARTWORK] Restored {images} article/card images across {changed} pages.', flush=True)


if __name__ == '__main__':
    restore(ROOT / 'dist')
