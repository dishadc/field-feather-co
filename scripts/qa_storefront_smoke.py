#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'ops' / 'checklists'
OUT_JSON = OUT_DIR / 'storefront_smoke_report.json'
OUT_MD = OUT_DIR / 'storefront_smoke_report.md'

CHECKS = [
    ('home', 'https://dishadc.github.io/field-feather-co/index.html', ['Field & Feather Co.', 'Paper goods for the birder with a careful eye.', 'app.v8.js']),
    ('shop', 'https://dishadc.github.io/field-feather-co/shop.html', ['Filter the shop', 'shop-grid', 'app.v8.js']),
    ('downloads', 'https://dishadc.github.io/field-feather-co/downloads.html', ['Digital Downloads', 'downloads-grid', 'app.v8.js']),
    ('about', 'https://dishadc.github.io/field-feather-co/about.html', ['About the house', 'Field & Feather', 'app.v8.js']),
    ('privacy', 'https://dishadc.github.io/field-feather-co/privacy.html', ['Privacy', 'Field & Feather', 'app.v8.js']),
    ('terms', 'https://dishadc.github.io/field-feather-co/terms.html', ['Terms', 'Field & Feather', 'app.v8.js']),
    ('product_shell', 'https://dishadc.github.io/field-feather-co/product.html?sku=DIGI-STATE-TEXAS', ['product-detail', 'related-grid', 'app.v8.js']),
    ('journal_hub', 'https://dishadc.github.io/field-feather-co/blog/', ['Field Notes Journal', 'Week 1 blitz progress']),
    ('article_beginner', 'https://dishadc.github.io/field-feather-co/blog/birdwatching-for-beginners/', ['Birdwatching for Beginners: The Complete 2026 Guide', 'Sources:']),
    ('article_binoculars', 'https://dishadc.github.io/field-feather-co/blog/best-binoculars-for-birding/', ['Best Binoculars for Birding in 2026', 'Sources:']),
]


def fetch(url):
    req = Request(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    with urlopen(req, timeout=30) as resp:
        return resp.status, resp.read().decode('utf-8', errors='replace')


def main():
    ts = datetime.now(timezone.utc).isoformat()
    results = []
    overall = 'PASS'

    for name, url, needles in CHECKS:
        item = {'name': name, 'url': url, 'status': 'PASS', 'missing': []}
        try:
            status, text = fetch(url)
            item['http_status'] = status
            if status != 200:
                item['status'] = 'FAIL'
            for needle in needles:
                if needle not in text:
                    item['missing'].append(needle)
            if item['missing']:
                item['status'] = 'FAIL'
        except (HTTPError, URLError, TimeoutError, Exception) as e:
            item['status'] = 'FAIL'
            item['error'] = str(e)
        if item['status'] != 'PASS':
            overall = 'FAIL'
        results.append(item)

    payload = {
        'generated_at_utc': ts,
        'status': overall,
        'results': results,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + '\n')

    lines = ['# Storefront Smoke Report', '', f'Generated (UTC): {ts}', '', f'Overall status: {overall}', '', '## Checks']
    for item in results:
        lines.append(f"- {item['name']}: {item['status']} — {item['url']}")
        if item.get('http_status'):
            lines.append(f"  - HTTP: {item['http_status']}")
        if item.get('missing'):
            lines.append(f"  - Missing markers: {', '.join(item['missing'])}")
        if item.get('error'):
            lines.append(f"  - Error: {item['error']}")
    OUT_MD.write_text('\n'.join(lines) + '\n')
    print(json.dumps({'status': overall, 'out_json': str(OUT_JSON), 'out_md': str(OUT_MD)}))


if __name__ == '__main__':
    main()
