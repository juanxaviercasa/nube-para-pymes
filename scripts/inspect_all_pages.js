const authHeader = 'Basic ' + Buffer.from('bot_revisor:2hzI DUS0 IJyt 1JOs P8hH 8Xdo').toString('base64');
const WP_URL = 'https://dev-nube-para-pymes.pantheonsite.io/wp-json';

async function run() {
  const res = await fetch(`${WP_URL}/wp/v2/pages?per_page=100`, {
    headers: { 'Authorization': authHeader }
  });
  const pages = await res.json();
  
  // Also fetch page 58 if not in list
  if (!pages.find(p => p.id === 58)) {
    const p58Res = await fetch(`${WP_URL}/wp/v2/pages/58`);
    if (p58Res.ok) {
      pages.push(await p58Res.json());
    }
  }

  console.log(`Found ${pages.length} pages total:`);
  for (const p of pages) {
    const wordCount = (p.content?.rendered || '').replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
    console.log(`\n-----------------------------------------`);
    console.log(`[ID ${p.id}] "${p.title.rendered}"`);
    console.log(`Slug: ${p.slug} | Status: ${p.status} | Words: ~${wordCount} | Featured Media: ${p.featured_media}`);
    
    // Check Rank Math meta via schema / updateMeta or getMeta if available
    // Let's check what post_meta or Rank Math meta exists by querying rankmath if there is a get endpoint or inspecting page
  }
}

run().catch(console.error);
