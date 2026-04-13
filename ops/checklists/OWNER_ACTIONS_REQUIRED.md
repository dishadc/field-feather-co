# OWNER_ACTIONS_REQUIRED

Purpose: single inbox for anything required from you.
I keep this file updated continuously.

Last updated: 2026-04-12 21:52 

## OPEN (blocking revenue now)

1) Connect Gumroad payout method (hard blocker)
- Why needed: Gumroad API rejects product publishing until payout is connected.
- Evidence: `PUT /v2/products/:id/enable` -> `You must connect at least one payment method before you can publish this product for sale.`
- Current impact snapshot:
  - Ready SKUs: 28
  - Ready with checkout URLs: 8
  - Ready published on Gumroad: 0
  - Ready missing links: 20
- Your action:
  - Log in to Gumroad
  - Settings -> Payments/Payouts
  - Connect bank/PayPal and complete verification
- What I will do immediately after:
  - auto-run publish/sync loops to drive 20/20 published launch SKUs.

## OPEN (channel expansion blocker)

2) Etsy app approval completion
- Why needed: Etsy OAuth remains blocked while app is pending approval.
- Your action:
  - Complete Etsy app approval to active status.
- What I will do immediately after:
  - OAuth token exchange
  - persist tokens in `.env`
  - activate Etsy publish automation.

## OPEN (security hygiene, post-launch)

3) Rotate previously shared credentials/tokens
- Why needed: credentials shared in chat should be treated as compromised.
- Your action: rotate account password and API tokens after payout setup stabilization.
- What I will do: update `.env` references and verify automation with new secrets.

## Diagnostic detail (agent-managed)
- Pages consistency status: PASS
- Pages reasons: none
- Pages live matches raw main: True
- Pages has catalog preview copy: True
- Unpublished ready SKUs with links:
  - DIGI-STATE-CALIFORNIA, DIGI-STATE-COLORADO, DIGI-STATE-FLORIDA, DIGI-STATE-NEW-YORK, DIGI-STATE-NORTH-CAROLINA, DIGI-STATE-TEXAS, DIGI-STATE-WASHINGTON, DIGI-WARBLER-BUNDLE-001
- Ready SKUs missing checkout links:
  - DIGI-MIGRATION-FIRST-SEEN-010, DIGI-MIGRATION-WEEKLY-001, DIGI-MIGRATION-WEEKLY-002, DIGI-MIGRATION-WEEKLY-003, DIGI-MIGRATION-WEEKLY-004, DIGI-MIGRATION-WEEKLY-005, DIGI-MIGRATION-WEEKLY-006, DIGI-MIGRATION-WEEKLY-007, DIGI-MIGRATION-WEEKLY-008, DIGI-MIGRATION-WEEKLY-009, DIGI-PLANNER-GOODNOTES-DAILY-015, DIGI-PLANNER-GOODNOTES-SEASONAL-017, DIGI-PLANNER-GOODNOTES-WEEKLY-016, DIGI-STATE-ARIZONA, DIGI-STATE-OREGON, DIGI-STATE-PENNSYLVANIA, DIGI-WARBLER-HABITAT-013, DIGI-WARBLER-LIFER-CHECKLIST-014, DIGI-WARBLER-PEAK-WEEK-011, DIGI-WARBLER-SONG-CODES-012
