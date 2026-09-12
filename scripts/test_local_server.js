const http = require('http');
const fs = require('fs');
const path = require('path');

const DIST = path.resolve(__dirname, '..', 'dist');
const PORT = 3456;

const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.xml': 'application/xml; charset=utf-8',
    '.txt': 'text/plain; charset=utf-8',
};

const server = http.createServer((req, res) => {
    let reqPath = decodeURIComponent(req.url.split('?')[0]);
    if (reqPath.endsWith('/')) {
        reqPath += 'index.html';
    } else if (!path.extname(reqPath)) {
        if (fs.existsSync(path.join(DIST, reqPath, 'index.html'))) {
            reqPath += '/index.html';
        }
    }

    const filePath = path.join(DIST, reqPath);
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath).toLowerCase();
        res.writeHead(200, { 'Content-Type': MIME_TYPES[ext] || 'application/octet-stream' });
        fs.createReadStream(filePath).pipe(res);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }
});

const URLS_TO_TEST = [
    '/',
    '/herramientas/',
    '/herramientas/marketing/analizador-titulares/',
    '/herramientas/finanzas/calculadora-descuentos-promociones/',
    '/herramientas/ventas/crm-pymes/',
    '/herramientas/operaciones/inventario-compras-pymes/',
    '/herramientas/legal/generador-contratos-servicios/',
    '/herramientas/productividad/conversor-optimizador-imagenes/',
    '/herramientas/guia-uso/',
    '/directorio-herramientas/',
    '/sobre-nosotros/',
    '/blog/',
    '/herramientas/css/analizador-titulares.css',
    '/herramientas/js/datos-compartidos.js',
    '/sitemap.xml',
    '/robots.txt',
    '/llms.txt',
];

server.listen(PORT, async () => {
    console.log(`Servidor de prueba local activo en http://localhost:${PORT}`);
    let passed = 0;
    let failed = 0;

    for (const u of URLS_TO_TEST) {
        try {
            const res = await fetch(`http://localhost:${PORT}${u}`);
            if (res.status === 200) {
                console.log(`  ✅ [200 OK] ${u}`);
                passed++;
            } else {
                console.error(`  ❌ [${res.status}] ${u}`);
                failed++;
            }
        } catch (err) {
            console.error(`  ❌ [ERROR] ${u}: ${err.message}`);
            failed++;
        }
    }

    server.close(() => {
        console.log(`\nResultados: ${passed} exitosas, ${failed} fallidas.`);
        if (failed === 0) {
            console.log('🚀 ¡TODAS LAS RUTAS CRÍTICAS RESPONDEN 200 OK!');
            process.exit(0);
        } else {
            process.exit(1);
        }
    });
});
