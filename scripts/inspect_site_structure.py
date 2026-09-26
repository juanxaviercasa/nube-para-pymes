import os

def check():
    folders_in_root = [d for d in os.listdir('.') if os.path.isdir(d) and os.path.exists(os.path.join(d, 'index.html'))]
    print('Folders in root with index.html:', len(folders_in_root), folders_in_root[:10])
    
    # Check what index.html links to
    with open('index.html', encoding='utf-8', errors='ignore') as f:
        idx_content = f.read()
    
    import re
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', idx_content)
    print(f"Total hrefs in index.html: {len(hrefs)}")
    post_hrefs = [h for h in hrefs if not h.startswith('#') and not h.startswith('http') and not h.endswith('.css') and not h.endswith('.js') and not h.endswith('.html')]
    print("Sample post/page links from index.html:", post_hrefs[:15])

if __name__ == '__main__':
    check()
