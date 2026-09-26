import os
import re

def analyze_dist_dirs():
    dist_dirs = [d for d in os.listdir('dist') if os.path.isdir(os.path.join('dist', d)) and os.path.exists(os.path.join('dist', d, 'index.html'))]
    print(f"Total directories in dist/ with index.html: {len(dist_dirs)}", flush=True)
    
    posts = []
    categories = []
    pages = []
    
    for d in dist_dirs:
        path = os.path.join('dist', d, 'index.html')
        try:
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                # read first 5000 chars
                chunk = f.read(5000)
        except Exception as e:
            continue
            
        m_title = re.search(r'<title>(.*?)</title>', chunk, re.IGNORECASE | re.DOTALL)
        title = m_title.group(1).strip() if m_title else ""
        
        m_canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', chunk, re.IGNORECASE)
        canonical = m_canon.group(1) if m_canon else ""
        
        # Check type
        if 'category' in canonical or 'categoria' in d or 'category' in d or d.startswith('category-'):
            categories.append((d, title))
        elif d in ['blog', 'contacto', 'sobre-nosotros', 'politica-privacidad', 'terminos-condiciones', 'author']:
            pages.append((d, title))
        else:
            posts.append((d, title))
            
    print(f"Posts: {len(posts)}", flush=True)
    print(f"Categories: {len(categories)}", flush=True)
    print(f"Pages: {len(pages)}", flush=True)
    
    print("\nSample posts (first 10):", flush=True)
    for d, t in posts[:10]:
        print(f"  {d}: {t[:60]}", flush=True)
        
    print(f"\nAll {len(posts)} post slugs:", flush=True)
    print([d for d, t in posts], flush=True)

if __name__ == '__main__':
    analyze_dist_dirs()
