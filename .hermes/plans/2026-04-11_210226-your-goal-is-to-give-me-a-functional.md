# Functional Running Birdwatching Business — End-to-End Execution Plan

## Goal
Build and launch a fully operational, publicly purchasable birdwatching e-commerce business where any customer can discover products and complete purchases, with automated operations for product publishing, fulfillment, marketing, and KPI reporting.

## Success criteria (definition of done)
1. Public storefront(s) live and accessible (Etsy + owned website channel).
2. At least 20 purchasable listings live (digital-first), with working checkout.
3. Payment, tax, and delivery (digital + POD) configured correctly.
4. Daily KPI reporting + weekly listing generation automation running.
5. Customer support and post-purchase flows (email/download/support) working.
6. Minimum launch QA passed across desktop/mobile.

## Current context and assumptions
- Existing workspace already includes:
  - `SOUL.md`, `AGENTS.md`
  - product assets and listing drafts
  - `scripts/daily_kpi_report.py`, `scripts/generate_state_listing_drafts.py`
  - 50 state draft JSON listings and first warbler digital pack
  - active cron jobs for daily KPI and weekly batch generation
- Brand direction: digital-first, low COGS, birding niche (regional + warbler + migration themes).
- User wants autonomous execution and end-to-end operator ownership.
- External account access/credentials are required for final go-live actions.

## Strategic approach
Use a 3-channel launch stack:
1. **Primary demand channel:** Etsy (fastest organic demand capture)
2. **Owned conversion channel:** Shopify storefront (brand + direct checkout)
3. **High-margin digital channel:** Gumroad (bundles + email capture)

Prioritize zero-COGS digital products first to validate demand and cash flow, then layer POD SKUs via Printify.

## Execution phases

## Phase 0 — Access, legal, and commercial prerequisites (Day 0–2)
Objective: unblock all external dependencies before scaling work.

Steps:
1. Create/secure business identity and operations baseline:
   - Business name finalization
   - Brand email + domain procurement
   - Basic legal posture (sole prop/LLC as desired), tax nexus assumptions
2. Set up and verify required accounts:
   - Etsy seller
   - Shopify
   - Gumroad
   - Printify
   - Pinterest Business
   - Klaviyo or Mailchimp
3. Configure payments/tax/payout rails:
   - Etsy Payments onboarding
   - Shopify Payments/Stripe + tax settings
   - Gumroad payout settings
4. Document operating credentials map and recovery ownership.

Validation:
- All platforms show verified payout + identity status.
- Test $1 checkout path available in owned channel (or sandbox equivalent).

Risks:
- KYC delays and account holds.
- Tax configuration errors.

## Phase 1 — Productization and catalog build (Day 1–7)
Objective: build conversion-ready catalog with real downloadable deliverables.

Steps:
1. Standardize digital product packaging:
   - Convert SVG sources into polished PDFs where needed
   - ZIP deliverables with clear file naming, readme/license
2. Build launch catalog:
   - 1 warbler bundle
   - 10 priority state checklist singles (CA, TX, FL, NY, WA, CO, NC, AZ, OR, PA)
   - 3 migration-season trackers
   - 2 GoodNotes-compatible planner variants
3. Create listing metadata packs:
   - Title variants (50–70 chars)
   - 13 tags per listing
   - SEO descriptions and FAQ snippets
4. Produce listing media:
   - Cover images
   - 4–8 gallery images per listing
   - Short listing video templates

Likely files to change/create:
- `products/digital/**`
- `listings/etsy-drafts/**`
- `marketing/pinterest/**`
- `data/catalog_master.csv` (new)

Validation:
- Every launch SKU has: downloadable file, thumbnail set, listing copy, tags, and price.
- Manual spot QA on downloadable files and print-readability.

Risks/tradeoffs:
- Speed vs polish on media assets.
- Need strict IP-safe artwork sourcing.

## Phase 2 — Sales channel go-live (Day 5–10)
Objective: make products publicly purchasable.

Steps:
1. Etsy launch:
   - Publish first 15 listings
   - Configure shop policies, FAQs, about section, banner, profile
   - Add coupon and opening promo
2. Shopify launch:
   - Theme setup with brand system
   - Product pages for digital bundles and best-seller state packs
   - Digital delivery app integration
   - Checkout + legal pages + contact/support pages
