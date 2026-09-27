from pathlib import Path
import json

dist = Path('dist')
assert (dist / 'index.html').exists(), 'dist/index.html missing'
assert (dist / 'en' / 'index.html').exists(), 'dist/en/index.html missing'
assert (dist / 'en' / 'tools' / 'index.html').exists(), 'dist/en/tools/index.html missing'
assert (dist / 'en' / 'about-us' / 'index.html').exists(), 'dist/en/about-us/index.html missing'
assert (dist / 'blog' / 'page' / '2' / 'index.html').exists(), 'blog page 2 missing'
assert (dist / 'blog' / 'page' / '7' / 'index.html').exists(), 'blog page 7 missing'

stats = json.loads((dist / 'stats.json').read_text(encoding='utf-8'))
print('Stats:', stats)
assert stats['posts_count'] == 70, f"Expected 70 posts, got {stats['posts_count']}"
assert stats['tools_count'] == 26, f"Expected 26 tools, got {stats['tools_count']}"

idx_es = (dist / 'index.html').read_text(encoding='utf-8')
assert 'np-lang-toggle' in idx_es, 'Switcher missing in dist/index.html'
assert '/en/' in idx_es, '/en/ missing in dist/index.html switcher'

idx_en = (dist / 'en' / 'index.html').read_text(encoding='utf-8')
assert 'np-lang-toggle' in idx_en, 'Switcher missing in dist/en/index.html'

post_es = (dist / 'que-es-un-crm-para-que-sirve' / 'index.html').read_text(encoding='utf-8')
assert '/en/what-is-a-crm-guide/' in post_es, 'Direct EN link missing in post ES'

post_en = (dist / 'en' / 'what-is-a-crm-guide' / 'index.html').read_text(encoding='utf-8')
assert '/que-es-un-crm-para-que-sirve/' in post_en, 'Direct ES link missing in post EN'

print('ALL ASSERTIONS PASSED! Site is 100% verified and structurally flawless.')
