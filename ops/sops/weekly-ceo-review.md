# SOP: Weekly CEO Review

## Intraday execution review cadence
- During active build/publish windows, the CEO runs an operational review every 2–4 hours.
- Use `ops/sops/active-execution-review.md` as the intraday checklist.
- Use `ops/CEO_EXECUTION_BOARD.md` as the single operating board for current priorities, workstreams, blockers, and system-improvement work.
- Each review must inspect workstreams, delegated agents, blockers, deploy status, and validation reports.
- Each review must leave a trace in TODO state, the CEO execution board, review artifacts, delegated-task summaries, or `data/decision-log.csv`.

## Friday review agenda (45 minutes)
1. KPI snapshot:
   - Revenue, orders, conversion, margin
2. Listing funnel:
   - views -> favorites -> orders for top 20 SKUs
3. Channel performance:
   - Etsy vs Shopify vs Gumroad
4. Operations health:
   - support SLA adherence, refund rate
5. Decisions:
   - promote winning SKU families
   - pause low-intent experiments
6. Validation health:
   - pages consistency
   - storefront smoke
   - browser QA
   - content integrity

## Decision rules
- If SKU conversion < 1% after 200 visits: rework thumbnail + title.
- If digital bundle conversion > 3%: build 3 adjacent variants.
- If blended margin < 70%: reduce paid tools/ads and increase digital mix.
- If any validation report is FAIL: redirect work to fixes before expansion.

## Outputs
- Updated top-10 publish queue
- Next week pin/content schedule
- Tool spend adjustments
- Latest CEO execution review artifact


## Roadmap discipline
- Treat `ROADMAP.md` as the canonical sequencing document for company direction.
- If active work drifts from the roadmap, either update the roadmap immediately or redirect the work.
