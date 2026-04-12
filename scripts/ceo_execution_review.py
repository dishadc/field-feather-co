#!/usr/bin/env python3
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'ops' / 'checklists'
OUT_JSON = OUT_DIR / 'ceo_execution_review.json'
OUT_MD = OUT_DIR / 'ceo_execution_review.md'

REPORTS = {
    'pages_consistency': OUT_DIR / 'pages_consistency_report.json',
    'storefront_smoke': OUT_DIR / 'storefront_smoke_report.json',
    'browser_qa': OUT_DIR / 'browser_qa_report.json',
    'content_integrity': OUT_DIR / 'content_integrity_report.json',
}


def load_json(path: Path):
    if not path.exists():
        return {'status': 'MISSING', 'path': str(path)}
    try:
        data = json.loads(path.read_text())
        data.setdefault('status', 'UNKNOWN')
        data['path'] = str(path)
        return data
    except Exception as e:
        return {'status': 'ERROR', 'path': str(path), 'error': str(e)}


def content_calendar_summary():
    p = ROOT / 'data' / 'content-calendar.csv'
    rows = list(csv.DictReader(p.open())) if p.exists() else []
    published = sum(1 for r in rows if r.get('status') == 'PUBLISHED')
    queued = sum(1 for r in rows if r.get('status') == 'QUEUED')
    return {'total': len(rows), 'published': published, 'queued': queued}


def published_summary():
    p = ROOT / 'data' / 'published-articles.csv'
    rows = list(csv.DictReader(p.open())) if p.exists() else []
    return {'count': len(rows), 'latest': rows[-3:] if rows else []}


def overall_status(reports: dict):
    statuses = [r.get('status', 'UNKNOWN') for r in reports.values()]
    if any(s in {'FAIL', 'ERROR'} for s in statuses):
        return 'FAIL'
    if any(s in {'WARN', 'MISSING', 'UNKNOWN'} for s in statuses):
        return 'WARN'
    return 'PASS'


def main():
    ts = datetime.now(timezone.utc).isoformat()
    reports = {name: load_json(path) for name, path in REPORTS.items()}
    calendar = content_calendar_summary()
    published = published_summary()
    status = overall_status(reports)

    payload = {
        'generated_at_utc': ts,
        'status': status,
        'reports': reports,
        'content_calendar': calendar,
        'published_articles': published,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + '\n')

    lines = [
        '# CEO Execution Review',
        '',
        f'Generated (UTC): {ts}',
        '',
        f'Overall status: {status}',
        '',
        '## Validation stack',
    ]
    for name, report in reports.items():
        lines.append(f"- {name}: {report.get('status', 'UNKNOWN')} ({report.get('path')})")
    lines.extend([
        '',
        '## Content pipeline',
        f"- planned articles: {calendar['total']}",
        f"- published in calendar: {calendar['published']}",
        f"- still queued: {calendar['queued']}",
        f"- published-articles rows: {published['count']}",
        '',
        '## Latest published entries',
    ])
    if published['latest']:
        for row in published['latest']:
            lines.append(f"- {row.get('publish_date')} — {row.get('title')} — {row.get('status')}")
    else:
        lines.append('- none yet')

    lines.extend([
        '',
        '## CEO review guidance',
        '- If any report is FAIL, redirect active work toward fixes first.',
        '- If reports are missing, the validation system is incomplete for this cycle.',
        '- Use this file as the trace for intraday C-suite/agent/workstream reviews.',
        ''
    ])

    OUT_MD.write_text('\n'.join(lines))
    print(json.dumps({'status': status, 'out_json': str(OUT_JSON), 'out_md': str(OUT_MD)}))


if __name__ == '__main__':
    main()
