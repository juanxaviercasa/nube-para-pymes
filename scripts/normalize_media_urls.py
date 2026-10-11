"""Serve exported WordPress media from the same deployment as the pages."""
import re
from pathlib import Path
from urllib.parse import unquote

MEDIA_URL = re.compile(
    r'(?:https?:)?//(?:dev-nube-para-pymes\.pantheonsite\.io|nubeparapymes\.online)'
    r'(?P<path>/wp-content/uploads/[^\s"\'<>\\),]+)', re.IGNORECASE
)

# Stale names left in the original export and its archived cards.
LEGACY_MEDIA = {
    '/wp-content/uploads/2026/07/digitalizacion-procesos-pyme-sin-programar.webp': '/wp-content/uploads/2026/09/digitalizacion-procesos-pyme-sin-programar-destacada.webp',
    '/wp-content/uploads/2026/07/geo-para-pymes-respuestas-inteligencia-artificial.webp': '/wp-content/uploads/2026/09/geo-para-pymes-respuestas-inteligencia-artificial-destacada.webp',
    '/wp-content/uploads/2026/07/zoho-crm-gratis-dashboard-1024x550.webp': '/wp-content/uploads/2026/07/zoho-dashboard-comparativa-1024x550.webp',
}


def normalize_media_urls(dist: Path):
    changed = 0
    missing = set()
    # Includes srcset, lazy-loading attributes, CSS backgrounds and JSON metadata.
    for file in dist.rglob('*'):
        if file.suffix not in {'.html', '.css', '.js', '.json', '.xml'}:
            continue
        text = file.read_text(encoding='utf-8')

        def local_url(match):
            url = LEGACY_MEDIA.get(match['path'], match['path'])
            path = unquote(url.split('?', 1)[0].split('#', 1)[0])
            if not (dist / path.lstrip('/')).is_file():
                # Some exports omit an intermediate WordPress thumbnail size.
                original = re.sub(r'-\d+x\d+(?=\.[^.]+$)', '', path)
                if original != path and (dist / original.lstrip('/')).is_file():
                    return url.replace(path, original, 1)
                missing.add(path)
            return url

        normalized = MEDIA_URL.sub(local_url, text)
        for old, new in LEGACY_MEDIA.items():
            if old in normalized:
                if not (dist / new.lstrip('/')).is_file():
                    missing.add(new)
                normalized = normalized.replace(old, new)
        if normalized != text:
            file.write_text(normalized, encoding='utf-8')
            changed += 1
    if missing:
        raise RuntimeError('Exported media files missing: ' + ', '.join(sorted(missing)))
    print(f'[MEDIA] Normalized WordPress media URLs in {changed} files.', flush=True)


if __name__ == '__main__':
    normalize_media_urls(Path(__file__).resolve().parents[1] / 'dist')
