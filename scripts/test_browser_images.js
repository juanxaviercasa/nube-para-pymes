const {chromium} = require('playwright');
const {createServer} = require('./preview_server');
const fs = require('node:fs');
const assert = require('node:assert/strict');

(async () => {
    const server = createServer();
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    const base = `http://127.0.0.1:${server.address().port}`;
    const chrome = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
    const browser = await chromium.launch({executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || (fs.existsSync(chrome) ? chrome : undefined), headless: true});
    try {
        for (const width of [390, 1366]) {
            const page = await browser.newPage({viewport: {width, height: 900}});
            await page.route('**/*', route => new URL(route.request().url()).origin === base ? route.continue() : route.abort());
            for (const route of ['/', '/blog/', '/blog/page/2/', '/seo-geo-para-pymes-visibilidad-ia/', '/alternativas-gratuitas-asana/', '/mejores-crm-gratuitos-espanol/', '/en/blog/', '/en/free-asana-alternatives/']) {
                await page.goto(base + route, {waitUntil: 'load'});
                const images = page.locator('img[src*="/wp-content/uploads/"]');
                assert.ok(await images.count() > 0, `No media on ${route}`);
                // Force lazy images to load, including those below the fold.
                await images.evaluateAll(items => items.forEach(img => img.loading = 'eager'));
                await page.waitForFunction(() => [...document.querySelectorAll('img[src*="/wp-content/uploads/"]')].every(img => img.complete), null, {timeout: 15000});
                const broken = await images.evaluateAll(items => items.filter(img => !img.naturalWidth || new URL(img.currentSrc).origin !== location.origin).map(img => img.currentSrc));
                assert.deepEqual(broken, [], `${width}px ${route}`);
                console.log(`OK ${width}px ${route}: ${await images.count()} images loaded`);
                if (width === 1366 && route === '/blog/') {
                    fs.mkdirSync('artifacts', {recursive: true});
                    await page.screenshot({path: 'artifacts/blog-images-fixed.png'});
                }
            }
            await page.close();
        }
    } finally {
        await browser.close();
        await new Promise(resolve => server.close(resolve));
    }
})().catch(error => {console.error(error); process.exitCode = 1;});
