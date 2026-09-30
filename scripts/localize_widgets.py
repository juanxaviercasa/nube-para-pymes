"""Build language-specific widget assets without translating user content."""
from pathlib import Path

SEARCH_TEXT = {
    'Escribe una palabra clave para buscar en todo el contenido estático.': 'Enter a keyword to search the website.',
    'Escribe al menos 2 caracteres para buscar...': 'Type at least 2 characters to search...',
    'Escribe una palabra clave para buscar...': 'Enter a keyword to search...',
    'No se encontraron resultados para': 'No results found for',
    "'Página'": "'Page'", "'Artículo'": "'Article'",
}
COMMENT_TEXT = {
    'No fue posible cargar los comentarios en este momento.': 'Comments could not be loaded right now.',
    'Aún no hay comentarios. ¡Sé el primero en compartir tu opinión!': 'No comments yet. Be the first to share your thoughts!',
    'Por favor completa todos los campos requeridos.': 'Please complete all required fields.',
    'Por favor completa la verificación de seguridad anti-spam.': 'Please complete the anti-spam security check.',
    '¡Comentario publicado exitosamente!': 'Comment posted successfully!',
    '¡Gracias por tu comentario! Ha sido enviado para moderación y aparecerá publicado en breve.': 'Thank you! Your comment has been submitted for moderation and will appear once approved.',
    'Hubo un inconveniente al enviar tu comentario. Por favor intenta de nuevo.': 'There was a problem submitting your comment. Please try again.',
    "'es'": "'en'", "'es-ES'": "'en-US'",
    "'hace un momento'": "'just now'",
    "`hace ${mins} ${mins === 1 ? 'minuto' : 'minutos'}`": "`${mins} ${mins === 1 ? 'minute' : 'minutes'} ago`",
    "`hace ${hours} ${hours === 1 ? 'hora' : 'horas'}`": "`${hours} ${hours === 1 ? 'hour' : 'hours'} ago`",
    "`hace ${days} ${days === 1 ? 'día' : 'días'}`": "`${days} ${days === 1 ? 'day' : 'days'} ago`",
}

def build(root, dist):
    source = root / 'nubepymesexport/wp-static-arquitect-assets'
    target = dist / 'wp-static-arquitect-assets'
    for name, translations in [('search-client', SEARCH_TEXT), ('supabase-comments', COMMENT_TEXT)]:
        text = (source / (name + '.js')).read_text(encoding='utf-8')
        for old, new in translations.items():
            text = text.replace(old, new)
        if name == 'search-client':
            start = text.index('    function getIndexUrl() {')
            end = text.index('    function loadIndex(', start)
            text = text[:start] + "    function getIndexUrl() { return '/en/search-index.json'; }\n\n" + text[end:]
        (target / (name + '-en.js')).write_text(text, encoding='utf-8')
