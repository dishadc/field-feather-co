# Public Surface Leak Audit

Date: 2026-04-12
Scope: customer-facing `docs/` pages, with immediate remediation focused on the blog hub and launch note.

## Findings
1. `docs/blog/index.html`
   - leaked phrases: `Temporary editorial HQ`, `GitHub Pages journal`, `temporary live publishing home`, `Editorial ops`, `Why this temporary journal exists`, `Temporary publishing base`, `Primary live URL until WordPress cutover`, footer host disclosure
   - leak type: infrastructure / operating-workaround / editorial-process disclosure
   - remediation: rewrite as evergreen editorial positioning and customer-safe navigation copy

2. `docs/blog/welcome/index.html`
   - leaked phrases: `Temporary hosting infrastructure update`, references to WordPress stack, GitHub Pages, Cloudways, DNS, CMS credentials, migration plan, temporary base URL
   - leak type: infrastructure / blocker / provisioning disclosure
   - remediation: rewrite as an evergreen journal orientation page

3. Blog article footers
   - leaked phrase: `Temporary journal host live on GitHub Pages.`
   - leak type: infrastructure disclosure
   - remediation: replace with neutral brand footer copy

4. Affiliate placeholder copy across gear/backyard articles
   - leaked phrases: `Affiliate placeholder(s)`, `temporary placeholders`, `pending setup`, `routing is finalized`
   - leak type: monetization/workflow disclosure
   - remediation: rewrite as customer-safe recommendation language without setup/process notes

## Remediation target for this cycle
- constitutional hardening in `SOUL.md`, `SOUL.BLOGS.md`, and `AGENTS.md`
- sanitize blog hub and welcome page
- neutralize blog footers
- remove visible placeholder/process language from affected public articles
- add QA enforcement for forbidden public markers
