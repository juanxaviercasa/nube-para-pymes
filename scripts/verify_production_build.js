const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');

const TOOLS = [
    // Marketing
    { slug: 'analizador-titulares', cat: 'marketing' },
    { slug: 'auditor-seo-basico', cat: 'marketing' },
    { slug: 'comparador-campanas-avanzado', cat: 'marketing' },
    { slug: 'consola-campanas', cat: 'marketing' },
    { slug: 'organizador-matriz-contenidos', cat: 'marketing' },

    // Finanzas
    { slug: 'calculadora-descuentos-promociones', cat: 'finanzas' },
    { slug: 'calculadora-precios-venta-igv', cat: 'finanzas' },
    { slug: 'calculadora-prestamos-amortizaciones', cat: 'finanzas' },
    { slug: 'calculadora-sobrecostos-laborales', cat: 'finanzas' },
    { slug: 'flujo-caja-pymes', cat: 'finanzas' },

    // Ventas
    { slug: 'creador-facturas-proforma', cat: 'ventas' },
    { slug: 'generador-codigos-qr', cat: 'ventas' },
    { slug: 'generador-cotizaciones', cat: 'ventas' },
    { slug: 'guiones-manejo-objeciones', cat: 'ventas' },
    { slug: 'crm-pymes', cat: 'ventas' },

    // Legal
    { slug: 'generador-contratos-servicios', cat: 'legal' },
    { slug: 'generador-politicas-devolucion', cat: 'legal' },
    { slug: 'generador-politicas-terminos', cat: 'legal' },

    // Operaciones
    { slug: 'calculadora-flete-envio-local', cat: 'operaciones' },
    { slug: 'simulador-tco-fisico-nube', cat: 'operaciones' },
    { slug: 'inventario-compras-pymes', cat: 'operaciones' },

    // Productividad
    { slug: 'conversor-optimizador-imagenes', cat: 'productividad' },
    { slug: 'firma-correo-html', cat: 'productividad' },
    { slug: 'generador-contrasenas-pymes', cat: 'productividad' },
    { slug: 'generador-paletas-corporativas', cat: 'productividad' },
    { slug: 'tareas-proyectos-pymes', cat: 'productividad' },
];

let errors = [];
let warnings = [];

function check(desc, condition) {
    if (condition) {
        console.log(`  ✅ ${desc}`);
    } else {
        console.error(`  ❌ FALLO: ${desc}`);
        errors.push(desc);
    }
}

console.log('=== AUDITORÍA DEL BUILD DE PRODUCCIÓN (dist/) ===\n');

// 1. Verificación de Raíz y WordPress
console.log('1. Verificando Portada y Páginas Principales de WordPress...');
check('dist/index.html existe (Portada WP)', fs.existsSync(path.join(DIST, 'index.html')));
check('dist/blog/index.html existe', fs.existsSync(path.join(DIST, 'blog', 'index.html')));
check('dist/sobre-nosotros/index.html existe', fs.existsSync(path.join(DIST, 'sobre-nosotros', 'index.html')));
check('dist/contacto/index.html existe', fs.existsSync(path.join(DIST, 'contacto', 'index.html')));
check('dist/wp-content existe', fs.existsSync(path.join(DIST, 'wp-content')));
check('dist/wp-includes existe', fs.existsSync(path.join(DIST, 'wp-includes')));

// 2. Verificación de Portal de Herramientas
console.log('\n2. Verificando Portal Interactivo de Herramientas (/herramientas/)...');
const portalPath = path.join(DIST, 'herramientas', 'index.html');
check('dist/herramientas/index.html existe', fs.existsSync(portalPath));
if (fs.existsSync(portalPath)) {
    const portalHtml = fs.readFileSync(portalPath, 'utf8');
    check('Portal enlaza a /herramientas/css/index.css', portalHtml.includes('/herramientas/css/index.css'));
    check('Portal enlaza a /herramientas/js/index.js', portalHtml.includes('/herramientas/js/index.js'));
    check('Portal contiene enlace a /herramientas/marketing/analizador-titulares/', portalHtml.includes('/herramientas/marketing/analizador-titulares/'));
    check('Portal contiene enlace a /herramientas/finanzas/calculadora-descuentos-promociones/', portalHtml.includes('/herramientas/finanzas/calculadora-descuentos-promociones/'));
    check('Portal no contiene enlaces rotos ./analizador-titulares.html', !portalHtml.includes('./analizador-titulares.html'));
}

// 3. Verificación de las 26 Herramientas Categorizadas
console.log('\n3. Verificando las 26 Herramientas Categorizadas...');
let toolsFound = 0;
let toolsWithBadAssets = 0;

