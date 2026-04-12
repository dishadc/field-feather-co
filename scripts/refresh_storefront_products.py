#!/usr/bin/env python3
import csv
import json
from pathlib import Path

catalog = list(csv.DictReader(open('data/catalog_master.csv')))
links = {r['sku']: r for r in csv.DictReader(open('data/product_links.csv'))}

map_path = Path('data/gumroad_product_map.csv')
map_rows = list(csv.DictReader(open(map_path))) if map_path.exists() else []
map_by_sku = {r['sku']: r for r in map_rows}

products = []
for c in catalog:
    sku = c['sku']
    lk = links.get(sku, {})
    gm = map_by_sku.get(sku, {})

    checkout_url = (lk.get('checkout_url') or gm.get('checkout_url') or '').strip()
    published_raw = (gm.get('published') or '').strip().lower()
    published = published_raw in {'true', '1', 'yes'}
    purchasable = checkout_url.startswith('http') and published

    products.append({
        'sku': sku,
        'title': c['product_name'],
        'price': float(c['price_usd']),
        'status': lk.get('status', c.get('status', 'draft')),
        'channel': lk.get('channel', 'etsy'),
        'checkout_url': checkout_url,
        'published': published,
        'purchasable': purchasable,
        'keyword': c.get('primary_keyword', '')
    })

with open('web/products.json', 'w') as f:
    json.dump(products, f, indent=2)

linked = sum(1 for p in products if (p['checkout_url'] or '').startswith('http'))
live = sum(1 for p in products if p.get('purchasable'))
print('Updated storefront product data')
print('Total products:', len(products))
print('Checkout links present:', linked)
print('Purchasable now:', live)
