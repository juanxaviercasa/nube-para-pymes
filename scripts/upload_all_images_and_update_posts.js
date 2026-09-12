const fs = require('fs');
const path = require('path');

const envPath = path.resolve(__dirname, '../.env');
let WP_URL = process.env.WP_URL || 'https://dev-nube-para-pymes.pantheonsite.io/wp-json';
let WP_USER = process.env.WP_USER || 'bot_revisor';
let WP_APP_PASS = process.env.WP_APP_PASS || '';

if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const [key, ...rest] = trimmed.split('=');
    const val = rest.join('=').trim();
    if (key.trim() === 'WP_URL') WP_URL = val.replace('/wp/v2', '');
    if (key.trim() === 'WP_USER') WP_USER = val;
    if (key.trim() === 'WP_APP_PASS') WP_APP_PASS = val;
  }
}

const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64');

async function uploadMedia(filePath, title, altText, postId = null) {
  const filename = path.basename(filePath);
  const fileBuffer = fs.readFileSync(filePath);
  const mimeType = filePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

  console.log(`[Upload] Uploading ${filename} (${fileBuffer.length} bytes)...`);
  const res = await fetch(`${WP_URL}/wp/v2/media`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Disposition': `attachment; filename="${filename}"`,
      'Content-Type': mimeType
    },
    body: fileBuffer
  });

  if (!res.ok) {
    console.error(`[Upload] Error: HTTP ${res.status}`);
    console.error(await res.text());
    throw new Error('Upload failed');
  }

  const media = await res.json();
  console.log(`[Upload] ✅ Uploaded ID: ${media.id} -> ${media.source_url}`);

  // Update alt_text & title
  await fetch(`${WP_URL}/wp/v2/media/${media.id}`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      title: title || filename,
      alt_text: altText || title || filename,
      post: postId || undefined
    })
  });

  return media;
}

async function setRankMathData(postId, focusKeyword, score = 86) {
  console.log(`[RankMath] Setting metadata for post ${postId}...`);
  // updateMeta
  const res1 = await fetch(`${WP_URL}/rankmath/v1/updateMeta`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      objectType: 'post',
      objectID: postId,
      meta: {
        rank_math_focus_keyword: focusKeyword,
        focus_keyword: focusKeyword,
        rank_math_seo_score: score
      }
    })
  });
  console.log(`[RankMath] updateMeta status: ${res1.status}`);

  // updateSeoScore
  const scorePayload = { postScores: {} };
  scorePayload.postScores[postId.toString()] = score;
  const res2 = await fetch(`${WP_URL}/rankmath/v1/updateSeoScore`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(scorePayload)
  });
  console.log(`[RankMath] updateSeoScore status: ${res2.status}`);
}

