import re
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

slug_map_file = ROOT / "scripts" / "posts_slug_map.json"
es_to_en = json.loads(slug_map_file.read_text(encoding="utf-8")) if slug_map_file.exists() else {}
en_to_es = {v: k for k, v in es_to_en.items()}

special_en_to_es = {
    "about-us": "sobre-nosotros",
    "tools": "herramientas",
    "user-guide": "herramientas/guia-uso",
}
special_es_to_en = {
    "sobre-nosotros": "about-us",
    "herramientas": "tools",
    "directorio-herramientas": "tools",
}

def make_sleek_switcher(target_url, is_en=False):
    globe = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.75;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>'
    
    if is_en:
        return f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{target_url}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Cambiar a español" aria-label="Cambiar a español">
    {globe}
    <span style="color:#f97316;font-weight:700;">EN</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">ES</span>
  </a>
</li>'''
    else:
        return f'''<li class="menu-item-lang-switcher" style="display:inline-flex!important;align-items:center!important;height:100%!important;margin:0 0 0 16px!important;padding:0!important;list-style:none!important;">
  <a href="{target_url}" class="np-lang-toggle" style="display:inline-flex!important;align-items:center!important;gap:5px!important;height:28px!important;max-height:28px!important;line-height:26px!important;padding:0 10px!important;border-radius:14px!important;border:1px solid #d1d5db!important;background:#ffffff!important;color:#374151!important;font-size:12px!important;font-weight:600!important;text-decoration:none!important;box-shadow:0 1px 2px rgba(0,0,0,0.05)!important;white-space:nowrap!important;box-sizing:border-box!important;vertical-align:middle!important;" title="Switch to English" aria-label="Switch to English">
    {globe}
    <span style="color:#f97316;font-weight:700;">ES</span>
    <span style="color:#cbd5e1;font-weight:400;margin:0 1px;">|</span>
    <span style="color:#6b7280;font-weight:500;">EN</span>
  </a>
</li>'''

# Pattern to replace any existing language switcher in nav
SWITCHER_PATTERN = re.compile(
    r'<li[^>]*class=["\'][^"\']*menu-item-lang-switcher[^"\']*["\'][^>]*>[\s\S]*?</li>'
)

def update_files():
    count = 0
    targets = list(DIST.rglob("*.html")) + list((ROOT / "en").rglob("*.html"))
    targets.append(ROOT / "index.html")
    
    seen = set()
    for html_file in targets:
        if html_file in seen or not html_file.exists():
            continue
        seen.add(html_file)
        
        rel_str = str(html_file)
        if "herramientas" in rel_str and "herramientas/index.html" not in rel_str.replace("\\", "/"):
            continue
            
        try:
            content = html_file.read_text(encoding="utf-8")
            is_en = "/en/" in rel_str.replace("\\", "/") or "\\en\\" in rel_str
            
            # Determine slug
            parts = html_file.parts
            slug = ""
            if "en" in parts:
                idx = parts.index("en")
                if len(parts) > idx + 2:
                    slug = parts[idx + 1]
            elif "dist" in parts:
                idx = parts.index("dist")
                if len(parts) > idx + 2:
                    slug = parts[idx + 1]
            
            if is_en:
                if slug in en_to_es:
                    target_url = f"/{en_to_es[slug]}/"
                elif slug in special_en_to_es:
                    target_url = f"/{special_en_to_es[slug]}/"
                else:
                    target_url = "/"
            else:
                if slug in es_to_en:
                    target_url = f"/en/{es_to_en[slug]}/"
                elif slug in special_es_to_en:
                    target_url = f"/en/{special_es_to_en[slug]}/"
                else:
                    target_url = "/en/"
            
            new_switcher = make_sleek_switcher(target_url, is_en)
            
            if SWITCHER_PATTERN.search(content):
                content = SWITCHER_PATTERN.sub(new_switcher, content)
                html_file.write_text(content, encoding="utf-8")
                count += 1
        except Exception as e:
            pass

    print(f"Updated sleek, non-stretching language switcher across {count} HTML files!")

if __name__ == "__main__":
    update_files()
