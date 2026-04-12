#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_csv(path: Path):
    with path.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    catalog = load_csv(ROOT / 'data' / 'catalog_master.csv')
    links = {r['sku']: r for r in load_csv(ROOT / 'data' / 'product_links.csv')}
    gmap_rows = load_csv(ROOT / 'data' / 'gumroad_product_map.csv') if (ROOT / 'data' / 'gumroad_product_map.csv').exists() else []
    gmap = {r['sku']: r for r in gmap_rows}

    backlog = []
    for row in catalog:
        sku = row['sku']
        status = (row.get('status') or 'draft').lower()
        family = row.get('product_family', '')
        prio_base = 1 if status == 'ready' else 3
        if family == 'warbler':
            prio_base = max(1, prio_base - 1)

        l = links.get(sku, {})
        m = gmap.get(sku, {})
        has_link = (l.get('checkout_url') or '').startswith('http')
        published = (m.get('published') or '').lower() in {'true', '1', 'yes'}

        if status == 'ready' and (not has_link):
            action = 'create_product_link'
            priority_tier = 1
        elif status == 'ready' and has_link and not published:
            action = 'publish_existing_product'
            priority_tier = 1
        elif status == 'draft':
            action = 'prepare_then_publish'
            priority_tier = prio_base
        else:
            action = 'monitor'
            priority_tier = 4

        backlog.append({
            'priority_tier': priority_tier,
            'sku': sku,
            'status': status,
            'family': family,
            'price_usd': row.get('price_usd', ''),
            'action': action,
            'has_checkout_link': str(has_link).lower(),
            'published': str(published).lower(),
        })

    backlog.sort(key=lambda r: (int(r['priority_tier']), r['sku']))
    for i, r in enumerate(backlog, start=1):
        r['queue_order'] = i

    out = ROOT / 'ops' / 'checklists' / 'publish_backlog_all_channels.csv'
    with out.open('w', newline='') as f:
        fields = ['queue_order', 'priority_tier', 'sku', 'status', 'family', 'price_usd', 'action', 'has_checkout_link', 'published']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(backlog)

    print(f'wrote {out} with {len(backlog)} rows')


if __name__ == '__main__':
    main()
