const fs = require('fs');
const path = require('path');

const envPath = path.resolve(__dirname, '../.env');
let WP_USER = process.env.WP_USER || 'bot_revisor';
let WP_APP_PASS = process.env.WP_APP_PASS || '';
if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const [key, ...rest] = trimmed.split('=');
    const val = rest.join('=').trim();
    if (key.trim() === 'WP_USER') WP_USER = val;
    if (key.trim() === 'WP_APP_PASS') WP_APP_PASS = val;
  }
}
const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64');
const WP_BASE = 'https://dev-nube-para-pymes.pantheonsite.io';
const WP_API = `${WP_BASE}/wp-json/wp/v2`;

const pages = [
  { id: 37, slug: 'sobre-nosotros', name: 'Sobre Nosotros' },
  { id: 2, slug: '', name: 'Inicio' },
  { id: 1047, slug: 'directorio-herramientas', name: 'Directorio de Herramientas' },
  { id: 60, slug: 'metodologia-de-resenas', name: 'Metodología de Reseñas' },
  { id: 62, slug: 'contacto', name: 'Contacto' },
  { id: 64, slug: 'terminos-y-condiciones', name: 'Términos y Condiciones' },
  { id: 58, slug: 'politica-de-privacidad', name: 'Política de Privacidad' },
  { id: 68, slug: 'politica-de-cookies', name: 'Política de Cookies' },
  { id: 776, slug: 'descargo-de-responsabilidad', name: 'Descargo de Responsabilidad' },
  { id: 783, slug: 'aviso-legal', name: 'Aviso Legal' }
];

async function verify() {
  console.log('=== VERIFICACIÓN DE OPTIMIZACIÓN DE PÁGINAS ===\n');

  // 1. Check backups
  const backupDir = path.resolve(__dirname, '../wp_backups/pages');
  const backupFiles = fs.existsSync(backupDir) ? fs.readdirSync(backupDir) : [];
  console.log(`[Backups] ${backupFiles.length} archivos de respaldo guardados en ${backupDir}`);

  // 2. Check Sobre Nosotros details
  const p37Res = await fetch(`${WP_API}/pages/37`);
  if (p37Res.ok) {
    const p37 = await p37Res.json();
    const words = (p37.content?.rendered || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
    console.log(`\n[Sobre Nosotros ID 37]`);
    console.log(`- Longitud de contenido: ~${words} palabras (anteriormente ~210 palabras)`);
    console.log(`- Imagen destacada (featured_media): ID ${p37.featured_media}`);
    console.log(`- Excerpt: "${p37.excerpt?.rendered?.trim().replace(/<[^>]+>/g, '')}"`);
  }

  // 3. Verify public head on each page
  console.log('\n[Verificación de Cabeceras Públicas (<title> y <meta description>)]');
  for (const p of pages) {
    const url = p.slug ? `${WP_BASE}/${p.slug}/` : `${WP_BASE}/`;
    try {
      const res = await fetch(url);
      if (!res.ok) {
        console.log(`❌ [${p.id}] ${p.name}: HTTP ${res.status}`);
        continue;
      }
      const html = await res.text();
      const titleMatch = html.match(/<title>([^<]+)<\/title>/i);
      const descMatch = html.match(/<meta name="description" content="([^"]*)"/i);
      const title = titleMatch ? titleMatch[1] : 'NONE';
      const desc = descMatch ? descMatch[1] : 'NONE';

      const hasTemplateMarker = title.includes('%title%') || desc.includes('%excerpt%');
      console.log(`- [ID ${p.id}] ${p.name}:`);
      console.log(`   Título: "${title}"`);
      console.log(`   Desc:   "${desc}"`);
      if (hasTemplateMarker) {
        console.log(`   ⚠️ ALERTA: Detectado marcador de plantilla.`);
      } else {
        console.log(`   ✅ Metadatos limpios y personalizados.`);
      }
    } catch (err) {
      console.log(`❌ Error verificando [${p.id}] ${p.name}: ${err.message}`);
    }
  }

  console.log('\n=== VERIFICACIÓN FINALIZADA ===');
}

verify().catch(console.error);
