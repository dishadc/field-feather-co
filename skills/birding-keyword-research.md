---
name: birding-keyword-research
description: Pull and rank birdwatching keyword opportunities weekly
version: 2.0.0
---
# Birding Keyword Research

## Trigger
Every Monday at 7:00am. Also callable manually.

## Procedure

### Step 1: Pull Existing Performance Data
1. Query Google Search Console API for top 50 queries from last 7 days
2. Filter for birding-related terms not yet covered on the site
3. Note impressions, clicks, and average position for each

### Step 2: Competitor Gap Analysis
1. Web-search: "site:allaboutbirds.org [topic]" to check Cornell coverage
2. Web-search: "site:birdwatchinghq.com [topic]" to check HQ coverage  
3. Topics Cornell and HQ both rank for = competitive. Skip.
4. Topics neither covers well = opportunity. Prioritise.

### Step 3: Keyword Scoring
Score each candidate keyword 1–10 across:
- Search volume (estimate from DataForSEO API if available, else estimate)
- Competition level (inverse — low competition = high score)
- Commercial intent (gear/product queries score highest for affiliate $)
- Seasonal relevance (is this the right season to publish this?)
- Content gap (does fieldandfeather.co have anything similar?)

### Step 4: Select Weekly Topics
Pick top 3 scoring keywords. For each, define:
- Primary keyword (exact match focus)
- 3–5 secondary/LSI keywords to weave in naturally
- Target word count (1,800–3,500 based on SERP analysis)
- Article type: Guide / Comparison / List / How-To / Regional
- Affiliate opportunity: yes/no, which program

### Step 5: Write to Content Calendar
Append 3 rows to ./data/content-calendar.csv:
[date, keyword, title_draft, word_count_target, affiliate_y_n,
 assigned_publish_date, status=QUEUED]

### Output
Log: "Keyword research complete. This week's topics: [list]"
Notify: Skip Telegram (included in Sunday briefing)