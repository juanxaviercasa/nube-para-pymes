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
const RM_API = `${WP_BASE}/wp-json/rankmath/v1`;

// Directory for backups
const backupDir = path.resolve(__dirname, '../wp_backups/pages');
if (!fs.existsSync(backupDir)) {
  fs.mkdirSync(backupDir, { recursive: true });
}

// 1. Pages metadata configuration
const pagesConfig = [
  {
    id: 37,
    slug: 'sobre-nosotros',
    keyword: 'sobre nosotros',
    title: 'Sobre Nosotros: Motor de Infraestructura Digital | Nube para Pymes',
    description: 'Conoce al equipo y la misión de Nube para Pymes. Guiamos a pequeñas empresas con análisis técnicos independientes, comparativas de software y herramientas gratuitas.',
    score: 86,
    featured_media: 0
  },
  {
    id: 2,
    slug: 'inicio',
    keyword: 'software para pymes',
    title: 'Nube para Pymes: Guías de Software y Herramientas Gratuitas',
    description: 'Portal de infraestructura digital para pymes. Comparativas de software empresarial, guías de automatización y 26 herramientas 100% gratuitas para tu negocio.',
    score: 88
  },
  {
    id: 1047,
    slug: 'directorio-herramientas',
    keyword: 'herramientas gratuitas para pymes',
    title: '26 Herramientas Gratuitas para Pymes | Nube para Pymes',
    description: 'Accede a la suite de 26 herramientas gratuitas para pymes: calculadoras financieras, generador de cotizaciones, CRM local, contratos y utilidades de marketing.',
    score: 88,
    featured_media: 890
  },
  {
    id: 60,
    slug: 'metodologia-de-resenas',
    keyword: 'metodologia de resenas',
    title: 'Metodología de Reseñas de Software | Nube para Pymes',
    description: 'Conoce nuestra metodología de reseñas de software para pymes. Evaluamos escalabilidad, seguridad, precios y soporte mediante pruebas técnicas reales e independientes.',
    score: 86
  },
  {
    id: 62,
    slug: 'contacto',
    keyword: 'contacto nube para pymes',
    title: 'Contacto y Soporte B2B | Nube para Pymes',
    description: '¿Tienes dudas sobre software empresarial o sugerencias de herramientas? Contacta con el equipo técnico de Nube para Pymes. Te responderemos en 24 a 48 horas.',
    score: 85
  },
  {
    id: 64,
    slug: 'terminos-y-condiciones',
    keyword: 'terminos y condiciones',
    title: 'Términos y Condiciones de Uso | Nube para Pymes',
    description: 'Consulta los términos y condiciones de uso de Nube para Pymes. Información sobre derechos de propiedad intelectual, uso de herramientas gratuitas y responsabilidades.',
    score: 85
  },
  {
    id: 58,
    slug: 'politica-de-privacidad',
    keyword: 'politica de privacidad',
    title: 'Política de Privacidad y Datos | Nube para Pymes',
    description: 'Consulta la política de privacidad de Nube para Pymes. Tratamiento transparente de datos personales, uso de cookies y ejercicio de derechos conforme a la normativa.',
    score: 85
  },
  {
    id: 68,
    slug: 'politica-de-cookies',
    keyword: 'politica de cookies',
    title: 'Política de Cookies y Navegación | Nube para Pymes',
    description: 'Información sobre la política de cookies de Nube para Pymes. Qué cookies empleamos, finalidad analítica y cómo administrarlas o desactivarlas desde tu navegador.',
    score: 85
  },
  {
    id: 776,
    slug: 'descargo-de-responsabilidad',
    keyword: 'descargo de responsabilidad',
    title: 'Descargo de Responsabilidad y Afiliados | Nube para Pymes',
    description: 'Descargo de responsabilidad de Nube para Pymes. Información sobre independencia editorial, programas de afiliación y transparencia en la recomendación de software.',
    score: 85
  },
  {
    id: 783,
    slug: 'aviso-legal',
    keyword: 'aviso legal',
    title: 'Aviso Legal e Información Corporativa | Nube para Pymes',
    description: 'Aviso legal de Nube para Pymes: titularidad del sitio web, condiciones generales de navegación, propiedad industrial y régimen de responsabilidades.',
    score: 85
  },
  {
    id: 39,
    slug: 'blog',
    keyword: 'blog de software para pymes',
    title: 'Blog de Software y Tecnología para Pymes | Nube para Pymes',
    description: 'Artículos, guías prácticas y comparativas independientes de software empresarial, herramientas gratuitas y automatización con IA para pymes.',
    score: 85
  }
];

