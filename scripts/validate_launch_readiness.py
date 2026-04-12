#!/usr/bin/env python3
import csv
from pathlib import Path

required_files = [
    'SOUL.md',
    'AGENTS.md',
    'data/kpi_tracker.csv',
    'data/catalog_master.csv',
    'listings/etsy-publish-queue.csv',
    'web/index.html',
    'web/products.json',
    'ops/checklists/go-live-gate.md'
]

missing_files = [p for p in required_files if not Path(p).exists()]

catalog_rows = list(csv.DictReader(open('data/catalog_master.csv'))) if Path('data/catalog_master.csv').exists() else []
ready_skus = {r.get('sku', '').strip() for r in catalog_rows if (r.get('status') or '').strip().lower() == 'ready'}
ready_skus.discard('')

links_rows = list(csv.DictReader(open('data/product_links.csv'))) if Path('data/product_links.csv').exists() else []
links_by_sku = {r.get('sku', '').strip(): r for r in links_rows}

map_rows = list(csv.DictReader(open('data/gumroad_product_map.csv'))) if Path('data/gumroad_product_map.csv').exists() else []
map_by_sku = {r.get('sku', '').strip(): r for r in map_rows}

ready_with_checkout = 0
ready_published = 0
ready_missing_checkout = []
ready_unpublished = []

for sku in sorted(ready_skus):
    lrow = links_by_sku.get(sku, {})
    mrow = map_by_sku.get(sku, {})
    checkout = (lrow.get('checkout_url') or mrow.get('checkout_url') or '').strip()
    published_raw = (mrow.get('published') or '').strip().lower()
    is_published = published_raw in {'true', '1', 'yes'}

    if checkout.startswith('http'):
        ready_with_checkout += 1
    else:
        ready_missing_checkout.append(sku)

    if checkout.startswith('http') and is_published:
        ready_published += 1
    elif checkout.startswith('http') and not is_published:
        ready_unpublished.append(sku)

print('=== Launch Readiness Validator ===')
print('Required files present:', len(required_files) - len(missing_files), '/', len(required_files))
if missing_files:
    print('Missing files:')
    for m in missing_files:
        print('-', m)

print('Catalog SKUs:', len(catalog_rows))
print('Ready SKUs:', len(ready_skus))
print('Ready SKUs with checkout URL:', ready_with_checkout)
print('Ready SKUs published on Gumroad:', ready_published)

if len(ready_skus) >= 20 and ready_published >= 20 and not missing_files:
    print('STATUS: GO-LIVE READY')
else:
    print('STATUS: NOT READY')
    if len(ready_skus) < 20:
        print('- Need at least 20 ready SKUs')
    if ready_with_checkout < 20:
        print('- Need checkout URLs for all ready launch SKUs')
    if ready_published < 20:
        print('- Need Gumroad published=true for all ready launch SKUs')
    if ready_unpublished:
        print('- Unpublished ready SKUs with checkout URLs:', ', '.join(ready_unpublished[:12]))
    if ready_missing_checkout:
        print('- Ready SKUs missing checkout URLs:', ', '.join(ready_missing_checkout[:12]))