TOOLS.forEach(t => {
    const toolFile = path.join(DIST, 'herramientas', t.cat, t.slug, 'index.html');
    if (fs.existsSync(toolFile)) {
        toolsFound++;
        const content = fs.readFileSync(toolFile, 'utf8');
        // Chequeo de rutas relativas rotas en scripts/styles
        if (content.includes('src="./js/') || content.includes('href="./css/') || content.includes('href="./assets/')) {
            toolsWithBadAssets++;
            console.error(`     Advertencia: ${t.slug} contiene rutas relativas ./`);
        }
    } else {
        console.error(`     Falta herramienta: /herramientas/${t.cat}/${t.slug}/index.html`);
    }
});

check(`Se encontraron las 26 herramientas en dist/herramientas/[categoria]/[slug]/ (${toolsFound}/26)`, toolsFound === 26);
check(`Todas las herramientas usan rutas absolutas /herramientas/ (0 con rutas rotas)`, toolsWithBadAssets === 0);

// 4. Verificación de Guía de Uso
console.log('\n4. Verificando Guía de Uso...');
const guidePath = path.join(DIST, 'herramientas', 'guia-uso', 'index.html');
check('dist/herramientas/guia-uso/index.html existe', fs.existsSync(guidePath));

// 5. Verificación de Directorio WP
console.log('\n5. Verificando Página de Directorio de WordPress...');
const dirWpPath = path.join(DIST, 'directorio-herramientas', 'index.html');
check('dist/directorio-herramientas/index.html existe', fs.existsSync(dirWpPath));
if (fs.existsSync(dirWpPath)) {
    const dirHtml = fs.readFileSync(dirWpPath, 'utf8');
    check('Directorio WP no tiene enlaces a apps.nubeparapymes.online', !dirHtml.includes('https://apps.nubeparapymes.online/'));
    check('Directorio WP enlaza a /herramientas/marketing/analizador-titulares/', dirHtml.includes('/herramientas/marketing/analizador-titulares/'));
    check('Directorio WP enlaza a /herramientas/finanzas/calculadora-descuentos-promociones/', dirHtml.includes('/herramientas/finanzas/calculadora-descuentos-promociones/'));
}

// 6. Verificación de _redirects
console.log('\n6. Verificando Reglas de Redirección (_redirects)...');
const redPath = path.join(DIST, '_redirects');
check('dist/_redirects existe', fs.existsSync(redPath));
if (fs.existsSync(redPath)) {
    const redContent = fs.readFileSync(redPath, 'utf8');
    check('Redirección para /analizador-titulares.html presente', redContent.includes('/analizador-titulares.html    /herramientas/marketing/analizador-titulares/    301'));
    check('Redirección para /crm-pymes.html presente', redContent.includes('/crm-pymes.html    /herramientas/ventas/crm-pymes/    301'));
    check('Reglas de protección WP (/wp-admin/*) presentes', redContent.includes('/wp-admin/*'));
    check('Regla fallback 404 presente', redContent.includes('/*    /404.html    404'));
}

// 7. Verificación de Sitemap y Robots
console.log('\n7. Verificando Sitemap XML y Robots.txt...');
const sitemapPath = path.join(DIST, 'sitemap.xml');
check('dist/sitemap.xml existe', fs.existsSync(sitemapPath));
if (fs.existsSync(sitemapPath)) {
    const sitemapContent = fs.readFileSync(sitemapPath, 'utf8');
    check('Sitemap no contiene dominio de desarrollo pantheon', !sitemapContent.includes('dev-nube-para-pymes.pantheonsite.io'));
    check('Sitemap contiene /herramientas/', sitemapContent.includes('<loc>https://nubeparapymes.online/herramientas/</loc>'));
    check('Sitemap contiene /herramientas/finanzas/flujo-caja-pymes/', sitemapContent.includes('https://nubeparapymes.online/herramientas/finanzas/flujo-caja-pymes/'));
}

const robotsPath = path.join(DIST, 'robots.txt');
check('dist/robots.txt existe', fs.existsSync(robotsPath));
if (fs.existsSync(robotsPath)) {
    const robotsContent = fs.readFileSync(robotsPath, 'utf8');
    check('Robots apunta a sitemap de nubeparapymes.online', robotsContent.includes('Sitemap: https://nubeparapymes.online/sitemap.xml'));
}

console.log('\n=============================================');
if (errors.length === 0) {
    console.log('🎉 ¡AUDITORÍA SUPERADA CON ÉXITO! Todos los chequeos pasaron.');
    process.exit(0);
} else {
    console.error(`🚨 SE ENCONTRARON ${errors.length} ERRORES.`);
    process.exit(1);
}
