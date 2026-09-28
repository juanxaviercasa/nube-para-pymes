#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el Gestor Universal de Idiomas de Nube para Pymes (npp-lang-manager.js)
Provee:
1. Persistencia de idioma en localStorage y cookies cuando el usuario hace clic en el selector.
2. Mantenimiento del idioma activo durante toda la navegación: si el usuario eligió inglés,
   se mantiene fijo en inglés en cualquier página que visite.
3. Detección automática para nuevos visitantes de habla inglesa hacia /en/.
4. Enrutamiento inteligente entre equivalentes ES <-> EN usando el mapa completo de slugs.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

def generate_js():
    slug_map = json.loads((ROOT / "scripts" / "posts_slug_map.json").read_text(encoding="utf-8"))
    
    js_content = f'''/**
 * Nube para Pymes - Universal Language Persistence & Auto-Router
 * Preserves user language preference (EN/ES) across page reloads, tabs, and visits.
 */
(function() {{
  'use strict';

  var STORAGE_KEY = 'npp_user_lang';
  var COOKIE_KEY = 'npp_user_lang';
  
  var ES_TO_EN = {json.dumps(slug_map, indent=2)};
  
  var EN_TO_ES = {{}};
  for (var k in ES_TO_EN) {{
    EN_TO_ES[ES_TO_EN[k]] = k;
  }}

  var SPECIAL_ES_TO_EN = {{
    'sobre-nosotros': 'about-us',
    'herramientas': 'tools',
    'directorio-herramientas': 'tools',
    'blog': 'blog'
  }};

  var SPECIAL_EN_TO_ES = {{
    'about-us': 'sobre-nosotros',
    'tools': 'herramientas',
    'user-guide': 'herramientas/guia-uso',
    'blog': 'blog'
  }};

  function getStoredLang() {{
    try {{
      var cookieMatch = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_KEY + '=([^;]*)'));
      if (cookieMatch && cookieMatch[1]) {{
        return decodeURIComponent(cookieMatch[1]);
      }}
      return localStorage.getItem(STORAGE_KEY);
    }} catch (e) {{
      return null;
    }}
  }}

  function setStoredLang(lang) {{
    try {{
      localStorage.setItem(STORAGE_KEY, lang);
      document.cookie = COOKIE_KEY + '=' + encodeURIComponent(lang) + '; path=/; max-age=31536000; SameSite=Lax';
    }} catch (e) {{}}
  }}

  var path = window.location.pathname.replace(/^\\/+|\\/+$/g, '');
  var parts = path ? path.split('/') : [];
  var isEn = (parts.length > 0 && parts[0] === 'en');

  var currentPref = getStoredLang();

  // 1. Detección automática en primera visita (sin preferencia previa guardada)
  if (!currentPref) {{
    var userNavLang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (userNavLang.startsWith('en')) {{
      // Si el navegador es inglés y visita la portada raíz, enrutar a /en/
      if (parts.length === 0 || parts[0] === 'index.html') {{
        setStoredLang('en');
        window.location.replace('/en/');
        return;
      }}
    }}
  }} else {{
    // 2. Si el usuario TIENE preferencia activa 'en', mantenerlo fijo en inglés
    if (currentPref === 'en' && !isEn) {{
      // Usuario está en una ruta en español pero su preferencia es inglés
      var target = '/en/';
      if (parts.length === 0 || parts[0] === 'index.html') {{
        target = '/en/';
      }} else if (parts[0] in ES_TO_EN) {{
        target = '/en/' + ES_TO_EN[parts[0]] + '/';
      }} else if (parts[0] in SPECIAL_ES_TO_EN) {{
        target = '/en/' + SPECIAL_ES_TO_EN[parts[0]] + '/';
      }} else if (parts[0] === 'category' && parts.length > 1) {{
        target = '/en/category/' + parts[1] + '/';
      }} else if (parts[0] === 'blog') {{
        target = '/en/blog/';
      }}
      
      if (window.location.pathname !== target) {{
        window.location.replace(target);
        return;
      }}
    }}
  }}

  // 3. Capturar clics en selectores de idioma y en enlaces de navegación
  function bindInteractions() {{
    document.querySelectorAll('a.np-lang-toggle').forEach(function(btn) {{
      btn.addEventListener('click', function(e) {{
        var href = btn.getAttribute('href') || '';
        if (href.startsWith('/en/') || href === '/en') {{
          setStoredLang('en');
        }} else {{
          setStoredLang('es');
        }}
      }});
    }});

    // Si estamos en versión en inglés, proteger que los clics internos no salgan a español
    if (isEn) {{
      document.addEventListener('click', function(e) {{
        var a = e.target.closest('a');
        if (!a) return;
        if (a.classList.contains('np-lang-toggle')) return; // Permitir que el botón cambie a español
        
        var href = a.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:')) return;
        
        // Si el enlace apunta a /blog/ o /sobre-nosotros/ sin prefijo /en/
        if (href === '/blog/' || href === '/blog') {{
          e.preventDefault();
          window.location.href = '/en/blog/';
        }} else if (href === '/sobre-nosotros/' || href === '/sobre-nosotros') {{
          e.preventDefault();
          window.location.href = '/en/about-us/';
        }} else if (href === '/herramientas/' || href === '/directorio-herramientas/') {{
          e.preventDefault();
          window.location.href = '/en/tools/';
        }} else if (href.startsWith('/category/')) {{
          e.preventDefault();
          window.location.href = '/en' + href;
        }}
      }}, true);
    }}
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', bindInteractions);
  }} else {{
    bindInteractions();
  }}
}})();
'''
    destinations = [
        DIST / "wp-static-arquitect-assets" / "npp-lang-manager.js",
        ROOT / "wp-static-arquitect-assets" / "npp-lang-manager.js",
        ROOT / "nubepymesexport" / "wp-static-arquitect-assets" / "npp-lang-manager.js"
    ]
    for dest in destinations:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(js_content, encoding="utf-8")
        print(f"Escrito: {dest}")

if __name__ == "__main__":
    generate_js()
