import os
from bs4 import BeautifulSoup

def verify_posts():
    dist_dirs = [d for d in os.listdir('dist') if os.path.isdir(os.path.join('dist', d)) and os.path.exists(os.path.join('dist', d, 'index.html'))]
    excluded = {
        'aviso-legal', 'descargo-de-responsabilidad', 'metodologia-de-resenas',
        'politica-de-cookies', 'politica-de-privacidad', 'terminos-y-condiciones',
        'directorio-herramientas', 'herramientas', 'blog', 'contacto', 'sobre-nosotros',
        'category', 'author', 'wp-content', 'wp-includes', 'wp-json', 'feed', 'comments'
    }
    
    post_slugs = [d for d in sorted(dist_dirs) if d not in excluded]
    print(f"Total post slugs to verify: {len(post_slugs)}")
    
    verified_posts = []
    for slug in post_slugs:
        path = os.path.join('dist', slug, 'index.html')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            chunk = f.read(15000)
            
        soup = BeautifulSoup(chunk, 'html.parser')
        article = soup.find('article')
        is_post = False
        classes = []
        if article and article.has_attr('class'):
            classes = article['class']
            is_post = 'type-post' in classes
            
        h1 = soup.find('h1')
        h1_text = h1.text.strip() if h1 else 'NO H1'
        
        # Check date
        published = soup.find('meta', property='article:published_time')
        pub_date = published['content'][:10] if published and published.has_attr('content') else 'N/A'
        
        verified_posts.append({
            'slug': slug,
            'is_post': is_post,
            'h1': h1_text,
            'date': pub_date,
            'classes': [c for c in classes if c.startswith('category-') or c in ('type-post', 'type-page')]
        })
        
    print(f"Verified count: {len(verified_posts)}")
    print(f"Type-post count: {sum(1 for p in verified_posts if p['is_post'])}")
    non_posts = [p for p in verified_posts if not p['is_post']]
    print(f"Non type-post count: {len(non_posts)}")
    if non_posts:
        for np in non_posts:
            print(f"  Non-post: {np['slug']} | classes: {np['classes']} | H1: {np['h1']}")

if __name__ == '__main__':
    verify_posts()
