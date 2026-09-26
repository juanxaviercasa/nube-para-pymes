import os
import re

def list_posts():
    # Identify non-post pages
    excluded = {
        'aviso-legal', 'descargo-de-responsabilidad', 'metodologia-de-resenas',
        'politica-de-cookies', 'politica-de-privacidad', 'terminos-y-condiciones',
        'directorio-herramientas', 'herramientas', 'blog', 'contacto', 'sobre-nosotros',
        'category', 'author', 'wp-content', 'wp-includes', 'wp-json', 'feed', 'comments'
    }
    
    dist_dirs = [d for d in os.listdir('dist') if os.path.isdir(os.path.join('dist', d)) and os.path.exists(os.path.join('dist', d, 'index.html'))]
    
    posts = []
    pages = []
    
    for d in sorted(dist_dirs):
        if d in excluded:
            pages.append(d)
            continue
            
        path = os.path.join('dist', d, 'index.html')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            chunk = f.read(4000)
            
        m_title = re.search(r'<title>(.*?)</title>', chunk, re.IGNORECASE | re.DOTALL)
        title = m_title.group(1).strip() if m_title else d
        
        # Clean title
        title = title.replace('&iacute;', 'í').replace('&aacute;', 'á').replace('&eacute;', 'é').replace('&oacute;', 'ó').replace('&uacute;', 'ú').replace('&ntilde;', 'ñ')
        
        posts.append((d, title))
        
    print(f"Total post candidates: {len(posts)}")
    print(f"Excluded pages: {len(pages)} -> {pages}")
    
    print("\n--- ALL POST CANDIDATES ---")
    for i, (slug, title) in enumerate(posts, 1):
        print(f"{i:2d}. {slug} -> {title[:70]}")

if __name__ == '__main__':
    list_posts()
