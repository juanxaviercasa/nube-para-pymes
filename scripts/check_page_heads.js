const WP_BASE = 'https://dev-nube-para-pymes.pantheonsite.io';

const pages = [
  { id: 2, slug: '', name: 'Inicio' },
  { id: 37, slug: 'sobre-nosotros', name: 'Sobre Nosotros' },
  { id: 60, slug: 'metodologia-de-resenas', name: 'Metodología de Reseñas' },
  { id: 62, slug: 'contacto', name: 'Contacto' },
  { id: 64, slug: 'terminos-y-condiciones', name: 'Términos y Condiciones' },
  { id: 68, slug: 'politica-de-cookies', name: 'Política de Cookies' },
  { id: 58, slug: 'politica-de-privacidad', name: 'Política de Privacidad' },
  { id: 776, slug: 'descargo-de-responsabilidad', name: 'Descargo de Responsabilidad' },
  { id: 783, slug: 'aviso-legal', name: 'Aviso Legal' },
  { id: 1047, slug: 'directorio-herramientas', name: 'Directorio de Herramientas Gratuitas para Pymes' },
  { id: 39, slug: 'blog', name: 'Blog' }
];

async function checkHead() {
  for (const p of pages) {
    const url = p.slug ? `${WP_BASE}/${p.slug}/` : `${WP_BASE}/`;
    const res = await fetch(url);
    if (!res.ok) {
      console.log(`[${p.id}] ${p.name} -> HTTP ${res.status}`);
      continue;
    }
    const html = await res.text();
    const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
    const descMatch = html.match(/<meta name="description" content="([^"]*)"/i);
    const robotsMatch = html.match(/<meta name="robots" content="([^"]*)"/i);
    
    console.log(`\n========================================`);
    console.log(`[ID ${p.id}] ${p.name} (${url})`);
    console.log(`Title: ${titleMatch ? titleMatch[1] : 'NONE'}`);
    console.log(`Desc:  ${descMatch ? descMatch[1] : 'NONE'}`);
    console.log(`Robots: ${robotsMatch ? robotsMatch[1] : 'NONE'}`);
  }
}

checkHead().catch(console.error);
