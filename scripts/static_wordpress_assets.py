"""Adapt exported WordPress assets that previously required a live WP server."""
import html
import json
import re
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

CONSENT_CSS = '''.cmplz-hidden,.cmplz-dismissed{display:none!important}.cmplz-cookiebanner{position:fixed;bottom:20px;left:20px;z-index:99999;max-width:390px;width:calc(100vw - 40px);padding:20px;background:#fff;color:#173454;border:1px solid #cbd5e1;border-radius:14px;box-shadow:0 12px 36px #10244833;font:15px/1.5 system-ui,sans-serif}.cmplz-cookiebanner h2{font:700 19px/1.3 system-ui,sans-serif;margin:0 0 10px}.cmplz-cookiebanner p{margin:0 0 12px}.cmplz-buttons{display:flex;flex-wrap:wrap;gap:8px}.cmplz-buttons button{padding:9px 13px;border:1px solid #173454;border-radius:8px;background:#fff;color:#173454;font:600 14px system-ui;cursor:pointer}.cmplz-buttons .cmplz-accept{background:#173454;color:#fff}.cmplz-cookiebanner a{color:#174f9c;text-decoration:underline}.cmplz-manage-consent{position:fixed;bottom:12px;left:12px;z-index:99998;padding:7px 12px;border:1px solid #cbd5e1;border-radius:20px;background:#fff;color:#173454;font:12px system-ui;cursor:pointer}'''

def prepare(dist):
    asset_dir = dist / 'wp-content/uploads/astra-addon'
    assets = {}
    for suffix in ('css', 'js'):
        candidates = sorted(asset_dir.glob('astra-addon-*.' + suffix))
        if not candidates:
            raise FileNotFoundError(f'Missing exported Astra {suffix} bundle')
        assets[suffix] = '/' + candidates[-1].relative_to(dist).as_posix()
    (dist / 'wp-static-arquitect-assets/static-consent.css').write_text(CONSENT_CSS, encoding='utf-8')
    return assets

def normalize(text, is_en, assets):
    # Native Unicode needs no unavailable WordPress emoji REST/static fallback.
    text = re.sub(r'<!--[\s\S]*?-->|<style\b[^>]*>[\s\S]*?</style>|<script\b[^>]*>[\s\S]*?</script>',
                  lambda m: '' if m[0].lower().startswith('<script') and ('wpEmojiSettingsSupports' in m[0] or re.search(r'id=["\x27]wp-emoji-settings["\x27]', m[0])) else m[0], text, flags=re.I)
    for suffix, target in assets.items():
        text = re.sub(r'/wp-content/uploads/astra-addon/astra-addon-[a-zA-Z0-9-]+\.' + suffix, target, text)
    if 'var complianz = ' not in text:
        return text
    def config(match):
        data = json.loads(match[1])
        # The export has no WP REST endpoint or GeoIP service. Keep the existing
        # opt-in engine, cookies and events, with locally rendered banner data.
        data.update(geoip='0', region='eu', consenttype='optin', store_consent='',
                    css_file='/wp-static-arquitect-assets/static-consent.css',
                    locale='lang=en&locale=en_US' if is_en else 'lang=es&locale=es_ES')
        if is_en:
            data['categories'] = {'statistics': 'analytics', 'marketing': 'marketing'}
            data['placeholdertext'] = 'Accept {category} cookies to enable this content'
            data['aria_label'] = data['placeholdertext']
            for links in data.get('page_links', {}).values():
                for key, label, url in [('impressum', 'Legal Notice', '/en/legal-notice/'), ('disclaimer', 'Disclaimer', '/en/disclaimer/')]:
                    if key in links:
                        links[key].update(title=label, url=url)
        return 'var complianz = ' + json.dumps(data, ensure_ascii=False) + ';'
    text = re.sub(r'var complianz = (\{[^\n]+\});', config, text)
    title = 'Cookie preferences' if is_en else 'Preferencias de cookies'
    description = 'We use cookies for essential features, analytics, and advertising. Choose which optional cookies to allow.' if is_en else 'Usamos cookies para funciones esenciales, estadísticas y publicidad. Elige si deseas permitir las cookies opcionales.'
    deny = 'Essential only' if is_en else 'Solo esenciales'
    accept = 'Accept all' if is_en else 'Aceptar todas'
    policy = '/en/cookie-policy/' if is_en else '/politica-de-cookies/'
    policy_label = 'Cookie Policy' if is_en else 'Política de Cookies'
    banner = f'<div id="cmplz-cookiebanner-container"><section class="cmplz-cookiebanner banner-1 optin cmplz-hidden" role="region" aria-label="{title}"><h2>{title}</h2><p>{description} <a class="cmplz-external" href="{policy}">{policy_label}</a></p><div class="cmplz-buttons"><button type="button" class="cmplz-deny">{deny}</button><button type="button" class="cmplz-accept">{accept}</button></div></section></div>'
    text = re.sub(r'<div id="cmplz-cookiebanner-container">[\s\S]*?</div>(?=\s*<div id="cmplz-manage-consent")', lambda _: banner, text)
    text = re.sub(r'<div id="cmplz-manage-consent"[^>]*>[\s\S]*?</div>', f'<div id="cmplz-manage-consent" data-nosnippet="true"><button class="cmplz-manage-consent manage-consent-1 cmplz-hidden" type="button">{title}</button></div>', text)
    return text

def repair_artifact(dist):
    assets = prepare(dist)
    def repair(file):
        text = file.read_text(encoding='utf-8')
        updated = normalize(text, file.relative_to(dist).parts[0] == 'en', assets)
        if updated != text:
            file.write_text(updated, encoding='utf-8')
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(repair, dist.rglob('*.html')))
    print('Static WordPress assets verified and repaired.', flush=True)

if __name__ == '__main__':
    repair_artifact(Path(__file__).resolve().parents[1] / 'dist')
