import os
import json
from bs4 import BeautifulSoup

def catalog_all_posts():
    excluded = {
        'aviso-legal', 'descargo-de-responsabilidad', 'metodologia-de-resenas',
        'politica-de-cookies', 'politica-de-privacidad', 'terminos-y-condiciones',
        'directorio-herramientas', 'herramientas', 'blog', 'contacto', 'sobre-nosotros',
        'category', 'author', 'wp-content', 'wp-includes', 'wp-json', 'feed', 'comments'
    }
    
    dist_dirs = [d for d in sorted(os.listdir('dist')) if os.path.isdir(os.path.join('dist', d)) and os.path.exists(os.path.join('dist', d, 'index.html'))]
    posts = [d for d in dist_dirs if d not in excluded]
    
    catalog = []
    for slug in posts:
        path = os.path.join('dist', slug, 'index.html')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        title = soup.title.string if soup.title else ""
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_desc = meta_desc_tag['content'] if meta_desc_tag and meta_desc_tag.has_attr('content') else ""
        
        h1_tag = soup.find('h1')
        h1 = h1_tag.text.strip() if h1_tag else ""
        
        # Category
        cat_meta = soup.find('meta', property='article:section')
        cat = cat_meta['content'] if cat_meta and cat_meta.has_attr('content') else ""
        
        catalog.append({
            'slug': slug,
            'title': title,
            'h1': h1,
            'meta_description': meta_desc,
            'category': cat,
            'html_length': len(html)
        })
        
    print(f"Total posts cataloged: {len(catalog)}")
    with open('scripts/posts_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print("Saved to scripts/posts_catalog.json")

if __name__ == '__main__':
    catalog_all_posts()