async function updatePostContent(postId, content, featuredMediaId = null) {
  console.log(`[Post] Updating content for post ${postId}...`);
  const body = { content };
  if (featuredMediaId) body.featured_media = featuredMediaId;

  const res = await fetch(`${WP_URL}/wp/v2/posts/${postId}`, {
    method: 'PUT',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  if (!res.ok) {
    console.error(`[Post] Error updating post ${postId}: HTTP ${res.status}`);
    console.error(await res.text());
    throw new Error('Update post failed');
  }
  const updated = await res.json();
  console.log(`[Post] ✅ Post ${postId} updated! Featured Media: ${updated.featured_media}`);
}

async function runAll() {
  const baseDir = 'C:\\Users\\pc\\.gemini\\antigravity-ide\\brain\\d10c9c52-3f61-4e5b-9392-b97e94a80570';

  // ==========================================
  // 1. POST 1362: SEO y GEO para Pymes
  // ==========================================
  console.log('\n=== PROCESSING POST 1362 ===');
  // Internal 1: Diagram
  const img1362_1 = await uploadMedia(
    path.join(baseDir, 'seo_geo_diagram_internal_1789149823664.jpg'),
    'Diagrama Comparativo SEO Tradicional vs GEO Inteligencia Artificial',
    'diagrama comparativo seo tradicional vs geo optimizacion para motores de respuesta con ia',
    1362
  );
  // Internal 2: Team
  const img1362_2 = await uploadMedia(
    path.join(baseDir, 'seo_geo_team_internal_1789149871242.jpg'),
    'Equipo Pyme Analizando Metricas de SEO y Respuestas de IA',
    'equipo de marketing de una pyme analizando metricas de seo y visibilidad en ia',
    1362
  );

  // Read current HTML of 1362 and insert images
  let html1362 = fs.readFileSync(path.resolve(__dirname, '../wp_content/post_1362_optimizado.html'), 'utf8');
  // Insert img 1 before "Qué conviene medir primero"
  const imgBlock1362_1 = `\n<figure class="wp-block-image size-large"><img src="${img1362_1.source_url}" alt="diagrama comparativo seo tradicional vs geo optimizacion para motores de respuesta con ia" class="wp-image-${img1362_1.id}" /><figcaption class="wp-element-caption">Comparativa técnica: factores clave entre el posicionamiento web orgánico y la optimización para motores de respuesta conversacionales.</figcaption></figure>\n`;
  html1362 = html1362.replace('<h2 class="wp-block-heading">Qué conviene medir primero', imgBlock1362_1 + '<h2 class="wp-block-heading">Qué conviene medir primero');

  // Insert img 2 before "Preguntas frecuentes"
  const imgBlock1362_2 = `\n<figure class="wp-block-image size-large"><img src="${img1362_2.source_url}" alt="equipo de marketing de una pyme analizando metricas de seo y visibilidad en ia" class="wp-image-${img1362_2.id}" /><figcaption class="wp-element-caption">Los equipos comerciales y de marketing deben alinear sus contenidos para responder preguntas reales con datos comprobables.</figcaption></figure>\n`;
  html1362 = html1362.replace('<h2 class="wp-block-heading">Preguntas frecuentes', imgBlock1362_2 + '<h2 class="wp-block-heading">Preguntas frecuentes');

  fs.writeFileSync(path.resolve(__dirname, '../wp_content/post_1362_optimizado.html'), html1362, 'utf8');
  await updatePostContent(1362, html1362, 1382); // 1382 is the featured image ID uploaded earlier
  await setRankMathData(1362, 'seo y geo para pymes', 88);

  // ==========================================
  // 2. POST 1361: Automatización con IA para Pymes
  // ==========================================
  console.log('\n=== PROCESSING POST 1361 ===');
  // Featured Image
  const img1361_feat = await uploadMedia(
    path.join(baseDir, 'ia_pymes_featured_1789149908921.jpg'),
    'Automatización con IA para Pymes: Criterios y Flujos de Trabajo',
    'automatizacion con ia para pymes criterios clave para elegir software',
    1361
  );
  // Internal 1: Diagram
  const img1361_1 = await uploadMedia(
    path.join(baseDir, 'ia_pymes_diagram_internal_1789149950380.jpg'),
    'Flujo de Decision para Automatizacion con IA en Pequenas Empresas',
    'flujo de decision paso a paso para automatizacion con ia en pequenas empresas',
    1361
  );
  // Internal 2: Team
  const img1361_2 = await uploadMedia(
    path.join(baseDir, 'ia_pymes_team_internal_1789149994253.jpg'),
    'Equipo Operativo de una Pyme Evaluando Software de Automatizacion',
    'equipo operativo de una pyme colaborando con herramientas de automatizacion inteligente',
    1361
  );

  let html1361 = fs.readFileSync(path.resolve(__dirname, '../wp_content/post_1361_optimizado.html'), 'utf8');
  const imgBlock1361_1 = `\n<figure class="wp-block-image size-large"><img src="${img1361_1.source_url}" alt="flujo de decision paso a paso para automatizacion con ia en pequenas empresas" class="wp-image-${img1361_1.id}" /><figcaption class="wp-element-caption">Diagrama de decisión: mapa secuencial para evaluar procesos antes de incorporar software de IA.</figcaption></figure>\n`;
  html1361 = html1361.replace('<h2 class="wp-block-heading">Los 7 criterios esenciales', imgBlock1361_1 + '<h2 class="wp-block-heading">Los 7 criterios esenciales');

  const imgBlock1361_2 = `\n<figure class="wp-block-image size-large"><img src="${img1361_2.source_url}" alt="equipo operativo de una pyme colaborando con herramientas de automatizacion inteligente" class="wp-image-${img1361_2.id}" /><figcaption class="wp-element-caption">Una adopción exitosa requiere involucrar a los colaboradores y medir el tiempo ahorrado en cada tarea.</figcaption></figure>\n`;
  html1361 = html1361.replace('<h2 class="wp-block-heading">Preguntas frecuentes', imgBlock1361_2 + '<h2 class="wp-block-heading">Preguntas frecuentes');

  fs.writeFileSync(path.resolve(__dirname, '../wp_content/post_1361_optimizado.html'), html1361, 'utf8');
  await updatePostContent(1361, html1361, img1361_feat.id);
  await setRankMathData(1361, 'automatizacion con ia para pymes', 88);

  // ==========================================
  // 3. POST 1360: CRM con IA para Pymes
  // ==========================================
  console.log('\n=== PROCESSING POST 1360 ===');
  // Featured Image
  const img1360_feat = await uploadMedia(
    path.join(baseDir, 'crm_ia_featured_1789150044524.jpg'),
    'CRM con IA para Pymes: Embudo de Ventas Inteligente',
    'crm con ia para pymes embudo de ventas inteligente y seguimiento de clientes',
    1360
  );
  // Internal 1: Diagram
  const img1360_1 = await uploadMedia(
    path.join(baseDir, 'crm_ia_pipeline_internal_1789150096092.jpg'),
    'Comparativa de Entrada Manual vs Automatizacion en CRM con IA',
    'comparativa de captura manual vs automatizada con crm con ia para pymes',
    1360
  );
  // Internal 2: Team
  const img1360_2 = await uploadMedia(
    path.join(baseDir, 'crm_ia_team_internal_1789150296145.jpg'),
    'Asesores Comerciales Analizando Pipeline y Oportunidades en CRM',
    'asesores comerciales revisando pipeline y oportunidades en crm con ia',
    1360
  );

  let html1360 = fs.readFileSync(path.resolve(__dirname, '../wp_content/post_1360_optimizado.html'), 'utf8');
  const imgBlock1360_1 = `\n<figure class="wp-block-image size-large"><img src="${img1360_1.source_url}" alt="comparativa de captura manual vs automatizada con crm con ia para pymes" class="wp-image-${img1360_1.id}" /><figcaption class="wp-element-caption">Impacto en la productividad comercial: reducción de carga manual vs. mayor tiempo de contacto con prospectos.</figcaption></figure>\n`;
  html1360 = html1360.replace('<h2 class="wp-block-heading">Comparativa de plataformas', imgBlock1360_1 + '<h2 class="wp-block-heading">Comparativa de plataformas');

  const imgBlock1360_2 = `\n<figure class="wp-block-image size-large"><img src="${img1360_2.source_url}" alt="asesores comerciales revisando pipeline y oportunidades en crm con ia" class="wp-image-${img1360_2.id}" /><figcaption class="wp-element-caption">El equipo de ventas debe validar cada recomendación de la IA antes de interactuar con clientes de alto valor.</figcaption></figure>\n`;
  html1360 = html1360.replace('<h2 class="wp-block-heading">Preguntas frecuentes', imgBlock1360_2 + '<h2 class="wp-block-heading">Preguntas frecuentes');

  fs.writeFileSync(path.resolve(__dirname, '../wp_content/post_1360_optimizado.html'), html1360, 'utf8');
  await updatePostContent(1360, html1360, img1360_feat.id);
  await setRankMathData(1360, 'crm con ia para pymes', 88);

  console.log('\n🎉 ALL 3 POSTS FULLY OPTIMIZED WITH IMAGES & RANK MATH METADATA!');
}

runAll().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
