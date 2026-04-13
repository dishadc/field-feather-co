# Branded Subscriber Rollout Spec

Date: 2026-04-13
Owner: CEO
Status: Implemented soft rollout; awaiting live subscriber infrastructure

## Goal
Define the customer-safe Morning Warbler CTA pattern now, so the brand can build subscriber intent before Beehiiv capture is live, then swap the CTA destination later without rethinking page strategy.

## Live pages in rollout v1
1. /blog/birdwatching-for-beginners/
2. /blog/essential-birding-gear-for-beginners/
3. /blog/backyard-birding-for-beginners/
4. /blog/spring-bird-migration/
5. /blog/how-to-use-ebird-migration/

## CTA pattern
Each live module uses:
- eyebrow: The Morning Warbler
- one page-specific promise
- one sentence explaining the eventual subscriber value
- single customer-safe CTA button pointing to `../welcome/index.html`

This keeps the brand polished while avoiding fake forms, brittle signup mechanics, or exposed fallback contact methods.

## Lead magnet mapping by page
- Birdwatching for Beginners -> Beginner Birding Starter Checklist
- Essential Birding Gear for Beginners -> Beginner Field Kit Shortlist
- Backyard Birding for Beginners -> Backyard Habitat Starter Planner
- Spring Bird Migration -> Spring Migration Tracker
- How to Use eBird to Track Migration in Real Time -> Migration Worksheet + seasonal notes

## Swap plan when Beehiiv is ready
Replace the current journal-guide CTA target with one of these patterns:

### Pattern A — Direct newsletter signup
Use when the value proposition is broad and recurring.
Best fit:
- Birdwatching for Beginners
- Spring Bird Migration
- How to Use eBird to Track Migration in Real Time

### Pattern B — Lead magnet first, newsletter second
Use when the page has strong practical-intent alignment with a downloadable asset.
Best fit:
- Essential Birding Gear for Beginners
- Backyard Birding for Beginners
- state guide pages later

## Copy rules for future rollout
- Keep CTA copy specific to page intent
- Do not use one generic newsletter CTA everywhere
- Do not interrupt before the page has delivered value
- Preserve premium editorial tone; avoid popup-style growth tactics unless proven necessary

## Recommended next expansion
When the next rollout wave ships, add customer-safe Morning Warbler modules to:
- /blog/birds-in-florida/
- /blog/birds-in-california/
- /blog/birds-in-texas/
- /blog/hawk-migration/

## Success criteria
Short-term:
- high-intent pages normalize the brand-to-subscriber transition
- no QA regressions
- no public-surface trust degradation

Later, once live capture exists:
- newsletter signup rate by page
- lead magnet conversion rate by page
- article-to-signup assisted conversion rate
- subscriber-to-product clickthrough by entry cluster
