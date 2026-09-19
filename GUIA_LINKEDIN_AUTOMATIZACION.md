# 🚀 Guía Maestra: Automatización de Marketing en LinkedIn
### Autor y Creador: Xavier Cabello | Nube para Pymes (`nubeparapymes.online`)

Esta guía detalla paso a paso cómo activar y operar el ecosistema de marketing y posicionamiento en LinkedIn para **Nube para Pymes**, posicionando a **Xavier Cabello** como el arquitecto/desarrollador y atrayendo tráfico calificado de forma 100% orgánica y segura.

---

## 📋 Resumen del Ecosistema

El sistema consta de dos componentes estratégicos:

1. **Componente 1: Catálogo Visual de las 26 Herramientas (PDF Carrusel)**
   - **Formato:** Documento PDF vertical de 28 diapositivas (1080x1350 px, proporción 4:5 optimizada para móviles y feed de LinkedIn).
   - **Objetivo:** Generar alto tiempo de permanencia (*dwell time*) en el feed, mostrar la amplitud de las 26 herramientas gratuitas y posicionar a Xavier Cabello como creador.
   - **Archivo generado:** `Catalogo_26_Herramientas_NubeParaPymes.pdf`.
   - **Publicación:** Manual mediante la opción "Añadir documento" en LinkedIn (los carruseles PDF requieren subida manual directa).

2. **Componente 2: Motor de Publicación Automatizada (API Oficial)**
   - **Formato Intercalado:** Alterna publicaciones editoriales de artículos con posts dedicados a las **26 herramientas interactivas gratuitas** (con su propuesta de valor, el problema que resuelven en una Pyme y enlace directo para probarlas).
   - **Frecuencia programada:** 1 post diario de lunes a viernes a las 13:30 UTC (08:30 AM hora Lima/Bogotá), horario pico de engagement B2B.
   - **Tecnología:** GitHub Actions + Python + API Oficial de LinkedIn v2 (`ugcPosts`). Cero riesgo de bloqueos por no usar scraping ni bots de navegador.
   - **Total de contenidos en rotación:** 94 publicaciones (68 artículos editoriales + 26 herramientas prácticas interactivas).

---

## 🔍 ¿Dónde ver los Posts Publicados en LinkedIn?

Cuando ejecutas el workflow manualmente o por cron:
1. **En el feed principal de LinkedIn:** LinkedIn **no** muestra tus propios posts recién creados en la parte superior de tu página de inicio (`/feed/`), porque su algoritmo ordena por defecto por publicaciones "Principales/Relevantes" de tu red con interacciones previas.
2. **Para ver tus publicaciones inmediatamente:**
   - Ve a tu **Perfil Personal** en LinkedIn.
   - Baja a la sección **"Actividad" (Activity)** y haz clic en el filtro o pestaña **"Publicaciones" (Posts)**.
   - O visita directamente tu panel de publicaciones: `https://www.linkedin.com/in/tu-usuario/recent-activity/all/`
3. **En el resumen de GitHub Actions:**
   - Ahora, cada vez que corras el workflow en GitHub Actions, la pantalla de resumen del paso mostrará una caja con el **enlace directo y cliqueable** a la publicación recién creada.
