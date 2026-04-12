# Go-Live Blockers

Last updated: 2026-04-12 (PDT)

## 1) Gumroad payouts not connected (hard blocker)
- Evidence:
  - API call `PUT /v2/products/:id/enable` returns:
  - `You must connect at least one payment method before you can publish this product for sale.`
  - Current API product state shows created products remain unpublished.
- Impact:
  - Checkout links exist but ready SKUs cannot be published for sale.
  - Launch readiness cannot pass while this is unresolved.
- Owner:
  - Stakeholder account action required in Gumroad settings (bank or PayPal payout setup).
- Unblock action:
  1. Log in to Gumroad account.
  2. Go to Settings -> Payments/Payouts.
  3. Connect at least one payout method and complete identity verification if prompted.
  4. Re-run: `python3 scripts/publish_gumroad_products.py --max-create 10`
  5. Re-run readiness: `python3 scripts/validate_launch_readiness.py`

## 2) Gumroad product create throttling (secondary blocker)
- Evidence:
  - Product create endpoint returns `429 Retry later` during rollout windows.
- Impact:
  - Remaining ready SKUs cannot all be created in a single run.
- Owner:
  - Agent automation (already in place) + platform limit windows.
- Mitigation in place:
  - Capped publisher runs and recurring rollout cron jobs.
  - Missing SKU queue tracked in `ops/checklists/current_missing_ready_skus.csv`.
