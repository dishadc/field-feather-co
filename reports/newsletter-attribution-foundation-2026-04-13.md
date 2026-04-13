# Newsletter Attribution Foundation — 2026-04-13

## Summary
Built a source-tagged attribution layer for Morning Warbler soft CTAs so the editorial rollout now passes entry context into the journal guide and is ready for a later live-signup swap with better measurement hygiene.

## What shipped
- Added `data-newsletter-source`, `data-newsletter-offer`, and `data-newsletter-cluster` attributes to every live Morning Warbler CTA module in `docs/blog/`.
- Updated `docs/app.v8.js` and `web/app.v8.js` to append source parameters to CTA links and store local click history in `localStorage` under `ff-newsletter-clicks`.
- Added a context handoff panel to `docs/blog/welcome/index.html` that reflects the reader's originating article cluster.
- Extended `scripts/qa_content_integrity.py` so any page with a Morning Warbler module fails if attribution attributes are missing.

## Current parameter contract
- `mw_source` = source article slug
- `mw_offer` = mapped offer / lead magnet name
- `mw_cluster` = subscriber entry cluster

## Why this matters
This creates a measurement-ready handoff without exposing brittle signup mechanics. When the live subscriber path is ready, the site can swap the CTA destination while preserving page-level source context and attribution discipline.
