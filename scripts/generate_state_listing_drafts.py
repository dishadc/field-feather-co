#!/usr/bin/env python3
import csv, json
from pathlib import Path

seed = Path('products/digital/state-checklists/states_seed.csv')
outdir = Path('listings/etsy-drafts/state-series')
outdir.mkdir(parents=True, exist_ok=True)

if not seed.exists():
    print('Missing seed file:', seed)
    raise SystemExit(1)

rows = list(csv.DictReader(seed.open()))
for r in rows:
    state = r['state']
    slug = state.lower().replace(' ', '-')
    tags = [
      f"{state.lower()} birds", 'bird checklist', 'birding printable', 'life list',
      'bird watcher gift', 'birding log', 'nature printable', 'local birds',
      'birding planner', 'eBird tracker', 'backyard birding', 'ornithology', 'instant download'
    ]
    data = {
      'sku': f'DIGI-STATE-{slug.upper()}',
      'title': f'{state} Birding Life List Checklist Printable, Birdwatch Log',
      'price_usd': float(r.get('price_usd', 5.99)),
      'primary_keyword': r.get('primary_keyword', ''),
      'description': f'Track your sightings with this {state}-focused birding life list checklist. Instant digital download. No physical item shipped.',
      'tags': tags,
      'materials': 'digital pdf, printable pages',
      'category': 'Digital > Printable Checklist'
    }
    with open(outdir / f'{slug}.json', 'w') as f:
      json.dump(data, f, indent=2)

print('Generated', len(rows), 'state listing drafts in', outdir)
