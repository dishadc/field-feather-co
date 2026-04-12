# Etsy Approval Unblock Runbook

Current blocker:
- Etsy app is still pending personal approval, so OAuth token exchange cannot complete.

## Immediate actions once Etsy approval email/notification appears
1) Confirm app status is active in Etsy developer dashboard.
2) Run:
   - `python3 scripts/etsy_oauth_helper.py start`
3) Open returned authorization URL in browser logged into business Etsy account.
4) Approve app access.
5) Copy redirected callback URL.
6) Run:
   - `python3 scripts/etsy_oauth_helper.py exchange "<FULL_CALLBACK_URL>"`
7) Save returned access/refresh tokens into `.env`:
   - `ETSY_ACCESS_TOKEN`
   - `ETSY_REFRESH_TOKEN`
   - `ETSY_EXPIRES_AT` (if provided)

## Post-token validation
1) Call a lightweight Etsy endpoint with bearer token and confirm 200.
2) Mark `ops/go-live-blockers.md` Etsy auth blocker as resolved.
3) Enable Etsy publish channel for ready SKUs in parallel with Gumroad.

## Safety
- Never commit `.env`.
- Rotate Etsy tokens if exposed in logs or chat.
