# Morning Warbler Hub Launch — 2026-04-13

## Summary
Launched a dedicated customer-safe Morning Warbler hub page and retargeted all live subscriber CTAs to it so the brand now has a more intentional newsletter destination than the generic journal guide.

## What shipped
- New live page: `docs/blog/morning-warbler/index.html`
- Retargeted all 13 live Morning Warbler CTAs from the journal guide to the new hub
- Kept attribution parameters and context handoff intact
- Updated support routing so newsletter questions point to the Morning Warbler hub

## Why this matters
The company now has a clearer branded relationship page for subscriber intent. This improves trust, creates a stronger pre-ESP destination, and gives the eventual Beehiiv cutover a cleaner public surface to swap from.

## Verification target
A live CTA should now resolve to `/blog/morning-warbler/?mw_source=...&mw_offer=...&mw_cluster=...` and render a source-aware context panel.
