import os
import sys
import time
import json
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLUG_MAP_FILE = os.path.join(ROOT_DIR, 'scripts', 'posts_slug_map.json')
SEARCH_INDEX_FILE = os.path.join(ROOT_DIR, 'dist', 'search-index.json')
SITEMAP_FILE = os.path.join(ROOT_DIR, 'dist', 'sitemap.xml')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from batch_translate_post import translate_full_post, save_cache, _cache

with open(SLUG_MAP_FILE, 'r', encoding='utf-8') as f:
    SLUG_MAP = json.load(f)

def run_all_translations():
    start_time = time.time()
    total = len(SLUG_MAP)
    print(f"=== STARTING BATCH TRANSLATION OF ALL {total} BLOG POSTS ===", flush=True)
    
    success_count = 0
    fail_count = 0
    
    for i, (sp_slug, en_slug) in enumerate(SLUG_MAP.items(), 1):
        print(f"[{i:02d}/{total}] Processing: {sp_slug} -> {en_slug}...", end="", flush=True)
        try:
            ok = translate_full_post(sp_slug, en_slug)
            if ok:
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f" [FAILED]: {e}", flush=True)
            fail_count += 1
            
        # Polite pause
        time.sleep(0.3)
        if i % 10 == 0:
            save_cache()
            print(f"--- Checkpoint: {i}/{total} posts completed ---", flush=True)
            
    save_cache()
    elapsed = time.time() - start_time
    print(f"\n=== FINISHED TRANSLATIONS in {elapsed:.1f}s ===", flush=True)
    print(f"Successful: {success_count} | Failed: {fail_count}", flush=True)
    
    # Now update search-index.json and sitemap.xml
    update_search_index()
    update_sitemap()

def update_search_index():
    print("Updating dist/search-index.json with English posts...", flush=True)
    if not os.path.exists(SEARCH_INDEX_FILE):
        print("search-index.json not found, skipping.")
        return
        
    try:
        with open(SEARCH_INDEX_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Remove existing English post entries if any
        data = [item for item in data if not item.get('url', '').startswith('/en/')]
        
        # Add English tools
        # Add English posts
        for sp_slug, en_slug in SLUG_MAP.items():
            en_file = os.path.join(ROOT_DIR, 'en', en_slug, 'index.html')
            if not os.path.exists(en_file):
                continue
                
            from bs4 import BeautifulSoup
            with open(en_file, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                
            title = soup.title.string.replace(' — Nube para Pymes', '').strip() if soup.title else en_slug
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            desc = meta_desc['content'] if meta_desc and meta_desc.get('content') else ""
            
            data.append({
                "title": title,
                "url": f"/en/{en_slug}/",
                "excerpt": desc,
                "content": f"{title} - {desc}",
                "type": "post"
            })
            
        with open(SEARCH_INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        print(f"dist/search-index.json updated. Total indexed items: {len(data)}", flush=True)
    except Exception as e:
        print(f"Error updating search index: {e}", flush=True)

def update_sitemap():
    print("Updating dist/sitemap.xml with English posts...", flush=True)
    if not os.path.exists(SITEMAP_FILE):
        print("sitemap.xml not found, skipping.")
        return
        
    try:
        with open(SITEMAP_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            
        now = datetime.now().strftime("%Y-%m-%d")
        new_entries = []
        for sp_slug, en_slug in SLUG_MAP.items():
            url = f"https://nubeparapymes.online/en/{en_slug}/"
            if url not in content:
                new_entries.append(
                    f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{now}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>"
                )
                
        if new_entries and "</urlset>" in content:
            block = "\n" + "\n".join(new_entries) + "\n</urlset>"
            content = content.replace("</urlset>", block)
            with open(SITEMAP_FILE, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Injected {len(new_entries)} English post URLs into dist/sitemap.xml", flush=True)
        else:
            print("No new URLs to inject or </urlset> not found.")
    except Exception as e:
        print(f"Error updating sitemap: {e}", flush=True)

if __name__ == '__main__':
    run_all_translations()
