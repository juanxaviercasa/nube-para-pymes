import xml.etree.ElementTree as ET

def parse_sitemap():
    tree = ET.parse('dist/sitemap.xml')
    root = tree.getroot()
    # xml namespace
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    locs = [elem.text for elem in root.findall('.//sm:loc', ns)]
    print(f"Total URLs in dist/sitemap.xml: {len(locs)}")
    
    # Classify locs
    tools = [l for l in locs if 'herramientas/' in l or l.endswith('.html')]
    categories = [l for l in locs if '/category/' in l]
    authors = [l for l in locs if '/author/' in l]
    posts = [l for l in locs if l not in tools and l not in categories and l not in authors and l != 'https://dev-nube-para-pymes.pantheonsite.io/']
    
    print(f"Tools/HTML: {len(tools)}")
    print(f"Categories: {len(categories)}")
    print(f"Authors: {len(authors)}")
    print(f"Posts/Articles: {len(posts)}")
    print("\nSample posts in sitemap:")
    for p in posts[:10]:
        print(" ", p)

if __name__ == '__main__':
    parse_sitemap()
