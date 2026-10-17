"""Refresh only tool pages and assets after local edits, without rebuilding WordPress."""
import re
import shutil
import time
from pathlib import Path
from site_routes import ROOT, TOOLS_MAP
from tool_experience import enhance, VERSION
from assemble_production_site import transform_html_asset_links

dist = ROOT / 'dist'
for tool in TOOLS_MAP.values():
    for source, target, english, prefix in [
        (ROOT / tool['src'], dist / 'herramientas' / tool['cat'] / tool['slug'] / 'index.html', False, '/herramientas/'),
        (ROOT / 'en' / (tool['en_slug'] + '.html'), dist / 'en' / tool['en_slug'] / 'index.html', True, '/'),
    ]:
        # Preserve localization metadata and author credits from the full build.
        text = target.read_text(encoding='utf-8')
        text = enhance(text, tool, english, prefix)
        target.write_text(re.sub(r'[ \t]+$', '', text, flags=re.M), encoding='utf-8')
for file in (dist / 'herramientas/index.html', dist / 'en/tools/index.html'):
    text = file.read_text(encoding='utf-8')
    text = re.sub(r'<script\b[^>]*data-npp-regional(?:-ui)?[^>]*></script>\s*', '', text)
    text = re.sub(r'(<head\b[^>]*>)\s*', lambda m: m[1] + f'\n<script src="/js/regional-settings.js?v={VERSION}" data-npp-regional></script>\n<script defer src="/js/regional-ui.js?v={VERSION}" data-npp-regional-ui></script>\n', text, count=1)
    file.write_text(text, encoding='utf-8')
for folder in ('js', 'css'):
    for file in (ROOT / folder).iterdir():
        if file.is_file():
            for base in (dist, dist / 'herramientas'):
                if folder == 'js' and file.name == 'index.js':
                    text = file.read_text(encoding='utf-8').replace('./en/index.html', '/en/tools/').replace('./guia-uso-22-apps.html', '/herramientas/guia-uso/')
                    for tool in TOOLS_MAP.values():
                        text = text.replace('./' + tool['src'], f'/herramientas/{tool["cat"]}/{tool["slug"]}/')
                    (base / folder / file.name).write_text(text, encoding='utf-8')
                else:
                    for attempt in range(5):
                        try:
                            shutil.copyfile(file, base / folder / file.name)
                            break
                        except OSError:
                            if attempt == 4:
                                raise
                            time.sleep(.2)
print('Refreshed 52 tools, both directories and shared assets.')