4. **Publicaciones ya activas en tu perfil:**
   - [Publicación #1: Cómo Ahorrar Horas de Trabajo Administrativo](https://www.linkedin.com/feed/update/urn:li:share:7507016780972711936/)
   - [Publicación #2: Alternativas a Excel para Control de Inventario](https://www.linkedin.com/feed/update/urn:li:share:7507100894451359744/)

---

## 🔑 Paso a Paso: Obtención de Credenciales de LinkedIn

Para que GitHub Actions pueda publicar en tu perfil en tu nombre, se utiliza la API oficial de LinkedIn. Sigue estos sencillos pasos:

### Paso 1: Acceder al Portal de Desarrolladores de LinkedIn
1. Inicia sesión en tu cuenta de LinkedIn.
2. Ingresa a: [https://www.linkedin.com/developers/](https://www.linkedin.com/developers/)
3. Haz clic en el botón azul **"Create app"** (Crear aplicación).

### Paso 2: Crear tu Aplicación
1. **App name:** `Nube para Pymes Auto-Poster` (o el nombre que prefieras).
2. **LinkedIn Page:** Asocia tu página de empresa en LinkedIn si tienes una, o tu perfil personal. Si te pide URL de página y no tienes una, puedes crear una página de empresa gratuita en LinkedIn en 2 minutos llamada "Nube para Pymes".
3. **App logo:** Puedes subir el logo oficial de Nube para Pymes ubicado en `assets/brand/logo-light.svg` o `apple-touch-icon.png`.
4. Acepta los términos de uso y haz clic en **"Create app"**.

### Paso 3: Solicitar Acceso a los Productos de la API
1. En el menú superior de tu app en el portal de desarrolladores, ve a la pestaña **"Products"** (Productos).
2. Busca y solicita acceso (haz clic en **"Request access"** o **"Select"**) a:
   - **Share on LinkedIn** (permite publicar contenido, enlaces e imágenes en tu perfil o página).
   - **Sign In with LinkedIn using OpenID Connect** (permite identificar tu ID de miembro).
   - Si vas a publicar en tu Página de Empresa, asocia tu página de LinkedIn en la pestaña **Settings** -> **LinkedIn Page** y verifica la vinculación.
3. Ambos productos se aprueban automáticamente de forma instantánea.

### Paso 4: Generar tu Token de Acceso (Access Token)
1. En el portal de desarrolladores, ve a la pestaña superior **"Tools"** -> **"Token Generator"** (Generador de tokens).
2. Selecciona tu aplicación (`Nube para Pymes Auto-Poster`).
3. Marca los siguientes permisos (*scopes*):
   - `w_organization_social` (escritura en la Página de Empresa de Nube para Pymes - **Recomendado**)
   - `w_member_social` (escritura en tu perfil personal)
   - `openid` y `profile`
4. Haz clic en **"Request access token"**.
5. Se abrirá la ventana de autorización. Haz clic en **"Permitir"** (Allow).
6. Copia el **Access Token** generado.

### Paso 5: Obtener tu URN de Página de Empresa (Nube para Pymes)
Para que las publicaciones vayan exclusivamente a tu **Página de Empresa** y **nunca a tu feed personal**:

1. **Obtener el ID de tu Organización:**
   - Entra a LinkedIn y ve a administrar tu página de empresa ("Nube para Pymes").
   - Revisa la URL en tu navegador: `https://www.linkedin.com/company/<NUMERO_ID>/admin/...`
   - Ese número es el ID de tu empresa (ejemplo: si es `10594321`, tu URN es `urn:li:organization:10594321`).
   - *(Si la URL muestra el nombre/slug como `/company/nube-para-pymes/admin/`, haz clic derecho en la página -> "Ver código fuente" y busca `urn:li:organization:`; el número que le sigue es el ID).*
2. **Permisos del Token para Empresa:**
   - Tu app en [LinkedIn Developers](https://www.linkedin.com/developers/) debe tener tu página asociada y verificada en la pestaña **Settings** -> **LinkedIn Page** -> **Verify**.
   - En **Tools** -> **Token Generator**, debes generar el token marcando la casilla **`w_organization_social`** (que permite publicar en nombre de la empresa).
3. **Verificación rápida en local:**
   Puedes ejecutar en tu terminal:
   ```bash
   python scripts/obtener_linkedin_token.py
   ```
   El script consultará automáticamente la API de LinkedIn y te confirmará si tu token tiene acceso a la página de Nube para Pymes y su URN exacto.

---

## ⚙️ Configuración en GitHub Secrets (Blindaje de Empresa)

Ve a tu repositorio en GitHub: `Settings` -> `Secrets and variables` -> `Actions` y configura:

1. **`LINKEDIN_ACCESS_TOKEN`**: Tu token de acceso con permiso `w_organization_social`.
2. **`LINKEDIN_ORGANIZATION_URN`**: `urn:li:organization:<TU_ID_NUMÉRICO>`
3. **`LINKEDIN_REQUIRE_ORGANIZATION`**: `true`
   *(Al colocar este secreto en `true`, el sistema se blindará: si alguna vez falta el URN de empresa o el token caduca, la publicación se detendrá automáticamente con un error explícito, evitando que por accidente se publique en tu feed personal).*

---

## 🖼️ Galería de Mínimo 3 Imágenes por Post (Garantía Estricta)
El motor ahora implementa la **API moderna de LinkedIn (`/rest/images` + `/rest/posts` con soporte nativo para `multiImage`)**:
- **Artículos de blog:** Extrae de 3 a 4 capturas de pantalla, paneles y gráficos reales del artículo (convirtiéndolos a JPEG en memoria).
- **Herramientas interactivas:** Genera automáticamente 3 tarjetas visuales cuadradas (1080x1080 px) con diseño profesional dark mode, destacando el problema de las Pymes, capacidades y privacidad.
- **Subida binaria corregida:** La subida se realiza a la URL pre-firmada sin cabeceras de autorización conflictivas, garantizando la carga exitosa de las 3 imágenes.
- **Validación estricta sin fallbacks silenciosos:** Si por cualquier motivo de red o de API no se logran subir al menos 3 imágenes, el sistema aborta de inmediato y emite un fallo visible en GitHub Actions en lugar de publicar un post incompleto sin imágenes.
- **Resultado en LinkedIn:** La publicación se muestra como una **galería/mosaico visual interactivo de 3 imágenes** con el texto estratégico y el enlace a la web.
---

## 🎬 Cómo Probar y Disparar el Sistema

### 1. Prueba Manual desde GitHub Actions (Sin esperar al cron)
1. Ve a la pestaña **Actions** en tu repositorio de GitHub.
2. En la lista de flujos a la izquierda, selecciona **"Publicación Automatizada en LinkedIn"**.
3. A la derecha verás el botón **"Run workflow"**:
   - Puedes marcar la casilla `¿Ejecutar en modo simulación (Dry Run)?` para verificar que todo funcione sin publicar nada en tu muro.
   - O dejarla desmarcada para publicar de inmediato el siguiente post programado.
4. Haz clic en **Run workflow**. En ~15 segundos el post estará publicado en tu perfil de LinkedIn.

### 2. Publicación Automática Programada
El archivo `.github/workflows/linkedin-auto-post.yml` está configurado para ejecutarse automáticamente de **lunes a viernes a las 13:30 UTC (08:30 AM hora Lima/Bogotá)**.
- Cada día toma el siguiente artículo no publicado de la cola de 69 artículos.
- Extrae el título, la descripción, los 3 puntos clave y genera el copy adaptado para el algoritmo.
- Lo publica a través de la API oficial.
- Actualiza el archivo `scripts/linkedin_queue.json` marcando el artículo como publicado con fecha y ID del post, y guarda el commit automáticamente.
- Cuando se terminan los 69 artículos (tras ~3 meses de publicaciones diarias), reinicia automáticamente la rotación con nuevos ángulos de gancho.

---

## 📄 Cómo Publicar el Catálogo Visual (PDF Carrusel)

El carrusel de las 26 herramientas es el contenido de mayor impacto para tu perfil:

1. **Generar o regenerar el PDF:**
   En tu terminal local ejecuta:
   ```bash
   python scripts/generar_catalogo_herramientas.py
   ```
   Esto compila `Catalogo_26_Herramientas_NubeParaPymes.pdf` en la raíz del proyecto.

2. **Publicar en LinkedIn:**
   - En tu feed de LinkedIn, haz clic en **"Crear publicación"** (Start a post).
   - Haz clic en el icono de **"Añadir documento"** (icono con forma de hoja de papel o tres puntos -> Añadir un documento).
   - Selecciona el archivo `Catalogo_26_Herramientas_NubeParaPymes.pdf`.
   - **Título del documento:** `Catálogo Oficial: 26 Herramientas Gratuitas para Pymes (2026)`.
   - **Texto de la publicación:** Copia y pega el texto sugerido que imprime el script (también disponible abajo).

### Texto Recomendado para la Publicación del Carrusel:
```text
🚨 El 82% de las pequeñas empresas fracasa por falta de control en su flujo de efectivo, desorden en ventas o cobros tardíos.

La mayoría cree que la solución es pagar cientos de dólares al mes en suscripciones de software complejas que nadie en el equipo termina usando.

Por eso construí y puse a disposición pública este catálogo de 26 herramientas 100% gratuitas, privadas y diseñadas para el día a día de una Pyme:

📊 ¿Qué incluye este catálogo interactivo?
• Finanzas: Flujo de caja proyectado, cálculo de margen e IGV, tabla de amortización de préstamos y sobrecostos laborales.
• Ventas: CRM visual liviano, generador de cotizaciones profesionales y creador de facturas proforma.
• Marketing: Analizador de titulares persuasivos, auditor SEO on-page y consola de enlaces UTM.
• Operaciones y Legal: Control de stock de almacén, calculadora de fletes y generadores de contratos de servicios.
• Productividad: Compresor WebP de imágenes, generador de firmas HTML corporativas y contraseñas seguras.

🔒 Lo más importante:
1. Sin necesidad de registro obligatorio.
2. Cero costos ni suscripciones ocultas.
3. Tus datos nunca salen de tu computadora (se procesan en local en tu navegador).

👉 Desliza el carrusel para ver las 26 herramientas en detalle.
🔗 Pruébalas gratis directamente en: https://nubeparapymes.online/herramientas/

¿Cuál de estas áreas es la que más te quita tiempo hoy en tu negocio? Te leo en los comentarios. 👇

──────────
👨‍💻 Desarrollado por Xavier Cabello · Nube para Pymes
#Pymes #SoftwareEmpresarial #Productividad #FinanzasPyme #VentasB2B #TransformacionDigital #Emprendimiento #XavierCabello #NubeParaPymes
```

---

## 🛠️ Comandos Útiles del Motor de Contenidos

Puedes ejecutar el motor localmente en cualquier momento con estos comandos:

- **Ver el estado de la cola:**
  ```bash
  python scripts/linkedin_content_engine.py --list
  ```

- **Ver una vista previa del próximo post:**
  ```bash
  python scripts/linkedin_content_engine.py --dry-run
  ```

- **Publicar manualmente desde tu máquina:**
  ```bash
  python scripts/linkedin_content_engine.py --publish
  ```

- **Reiniciar la cola para un nuevo ciclo:**
  ```bash
  python scripts/linkedin_content_engine.py --reset-queue
  ```

---
*Documentación generada para Xavier Cabello · Nube para Pymes · 2026*
