# SOP: Active Execution CEO Review

Purpose: enforce intraday CEO oversight of the C-suite, agent team, and active workstreams without turning execution into permission-seeking.

## Cadence
- Run an operational review every 2–4 hours during active execution windows.
- Run an immediate review after any major deploy, major delegation batch, or validation failure.
- Do not pause delivery waiting for review approval; reviews are steering actions.

## Inputs to review
0. CEO operating board
   - `ops/CEO_EXECUTION_BOARD.md`
   - current top priorities
   - active workstreams
   - external blockers
   - operating-system improvement backlog
1. Workstream status
   - active TODOs
   - delegated agent batches
   - in-flight content or engineering work
2. Validation status
   - `ops/checklists/pages_consistency_report.json`
   - `ops/checklists/storefront_smoke_report.json`
   - `ops/checklists/browser_qa_report.json`
   - `ops/checklists/content_integrity_report.json`
   - latest visual/browser audit notes if available
3. Delivery state
   - latest deploy run
   - git status / recent commits
   - live-site spot checks
4. Business blockers
   - owner actions required
   - credential failures
   - hosting / checkout / reporting issues

## Review checklist
- What is each active workstream producing right now?
- Which agent streams are blocked, stale, or underperforming?
- Which validation checks are red, yellow, or missing?
- Did the latest deploy improve the product or regress it?
- What should be delegated, stopped, or reprioritized immediately?
- What needs an owner escalation versus an autonomous fix?

## Required outputs
Each review must leave a trace in at least one of:
- updated `ops/CEO_EXECUTION_BOARD.md`
- updated TODO state
- `data/decision-log.csv`
- `ops/checklists/ceo_execution_review.md`
- delegated-task review summaries
- scheduled review/report automation

## Decision rules
- If any validation report is FAIL: route work to bug fixing before cosmetic expansion.
- If browser QA and smoke QA disagree: trust the failing interactive/browser result until explained.
- If deploy is green but visual quality regresses: treat as product issue, not merely styling preference.
- If a delegated stream stalls or returns weak output: replace or redirect it immediately.
- If live-site confidence is based only on spot checks, label readiness as partial, not complete.

## Minimum confidence standard for 'working correctly'
Do not claim the website is working correctly unless all are true for the current release:
- Pages consistency: PASS
- Storefront smoke report: PASS
- Browser QA report: PASS
- Content integrity report: PASS
- Recent manual/browser visual audit finds no obvious premium-UX regressions

## Notes
- This review cadence is operational leadership, not a human approval loop.
- The CEO is expected to self-propel, reallocate work, and keep all teams moving.