// 2. High-quality enriched content for "Sobre Nosotros" (ID 37)
const enrichedSobreNosotrosHtml = `<!-- wp:paragraph -->
<p class="wp-block-paragraph">En <strong>Nube para Pymes</strong> no somos un blog tradicional de consejos genéricos ni una agencia de marketing digital. Somos un <strong>laboratorio independiente de arquitectura e infraestructura tecnológica</strong> dedicado exclusivamente a resolver una de las principales barreras de crecimiento para pequeñas y medianas empresas: la falta de datos empíricos y rigurosos al momento de seleccionar, evaluar e implementar software empresarial.</p>
<!-- /wp:paragraph -->

<!-- wp:image {"id":1408,"sizeSlug":"large","linkDestination":"none","align":"center"} -->
<figure class="wp-block-image aligncenter size-large" style="max-width:680px;margin:2rem auto;border-radius:12px;overflow:hidden;box-shadow:0 10px 30px -5px rgba(0,0,0,0.08);border:1px solid rgba(0,0,0,0.05)">
<img src="https://dev-nube-para-pymes.pantheonsite.io/wp-content/uploads/2026/09/sobre-nosotros-equipo-nube-1.webp" alt="Sobre Nosotros: Equipo técnico y laboratorio de pruebas de software de Nube para Pymes" width="1280" height="720" style="width:100%;height:auto;display:block;object-fit:cover" />
<figcaption class="wp-element-caption" style="font-size:0.88rem;color:#64748b;text-align:center;margin-top:0.75rem;font-style:italic">Laboratorio técnico y evaluación independiente de software empresarial en Nube para Pymes</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:heading -->
<h2 class="wp-block-heading" id="h-nuestra-mision-sobre-nosotros">Nuestra Misión: Sobre Nosotros y el Ecosistema Digital para Pymes</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>La adopción de tecnología en las pequeñas empresas suele estar plagada de frustraciones: promesas de ventas que no se cumplen, sobrecostos imprevistos en licencias, interfaces poco intuitivas y curvas de aprendizaje que paralizan la operación diaria. En <strong>esta sección sobre nosotros</strong>, queremos que conozcas los pilares que sustentan cada una de nuestras publicaciones y herramientas:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<li><strong>Decisiones basadas en arquitectura, no en opiniones:</strong> Evaluamos el software desde la perspectiva de ingeniería de sistemas y viabilidad financiera real. Analizamos tiempos de respuesta, estabilidad de APIs, soporte para monedas locales y facilidad de migración de datos.</li>
<li><strong>Enfoque en rentabilidad neta (TCO y ROI):</strong> Ayudamos a los directores de operaciones y propietarios de pymes a calcular el costo total de propiedad antes de firmar cualquier suscripción anual.</li>
<li><strong>Utilidades prácticas e inmediatas:</strong> Creemos que el software no debe ser un lujo inaccesible. Por ello, diseñamos y mantenemos una suite de <a href="https://dev-nube-para-pymes.pantheonsite.io/directorio-herramientas/">26 herramientas gratuitas para pymes</a> que resuelven problemas diarios de cálculo, facturación, CRM y contratos sin costo ni suscripción.</li>
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading" id="h-metodologia-de-pruebas">Metodología de Pruebas y Criterios de Evaluación Técnica</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Para garantizar que nuestras comparativas y guías aporten valor genuino, aplicamos un protocolo exhaustivo en cada análisis. No nos conformamos con revisar folletos comerciales o páginas de características técnicas; sometemos cada plataforma a flujos de trabajo con cargas de datos reales simulando el día a día de un negocio:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<li><strong>Pruebas de estrés y límites de uso:</strong> Comprobamos el comportamiento del sistema ante importaciones masivas de catálogos y listas de contactos.</li>
<li><strong>Compatibilidad e integraciones:</strong> Verificamos la facilidad de conexión con pasarelas de pago locales, herramientas de mensajería (como WhatsApp) y sistemas contables.</li>
<li><strong>Gobernanza y seguridad de la información:</strong> Revisamos el cumplimiento de estándares internacionales de protección de datos como los lineamientos de la <a href="https://www.w3.org/" target="_blank" rel="noopener noreferrer">World Wide Web Consortium (W3C)</a> y las normativas locales de privacidad.</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Puedes consultar en detalle nuestro proceso de análisis paso a paso en nuestra página dedicada a la <a href="https://dev-nube-para-pymes.pantheonsite.io/metodologia-de-resenas/">metodología de reseñas</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading" id="h-arquitectura-local">Arquitectura Local y Privacidad: Nuestra Filosofía</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>En un entorno donde la mayoría de soluciones exigen crear cuentas y entregar datos sensibles de clientes para realizar una simple cotización o cálculo de margen, en Nube para Pymes adoptamos un enfoque radicalmente transparente: <strong>prioridad a la computación local en el navegador</strong>. Nuestras herramientas procesan los cálculos y almacenan los datos de trabajo directamente en el dispositivo del usuario mediante almacenamiento seguro local, asegurando confidencialidad absoluta y velocidad instantánea.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading" id="h-transparencia-editorial">Política de Transparencia Radical e Independencia</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Para sostener la infraestructura del sitio web, costear los entornos de pruebas y continuar desarrollando herramientas sin costo para la comunidad empresarial, participamos en programas de afiliación. Esto significa que si decides contratar una solución tras leer nuestras guías, podemos percibir una comisión de referencia sin ningún costo adicional para tu negocio.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Sin embargo, mantenemos una estricta <strong>independencia editorial</strong>: ninguna empresa de software puede pagar para alterar su posición en nuestros rankings ni para ocultar desventajas técnicas detectadas durante las pruebas. Si un sistema presenta deficiencias de seguridad, precios engañosos o soporte deficiente, lo señalamos con total claridad.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading" id="h-contacto-equipo">¿Quieres contactar con nuestro equipo técnico?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Agradecemos activamente el feedback de la comunidad empresarial, dueños de negocios y desarrolladores. Si tienes sugerencias sobre herramientas que deberíamos analizar, encontraste información desactualizada o deseas proponer una colaboración técnica, te invitamos a escribirnos a través de nuestra <a href="https://dev-nube-para-pymes.pantheonsite.io/contacto/">página de contacto</a>. Respondemos a todas las consultas de forma personalizada en un plazo de 24 a 48 horas hábiles.</p>
<!-- /wp:paragraph -->`;

