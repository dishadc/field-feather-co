#!/usr/bin/env python3
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'catalog_master.csv'


def load_csv(path: Path):
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    rows = load_csv(CATALOG)
    issues = []

    pin_manifest = {r.get('sku', '').strip() for r in load_csv(ROOT / 'marketing' / 'pinterest' / 'pin_creative_manifest.csv')}

    for r in rows:
        sku = r.get('sku', '').strip()
        sku_l = sku.lower()

        checks = {
            'listing_json': (ROOT / 'listings' / 'etsy-drafts' / f'{sku}.json').exists() or (ROOT / 'listings' / 'etsy-drafts' / 'state-series' / f"{sku.replace('DIGI-STATE-', '').lower()}.json").exists(),
            'preview_docs': (ROOT / 'docs' / 'assets' / 'previews' / f'{sku_l}.svg').exists(),
            'preview_web': (ROOT / 'web' / 'assets' / 'previews' / f'{sku_l}.svg').exists(),
            'delivery_pack': (ROOT / 'products' / 'digital' / 'delivery-packs' / f'{sku_l}.zip').exists(),
            'pin_creative': sku in pin_manifest,
        }

        for check_name, ok in checks.items():
            if not ok:
                issues.append({'sku': sku, 'check': check_name, 'status': 'missing'})

    out_csv = ROOT / 'ops' / 'checklists' / 'catalog_completeness_report.csv'
    out_md = ROOT / 'ops' / 'checklists' / 'catalog_completeness_report.md'
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with out_csv.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['sku', 'check', 'status'])
        w.writeheader()
        w.writerows(issues)

    total = len(rows)
    missing = len(issues)
    ok = missing == 0
    by_check = {}
    for i in issues:
        by_check[i['check']] = by_check.get(i['check'], 0) + 1

    lines = [
        '# Catalog Completeness Report',
        '',
        f'- Total SKUs checked: {total}',
        f'- Missing checks: {missing}',
        f'- Status: {"PASS" if ok else "FAIL"}',
        '',
        '## Missing by check',
    ]
    if by_check:
        for k, v in sorted(by_check.items()):
            lines.append(f'- {k}: {v}')
    else:
        lines.append('- None')

    out_md.write_text('\n'.join(lines) + '\n')

    print(json.dumps({'total_skus': total, 'missing_checks': missing, 'status': 'PASS' if ok else 'FAIL'}))


if __name__ == '__main__':
    main()
