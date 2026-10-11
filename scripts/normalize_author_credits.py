"""Keep exported and generated author credits on the owner's current domain."""
import re
from pathlib import Path

AUTHOR_URL = 'https://xavier.cabellosalirrosas.com'
OLD_DOMAIN = re.compile(r'https?://(?:juan|xavier)\.(?:cabellorosas|cabellosalirosas|cabellosalirrosas)\.com', re.I)

def normalize_author_credits(dist: Path):
    changed = 0
    for file in dist.rglob('*'):
        if file.suffix not in ('.html', '.js', '.json', '.xml', '.txt'):
            continue
        text = file.read_text(encoding='utf-8')
        updated = OLD_DOMAIN.sub(AUTHOR_URL, text)
        if file.suffix == '.html' and 'ast-footer-copyright' in updated:
            def credit(match):
                block = match[0]
                if AUTHOR_URL in block:
                    return block
                english = '/en/' in file.as_posix()
                label = 'Designed and Developed by' if english else 'Desarrollado por'
                return block.replace('</p>', f' · {label} <a href="{AUTHOR_URL}" rel="noopener" target="_blank">Xavier Cabello</a></p>', 1)
            updated = re.sub(r'<div\b[^>]*class="ast-footer-copyright"[^>]*>\s*<p>[\s\S]*?</p>\s*</div>', credit, updated)
        if file.suffix == '.html':
            def generic_credit(match):
                block = match[0]
                if AUTHOR_URL in block:
                    return block
                label = 'Designed and Developed by' if '/en/' in file.as_posix() else 'Desarrollado por'
                return block.replace('</footer>', f'<p class="np-author-credit">{label} <a href="{AUTHOR_URL}" rel="noopener" target="_blank">Xavier Cabello</a></p></footer>')
            updated = re.sub(r'<footer\b[^>]*>[\s\S]*?</footer>', generic_credit, updated)
        if updated != text:
            file.write_text(updated, encoding='utf-8')
            changed += 1
    print(f'[AUTHOR] Updated current author domain in {changed} files.')

if __name__ == '__main__':
    normalize_author_credits(Path(__file__).resolve().parents[1] / 'dist')
