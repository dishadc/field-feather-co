# AGENTS.md — Business Context

Business: Field & Feather Co.
Primary channel: Etsy (phase 1), Gumroad (phase 2)
Niche focus:
1) State-specific birding checklists (underserved long-tail SEO)
2) Warbler-themed enthusiasts products
3) Migration-season journals/logs
4) GoodNotes-compatible planners

Pricing guardrails:
- Single printable SKU: $4.99–$6.99
- Small bundles: $9.99–$14.99
- Mega bundles (Gumroad): $19.99–$49.99

Profit policy:
- Target blended gross margin >70% in first 90 days.
- Keep software/tool spend <= $145/month until trailing 30-day revenue > $500.

Weekly cadence:
- Monday: keyword and competitor scan
- Tuesday: design/asset generation
- Wednesday: listing draft + SEO
- Thursday: publish + Pinterest pins
- Friday: KPI review + backlog reprioritization

Leadership cadence:
- CEO reviews C-suite/agent-team/workstream status every few hours during active execution windows.
- Each review checks progress, blockers, quality, and reallocation opportunities.
- These are operational check-ins, not permission pauses.

Public Surface & Information Hygiene:
- Never expose internal blockers, owner action queues, temporary workarounds, hosting contingencies, automation details, agent structure, or QA internals on any public-facing website page, listing, or reader-facing artifact.
- Public copy must be reader-safe, brand-safe, and useful on its own. Internal execution details belong in `ops/`, `reports/`, `data/`, and other internal artifacts only.
- When in doubt, rewrite for customer value rather than operational transparency.

CEO Operating System Responsibility:
- The CEO must continuously improve the repo, team design, delegation model, processes, agents, SOPs, QA/reporting loops, and constitutional documents.
- Building the right agentic team and operating system is a core company responsibility, not a one-time setup task.
- If a leak, process failure, or repeated management issue appears, update the system so the failure becomes harder to repeat.

Initial SKU roadmap (first 30 days):
- 20 state checklist listings
- 5 warbler products
- 5 migration-season products
- 3 birding planner variants

File map:
- products/: source assets and pack definitions
- listings/etsy-drafts/: Etsy-ready listing JSON/MD
- marketing/pinterest/: pin title/description/URL matrix
- data/: KPI and sales tracker
- scripts/: automation tasks

# Blogs Division

## Business Overview
- Brand: Field & Feather Co.
- Niche: Birdwatching / birding lifestyle
- Website: fieldandfeather.co (WordPress)
- Newsletter: The Morning Warbler (Beehiiv)
- Target audience: Birders aged 35–65, educated, affluent
- Current phase: Blog buildout

## WordPress Access
- Primary target URL: https://fieldandfeather.co
- REST API endpoint: https://fieldandfeather.co/wp-json/wp/v2/
- Auth method: Application Password (stored in MEMORY.md)
- SEO plugin: RankMath Pro
- Meta fields: rank_math_focus_keyword, rank_math_description,
  rank_math_title, rank_math_og_title

## Temporary Publishing Fallback
- Temporary live journal URL: https://dishadc.github.io/field-feather-co/blog/
- Until WordPress hosting is live, publish editorial content as static HTML
  under `docs/blog/` and treat GitHub Pages as the live article host.
- When WordPress is ready, migrate article canonicals and publishing workflow.

## Beehiiv Access
- Publication ID: [stored in MEMORY.md]
- API key: [stored in MEMORY.md]
- Base URL: https://api.beehiiv.com/v2/
- Newsletter name: The Morning Warbler
- Send day: Sunday, 8:00am Eastern
- Subscriber count target: 5,000 by month 18

## Brand Voice
Knowledgeable but warm. Precise but accessible. Write like the smartest 
birder at your local Audubon chapter — not a professor, not a casual.
Use field guide terminology correctly. Never talk down to readers.

## Design Standards
- Brand colours: Forest green #2D4A2D, Cream #F5F0E8, 
  Terracotta #C4714A, Robin's egg #7EC8C8
- Always use Oxford commas
- Spell "birdwatching" as one word, "life list" as two words,
  "field guide" as two words

## Content Rules
- Minimum article length: 2,000 words
- Every article must have: H2 structure, internal links (3+),
  affiliate links where relevant, a clear meta description under 160 chars
- Always cite Cornell Lab / eBird / USGS for species data
- Never make unverified claims about species range or behaviour
- Image attribution: always include Macaulay Library photographer credit

## Affiliate Programs Active
- Amazon Associates (3–4.5%): books, binoculars, feeders
- OpticsPlanet (5%): binoculars, spotting scopes
- Bookshop.org (10%): field guides
- REI (5%): outdoor/birding gear

## Current Content Status
- Total articles published: [auto-updated by Hermes]
- Top performing article: [auto-updated by Hermes]
- Current monthly traffic: [auto-updated by Hermes]
