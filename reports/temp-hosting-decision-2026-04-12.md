# Temporary Hosting Decision — 2026-04-12

Decision: Use GitHub Pages as the temporary live editorial host for Field & Feather Co.

Live base URLs
- Storefront root: https://dishadc.github.io/field-feather-co/
- Temporary journal hub: https://dishadc.github.io/field-feather-co/blog/

Why this was chosen
- Already configured and live from `main:/docs`
- Zero incremental hosting cost
- No new account setup required
- Unblocks public article publishing immediately while permanent WordPress hosting is pending
- Integrates cleanly with the existing repo and Pages verification script

Implementation completed
- Added a live journal hub at `docs/blog/index.html`
- Added a launch note at `docs/blog/welcome/index.html`
- Linked the journal from the homepage nav
- Updated AGENTS.md with temporary publishing fallback
- Updated wordpress-publisher skill with GitHub Pages fallback instructions
- Updated article-writing cron jobs to publish statically if WordPress remains unavailable

Operational rule
- Until WordPress is live, all blog articles should publish as static HTML under `docs/blog/[slug]/index.html` and be tracked in `data/published-articles.csv` with status `LIVE_STATIC_TEMP`.

Exit criterion
- Replace temporary hosting only after a live CMS exists at fieldandfeather.co and can accept scheduled article publication with SEO metadata.
