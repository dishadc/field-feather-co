#!/usr/bin/env python3
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DOCS_INDEX = ROOT / 'docs' / 'index.html'
OUT_DIR = ROOT / 'ops' / 'checklists'
OUT_JSON = OUT_DIR / 'pages_consistency_report.json'
OUT_MD = OUT_DIR / 'pages_consistency_report.md'

LIVE_URL = 'https://dishadc.github.io/field-feather-co/index.html'
RAW_URL = 'https://raw.githubusercontent.com/dishadc/field-feather-co/main/docs/index.html'

NEEDLES = {
    'catalog_preview_copy': [
        'The collection is in preview while checkout finishes its final setup.',
        'Gathering today’s availability from the catalog.'
    ],
    'coming_soon_cta': 'Coming Soon',
    'legacy_live_copy': 'live downloads now available',
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def fetch_text(url: str) -> str:
    req = Request(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode('utf-8', errors='replace')


def gh_latest_pages_run() -> dict:
    try:
        cmd = ['gh', 'run', 'list', '--workflow', 'pages-build-deployment', '--limit', '1', '--json', 'databaseId,status,conclusion,createdAt,updatedAt,url']
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        if p.returncode != 0:
            return {'ok': False, 'error': (p.stderr or p.stdout).strip()[:400]}
        data = json.loads(p.stdout or '[]')
        if not data:
            return {'ok': False, 'error': 'No pages-build-deployment runs found'}
        run = data[0]
        return {'ok': True, 'run': run}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main() -> None:
    ts = datetime.now(timezone.utc).isoformat()
    local_text = DOCS_INDEX.read_text(encoding='utf-8')
    raw_text = fetch_text(RAW_URL)
    live_text = fetch_text(LIVE_URL)

    local_sha = sha256_text(local_text)
    raw_sha = sha256_text(raw_text)
    live_sha = sha256_text(live_text)

    checks = {
        'raw_matches_local': raw_sha == local_sha,
        'live_matches_raw': live_sha == raw_sha,
        'live_has_catalog_preview_copy': any(needle in live_text for needle in NEEDLES['catalog_preview_copy']),
        'live_has_coming_soon': NEEDLES['coming_soon_cta'] in live_text,
        'live_has_legacy_live_copy': NEEDLES['legacy_live_copy'] in live_text,
    }

    pages_run = gh_latest_pages_run()

    status = 'PASS'
    reasons = []
    if not checks['raw_matches_local']:
        status = 'FAIL'
        reasons.append('raw_github_not_matching_local_main')
    if not checks['live_matches_raw']:
        status = 'WARN' if status == 'PASS' else status
        reasons.append('gh_pages_edge_not_yet_in_sync')
    if not checks['live_has_catalog_preview_copy']:
        status = 'FAIL'
        reasons.append('missing_catalog_preview_copy_on_live')

    payload = {
        'generated_at_utc': ts,
        'status': status,
        'reasons': reasons,
        'urls': {'live': LIVE_URL, 'raw': RAW_URL},
        'sha256': {'local_docs_index': local_sha, 'raw_main_docs_index': raw_sha, 'live_docs_index': live_sha},
        'checks': checks,
        'latest_pages_run': pages_run,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')

    run_line = 'Unavailable'
    if pages_run.get('ok'):
        run = pages_run['run']
        run_line = f"{run.get('status')} / {run.get('conclusion')} / {run.get('url')}"
    else:
        run_line = f"error: {pages_run.get('error')}"

    md = f"""# GitHub Pages Consistency Report

Generated (UTC): {ts}

Status: {status}
Reasons: {', '.join(reasons) if reasons else 'none'}

## Pipeline
Latest pages-build-deployment: {run_line}

## Content consistency
- raw matches local docs/index.html: {checks['raw_matches_local']}
- live matches raw main docs/index.html: {checks['live_matches_raw']}
- live has catalog preview copy: {checks['live_has_catalog_preview_copy']}
- live has Coming Soon text: {checks['live_has_coming_soon']}
- live still has legacy \"live downloads now available\" string: {checks['live_has_legacy_live_copy']}

## SHA256
- local docs/index.html: `{local_sha}`
- raw main docs/index.html: `{raw_sha}`
- live index.html: `{live_sha}`

## URLs
- Live: {LIVE_URL}
- Raw main docs: {RAW_URL}
"""
    OUT_MD.write_text(md, encoding='utf-8')

    print(json.dumps({'status': status, 'reasons': reasons, 'out_json': str(OUT_JSON), 'out_md': str(OUT_MD)}))


if __name__ == '__main__':
    main()
