import json

def inspect_catalog():
    with open('scripts/posts_catalog.json', encoding='utf-8') as f:
        catalog = json.load(f)
        
    print(f"Total entries: {len(catalog)}")
    for i, p in enumerate(catalog[:10], 1):
        print(f"{i:2d}. {p['slug']}")
        print(f"    H1: {p['h1']}")
        print(f"    Cat: {p['category']}")
        print(f"    Desc: {p['meta_description'][:80]}...")

if __name__ == '__main__':
    inspect_catalog()
