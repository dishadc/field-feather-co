# Public Surface Information Hygiene

Purpose: keep Field & Feather public surfaces free of internal operations leakage.

## Rule
Customer-facing surfaces must not reveal internal operations, blockers, workarounds, provisioning state, owner action requests, agent/team structure, automation details, QA internals, or temporary execution mechanics.

## Public surfaces covered
- `docs/` website pages
- blog pages
- marketplace listings
- email/newsletter copy
- social copy
- any customer-facing landing page

## Never publish
- blocker explanations
- credential or account-state gaps
- references to temporary hosting fallbacks or infrastructure substitutions
- cron, workflow, or agent-process details
- owner action requests or operational inbox content
- "placeholder" or "pending setup" language visible to customers

## Preferred replacement strategy
- Replace infra/process explanations with reader value
- Replace temporary/project language with stable brand language
- Replace ops notes with editorial framing, trust language, or simple navigation help

## Pre-publish check
Before shipping public copy, confirm:
1. No internal blocker/workaround language
2. No owner-action or process language
3. No agent/team/tooling references
4. Copy reads as finished customer-facing brand copy

## Enforcement
- QA scripts should fail when forbidden public markers appear in `docs/` pages
- CEO execution review should treat information-hygiene failures as process failures
- Repeat failures require SOP or constitutional updates, not just copy fixes
