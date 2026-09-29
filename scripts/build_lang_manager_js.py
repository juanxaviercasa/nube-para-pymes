#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el Gestor Universal de Idiomas de Nube para Pymes (npp-lang-manager.js)
Provee:
1. Persistencia de idioma en localStorage y cookies cuando el usuario hace clic en el selector.
2. Mantenimiento del idioma activo durante toda la navegación: si el usuario eligió inglés,
   se mantiene fijo en inglés en cualquier página que visite sin secuestrar ni romper herramientas.
3. Mapeo bidireccional exhaustivo: 70 artículos de blog, 6 categorías, páginas maestras y las 26 herramientas.
4. Prevención de redirección destructiva: si no hay equivalente exacto, no redirige a ciegas a /en/.
5. Captura inteligente de clics internos en modo /en/ para que los enlaces a herramientas o blog
   se mantengan dentro de la versión en inglés.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

TOOLS_MAP_ES_TO_EN = {
    "analizador-titulares": "headline-analyzer",
    "auditor-seo-basico": "basic-on-page-seo-auditor",
    "calculadora-descuentos-promociones": "discount-promotions-calculator",
    "calculadora-flete-envio-local": "local-shipping-calculator",
    "calculadora-precios-venta-igv": "sales-pricing-tax-calculator",
    "calculadora-prestamos-amortizaciones": "loan-amortization-calculator",
    "calculadora-sobrecostos-laborales": "labor-cost-payroll-burden-calculator",
    "comparador-campanas-avanzado": "advanced-campaign-comparator",
    "consola-campanas": "campaign-utm-console",
    "conversor-optimizador-imagenes": "image-converter-optimizer",
    "creador-facturas-proforma": "proforma-invoice-generator",
    "crm-pymes": "smb-crm",
    "firma-correo-html": "html-email-signature",
    "flujo-caja-pymes": "cash-flow-tracker",
    "generador-codigos-qr": "qr-code-generator",
    "generador-contrasenas-pymes": "smb-password-generator",
    "generador-contratos-servicios": "service-contracts-generator",
    "generador-cotizaciones": "quote-estimate-generator",
    "generador-paletas-corporativas": "brand-palette-generator",
    "generador-politicas-devolucion": "return-policy-generator",
    "generador-politicas-terminos": "terms-privacy-generator",
    "guia-uso-22-apps": "user-guide",
    "guiones-manejo-objeciones": "objection-handling-scripts",
    "inventario-compras-pymes": "inventory-purchasing",
    "organizador-matriz-contenidos": "content-matrix-planner",
    "simulador-tco-fisico-nube": "cloud-vs-onprem-tco-simulator",
    "tareas-proyectos-pymes": "tasks-projects-tracker"
}

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
  var TOOLS_ES_TO_EN = {json.dumps(TOOLS_MAP_ES_TO_EN, indent=2)};
  
  var EN_TO_ES = {{}};
  for (var k in ES_TO_EN) {{
    EN_TO_ES[ES_TO_EN[k]] = k;
  }}

  var TOOLS_EN_TO_ES = {{}};
  for (var tk in TOOLS_ES_TO_EN) {{
    TOOLS_EN_TO_ES[TOOLS_ES_TO_EN[tk]] = tk;
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
    // 2. Si el usuario TIENE preferencia activa 'en', enrutar a la página en inglés correspondiente
    if (currentPref === 'en' && !isEn) {{
      var target = null;
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
      }} else if (parts[0] === 'herramientas') {{
        if (parts.length >= 3 && parts[2] in TOOLS_ES_TO_EN) {{
          target = '/en/' + TOOLS_ES_TO_EN[parts[2]] + '.html';
        }} else if (parts.length >= 2 && parts[1] === 'guia-uso') {{
          target = '/en/user-guide.html';
        }} else {{
          target = '/en/tools/';
        }}
      }} else if (parts[0].endsWith('.html')) {{
        var baseSlug = parts[0].replace(/\\.html$/, '');
        if (baseSlug in TOOLS_ES_TO_EN) {{
          target = '/en/' + TOOLS_ES_TO_EN[baseSlug] + '.html';
        }} else if (baseSlug === 'guia-uso-22-apps') {{
          target = '/en/user-guide.html';
        }}
      }}
      
      // Solo redirigir si encontramos un target válido y es diferente de la URL actual
      if (target && window.location.pathname !== target) {{
        window.location.replace(target);
        return;
      }}
    }}
  }}

  // 4. Inyectar pill de idioma en herramientas si no existe en el header
  function renderToolHeaderPill() {{
    var isToolPage = !!document.querySelector('body[data-app-id]') || !!document.querySelector('.np-global-footer') || parts[0] === 'herramientas' || (parts.length > 0 && parts[0].endsWith('.html')) || (isEn && parts.length > 1 && parts[1].endsWith('.html'));
    if (!isToolPage) return;

    var existingPill = document.querySelector('.np-lang-toggle');
    if (existingPill) return;

    var footerLang = document.querySelector('.np-footer-lang');
    var targetUrl = footerLang ? footerLang.getAttribute('href') : null;
    
    if (!targetUrl) {{
      var appId = document.body.getAttribute('data-app-id');
      if (isEn) {{
        targetUrl = '/herramientas/';
      }} else {{
        if (appId && appId in TOOLS_ES_TO_EN) {{
          targetUrl = '/en/' + TOOLS_ES_TO_EN[appId] + '.html';
        }} else {{
          targetUrl = '/en/tools/';
        }}
      }}
    }}

    // Si tiene .op-nav (herramientas operativas)
    var nav = document.querySelector('.op-nav');
    if (nav && !nav.querySelector('.np-lang-toggle')) {{
      var a = document.createElement('a');
      a.className = 'np-lang-toggle';
      a.href = targetUrl;
      a.style.cssText = 'display:inline-flex;align-items:center;gap:4px;border:1px solid rgba(255,255,255,0.3);border-radius:9px;padding:6px 10px;font-size:12px;font-weight:700;color:#fff;text-decoration:none;margin-left:4px;background:rgba(255,255,255,0.1);';
      a.title = isEn ? 'Cambiar a español' : 'Switch to English';
      a.innerHTML = isEn ? '<span style="color:#f97316;">EN</span> | ES' : 'EN | <span style="color:#f97316;">ES</span>';
      nav.appendChild(a);
      return;
    }}

    // Para el resto de herramientas (React / Vite)
    if (!document.getElementById('np-floating-lang')) {{
      var aside = document.createElement('aside');
      aside.id = 'np-floating-lang';
      aside.setAttribute('aria-label', isEn ? 'Language selector' : 'Selector de idioma');
      aside.style.cssText = 'position:fixed;top:14px;right:18px;z-index:99999;display:inline-flex;align-items:center;pointer-events:auto;';
      var a = document.createElement('a');
      a.className = 'np-lang-toggle';
      a.href = targetUrl;
      a.style.cssText = 'display:inline-flex;align-items:center;gap:6px;height:32px;line-height:30px;padding:0 12px;border-radius:16px;border:1px solid rgba(255,255,255,0.25);background:rgba(15,23,42,0.88);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);color:#f8fafc;font-size:12px;font-weight:700;text-decoration:none;box-shadow:0 4px 16px rgba(0,0,0,0.3);transition:all 0.2s ease;';
      a.title = isEn ? 'Cambiar a español' : 'Switch to English';
      a.setAttribute('aria-label', isEn ? 'Cambiar a español' : 'Switch to English');
      var globe = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.85;flex-shrink:0;"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>';
      var labels = isEn 
        ? '<span style="color:#f97316;font-weight:800;">EN</span><span style="color:rgba(255,255,255,0.3);margin:0 2px;">|</span><span style="color:#94a3b8;font-weight:500;">ES</span>' 
        : '<span style="color:#94a3b8;font-weight:500;">EN</span><span style="color:rgba(255,255,255,0.3);margin:0 2px;">|</span><span style="color:#f97316;font-weight:800;">ES</span>';
      a.innerHTML = globe + labels;
      aside.appendChild(a);
      document.body.appendChild(aside);
    }}
  }}

  // 3. Capturar clics en selectores de idioma y en enlaces de navegación
  function bindInteractions() {{
    renderToolHeaderPill();

    document.querySelectorAll('a.np-lang-toggle, a.np-footer-lang').forEach(function(btn) {{
      btn.addEventListener('click', function(e) {{
        var href = btn.getAttribute('href') || '';
        if (href.startsWith('/en/') || href === '/en' || href.indexOf('/en/') !== -1) {{
          setStoredLang('en');
        }} else {{
          setStoredLang('es');
        }}
      }});
    }});

    // Si estamos en versión en inglés, proteger que los clics internos no salgan accidentalmente a español
    if (isEn) {{
      document.addEventListener('click', function(e) {{
        var a = e.target.closest('a');
        if (!a) return;
        if (a.classList.contains('np-lang-toggle') || a.classList.contains('np-footer-lang')) return;
        
        var href = a.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('javascript:')) return;
        
        if (href === '/blog/' || href === '/blog') {{
          e.preventDefault();
          window.location.href = '/en/blog/';
        }} else if (href === '/sobre-nosotros/' || href === '/sobre-nosotros') {{
          e.preventDefault();
          window.location.href = '/en/about-us/';
        }} else if (href === '/herramientas/' || href === '/directorio-herramientas/' || href === '/herramientas') {{
          e.preventDefault();
          window.location.href = '/en/tools/';
        }} else if (href.startsWith('/category/')) {{
          e.preventDefault();
          window.location.href = '/en' + href;
        }} else if (href.startsWith('/herramientas/')) {{
          var hParts = href.replace(/^\\/+|\\/+$/g, '').split('/');
          if (hParts.length >= 3 && hParts[2] in TOOLS_ES_TO_EN) {{
            e.preventDefault();
            window.location.href = '/en/' + TOOLS_ES_TO_EN[hParts[2]] + '.html';
          }} else if (hParts.length >= 2 && hParts[1] === 'guia-uso') {{
            e.preventDefault();
            window.location.href = '/en/user-guide.html';
          }}
        }} else {{
          // Manejo de enlaces relativos como ./crm-pymes.html o crm-pymes.html
          var cleanName = href.replace(/^\\.\\//, '').replace(/\\.html$/, '');
          if (cleanName in TOOLS_ES_TO_EN) {{
            e.preventDefault();
            window.location.href = '/en/' + TOOLS_ES_TO_EN[cleanName] + '.html';
          }}
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
