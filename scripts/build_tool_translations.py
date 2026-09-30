"""Reuse reviewed tool translations for React-rendered and dynamic UI text."""
import ast
import html
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from site_routes import ROOT, TOOLS_MAP

def build(dist):
    common = {}
    overrides = {}
    for name in ('tool-ui.json', 'tool-ui-additions.json'):
        overrides.update(json.loads((ROOT / 'content/en' / name).read_text(encoding='utf-8')))
    def add(source, target):
        source, target = html.unescape(source).strip(), html.unescape(target).strip()
        if source.startswith('>') and source.endswith('<'):
            source, target = source[1:-1], target.strip('><')
        if re.search(r'<[a-zA-Z]', source):
            source = BeautifulSoup(source, 'html.parser').get_text(' ', strip=True)
            target = BeautifulSoup(target, 'html.parser').get_text(' ', strip=True)
        source, target = re.sub(r'\s+', ' ', source), re.sub(r'\s+', ' ', target)
        if source and source != target and '<' not in source and '=' not in source and '<' not in target:
            common[source] = target
    def collect(value):
        if isinstance(value, dict):
            for key, item in value.items():
                if isinstance(key, str) and isinstance(item, str): add(key, item)
                else: collect(item)
        elif isinstance(value, (list, tuple)):
            if len(value) == 2 and all(isinstance(x, str) for x in value): add(*value)
            else:
                for item in value: collect(item)
    for name in ('translate_all_tools.py', 'translate_tools_deep.py', 'translate_all_tools_deep_v2.py', 'translate_tools_deep_v3.py', 'translate_tools_deep_v4.py', 'translate_tools_deep_final.py'):
        tree = ast.parse((ROOT / 'scripts' / name).read_text(encoding='utf-8-sig'))
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and 'REPLACEMENTS' in t.id for t in node.targets):
                collect(ast.literal_eval(node.value))
    common.update(overrides)
    dictionaries = {}
    def tool_dictionary(tool):
        es = BeautifulSoup((ROOT / tool['src']).read_text(encoding='utf-8'), 'html.parser')
        en = BeautifulSoup((ROOT / 'en' / (tool['en_slug'] + '.html')).read_text(encoding='utf-8'), 'html.parser')
        mapping = dict(common)
        for old, new in zip(es.select('h1'), en.select('h1')):
            left, right = old.get_text(' ', strip=True), new.get_text(' ', strip=True)
            if left != right: mapping[left] = right
        targets = {}
        for node in en.select('[data-visual-edit-loc]'):
            targets.setdefault(node['data-visual-edit-loc'], []).append(node)
        positions = {}
        for node in es.select('[data-visual-edit-loc]'):
            location = node['data-visual-edit-loc']
            position = positions.get(location, 0)
            positions[location] = position + 1
            candidates = targets.get(location, [])
            if position >= len(candidates): continue
            target = candidates[position]
            left = [str(x).strip() for x in node.children if isinstance(x, str) and str(x).strip()]
            right = [str(x).strip() for x in target.children if isinstance(x, str) and str(x).strip()]
            if len(left) == len(right):
                for old, new in zip(left, right):
                    if old != new: mapping[old] = new
            for attr in ('placeholder', 'aria-label', 'title'):
                if node.get(attr) and target.get(attr) and node[attr] != target[attr]: mapping[node[attr]] = target[attr]
        mapping.update(overrides)
        # Earlier static translations occasionally left a Spanish phrase inside
        # an otherwise English sentence. Resolve those reviewed fragments too.
        fragments = sorted(overrides.items(), key=lambda item: len(item[0]), reverse=True)
        for source, target in mapping.items():
            for old, new in fragments:
                if old in target:
                    target = re.sub(r'(?<!\w)' + re.escape(old) + r'(?!\w)', lambda _: new, target)
            mapping[source] = target
        return tool['en_slug'], mapping
    with ThreadPoolExecutor(max_workers=8) as executor:
        dictionaries.update(executor.map(tool_dictionary, TOOLS_MAP.values()))
    directory = dist / 'en/translations'
    directory.mkdir(parents=True, exist_ok=True)
    runtime = (ROOT / 'js/tool-localization.js').read_text(encoding='utf-8')
    patterns = (ROOT / 'content/en/tool-ui-patterns.json').read_text(encoding='utf-8')
    json.loads(patterns)
    for slug, mapping in dictionaries.items():
        (directory / (slug + '.js')).write_text('window.NPP_TOOL_TEXT = ' + json.dumps(mapping, ensure_ascii=False) + ';\nwindow.NPP_TOOL_PATTERNS = ' + patterns + ';\n' + runtime, encoding='utf-8')
    print(f'[I18N] Dynamic translations generated for {len(dictionaries)} tools', flush=True)

if __name__ == '__main__':
    build(ROOT / 'dist')
