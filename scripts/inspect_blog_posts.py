import os
import glob
import json

def inspect():
    dist_dirs = [d for d in os.listdir('dist') if os.path.isdir(os.path.join('dist', d)) and os.path.exists(os.path.join('dist', d, 'index.html'))]
    print(f"Total HTML post folders in dist/: {len(dist_dirs)}")
    
    # Check if there are other files in dist/
    dist_root_files = [f for f in os.listdir('dist') if os.path.isfile(os.path.join('dist', f))]
    print(f"Files in dist/ root: {dist_root_files}")
    
    # Check nubepymesexport
    if os.path.exists('nubepymesexport'):
        nube_dirs = [d for d in os.listdir('nubepymesexport') if os.path.isdir(os.path.join('nubepymesexport', d)) and os.path.exists(os.path.join('nubepymesexport', d, 'index.html'))]
        print(f"Total in nubepymesexport: {len(nube_dirs)}")
    
    # Check borradores
    md_files = glob.glob('borradores/**/*.md', recursive=True)
    print(f"Total Markdown files in borradores: {len(md_files)}")
    for md in md_files:
        print(f"  - {md}")

    # Check search-index.json to see what's indexed
    if os.path.exists('dist/search-index.json'):
        with open('dist/search-index.json', encoding='utf-8') as f:
            idx = json.load(f)
        print(f"Total items in dist/search-index.json: {len(idx)}")
        types = {}
        for item in idx:
            t = item.get('type', 'none')
            types[t] = types.get(t, 0) + 1
        print(f"Types in search-index.json: {types}")
        
    # Check sitemap.xml
    if os.path.exists('dist/sitemap.xml'):
        with open('dist/sitemap.xml', encoding='utf-8') as f:
            sitemap_content = f.read()
        loc_count = sitemap_content.count('<loc>')
        print(f"Total URLs in dist/sitemap.xml: {loc_count}")

    # Also check root sitemap.xml if exists
    if os.path.exists('sitemap.xml'):
        with open('sitemap.xml', encoding='utf-8') as f:
            sitemap_root = f.read()
        print(f"Total URLs in root sitemap.xml: {sitemap_root.count('<loc>')}")

if __name__ == '__main__':
    inspect()
