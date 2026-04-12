# Final Go-Live Blockers (Credential-Dependent)

Current hard blocker: checkout URLs are not populated for launch SKUs.

## What must be completed externally
1. Etsy shop/listings must be published.
2. For each launch SKU, copy final listing URL into `data/product_links.csv`.
3. Rebuild storefront catalog:
   - `python3 scripts/refresh_storefront_products.py`
4. Re-run readiness validation:
   - `python3 scripts/validate_launch_readiness.py`

## Required account access
- Etsy seller owner/admin
- Shopify owner/admin (if using owned checkout)
- Gumroad owner/admin (if using bundle channel)
- Domain/DNS access for public website deploy

## Immediate operator runbook once access is available
1. Publish 20 queued Etsy listings from `listings/etsy-publish-queue.csv`.
2. Paste each resulting URL into `data/product_links.csv`.
3. Run `python3 scripts/refresh_storefront_products.py`.
4. Validate with `python3 scripts/validate_launch_readiness.py` until status shows GO-LIVE READY.
5. Deploy `web/` to static host (Cloudflare Pages/Netlify/Vercel) and connect domain.

## Launch cutover checklist
- [ ] 20/20 SKUs have live checkout links.
- [ ] Website buy buttons active.
- [ ] Test purchase succeeds.
- [ ] Download delivery confirmed.
- [ ] Support inbox monitored.
