#!/usr/bin/env python3
import csv, json
from pathlib import Path

catalog = list(csv.DictReader(open('data/catalog_master.csv')))
links = {r['sku']: r for r in csv.DictReader(open('data/product_links.csv'))}

products=[]
for c in catalog:
    lk = links.get(c['sku'], {})
    products.append({
      'sku': c['sku'],
      'title': c['product_name'],
      'price': float(c['price_usd']),
      'status': lk.get('status', c.get('status','draft')),
      'channel': lk.get('channel','etsy'),
      'checkout_url': lk.get('checkout_url',''),
      'keyword': c.get('primary_keyword','')
    })

Path('web').mkdir(exist_ok=True)
with open('web/products.json','w') as f:
    json.dump(products,f,indent=2)
print('wrote web/products.json with',len(products),'products')
