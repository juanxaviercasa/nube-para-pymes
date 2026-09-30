# Corrección de navegación ES / EN

## Causas encontradas

- Los enlaces relativos del portal producían rutas como `/en/tools/en/index.html`.
- El pie inglés apuntaba a traducciones que no se generaban.
- Varios scripts reconstruían o corregían las mismas páginas con criterios distintos.
- El portal inglés cargaba el controlador español y perdía sus traducciones al iniciar JavaScript.
- Las herramientas también reemplazaban texto estático traducido al montar sus componentes.
- La preferencia de idioma guardada podía anular un cambio explícito a español.
- Faltaban archivos mensuales y equivalencias de categorías, etiquetas y páginas numeradas.
- Algunas redirecciones entraban en conflicto con las URLs sin extensión de Cloudflare.
- La exportación conservaba referencias a recursos Astra y servicios de WordPress inexistentes.
- Dos herramientas tenían errores de JavaScript: componentes duplicados en flete y una variable sin declarar en TCO.

## Solución

`scripts/site_routes.py` centraliza las equivalencias y rutas antiguas. La compilación genera páginas reales, normaliza navegación, enlaces de idioma, canonical, hreflang, sitemap y buscador, y falla si falta una traducción declarada. Las traducciones informativas están en `content/en/`.

Las herramientas mantienen su lógica y sus formularios. `scripts/build_tool_translations.py` reutiliza sus traducciones existentes para actualizar texto dinámico sin reemplazar nodos React ni sus eventos. El portal inglés utiliza su propio controlador y sus filtros y ajustes funcionan.

La compilación modifica únicamente `dist/`. Las rutas antiguas tienen destinos canónicos; los enlaces no se fabrican agregando `/en/` indiscriminadamente.

## Verificación reproducible

```bash
python -m pip install -r requirements.txt
npm ci
npm run build
npm test
npx playwright install chromium
npm run test:browser
```

- Auditoría de todos los enlaces HTML internos y de las 228 equivalencias de idioma.
- Verificación de redirecciones, etiquetas y destinos de los selectores.
- Navegación en Chrome/Chromium por el pie inglés, sus ocho páginas, el portal y las 26 herramientas.
- Comprobación de recursos locales, errores JavaScript y traducciones dinámicas.
- Caso de regresión: `/en/tools/en/index.html` debe llegar a `/en/tools/`.

Las pruebas de navegador bloquean servicios externos y no envían formularios ni comentarios. No verifican entregas de correo, publicidad, servicios externos ni todos los cálculos y documentos exportados de cada herramienta.

## Publicación pendiente

Resultados de la revisión local: compilación completa correcta; 608 páginas HTML y 24.972 enlaces internos auditados, sin destinos ausentes; 5.644 comprobaciones de localización superadas sobre 228 pares de páginas. La prueba de Chrome pasó con las 26 herramientas, las páginas del pie, los enlaces dinámicos y cero errores de JavaScript o recursos locales ausentes durante el recorrido.

El dominio público debe servir el contenido generado en `dist/`, mediante el proyecto Cloudflare vinculado a la rama de producción. Consulta `GUIA_DESPLIEGUE_HOSTING.md` para el comando de compilación y las comprobaciones posteriores. Subir el código y confirmar que Cloudflare publicó ese mismo commit son verificaciones distintas.
