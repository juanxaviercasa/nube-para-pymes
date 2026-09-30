"""Check every local navigation URL against the actual deployment artifact."""
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
from collections import defaultdict
from bs4 import BeautifulSoup
import json
import re
from html import unescape
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
HOST = 'https://nubeparapymes.online'

def page_url(file):
    path = '/' + file.relative_to(DIST).as_posix()
    return path[:-10] if path.endswith('index.html') else path

@lru_cache(maxsize=None)
def exists(path):
    target = DIST / unquote(path).lstrip('/')
    return target.is_file() or (target / 'index.html').is_file() or target.with_suffix('.html').is_file()

def audit():
    broken = defaultdict(list)
    count = 0
    files = list(DIST.rglob('*.html'))
    with ThreadPoolExecutor(max_workers=8) as executor:
        contents = list(executor.map(lambda file: file.read_text(encoding='utf-8'), files))
    for index, (file, text) in enumerate(zip(files, contents)):
        if index % 100 == 0:
            print(f'Auditing page {index}: {page_url(file)}', flush=True)
        text = re.sub(r'<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>|<!--[\s\S]*?-->', '', text, flags=re.I)
        for match in re.finditer(r'<a\b[^>]*\bhref\s*=\s*([\"\x27])(.*?)\1', text, re.I):
            href = unescape(match[2])
            url = urlsplit(urljoin(HOST + page_url(file), href))
            if url.scheme not in ('http', 'https') or url.netloc != 'nubeparapymes.online':
                continue
            count += 1
            if not exists(url.path):
                broken[url.path].append(page_url(file))
    report = {k: {'count': len(v), 'sources': v[:3]} for k, v in sorted(broken.items())}
    (ROOT / 'scripts' / 'link-audit.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f'{len(files)} HTML pages; {count} internal links; {len(broken)} missing destinations')
    for path, info in report.items():
        print(path, info)
    return broken

if __name__ == '__main__':
    raise SystemExit(bool(audit()))