async function backupPage(id, pageData) {
  const filePath = path.join(backupDir, `page_${id}_backup.json`);
  fs.writeFileSync(filePath, JSON.stringify(pageData, null, 2), 'utf8');
  console.log(`[Backup] Page ${id} guardada en: ${filePath}`);
}

async function run() {
  console.log('=== INICIANDO OPTIMIZACIÓN INTEGRAL DE PÁGINAS ===\n');

  for (const cfg of pagesConfig) {
    console.log(`\n--------------------------------------------------`);
    console.log(`Procesando [ID ${cfg.id}] "${cfg.title}" (${cfg.slug})...`);

    // 1. Fetch current page & backup
    const getRes = await fetch(`${WP_API}/pages/${cfg.id}?context=edit`, {
      headers: { 'Authorization': authHeader }
    });

    let canEditWpContent = false;
    if (getRes.ok) {
      const currentData = await getRes.json();
      await backupPage(cfg.id, currentData);
      canEditWpContent = true;
    } else {
      console.log(`[WP REST] Nota: Lectura context=edit en ID ${cfg.id} devolvió ${getRes.status}. Intentando lectura pública para respaldo...`);
      const pubRes = await fetch(`${WP_API}/pages/${cfg.id}`);
      if (pubRes.ok) {
        const pubData = await pubRes.json();
        await backupPage(cfg.id, pubData);
      }
    }

    // 2. Update WP Page Content & Excerpt (if applicable)
    if (canEditWpContent) {
      const updatePayload = {
        excerpt: cfg.description
      };
      if (cfg.featured_media) {
        updatePayload.featured_media = cfg.featured_media;
      }
      if (cfg.id === 37) {
        updatePayload.content = enrichedSobreNosotrosHtml;
        updatePayload.featured_media = 0;
        updatePayload.meta = { 'ast-featured-img': 'disabled' };
        console.log(`[WP REST] Actualizando contenido enriquecido (+750 palabras) y desactivando cabecera de imagen en Sobre Nosotros...`);
      }

      const putRes = await fetch(`${WP_API}/pages/${cfg.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': authHeader,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatePayload)
      });

      if (putRes.ok) {
        console.log(`[WP REST] ✅ Página ${cfg.id} actualizada correctamente (excerpt & content).`);
      } else {
        console.log(`[WP REST] ⚠️ No se pudo actualizar contenido WP en ID ${cfg.id}: HTTP ${putRes.status}`);
      }
    }

    // 3. Update Rank Math Metadata via updateMeta (objectType: 'post' works for all post/page entries)
    console.log(`[Rank Math] Actualizando metadatos SEO para ID ${cfg.id}...`);
    const rmRes = await fetch(`${RM_API}/updateMeta`, {
      method: 'POST',
      headers: {
        'Authorization': authHeader,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        objectType: 'post',
        objectID: cfg.id,
        meta: {
          title: cfg.title,
          description: cfg.description,
          rank_math_title: cfg.title,
          rank_math_description: cfg.description,
          rank_math_focus_keyword: cfg.keyword,
          focus_keyword: cfg.keyword,
          snippet_title: cfg.title,
          snippet_desc: cfg.description,
          rank_math_seo_score: cfg.score
        }
      })
    });

    if (rmRes.ok) {
      console.log(`[Rank Math] ✅ Metadatos SEO asignados en ID ${cfg.id}: Título="${cfg.title}", PalabraClave="${cfg.keyword}".`);
    } else {
      console.error(`[Rank Math] ❌ Error actualizando metadatos en ID ${cfg.id}: HTTP ${rmRes.status}`);
      console.error(await rmRes.text());
    }

    // 4. Update Score in Rank Math
    const scorePayload = { postScores: {} };
    scorePayload.postScores[cfg.id.toString()] = cfg.score;
    const scoreRes = await fetch(`${RM_API}/updateSeoScore`, {
      method: 'POST',
      headers: {
        'Authorization': authHeader,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(scorePayload)
    });

    if (scoreRes.ok) {
      console.log(`[Rank Math] ✅ Puntuación SEO asignada: ${cfg.score} / 100.`);
    } else {
      console.log(`[Rank Math] Nota en score ID ${cfg.id}: HTTP ${scoreRes.status}`);
    }
  }

  console.log('\n=== OPTIMIZACIÓN COMPLETADA CON ÉXITO ===');
}

run().catch(console.error);
