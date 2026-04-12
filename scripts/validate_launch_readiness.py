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

missing = [p for p in required_files if not Path(p).exists()]

catalog_rows = list(csv.DictReader(open('data/catalog_master.csv'))) if Path('data/catalog_master.csv').exists() else []
ready_count = sum(1 for r in catalog_rows if r.get('status') == 'ready')

links_rows = list(csv.DictReader(open('data/product_links.csv'))) if Path('data/product_links.csv').exists() else []
live_links = sum(1 for r in links_rows if (r.get('checkout_url') or '').startswith('http'))

print('=== Launch Readiness Validator ===')
print('Required files present:', len(required_files) - len(missing), '/', len(required_files))
if missing:
    print('Missing files:')
    for m in missing:
        print('-', m)

print('Catalog SKUs:', len(catalog_rows))
print('Ready SKUs:', ready_count)
print('Products with live checkout links:', live_links)

if ready_count >= 20 and live_links >= 20 and not missing:
    print('STATUS: GO-LIVE READY')
else:
    print('STATUS: NOT READY')
    if ready_count < 20:
        print('- Need at least 20 ready SKUs')
    if live_links < 20:
        print('- Need checkout URLs for launch SKUs')
