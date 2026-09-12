const fs = require('fs');
const path = require('path');

// Load environment variables from .env
function loadEnv() {
  const envPath = path.resolve(__dirname, '../.env');
  const config = {
    WP_URL: process.env.WP_URL || 'https://dev-nube-para-pymes.pantheonsite.io/wp-json/wp/v2',
    WP_USER: process.env.WP_USER || 'bot_revisor',
    WP_APP_PASS: process.env.WP_APP_PASS || ''
  };

  if (fs.existsSync(envPath)) {
    const lines = fs.readFileSync(envPath, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const [key, ...rest] = trimmed.split('=');
      const val = rest.join('=').trim();
      if (key.trim() === 'WP_URL') config.WP_URL = val;
      if (key.trim() === 'WP_USER') config.WP_USER = val;
      if (key.trim() === 'WP_APP_PASS') config.WP_APP_PASS = val;
    }
  }
  return config;
}

const config = loadEnv();
const authHeader = 'Basic ' + Buffer.from(`${config.WP_USER}:${config.WP_APP_PASS}`).toString('base64');

async function testConnection() {
  console.log(`[WP] Connecting to ${config.WP_URL}...`);
  const res = await fetch(`${config.WP_URL}/users/me`, {
    headers: { 'Authorization': authHeader }
  });
  if (!res.ok) {
    console.error(`[WP] Authentication failed: HTTP ${res.status}`);
    console.error(await res.text());
    process.exit(1);
  }
  const user = await res.json();
  console.log(`[WP] ✅ Connected as "${user.name}" (ID: ${user.id})`);

  const countRes = await fetch(`${config.WP_URL}/posts?per_page=1`, {
    headers: { 'Authorization': authHeader }
  });
  const total = countRes.headers.get('x-wp-total');
  console.log(`[WP] ✅ Total posts available in site: ${total}`);
}

async function listPosts(page = 1, perPage = 10, search = '') {
  let url = `${config.WP_URL}/posts?page=${page}&per_page=${perPage}&_fields=id,slug,title,status,date,categories`;
  if (search) url += `&search=${encodeURIComponent(search)}`;
  
  const res = await fetch(url, { headers: { 'Authorization': authHeader } });
  if (!res.ok) {
    console.error(`[WP] Error listing posts: HTTP ${res.status}`);
    console.error(await res.text());
    process.exit(1);
  }
  const posts = await res.json();
  const total = res.headers.get('x-wp-total');
  const totalPages = res.headers.get('x-wp-totalpages');
  console.log(`[WP] Page ${page}/${totalPages} (Total posts: ${total}):\n`);
  posts.forEach(p => {
    console.log(`- [ID ${p.id}] [${p.status}] "${p.title.rendered}"`);
    console.log(`   Slug: ${p.slug} | Categories: ${JSON.stringify(p.categories)}`);
  });
}

async function getPost(id, saveToFile = true) {
  const res = await fetch(`${config.WP_URL}/posts/${id}?context=edit`, {
    headers: { 'Authorization': authHeader }
  });
  if (!res.ok) {
    console.error(`[WP] Error fetching post ${id}: HTTP ${res.status}`);
    console.error(await res.text());
    process.exit(1);
  }
  const post = await res.json();
  console.log(`[WP] ✅ Retrieved post ID ${post.id}: "${post.title.raw || post.title.rendered}"`);
  console.log(`   Status: ${post.status} | Slug: ${post.slug}`);

  if (saveToFile) {
    const backupDir = path.resolve(__dirname, '../wp_backups');
    if (!fs.existsSync(backupDir)) fs.mkdirSync(backupDir, { recursive: true });
    
    const filePath = path.join(backupDir, `post_${post.id}_backup.json`);
    fs.writeFileSync(filePath, JSON.stringify(post, null, 2), 'utf8');
    
    const htmlPath = path.join(backupDir, `post_${post.id}_content.html`);
    fs.writeFileSync(htmlPath, post.content.raw || post.content.rendered, 'utf8');
    
    console.log(`[WP] 💾 Backup saved: ${filePath}`);
    console.log(`[WP] 💾 Content saved: ${htmlPath}`);
  }
  return post;
}

async function updatePost(id, contentFile, extraFields = {}) {
  // Always backup first!
  console.log(`[WP] Backing up post ${id} before update...`);
  await getPost(id, true);

  let newContent = '';
  if (contentFile && fs.existsSync(contentFile)) {
    newContent = fs.readFileSync(contentFile, 'utf8');
  } else if (contentFile) {
    newContent = contentFile;
  }

  const payload = { ...extraFields };
  if (newContent) {
    payload.content = newContent;
  }

  console.log(`[WP] Sending update for post ${id} (${Object.keys(payload).join(', ')})...`);
  const res = await fetch(`${config.WP_URL}/posts/${id}`, {
    method: 'PUT',
    headers: {
      'Authorization': authHeader,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!res.ok) {
    console.error(`[WP] Error updating post ${id}: HTTP ${res.status}`);
    console.error(await res.text());
    process.exit(1);
  }

  const updated = await res.json();
  console.log(`[WP] 🚀 Post ${id} successfully updated!`);
  console.log(`   Link: ${updated.link}`);
  return updated;
}

// CLI dispatcher
async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'test';

  if (command === 'test') {
    await testConnection();
  } else if (command === 'list') {
    const page = parseInt(args[1] || '1', 10);
    const perPage = parseInt(args[2] || '10', 10);
    const search = args[3] || '';
    await listPosts(page, perPage, search);
  } else if (command === 'get') {
    const id = args[1];
    if (!id) {
      console.error('Usage: node scripts/wp_client.js get <post_id>');
      process.exit(1);
    }
    await getPost(id);
  } else if (command === 'update') {
    const id = args[1];
    const file = args[2];
    const excerpt = args[3];
    if (!id || !file) {
      console.error('Usage: node scripts/wp_client.js update <post_id> <content_file_or_string> [excerpt]');
      process.exit(1);
    }
    const extra = {};
    if (excerpt) extra.excerpt = excerpt;
    await updatePost(id, file, extra);
  } else if (command === 'verify') {
    const ids = [1362, 1361, 1360, 723, 736];
    console.log('[WP] Verifying status of recent posts:');
    for (const id of ids) {
      const res = await fetch(`${config.WP_URL}/posts/${id}`);
      if (res.ok) {
        const p = await res.json();
        const wordCount = (p.content.rendered || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
        console.log(`- [ID ${p.id}] "${p.title.rendered}"`);
        console.log(`   Words: ~${wordCount} | Modified: ${p.modified} | Status: ${p.status}`);
      }
    }
  } else {
    console.log(`Unknown command: ${command}`);
    console.log('Available commands: test, list, get, update, verify');
  }
}

main().catch(err => {
  console.error('[WP] Fatal error:', err);
  process.exit(1);
});
