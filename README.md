# NubeParaPymes

> Herramientas web gratuitas, guías prácticas y comparativas para que las pequeñas empresas resuelvan tareas concretas con menos fricción.

[Web del proyecto](https://nubeparapymes.online) · [Abrir herramientas](https://apps.nubeparapymes.online)

## Qué problema resuelve

Las pequeñas empresas suelen perder tiempo en tareas repetitivas: preparar cotizaciones, calcular precios con IGV, revisar SEO, generar documentos, organizar campañas o responder consultas desde WhatsApp. NubeParaPymes reúne utilidades específicas que funcionan directamente en el navegador, sin instalación y sin exigir una cuenta para comenzar.

## Qué incluye

- Generadores de cotizaciones, facturas proforma, códigos QR y documentos comerciales.
- Calculadoras de precios, descuentos, fletes, préstamos y sobrecostos laborales.
- Herramientas para SEO básico, titulares, campañas, inventario, CRM y productividad.
- Guías de uso, comparativas de software y contenidos orientados a decisiones prácticas.

## Arquitectura del proyecto

El repositorio reúne una colección de aplicaciones web estáticas organizadas por herramienta. Cada utilidad dispone de su propia interfaz, estilos y lógica JavaScript, mientras que la web editorial funciona como punto de entrada, orientación y documentación para el catálogo.

## Tecnologías

HTML, CSS, JavaScript, diseño responsive, generación de documentos desde el navegador, SEO on-page y publicación web. El proyecto editorial utiliza WordPress para contenidos, estructura de categorías, páginas informativas y distribución de artículos.

## Ejecutar localmente

Requisitos: Python 3.12 y Node.js 22 o superior.

```bash
python -m pip install -r requirements.txt
npm ci
npm run build
npm test
node scripts/preview_server.js
```

Abre `http://127.0.0.1:3000`. La web editorial y las 26 herramientas se publican juntas desde **`dist/`**, nunca desde la raíz del repositorio. La raíz contiene las fuentes del portal español, no la portada editorial.

La compilación genera las páginas informativas en inglés, los archivos de blog y las correspondencias de idioma. `scripts/site_routes.py` define las rutas; `content/en/` contiene las traducciones de las páginas informativas. No edites `dist/` directamente: se reconstruye en cada compilación.

Para las pruebas con navegador: `npx playwright install chromium` y `node scripts/test_browser_localization.js`. En Windows se utiliza Chrome instalado si está disponible. También puedes indicar su ruta mediante `PLAYWRIGHT_CHROMIUM_EXECUTABLE`.

Consulta [la guía de publicación](GUIA_DESPLIEGUE_HOSTING.md) para configurar Cloudflare Pages.

## Decisiones de producto

La prioridad es resolver una tarea en pocos pasos, mostrar el resultado con claridad y evitar barreras innecesarias. Cada herramienta debe ser útil por sí misma, pero también conducir a una guía o comparativa cuando el problema requiere una decisión más amplia.

## Estado

Proyecto público en evolución. La versión publicada contiene herramientas y contenidos que se irán ampliando y refinando con base en necesidades reales de pequeñas empresas.

## Autor

**Juan Xavier Cabello** — desarrollo web, producto, contenidos y estrategia editorial.
