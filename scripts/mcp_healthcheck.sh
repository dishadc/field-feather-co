#!/usr/bin/env bash
set -euo pipefail

echo "=== mcporter local config healthcheck ==="
npx -y mcporter list --config config/mcporter.json --output json

echo ""
echo "=== commerce MCP template status ==="
python3 - <<'PY'
import json, subprocess
cmd = ['npx','-y','mcporter','list','--config','config/mcporter.commerce-template.json','--output','json']
res = subprocess.run(cmd, capture_output=True, text=True)
print(res.stdout.strip())
if res.returncode != 0:
    print('Commerce MCP servers not yet configured/reachable')
    raise SystemExit(0)
try:
    data = json.loads(res.stdout)
    ok = data.get('counts',{}).get('ok',0)
    if ok > 0:
        print(f'Commerce MCP reachable servers: {ok}')
    else:
        print('Commerce MCP servers not yet configured/reachable')
except Exception:
    print('Commerce MCP status parse failed; treat as not configured')
PY
