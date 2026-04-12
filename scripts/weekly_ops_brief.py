#!/usr/bin/env python3
import csv
from pathlib import Path

catalog = list(csv.DictReader(open('data/catalog_master.csv')))
queue = list(csv.DictReader(open('listings/etsy-publish-queue.csv')))
kpi = list(csv.DictReader(open('data/kpi_tracker.csv')))

latest = kpi[-1] if kpi else {}
ready = sum(1 for r in catalog if r.get('status') == 'ready')
drafts = sum(1 for r in catalog if r.get('status') != 'ready')
queued = sum(1 for r in queue if r.get('status') == 'queued')

print('=== Field & Feather Weekly Ops Brief ===')
print('Catalog total:', len(catalog), '| Ready:', ready, '| Draft:', drafts)
print('Etsy queue queued:', queued)
print('Latest KPI date:', latest.get('date', 'n/a'))
print('Revenue:', latest.get('revenue_usd', '0'), '| Orders:', latest.get('orders', '0'), '| Visits:', latest.get('etsy_visits', '0'))

if ready < 20:
    print('Priority: Move at least', 20-ready, 'draft SKUs to ready status.')
else:
    print('Priority: Publish/verify checkout links for all ready SKUs.')
