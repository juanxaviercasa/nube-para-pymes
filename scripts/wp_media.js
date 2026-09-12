const fs = require('fs');
const path = require('path');

const envPath = path.resolve(__dirname, '../.env');
let WP_URL = process.env.WP_URL || 'https://dev-nube-para-pymes.pantheonsite.io/wp-json/wp/v2';
let WP_USER = process.env.WP_USER || 'bot_revisor';
let WP_APP_PASS = process.env.WP_APP_PASS || '';

if (fs.existsSync(envPath)) {
  const lines = fs.readFileSync(envPath, 'utf8').split('\n');
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const [key, ...rest] = trimmed.split('=');
    const val = rest.join('=').trim();
    if (key.trim() === 'WP_URL') WP_URL = val;
    if (key.trim() === 'WP_USER') WP_USER = val;
    if (key.trim() === 'WP_APP_PASS') WP_APP_PASS = val;
  }
}

const authHeader = 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64');

async function uploadImage(filePath, title, altText, postId = null) {
  const filename = path.basename(filePath);
  const fileBuffer = fs.readFileSync(filePath);
  const mimeType = filePath.endsWith('.png') ? 'image/png' : 'image/jpeg';

  console.log(`[Media] Uploading ${filename} (${fileBuffer.length} bytes)...`);
  const res = await fetch(`${WP_URL}/media`, {
    method: 'POST',
    headers: {
      'Authorization': authHeader,
      'Content-Disposition': `attachment; filename="${filename}"`,
      'Content-Type': mimeType
    },
    body: fileBuffer
  });

  if (!res.ok) {
    console.error(`[Media] Upload error: HTTP ${res.status}`);
    console.error(await res.text());
    process.exit(1);
  }

  const media = await res.json();
  console.log(`[Media] ✅ Image uploaded successfully! ID: ${media.id}`);
  console.log(`[Media] URL: ${media.source_url}`);

  // Update alt text, title
  const updateRes = await fetch(`${WP_URL}/media/${media.id}`, {
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

  const updatedMedia = await updateRes.json();
  console.log(`[Media] ✅ Alt text updated to: "${updatedMedia.alt_text}"`);

  // If postId is provided and we want it as featured_media
  if (postId) {
    console.log(`[Media] Attaching as featured_media to post ${postId}...`);
    const postUpdateRes = await fetch(`${WP_URL}/posts/${postId}`, {
      method: 'PUT',
      headers: {
        'Authorization': authHeader,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        featured_media: media.id
      })
    });
    if (postUpdateRes.ok) {
      console.log(`[Media] 🚀 Post ${postId} featured_media set to ${media.id}!`);
    } else {
      console.error(`[Media] Failed to set featured_media:`, await postUpdateRes.text());
    }
  }

  return updatedMedia;
}

// Test upload with the generated image
const testFile = 'C:\\Users\\pc\\.gemini\\antigravity-ide\\brain\\d10c9c52-3f61-4e5b-9392-b97e94a80570\\seo_geo_pymes_featured_1789149584489.jpg';
uploadImage(testFile, 'Estrategia de SEO y GEO para Pymes en Buscadores e Inteligencia Artificial', 'seo y geo para pymes medicion de visibilidad en google y respuestas de ia', 1362)
  .catch(console.error);
