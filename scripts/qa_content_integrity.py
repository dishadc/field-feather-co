#!/usr/bin/env python3
import csv
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'ops' / 'checklists'
OUT_JSON = OUT_DIR / 'content_integrity_report.json'
OUT_MD = OUT_DIR / 'content_integrity_report.md'
BLOG_ROOT = ROOT / 'docs' / 'blog'
PUBLISHED = ROOT / 'data' / 'published-articles.csv'
PRODUCTS = ROOT / 'docs' / 'products.json'
PREVIEWS_DOCS = ROOT / 'docs' / 'assets' / 'previews'
PREVIEWS_WEB = ROOT / 'web' / 'assets' / 'previews'
PUBLIC_PAGES = list((ROOT / 'docs').rglob('*.html'))
LEGACY_NEWSLETTER_ROUTE_PAGES = list((ROOT / 'docs').glob('*.html')) + list((ROOT / 'web').glob('*.html'))
FORBIDDEN_PUBLIC_MARKERS = [
    'Temporary editorial HQ',
    'Editorial ops',
    'GitHub Pages',
    'Cloudways',
    'CMS credentials',
    'owner action',
    'temporary placeholders',
    'Affiliate placeholders',
    'placeholder pending',
    'pending Amazon setup',
    'pending Bookshop.org',
    'temporary live publishing home',
    'temporary publishing layer',
    'temporary publishing base',
    'Temporary journal host live on GitHub Pages',
    'WordPress cutover',
    'CMS stack',
    'permanent CMS stack',
    'wing_bustle30@icloud.com',
    'mailto:wing_bustle30@icloud.com',
]


