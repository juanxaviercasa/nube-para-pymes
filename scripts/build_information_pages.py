"""Build translated information pages using the existing site's layout."""
from pathlib import Path
from bs4 import BeautifulSoup
from site_routes import INFORMATION_PAGES, ROOT

CONTACT_TEXT = {
    'Contacto': 'Contact',
    '¿Tienes una pregunta, una sugerencia de software que deberíamos revisar, o encontraste algún dato desactualizado en uno de nuestros artículos? Escríbenos usando el formulario — leímos todos los mensajes y normalmente respondemos dentro de 2-3 días hábiles.': 'Have a question, a suggestion for software we should review, or outdated information to report? Use the form below. We read every message and normally reply within 2–3 business days.',
    'No rellenes este campo si eres humano:': 'Leave this field empty if you are human:',
    'Nombre': 'Name', 'Correo electrónico': 'Email address', 'Mensaje': 'Message',
    'He leído y acepto que Nube para Pymes trate mis datos para responder a este mensaje, conforme a su': 'I have read and agree that Nube para Pymes may process my data to reply to this message, in accordance with its',
    'Política de Privacidad': 'Privacy Policy', 'Enviar mensaje': 'Send message',
    'También puedes escribirnos directamente a': 'You can also email us directly at',
    '(o a': '(or', ') si lo prefieres.': ') if you prefer.',
    'Enviando...': 'Sending...',
    '¡Gracias! Tu mensaje fue enviado correctamente, te responderemos pronto.': 'Thank you! Your message was sent successfully. We will reply soon.',
    'Hubo un problema al enviar tu mensaje. Intenta de nuevo o escríbenos a contacto@nubeparapymes.online.': 'There was a problem sending your message. Please try again or email contacto@nubeparapymes.online.',
}

def build(dist):
    for es, (en, title) in INFORMATION_PAGES.items():
        if en == 'about-us':
            continue
        soup = BeautifulSoup((dist / es / 'index.html').read_text(encoding='utf-8'), 'html.parser')
        soup.html['lang'] = 'en'
        soup.title.string = title + ' | SMB Cloud'
        for heading in soup.select('h1.entry-title'):
            heading.string = title
        content = soup.select_one('.entry-content')
        if content is None:
            raise ValueError(f'Missing content container: {es}')
        if en == 'contact':
            for node in list(content.find_all(string=True)):
                stripped = str(node).strip()
                if stripped in CONTACT_TEXT:
                    node.replace_with(str(node).replace(stripped, CONTACT_TEXT[stripped]))
            for script in content.select('script'):
                value = script.string or ''
                for old, new in CONTACT_TEXT.items():
                    value = value.replace(old, new)
                script.string = value
        else:
            fragment = BeautifulSoup((ROOT / 'content/en' / (en + '.html')).read_text(encoding='utf-8'), 'html.parser')
            content.clear()
            for child in list(fragment.contents):
                content.append(child)
        # Remove inherited Spanish structured data; canonical/hreflang are added centrally.
        for script in soup.select('script[type="application/ld+json"]'):
            script.decompose()
        description = soup.select_one('meta[name="description"]')
        if description:
            description['content'] = f'{title} for NubeParaPymes.online (SMB Cloud).'
        for tag in soup.select('meta[property="og:title"], meta[name="twitter:title"]'):
            tag['content'] = title + ' | SMB Cloud'
        for tag in soup.select('meta[property="og:description"], meta[name="twitter:description"]'):
            tag['content'] = f'{title} for NubeParaPymes.online (SMB Cloud).'
        for tag in soup.select('meta[property="og:locale"]'):
            tag['content'] = 'en_US'
        dest = dist / 'en' / en / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(str(soup), encoding='utf-8')
