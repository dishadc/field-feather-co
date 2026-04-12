#!/usr/bin/env python3
import csv
from pathlib import Path
from datetime import date

kpi_file = Path('data/kpi_tracker.csv')
if not kpi_file.exists():
    print('KPI file missing: data/kpi_tracker.csv')
    raise SystemExit(1)

rows = list(csv.DictReader(kpi_file.open()))
if not rows:
    print('No KPI rows found')
    raise SystemExit(1)

latest = rows[-1]

def fnum(v, d=2):
    try:
        return f"{float(v):.{d}f}"
    except Exception:
        return str(v)

rev = float(latest.get('revenue_usd', 0) or 0)
ad = float(latest.get('ad_spend_usd', 0) or 0)
soft = float(latest.get('software_spend_usd', 0) or 0)
orders = float(latest.get('orders', 0) or 0)
visits = float(latest.get('etsy_visits', 0) or 0)
net_before_cogs = rev - ad - soft

print('=== Field & Feather Daily KPI Brief ===')
print('Date:', latest.get('date', date.today().isoformat()))
print('Listings live:', latest.get('listings_live', '0'))
print('Visits:', latest.get('etsy_visits', '0'))
print('Orders:', latest.get('orders', '0'))
print('Conversion rate:', latest.get('conversion_rate', '0'))
print('Favorites:', latest.get('favorites', '0'))
print('Revenue USD:', fnum(rev))
print('Ad spend USD:', fnum(ad))
print('Software spend USD:', fnum(soft))
print('Net pre-COGS USD:', fnum(net_before_cogs))
print('Gross margin %:', latest.get('gross_margin_pct', '0'))

if visits > 0 and orders == 0:
    print('Action: Improve first 10 listing thumbnails and first 40 title characters.')
elif visits < 100:
    print('Action: Publish 3 Pinterest pins and 2 new long-tail listings today.')
elif rev < 500:
    print('Action: Keep stack lean; do not upgrade paid tools yet.')
else:
    print('Action: Eligible to test Marmalead + Printify Premium ROI.')
