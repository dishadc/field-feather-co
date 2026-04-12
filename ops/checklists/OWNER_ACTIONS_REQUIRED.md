# OWNER_ACTIONS_REQUIRED

Purpose: single inbox for anything required from you.
I will keep this file updated continuously and append new items here.

Last updated: 2026-04-12 PDT

## OPEN (blocking revenue now)

1) Connect Gumroad payout method (hard blocker)
- Why needed: Gumroad API rejects product publishing until payout is connected.
- Evidence: `PUT /v2/products/:id/enable` -> `You must connect at least one payment method before you can publish this product for sale.`
- Your action:
  - Log in to Gumroad
  - Settings -> Payments/Payouts
  - Connect bank/PayPal and complete any verification
- What I will do immediately after: auto-run publish+sync loops and drive to 20/20 published launch SKUs.

## OPEN (channel expansion blocker)

2) Etsy app approval completion
- Why needed: Etsy OAuth remains blocked while app is pending approval.
- Your action:
  - Approve/complete Etsy app review state to active
- What I will do immediately after:
  - run OAuth helper exchange
  - persist tokens in `.env`
  - activate Etsy publishing automation in parallel with Gumroad.

## OPEN (security hygiene, post-launch)

3) Rotate previously shared credentials/tokens
- Why needed: secrets were exposed in chat context and should be treated as compromised.
- Your action: rotate account password and API tokens after payout setup and stabilization.
- What I will do: update `.env` references and verify all automations with new credentials.

## NOTES
- You can complete items in any order, but Item #1 is the immediate revenue unblocker.
- No reply needed per item; I will keep executing and poll/unblock automatically.
