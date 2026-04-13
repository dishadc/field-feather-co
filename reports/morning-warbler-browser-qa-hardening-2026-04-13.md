# Morning Warbler Browser QA Hardening — 2026-04-13

## Summary
Extended browser-level QA so the Morning Warbler growth surface is now validated end to end for both beginner and gear-trust attribution paths.

## What shipped
- Added `morning_warbler_beginner_flow` to `scripts/qa_browser_flows.js`
- Added `morning_warbler_gear_trust_flow` to `scripts/qa_browser_flows.js`

## Coverage added
- Source-aware context handoff is present on the Morning Warbler hub
- Offer label is preserved from the originating article CTA
- Recommendation module renders exactly three next-read cards
- Recommendation titles match the expected cluster-specific set

## Why this matters
The Morning Warbler system is now protected at the browser-journey layer, not just by static file QA. Future regressions in attribution, context rendering, or recommendation personalization will be caught earlier.

## Hidden JS issue resolved
- Fixed `app.v8.js` product-catalog loading so nested blog pages no longer request a non-existent relative `products.json` path.
- This removes a silent 404 that browser QA surfaced while exercising the Morning Warbler hub.
