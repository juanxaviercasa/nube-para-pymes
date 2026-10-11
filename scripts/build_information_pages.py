"""Build translated information pages using the existing site's layout."""
from pathlib import Path
from bs4 import BeautifulSoup
from site_routes import INFORMATION_PAGES, ROOT

def build(dist):
    from build_brand_pages import build as build_brand_pages
    build_brand_pages(dist)
    for es, (en, title) in INFORMATION_PAGES.items():
        if en in ('about-us', 'contact'):
            continue
        soup = BeautifulSoup((dist / es / 'index.html').read_text(encoding='utf-8'), 'html.parser')
        soup.html['lang'] = 'en'
        soup.title.string = title + ' | SMB Cloud'
        for heading in soup.select('h1.entry-title'):
            heading.string = title
        content = soup.select_one('.entry-content')
        if content is None:
            raise ValueError(f'Missing content container: {es}')
        fragment = BeautifulSoup((ROOT / 'content/en' / (en + '.html')).read_text(encoding='utf-8'), 'html.parser')
        content.clear()
        for child in list(fragment.contents):
            content.append(child)
        # Remove inherited Spanish structured data; canonical/hreflang are added centrally.
        for script in soup.select('script[type="application/ld+json"]'):
            script.decompose()
        description = soup.select_one('meta[name="description"]')
        if description:
            description['content'] = f'{title} for NubeParaPymes.online (SMB Cloud).'
        for tag in soup.select('meta[property="og:title"], meta[name="twitter:title"]'):
            tag['content'] = title + ' | SMB Cloud'
        for tag in soup.select('meta[property="og:description"], meta[name="twitter:description"]'):
            tag['content'] = f'{title} for NubeParaPymes.online (SMB Cloud).'
        for tag in soup.select('meta[property="og:locale"]'):
            tag['content'] = 'en_US'
        dest = dist / 'en' / en / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(str(soup), encoding='utf-8')