def fetch(url):
    req = Request(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    with urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode('utf-8', errors='replace')


def article_local_path(url):
    part = url.split('/blog/', 1)[-1].strip('/')
    return BLOG_ROOT / part / 'index.html'


def count_internal_links(html):
    hrefs = re.findall(r'href="([^"]+)"', html)
    count = 0
    for href in hrefs:
        if href.startswith('../') or 'dishadc.github.io/field-feather-co/blog/' in href:
            count += 1
    return count


def scan_forbidden_markers(path):
    text = path.read_text() if path.exists() else ''
    found = [marker for marker in FORBIDDEN_PUBLIC_MARKERS if marker in text]
    return {
        'path': str(path),
        'exists': path.exists(),
        'forbidden_markers': found,
        'status': 'PASS' if path.exists() and not found else 'FAIL',
    }




def scan_newsletter_cta(path):
    text = path.read_text() if path.exists() else ''
    has_module = 'The Morning Warbler' in text and ('morning-warbler/index.html' in text or 'welcome/index.html' in text) and 'Read about the journal' in text
    has_source = 'data-newsletter-source=' in text
    has_offer = 'data-newsletter-offer=' in text
    has_cluster = 'data-newsletter-cluster=' in text
    status = 'PASS'
    if has_module and not (has_source and has_offer and has_cluster):
        status = 'FAIL'
    return {
        'path': str(path),
        'has_module': has_module,
        'has_source': has_source,
        'has_offer': has_offer,
        'has_cluster': has_cluster,
        'status': status,
    }



def scan_legacy_newsletter_routes(path):
    text = path.read_text() if path.exists() else ''
    found = 'blog/welcome/index.html' in text
    return {
        'path': str(path),
        'legacy_route_found': found,
        'status': 'FAIL' if found else 'PASS',
    }

def main():
    ts = datetime.now(timezone.utc).isoformat()
    overall = 'PASS'
    article_results = []

    rows = list(csv.DictReader(PUBLISHED.open())) if PUBLISHED.exists() else []
    for row in rows:
        item = {'title': row.get('title'), 'url': row.get('url'), 'status': 'PASS'}
        local = article_local_path(row['url'])
        item['local_exists'] = local.exists()
        if not item['local_exists']:
            item['status'] = 'FAIL'
        try:
            http_status, html = fetch(row['url'])
            item['http_status'] = http_status
            title_ok = row['title'] in html
            meta_ok = '<meta name="description"' in html
            sources_ok = 'Sources:' in html
            internal_link_count = count_internal_links(html)
            item.update({
                'title_present': title_ok,
                'meta_present': meta_ok,
                'sources_present': sources_ok,
                'internal_links': internal_link_count,
            })
            if not (title_ok and meta_ok and sources_ok and internal_link_count >= 3):
                item['status'] = 'FAIL'
        except Exception as e:
            item['status'] = 'FAIL'
            item['error'] = str(e)
        if item['status'] != 'PASS':
            overall = 'FAIL'
        article_results.append(item)

    products = json.loads(PRODUCTS.read_text()) if PRODUCTS.exists() else []
    asset_results = []
    for p in products:
        sku = (p.get('sku') or '').lower()
        expected = f'{sku}.svg' if sku else None
        item = {'sku': p.get('sku'), 'status': 'PASS', 'expected': expected}
        if expected:
            item['docs_exists'] = (PREVIEWS_DOCS / expected).exists()
            item['web_exists'] = (PREVIEWS_WEB / expected).exists()
            if not (item['docs_exists'] and item['web_exists']):
                item['status'] = 'FAIL'
                overall = 'FAIL'
        asset_results.append(item)

    public_surface_results = [scan_forbidden_markers(path) for path in PUBLIC_PAGES]
    for item in public_surface_results:
        if item['status'] != 'PASS':
            overall = 'FAIL'

    newsletter_cta_results = [scan_newsletter_cta(path) for path in PUBLIC_PAGES]
    for item in newsletter_cta_results:
        if item['status'] != 'PASS':
            overall = 'FAIL'

    legacy_newsletter_route_results = [scan_legacy_newsletter_routes(path) for path in LEGACY_NEWSLETTER_ROUTE_PAGES]
    for item in legacy_newsletter_route_results:
        if item['status'] != 'PASS':
            overall = 'FAIL'

    payload = {
        'generated_at_utc': ts,
        'status': overall,
        'article_results': article_results,
        'asset_results': asset_results,
        'public_surface_results': public_surface_results,
        'newsletter_cta_results': newsletter_cta_results,
        'legacy_newsletter_route_results': legacy_newsletter_route_results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + '\n')

    lines = ['# Content Integrity Report', '', f'Generated (UTC): {ts}', '', f'Overall status: {overall}', '', '## Published article checks']
    for item in article_results:
        lines.append(f"- {item['title']}: {item['status']}")
        lines.append(f"  - url: {item['url']}")
        lines.append(f"  - local file exists: {item.get('local_exists')}")
        if 'http_status' in item:
            lines.append(f"  - HTTP: {item['http_status']}")
        if 'title_present' in item:
            lines.append(f"  - title present: {item['title_present']}")
            lines.append(f"  - meta present: {item['meta_present']}")
            lines.append(f"  - sources present: {item['sources_present']}")
            lines.append(f"  - internal links: {item['internal_links']}")
        if item.get('error'):
            lines.append(f"  - error: {item['error']}")
    lines.extend(['', '## Preview asset checks'])
    bad_assets = [a for a in asset_results if a['status'] != 'PASS']
    if bad_assets:
        for item in bad_assets:
            lines.append(f"- {item['sku']}: FAIL (docs={item.get('docs_exists')}, web={item.get('web_exists')})")
    else:
        lines.append('- All expected preview assets exist in docs/ and web/.')

    lines.extend(['', '## Public surface leakage checks'])
    for item in public_surface_results:
        lines.append(f"- {item['path']}: {item['status']}")
        if item.get('forbidden_markers'):
            lines.append(f"  - forbidden markers: {', '.join(item['forbidden_markers'])}")

    lines.extend(['', '## Newsletter CTA attribution checks'])
    for item in newsletter_cta_results:
        if item['has_module']:
            lines.append(f"- {item['path']}: {item['status']}")
            lines.append(f"  - source attr: {item['has_source']}")
            lines.append(f"  - offer attr: {item['has_offer']}")
            lines.append(f"  - cluster attr: {item['has_cluster']}")

    lines.extend(['', '## Legacy newsletter route checks'])
    for item in legacy_newsletter_route_results:
        lines.append(f"- {item['path']}: {item['status']}")
        lines.append(f"  - legacy welcome route found: {item['legacy_route_found']}")

    OUT_MD.write_text('\n'.join(lines) + '\n')
    print(json.dumps({'status': overall, 'out_json': str(OUT_JSON), 'out_md': str(OUT_MD)}))


if __name__ == '__main__':
    main()
