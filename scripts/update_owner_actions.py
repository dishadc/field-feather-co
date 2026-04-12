#!/usr/bin/env python3
import csv
import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_rows(path: Path):
    if not path.exists():
        return []
    with path.open() as f:
        return list(csv.DictReader(f))


def load_json(path: Path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except Exception:
        return {}


def main() -> None:
    catalog = load_rows(ROOT / 'data' / 'catalog_master.csv')
    links = load_rows(ROOT / 'data' / 'product_links.csv')
    gmap = load_rows(ROOT / 'data' / 'gumroad_product_map.csv')
    pages = load_json(ROOT / 'ops' / 'checklists' / 'pages_consistency_report.json')

    ready = {r.get('sku', '').strip() for r in catalog if (r.get('status') or '').strip().lower() == 'ready'}
    ready.discard('')

    links_by_sku = {r.get('sku', '').strip(): r for r in links}
    gmap_by_sku = {r.get('sku', '').strip(): r for r in gmap}

    ready_with_link = 0
    ready_published = 0
    for sku in ready:
        lrow = links_by_sku.get(sku, {})
        mrow = gmap_by_sku.get(sku, {})
        checkout = (lrow.get('checkout_url') or '').strip()
        published = (mrow.get('published') or '').strip().lower() in {'true', '1', 'yes'}
        if checkout.startswith('http'):
            ready_with_link += 1
        if checkout.startswith('http') and published:
            ready_published += 1

    missing_links = sorted([sku for sku in ready if not (links_by_sku.get(sku, {}).get('checkout_url') or '').strip().startswith('http')])
    unpublished = sorted([
        sku for sku in ready
        if (links_by_sku.get(sku, {}).get('checkout_url') or '').strip().startswith('http')
        and (gmap_by_sku.get(sku, {}).get('published') or '').strip().lower() not in {'true', '1', 'yes'}
    ])

    now = datetime.now().strftime('%Y-%m-%d %H:%M %Z')
    pages_status = (pages.get('status') or 'UNKNOWN').upper()
    pages_reasons = ', '.join(pages.get('reasons') or []) or 'none'
    pages_checks = pages.get('checks') or {}
    pages_live_sync = pages_checks.get('live_matches_raw', 'unknown')
    pages_preview_copy = pages_checks.get('live_has_catalog_preview_copy', 'unknown')

    body = f'''# OWNER_ACTIONS_REQUIRED

Purpose: single inbox for anything required from you.
I keep this file updated continuously.

Last updated: {now}

## OPEN (blocking revenue now)

1) Connect Gumroad payout method (hard blocker)
- Why needed: Gumroad API rejects product publishing until payout is connected.
- Evidence: `PUT /v2/products/:id/enable` -> `You must connect at least one payment method before you can publish this product for sale.`
- Current impact snapshot:
  - Ready SKUs: {len(ready)}
  - Ready with checkout URLs: {ready_with_link}
  - Ready published on Gumroad: {ready_published}
  - Ready missing links: {len(missing_links)}
- Your action:
  - Log in to Gumroad
  - Settings -> Payments/Payouts
  - Connect bank/PayPal and complete verification
- What I will do immediately after:
  - auto-run publish/sync loops to drive 20/20 published launch SKUs.

## OPEN (channel expansion blocker)

2) Etsy app approval completion
- Why needed: Etsy OAuth remains blocked while app is pending approval.
- Your action:
  - Complete Etsy app approval to active status.
- What I will do immediately after:
  - OAuth token exchange
  - persist tokens in `.env`
  - activate Etsy publish automation.

## OPEN (security hygiene, post-launch)

3) Rotate previously shared credentials/tokens
- Why needed: credentials shared in chat should be treated as compromised.
- Your action: rotate account password and API tokens after payout setup stabilization.
- What I will do: update `.env` references and verify automation with new secrets.

## Diagnostic detail (agent-managed)
- Pages consistency status: {pages_status}
- Pages reasons: {pages_reasons}
- Pages live matches raw main: {pages_live_sync}
- Pages has catalog preview copy: {pages_preview_copy}
- Unpublished ready SKUs with links:
  - {', '.join(unpublished) if unpublished else 'None'}
- Ready SKUs missing checkout links:
  - {', '.join(missing_links) if missing_links else 'None'}
'''

    out = ROOT / 'ops' / 'checklists' / 'OWNER_ACTIONS_REQUIRED.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body)
    print(f'updated {out}')


if __name__ == '__main__':
    main()
