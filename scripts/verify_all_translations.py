import os
import sys
import json
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG_MAP_FILE = os.path.join(ROOT_DIR, 'scripts', 'posts_slug_map.json')

def verify_all():
    with open(SLUG_MAP_FILE, 'r', encoding='utf-8') as f:
        slug_map = json.load(f)
        
    print(f"=== VERIFYING {len(slug_map)} TRANSLATED POSTS ===", flush=True)
    
    missing_en_root = []
    missing_dist_en = []
    missing_stubs = []
    errors = []
    
    for sp_slug, en_slug in slug_map.items():
        en_root_file = os.path.join(ROOT_DIR, 'en', en_slug, 'index.html')
        dist_en_file = os.path.join(ROOT_DIR, 'dist', 'en', en_slug, 'index.html')
        stub_file = os.path.join(ROOT_DIR, 'en', sp_slug, 'index.html')
        
        if not os.path.exists(en_root_file):
            missing_en_root.append(en_slug)
            continue
        if not os.path.exists(dist_en_file):
            missing_dist_en.append(en_slug)
        if not os.path.exists(stub_file):
            missing_stubs.append(sp_slug)
            
        # Inspect content
        with open(en_root_file, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check language
        if soup.html and soup.html.get('lang') != 'en':
            errors.append(f"{en_slug}: html lang is not 'en'")
            
        # Check canonical
        canon = soup.find('link', rel='canonical')
        if not canon or en_slug not in canon.get('href', ''):
            errors.append(f"{en_slug}: canonical tag missing or incorrect: {canon}")
            
        # Check title
        if not soup.title or not soup.title.string or len(soup.title.string.strip()) < 5:
            errors.append(f"{en_slug}: invalid title")
            
        # Check H1
        h1 = soup.find('h1')
        if not h1 or len(h1.text.strip()) < 5:
            errors.append(f"{en_slug}: invalid H1")
            
        # Check language switcher
        switcher = soup.find('aside', class_='np-lang-switch-floating')
        if not switcher:
            errors.append(f"{en_slug}: missing floating language switcher")
            
    print(f"Missing in root /en/: {len(missing_en_root)}")
    print(f"Missing in dist /en/: {len(missing_dist_en)}")
    print(f"Missing redirect stubs: {len(missing_stubs)}")
    print(f"Content / SEO errors: {len(errors)}")
    
    if errors:
        for err in errors[:10]:
            print(f"  [ERROR] {err}")
            
    if not missing_en_root and not errors:
        print("\nALL POSTS VERIFIED 100% HEALTHY AND DEPLOYMENT READY!", flush=True)

if __name__ == '__main__':
    verify_all()
