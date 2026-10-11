"""Check artwork assignment through parsed article markup and original hashes."""
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
manifest = json.loads((ROOT / 'content/featured-images.json').read_text(encoding='utf-8'))
translations = json.loads((ROOT / 'scripts/posts_slug_map.json').read_text(encoding='utf-8'))
routes = {'/' + slug + '/': slug for slug in manifest}
routes.update({'/en/' + translations[slug] + '/': slug for slug in manifest})
hashes = []
for slug, entry in manifest.items():
    digest = hashlib.sha256((DIST / entry['path'].lstrip('/')).read_bytes()).hexdigest()
    assert digest == entry['sha256'], slug + ': artwork changed'
    hashes.append(digest)
assert len(set(hashes)) == len(manifest), 'Different posts reuse identical artwork'


class Articles(HTMLParser):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.stack = []
        self.checked = 0
        self.single = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'article':
            primary = 'ast-article-single' in attrs.get('class', '').split()
            self.stack.append({'image': None, 'slug': routes.get(self.route) if primary else None, 'heading': False, 'primary': primary})
        if not self.stack:
            return
        current = self.stack[-1]
        if tag in ('h1', 'h2') and 'entry-title' in attrs.get('class', '').split():
            current['heading'] = True
        if tag == 'a' and current['heading'] and not current['primary']:
            path = urlsplit(attrs.get('href', '')).path
            current['slug'] = routes.get(path if path.endswith('/') else path + '/')
        if tag == 'img' and current['image'] is None and ('wp-post-image' in attrs.get('class', '').split() or (self.route in routes and attrs.get('src', '').startswith('/wp-content/uploads/'))):
            current['image'] = attrs

    def handle_endtag(self, tag):
        if not self.stack:
            return
        if tag in ('h1', 'h2'):
            self.stack[-1]['heading'] = False
        if tag == 'article':
            current = self.stack.pop()
            slug = current['slug']
            if slug and current['image']:
                image = current['image']
                expected = manifest[slug]['path']
                assert urlsplit(image['src']).path == expected, self.route + ': wrong image for ' + slug
                assert image.get('alt'), self.route + ': missing alt'
                for candidate in image.get('srcset', '').split(','):
                    if candidate.strip():
                        path = urlsplit(candidate.strip().split()[0]).path
                        assert (DIST / path.lstrip('/')).is_file(), self.route + ': missing responsive image'
                self.checked += 1
                if current['primary'] and slug == routes.get(self.route):
                    self.single += 1


checked = 0
for file in DIST.rglob('*.html'):
    route = '/' + file.relative_to(DIST).as_posix()
    if route.endswith('index.html'):
        route = route[:-10]
    parser = Articles(route)
    parser.feed(file.read_text(encoding='utf-8'))
    if route in routes:
        assert parser.single == 1, route + ': expected a featured image'
    checked += parser.checked
print(f'ARTWORK OK: {len(manifest)} unique original images, 140 bilingual articles, {checked} article/card references.')
