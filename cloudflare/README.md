# Formularios del ecosistema

Cada sitio usa un Worker independiente en `/api/contact`, con destinatario fijo,
Turnstile validado en el servidor y un límite de cinco solicitudes por minuto.
Los datos se entregan por correo; no se guardan en Supabase, Google Forms ni una
base de datos del sitio. `sites.json` documenta marca, categorías y destino.

El navegador consulta GET `/api/contact` para obtener únicamente el sitekey
público y el estado de disponibilidad. El POST valida origen, consentimiento,
campos, tamaño, honeypot, hostname y acción Turnstile antes de enviar. Un fallo
conserva el mensaje y muestra la dirección de correo alternativa.

`TURNSTILE_SECRET` se configura como binding secreto del Worker. El token de
despliegue nunca se almacena en este repositorio ni se expone al navegador.
Para actualizar, desde la raíz de Nube para Pymes configura `CF_TOKEN_FILE`
con la ruta de una credencial local y ejecuta:

```text
node scripts/deploy_contact_workers.cjs
node --test cloudflare/contact-worker.test.mjs
```

Permisos utilizados: Pages Edit (existente), Workers Scripts Edit y Turnstile
Edit en la cuenta; Workers Routes Edit en los tres dominios. Los MX y las reglas
de reenvío existentes se conservan. Workers.dev y las previews están desactivados.
