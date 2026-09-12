const WP_URL = 'https://dev-nube-para-pymes.pantheonsite.io/wp-json/wp/v2';
const WP_USER = process.env.WP_USER || 'bot_revisor';
const WP_APP_PASS = process.env.WP_APP_PASS || '';
const GEMINI_API_KEY = process.env.GEMINI_API_KEY || '';

async function optimizarPost() {
    try {
        console.log("1. Obteniendo el artículo 1362 de WordPress...");
        const wpResponse = await fetch(`${WP_URL}/posts/1362`, {
            method: 'GET',
            headers: { 'Authorization': 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64') }
        });
        const post = await wpResponse.json();
        console.log(`✅ Artículo recuperado: ${post.title.rendered}`);

        const contenidoOriginal = post.content.rendered;
        
        console.log("2. Enviando a la IA para optimización SEO, GEO y Copywriting...");
        
        const promptSistema = `
        Actúa como un experto en SEO (Rank Math), optimización GEO/AEO y Copywriting de respuesta directa.
        Tu objetivo es reescribir el siguiente código HTML de un artículo de WordPress para que alcance un score de 90-100 en Rank Math.
        
        Aplica estrictamente estas reglas:
        1. **Respuesta Inicial (GEO):** Inicia con una "Answer-First Architecture", dando una definición clara y directa en el primer párrafo.
        2. **Densidad de Keyword:** Asegura que la keyword principal esté en el primer 10% del texto y de forma natural en los subtítulos H2/H3[cite: 1].
        3. **Copywriting:** Usa un tono persuasivo, ganchos fuertes y elimina todo el texto de relleno ("fluff") sustituyéndolo por datos concretos[cite: 3].
        4. **Estructura HTML:** Respeta y mantén todas las etiquetas HTML originales (h2, p, strong, ul, li).
        
        Devuelve ÚNICAMENTE el código HTML modificado, sin markdown (no uses \`\`\`html) y sin explicaciones adicionales.
        
        Aquí está el contenido original a optimizar:
        ${contenidoOriginal}
        `;

        const geminiResponse = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key=${GEMINI_API_KEY}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contents: [{ parts: [{ text: promptSistema }] }]
            })
        });

        let geminiData;
        try {
            geminiData = await geminiResponse.json();
        } catch (parseError) {
            console.error("❌ La respuesta de Gemini no era JSON válido:", parseError);
            return;
        }

        // --- VALIDACIÓN DE ERROR ---
        if (!geminiResponse.ok || !geminiData?.candidates || !Array.isArray(geminiData.candidates) || !geminiData.candidates[0]?.content?.parts) {
            console.error("❌ Error devuelto por Google AI Studio:");
            console.error(JSON.stringify(geminiData, null, 2));
            return; // Detenemos la ejecución para no dañar el artículo
        }

        const contenidoOptimizado = geminiData.candidates
            .flatMap(candidate => candidate.content?.parts || [])
            .map(part => part.text || '')
            .join('');

        console.log("✅ IA terminó de redactar.");

        console.log("3. Actualizando WordPress...");
        const updateResponse = await fetch(`${WP_URL}/posts/1362`, {
            method: 'PUT',
            headers: {
                'Authorization': 'Basic ' + Buffer.from(`${WP_USER}:${WP_APP_PASS}`).toString('base64'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content: contenidoOptimizado })
        });

        if (updateResponse.ok) {
            console.log("🚀 ¡Éxito! El artículo ha sido actualizado con el nuevo contenido SEO.");
        } else {
            console.error("Error al actualizar WordPress", await updateResponse.text());
        }

    } catch (error) {
        console.error("Hubo un fallo en la ejecución:", error);
    }
}

optimizarPost();