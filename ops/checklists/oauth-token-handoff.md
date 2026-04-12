# OAuth/Token Handoff Checklist (Fast Path)

Goal: enable agent-driven publishing without sharing/reusing raw passwords.

## A) Etsy API access
1. Create Etsy developer app (or use existing app).
2. Capture:
   - ETSY_API_KEY / CLIENT_ID
   - ETSY_CLIENT_SECRET
3. Complete OAuth consent on your logged-in Etsy seller account.
4. Provide:
   - ETSY_ACCESS_TOKEN
   - ETSY_REFRESH_TOKEN
   - ETSY_SHOP_ID

## B) Gumroad API access
1. In Gumroad account settings, generate an API access token.
2. Provide:
   - GUMROAD_ACCESS_TOKEN
   - GUMROAD_SELLER_ID (if available)

## C) Delivery format to send me
Send as plain key=value lines in chat (I will use immediately):
ETSY_API_KEY=...
ETSY_CLIENT_ID=...
ETSY_CLIENT_SECRET=...
ETSY_ACCESS_TOKEN=...
ETSY_REFRESH_TOKEN=...
ETSY_SHOP_ID=...
GUMROAD_ACCESS_TOKEN=...
GUMROAD_SELLER_ID=...

## D) Security
- After launch, rotate tokens and keep only scoped least-privilege tokens.
- Prefer tokens over sharing account passwords.
