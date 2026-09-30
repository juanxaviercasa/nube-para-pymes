# Publicación del sitio bilingüe

El sitio combina la exportación editorial de WordPress, 26 herramientas y sus versiones inglesas. El único directorio de publicación es **dist/**. La raíz del repositorio contiene fuentes y no debe publicarse como sitio final.

## Compilar y comprobar

Requisitos: Python 3.12 y Node.js 22 o superior.

```bash
python -m pip install -r requirements.txt
npm ci
npm run build
npm test
node scripts/preview_server.js
```

Abre http://127.0.0.1:3000. Este servidor interpreta las redirecciones del proyecto, a diferencia de un servidor de archivos básico.

Para probar Chrome/Chromium:

```bash
npx playwright install chromium
node scripts/test_browser_localization.js
```

En Windows se utiliza Chrome instalado si está disponible. La variable PLAYWRIGHT_CHROMIUM_EXECUTABLE permite indicar otro ejecutable. Las pruebas no envían formularios ni publican comentarios; bloquean publicidad y servicios externos.

## Cloudflare Pages

Configura el proyecto Git conectado al repositorio:

- Directorio raíz: raíz del repositorio.
- Comando de compilación: `python -m pip install -r requirements.txt && npm ci && npm run build && npm test`.
- Directorio de salida: `dist`.
- Python: 3.12. Node.js: 22 o superior.

Después de subir un commit y completar el despliegue, comprueba la URL de vista previa antes del dominio público. No hace falta WordPress, PHP ni una base de datos para servir las páginas y herramientas. Los formularios y comentarios existentes conservan sus servicios externos.

Si publicas mediante carga manual, compila y comprueba primero; después sube únicamente el contenido de dist, incluidos _redirects, _headers y 404.html. No subas archivos .env ni la raíz del repositorio.

Cloudflare normaliza archivos .html a URLs sin extensión. Las herramientas inglesas se generan como directorios reales /en/nombre/index.html y se enlazan como /en/nombre/. Los enlaces antiguos .html redirigen hacia ellos. Evita volver a añadir reglas que manden estas URLs limpias a .html: pueden causar ciclos.

La página 404 se entrega mediante 404.html. No uses una regla global `/* /404.html 404`: ese código de respuesta no es una redirección admitida por Pages.

## Dónde modificar cada cosa

- `nubepymesexport/`: exportación editorial española y recursos de WordPress.
- HTML de la raíz y `js/`, `css/`, `assets/`: herramientas españolas.
- `en/`: traducciones existentes de artículos y herramientas.
- `content/en/`: contenido de las páginas informativas inglesas; conserva las condiciones y datos del original español.
- `content/en/tool-ui*.json`, `scripts/build_tool_translations.py` y `js/tool-localization.js`: traducciones de la interfaz dinámica de las herramientas, con variables y datos de entrada preservados.
- `scripts/site_routes.py`: correspondencias de idioma y rutas antiguas conocidas.
- `scripts/build_bilingual_archives.py`: mismas selecciones de artículos y paginación en ambos idiomas.
- `scripts/finalize_localization.py`: normalización final, selectores, etiquetas, metadatos, buscador y redirecciones.
- `js/language-navigation.js`: navegación de elementos añadidos por JavaScript.

No edites dist para corregir contenido: se reconstruye. La compilación tampoco debe reescribir las fuentes ni la exportación original.

## Comprobaciones antes de publicar

`npm test` verifica el artefacto, cada pareja ES/EN, etiquetas del pie, selectores, ausencia de ciclos y todos los enlaces internos de las páginas HTML. El informe de destinos ausentes se guarda en scripts/link-audit.json. La compilación o las pruebas deben detener el despliegue si fallan.

La prueba de navegador comprueba el pie inglés, las ocho páginas informativas, búsqueda y filtros del portal, las 26 herramientas inglesas, enlaces de idioma, recursos locales y el caso /en/tools/en/index.html. Los resultados de navegador se guardan en artifacts/.

La publicación automática de GitHub Pages también compila, verifica y sube dist. Es un destino distinto del proyecto Cloudflare: comprueba cuál está asociado al dominio antes de publicar.

## Verificación después del despliegue

Comprueba /en/, /en/tools/, /en/privacy-policy/, /en/contact/ y /en/smb-crm/. Cambia de idioma en ambas direcciones; el destino debe ser la misma página equivalente. Prueba también una página numerada del blog, una categoría y un enlace antiguo .html.

Si la vista previa nueva funciona pero el dominio muestra la versión anterior, revisa el despliegue asociado al dominio y su caché en Cloudflare. La configuración remota no cambia por editar el código local.

Documentación: https://developers.cloudflare.com/pages/configuration/serving-pages/ y https://developers.cloudflare.com/pages/configuration/redirects/.