3. Gumroad launch:
   - Publish bundle offers and cross-link from Etsy/Shopify
4. Cross-channel links and trust stack:
   - consistent branding, social proof placeholders, support email

Likely files to change/create:
- `ops/channel-launch-checklist.md` (new)
- `ops/brand-system.md` (new)
- `ops/legal-pages-copy.md` (new)

Validation:
- Real end-to-end purchase tests on each channel (buy, receipt, download delivery).
- Mobile QA for core purchase paths.

Risks:
- Platform policy mismatches for digital item disclosures.
- Broken download links if file routing is inconsistent.

## Phase 3 — Automation and operating cadence (Day 8–14)
Objective: reduce manual effort to weekly leadership decisions.

Steps:
1. Expand automation scripts:
   - listing publish queue generation
   - daily KPI aggregation from channel exports/APIs
   - exception alerts (conversion drop, ad overspend, delivery errors)
2. Cron operations:
   - daily KPI brief
   - weekly product batch generation
   - weekly SEO refresh tasks
3. Add lightweight ops dashboard artifact:
   - performance snapshot markdown/CSV
4. Add SOPs for recurring workflows:
   - weekly publishing
   - customer support response matrix
   - refund/escalation flow

Likely files to change/create:
- `scripts/*.py`
- `data/*.csv`
- `ops/sops/*.md`
- `marketing/pinterest/pin_matrix.csv`

Validation:
- Cron jobs run successfully twice with correct output.
- KPI report reconciles with source exports.

Risks:
- API/connectivity limitations on some platforms.
- Data drift if manual updates bypass scripts.

## Phase 4 — Growth engine and optimization (Week 3–6)
Objective: sustain demand and improve conversion economics.

Steps:
1. Pinterest content engine:
   - 3–5 fresh pins/day mapped to launch SKUs
2. Etsy SEO optimization loop:
   - A/B title hooks on top listings
   - seasonal keywords and long-tail refresh
3. Conversion improvements:
   - listing image reorder tests
   - bundle upsells and cross-sells
4. Expand catalog:
   - reach 50+ live listings
   - add first 5 POD products (stickers/mugs) once digital baseline converts

Validation targets:
- 30-day targets:
  - 20+ listings live
  - 1–2% listing conversion on Etsy
  - first 10 sales and first 3 reviews

Risks/tradeoffs:
- Premature ad spend can erode margin.
- Too many SKUs too early can reduce quality.

## Testing and validation plan
For each launch increment, execute:
1. Content QA: title/tags/description length and keyword coverage.
2. Asset QA: image dimensions, readability, download integrity.
3. Checkout QA: full purchase, receipt, access/download, support contact.
4. Analytics QA: sale appears in KPI tracker and daily brief.
5. Mobile QA: browse/listing/checkout on phone viewport.

Go-live gates (must pass):
- No broken downloads.
- No missing legal/policy pages.
- Payout configured and verified.
- Response SLA defined for support inquiries.

## Metrics and operating dashboard
Primary metrics:
- Listings live
- Visits by channel
- Orders
- Conversion rate
- Revenue
- Gross margin
- CAC (if ads used)
- Repeat purchase rate

Control thresholds:
- If conversion < 1% after 200 visits/listing cluster: revise thumbnails + first 40 title chars.
- If margin < 70% blended: cut tool spend and shift mix toward digital bundles.
- If visits low: increase listing velocity + Pinterest volume before ad spend.

## Required external inputs (open items)
1. Preferred brand/domain (or authorization to choose and buy).
2. Access credentials/invites for Etsy, Shopify, Gumroad, Printify, Pinterest.
3. Legal/tax preferences (entity status, filing assumptions, support address).
4. Budget ceiling for month 1 tools/ads.
5. Any prohibited product styles/claims/compliance constraints.

## Implementation sequence after this plan
1. Execute Phase 0 immediately to remove account/payment blockers.
2. Parallelize Phase 1 asset/listing production and Phase 2 storefront setup.
3. Run launch QA gates and publish initial 20 listings.
4. Activate automation and growth loops.
5. Report daily CEO brief and weekly reprioritization updates.

## Notes on tradeoffs
- Fastest path to first revenue is Etsy-first; strongest long-term asset is owned Shopify channel.
- Digital-first maximizes learning velocity and profitability at low risk.
- POD should be staged only after conversion proof to protect margins.
