#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ['python3', 'scripts/publish_gumroad_products.py', '--max-create', '10'],
    ['python3', 'scripts/refresh_storefront_products.py'],
    ['python3', 'scripts/validate_launch_readiness.py'],
    ['python3', 'scripts/validate_catalog_completeness.py'],
    ['python3', 'scripts/build_publish_backlog.py'],
    ['python3', 'scripts/update_owner_actions.py'],
    ['python3', 'scripts/daily_kpi_report.py'],
    ['python3', 'scripts/weekly_ops_brief.py'],
]


def run(cmd):
    print('\n$ ' + ' '.join(cmd))
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if p.stdout:
        print(p.stdout.strip())
    if p.stderr:
        print(p.stderr.strip())
    return p.returncode


def main():
    for cmd in STEPS:
        code = run(cmd)
        if code != 0:
            raise SystemExit(code)

    # keep docs copy in sync
    src = ROOT / 'web' / 'products.json'
    dst = ROOT / 'docs' / 'products.json'
    dst.write_text(src.read_text())
    print('\nSynced web/products.json -> docs/products.json')


if __name__ == '__main__':
    main()
