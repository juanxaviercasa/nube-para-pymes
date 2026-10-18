# Tutoriales ilustrados de Todo Lima

Las 16 herramientas con guía ilustrada muestran un acceso antes del área de trabajo y dentro de «Ayuda y tour». Las tarjetas de ambos catálogos también enlazan al tutorial exacto. El enlace abre otra pestaña para conservar los datos y el contexto de la herramienta. En inglés se identifica que el tutorial está en español.

El índice verificado está en `content/todolima-tutorials.json`, procedente de `https://todolima.com/tutoriales-herramientas.json`. No se consulta a Todo Lima durante la carga de las apps. El build valida el dominio y el slug de cada destino y usa las rutas canónicas del proyecto para las versiones inglesas. Las otras diez herramientas conservan su ayuda actual sin recibir enlaces a tutoriales inexistentes.

Para actualizar: revisar el índice de Todo Lima, actualizar la copia local, ejecutar `npm run build`, `npm test` y `npm run test:tutorials`. La integración se ejecuta al final del ensamblado y solo genera cambios en `dist/`; no reescribe fuentes exportadas de WordPress.

La prueba específica cubre las 32 rutas ES/EN, las 16 correspondencias, ambos catálogos, el panel de ayuda y pantallas de 390 y 1440 px. La evidencia visual local se guarda en `artifacts/tutoriales/`.

## Validación del 17 de octubre de 2026

- Build completo aprobado; tras corregir la conservación de metadatos se regeneró su etapa final de integración.
- `npm test`: auditoría de producción, 5.673 comprobaciones de idiomas, 610 HTML y 25.092 enlaces internos sin destinos faltantes, ecosistema e imágenes aprobados; nueve pruebas del formulario de contacto aprobadas.
- `npm run test:tutorials`: 16 tutoriales, 32 rutas bilingües, dos catálogos, ayuda, enlaces enfocables por teclado y pantallas de 390/1440 px aprobados. El catálogo conserva sus accesos cuando React vuelve a renderizar las tarjetas.
- Capturas de revisión en `artifacts/tutoriales/` (salida local excluida de Git). No se envían formularios ni datos externos durante las pruebas.

Los enlaces externos abren otra pestaña con `noopener noreferrer`. El catálogo vuelve a aplicar los enlaces tras sus actualizaciones de React, sin consultar servicios externos. Las pruebas no constituyen una certificación integral de accesibilidad.

## Corrección visual del catálogo y las preferencias

Las 26 tarjetas incluyen «Ver tutorial» en una zona de acciones consistente. Las 16 guías ilustradas abren Todo Lima; las otras diez abren la sección correspondiente de la guía propia de Nube. No se insertan enlaces junto a los bloques de inicio rápido ni como hijos sueltos de la cuadrícula.

La preferencia regional se abre como una vista de página `?configuracion=regional`, con el scroll del documento, encabezado y botón de regreso. El cálculo permanece montado y oculto mientras se editan las preferencias; volver o aplicar mantiene los valores introducidos. El acceso explica «Cambiar país y moneda» y muestra la preferencia vigente.

La reparación del modo claro cubre variantes de color con transparencia de las herramientas heredadas. Botones azules, avisos, etiquetas y texto secundario reciben colores legibles; las muestras de Chroma eligen blanco o negro según el contraste calculado. Los documentos y colores editados por el usuario conservan su contenido.

Pruebas: `npm run test:visual-repair`, `npm run test:tutorials`, `npm run test:regional:browser` y `npm run audit:contrast`. Evidencia local en `artifacts/visual-repair/`. La medición automática es una comprobación de estados revisados y no certifica accesibilidad integral.

### Resultado de validación de la reparación

Build completo aprobado (649 s), con sincronización final de los estilos compartidos. `npm test` aprobó producción, 5.673 comprobaciones de idiomas, 25.112 enlaces internos sin destinos faltantes, imágenes, ecosistema y contacto. Ocho pruebas regionales unitarias y el recorrido regional de 52 rutas en navegador aprobados. La nueva prueba visual aprobó 26 acciones consistentes, cuadrícula de seis accesos intacta, página de configuración sin scroll interno y conservación del costo al cambiar país. La auditoría de los estados iniciales en modo claro reportó cero incidencias en 26 herramientas; excluye contenido editable del usuario, gráficos y fondos con degradados. No constituye una certificación integral de accesibilidad.
