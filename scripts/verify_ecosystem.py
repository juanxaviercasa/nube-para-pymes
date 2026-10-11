"""Check generated referral destinations, author credits and bilingual bridge coverage."""
from pathlib import Path
import re
from urllib.parse import urlsplit, parse_qs
from bs4 import BeautifulSoup
from integrate_ecosystem import LISTING_ARTICLES, DIGITAL_ARTICLES, SCENARIOS
from site_routes import route_pairs
from normalize_author_credits import AUTHOR_URL, OLD_DOMAIN

root=Path(__file__).resolve().parents[1]
dist=root/'dist'
pairs=route_pairs(dist)
checks=0
for slug in sorted(LISTING_ARTICLES | DIGITAL_ARTICLES):
    for route in [f'/{slug}/',pairs[f'/{slug}/']]:
        source=(dist/route.strip('/')/'index.html').read_text(encoding='utf-8')
        soup=BeautifulSoup(source,'html.parser')
        bridges=soup.select('.npp-ecosystem-bridge')
        assert len(bridges)==1,(route,'duplicate/missing bridge')
        business=bridges[0].select_one('a[data-ecosystem-destination="todolima"]')
        url=urlsplit(business['href'])
        expected='/auditoria' if slug in DIGITAL_ARTICLES else '/para-negocios'
        assert url.hostname=='todolima.com' and url.path==expected,(route,url)
        assert parse_qs(url.query)['utm_source']==['nubeparapymes']
        assert parse_qs(url.query)['utm_content']==[slug]
        scenarios=bridges[0].select('a[data-ecosystem-destination="mundossimulados"]')
        assert len(scenarios)==int(slug in SCENARIOS)
        for link in scenarios:
            scenario=urlsplit(link['href'])
            assert scenario.hostname=='mundossimulados.online'
            assert scenario.path==f'/{SCENARIOS[slug][0]}/'
        assert any(a.get('href')==AUTHOR_URL for a in soup.select('footer a[href], .ast-footer-copyright a[href]')),(route,'missing current author footer')
        assert OLD_DOMAIN.sub(AUTHOR_URL,source)==source,(route,'stale author URL')
        checks+=1
for route in ['/','/blog/','/herramientas/','/en/','/en/tools/']:
    text=(dist/route.strip('/')/'index.html').read_text(encoding='utf-8')
    assert AUTHOR_URL in text,(route,'missing author credit')
    assert 'juan.cabell' not in text and 'xavier.cabellosalirosas.com' not in text
    checks+=1
print(f'Ecosystem: {checks} routes verified; separate listing/digital destinations, attribution and current author credits.')
