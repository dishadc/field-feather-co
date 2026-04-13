# Morning Warbler Recommendation Personalization — 2026-04-13

## Summary
Extended the Morning Warbler hub so it now renders cluster-aware recommended next reads based on the existing attribution parameters passed from live subscriber CTA modules.

## What shipped
- Added a recommendation section to `docs/blog/morning-warbler/index.html`
- Added cluster-aware recommendation rendering to `docs/app.v8.js` and `web/app.v8.js`
- Recommendation sets now adapt to:
  - beginner
  - beginner-gear
  - backyard
  - migration
  - migration-tools
  - regional
  - migration-event
  - gear-trust
  - editorial fallback

## Why this matters
The Morning Warbler hub is no longer just a holding destination. It now acts like a smarter relationship page that keeps readers inside the most relevant learning path before live subscriber capture is turned on.

## Verification target
A source-aware Morning Warbler visit should display a recommendation module whose article links match the reader's originating cluster.
