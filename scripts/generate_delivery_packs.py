#!/usr/bin/env python3
import csv
import json
import zipfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'data' / 'catalog_master.csv'
PREVIEWS = ROOT / 'docs' / 'assets' / 'previews'
LISTINGS = ROOT / 'listings' / 'etsy-drafts'
OUT_DIR = ROOT / 'products' / 'digital' / 'delivery-packs'
MANIFEST = ROOT / 'data' / 'product_asset_manifest.csv'

STATE_ASSETS = ROOT / 'products' / 'digital' / 'state-checklists' / 'assets'
MIGRATION_ASSETS = ROOT / 'products' / 'digital' / 'migration-trackers' / 'assets'
WARBLER_ASSETS = ROOT / 'products' / 'digital' / 'warbler-pack' / 'assets'


def load_catalog():
    with CATALOG.open() as f:
        return list(csv.DictReader(f))


def resolve_interior_assets(sku: str) -> list[Path]:
    sku = sku.strip().upper()

    if sku.startswith('DIGI-STATE-'):
        state = sku.replace('DIGI-STATE-', '').lower().replace('_', '-')
        p = STATE_ASSETS / f'{state}-life-list.svg'
        return [p] if p.exists() else []

    if sku.startswith('DIGI-MIGRATION-WEEKLY-'):
        num = sku.split('-')[-1]
        p = MIGRATION_ASSETS / f'migration-weekly-{num}.svg'
        return [p] if p.exists() else []

    if sku == 'DIGI-WARBLER-BUNDLE-001':
        return sorted(WARBLER_ASSETS.glob('*.svg'))

    if sku == 'DIGI-WARBLER-PEAK-WEEK-011':
        p = WARBLER_ASSETS / '02-spring-migration-tracker.svg'
        return [p] if p.exists() else []

    if sku == 'DIGI-WARBLER-LIFER-CHECKLIST-014':
        p = WARBLER_ASSETS / '03-county-life-list.svg'
        return [p] if p.exists() else []

    return []


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = load_catalog()
    manifest_rows = []
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    for row in rows:
        sku = row['sku'].strip()
        title = row.get('product_name', '').strip()
        price = row.get('price_usd', '').strip()
        status = (row.get('status') or 'draft').strip().lower()
        family = row.get('product_family', 'birding').strip()

        zip_path = OUT_DIR / f'{sku.lower()}.zip'
        preview = PREVIEWS / f'{sku.lower()}.svg'
        listing_json = LISTINGS / f'{sku}.json'
        interiors = resolve_interior_assets(sku)

        readme = f'''Field & Feather Co.\nSKU: {sku}\nTitle: {title}\nFamily: {family}\nStatus: {status}\nPrice USD: {price}\n\nPackage generated: {now}\nContents:\n- preview.svg (cover/marketing creative)\n- listing.json (commerce metadata, if available)\n- interiors/*.svg (printable interior pages, when available)\n- license.txt\n\nLicense:\nOriginal Field & Feather Co. product creative for commercial sale via brand-owned channels.\n'''

        license_txt = f'''Field & Feather Co. Asset License\n\nSKU: {sku}\nGenerated: {now}\n\nThese assets are proprietary to Field & Feather Co.\nPermitted use: listing images, storefront display, customer delivery packs for this SKU.\nProhibited use: resale or redistribution outside Field & Feather Co. channels.\n'''

        with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('README.txt', readme)
            zf.writestr('license.txt', license_txt)
            if preview.exists():
                zf.write(preview, arcname='preview.svg')
            else:
                zf.writestr('preview-missing.txt', f'Preview missing for {sku}.')
            if listing_json.exists():
                zf.write(listing_json, arcname='listing.json')
            else:
                zf.writestr('listing-missing.txt', f'Listing draft missing for {sku}.')

            if interiors:
                for p in interiors:
                    zf.write(p, arcname=f'interiors/{p.name}')
            else:
                zf.writestr('interiors-missing.txt', f'No mapped interior pages found for {sku}.')

        manifest_rows.append({
            'sku': sku,
            'zip_path': str(zip_path.relative_to(ROOT)),
            'preview_present': str(preview.exists()).lower(),
            'listing_json_present': str(listing_json.exists()).lower(),
            'interior_pages': str(len(interiors)),
            'status': status,
            'generated_at_utc': now,
        })

    with MANIFEST.open('w', newline='') as f:
        fields = ['sku', 'zip_path', 'preview_present', 'listing_json_present', 'interior_pages', 'status', 'generated_at_utc']
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(manifest_rows)

    print(json.dumps({'generated_packs': len(manifest_rows), 'with_interiors': sum(1 for r in manifest_rows if int(r['interior_pages']) > 0), 'out_dir': str(OUT_DIR), 'manifest': str(MANIFEST)}))


if __name__ == '__main__':
    main()
