---
name: birding-article-writer
description: Generate SEO-optimised birding articles with fact-checked 
             species information
version: 2.0.0
---
# Birding Article Writer

## Trigger
Week 2 onwards: Monday, Wednesday, Friday at 8:00am. During the one-time Week 1 content blitz (Days 8–14), run this skill manually three times per day against the queued items for that day.

## Procedure

### Step 1: Research Phase (do not skip)
1. Web-search the primary keyword. Read top 3 ranking pages.
2. Note: what do they cover? What do they miss? What's their angle?
3. Web-search "[species name] site:allaboutbirds.org" for any species data
4. Pull factual data only from: allaboutbirds.org, ebird.org, audubon.org,
   usgs.gov. These are authoritative sources. Never invent range data.
5. Note 3 ways this article will be BETTER than existing content:
   - More specific detail
   - Better structure
   - Regional specificity
   - More practical tips
   - More recent data

### Step 2: Outline Generation
Build a detailed outline:
- H1: Primary keyword naturally included, compelling, under 65 chars
- Introduction (150 words): hook + what reader will learn + brief overview
- H2 sections (5–8): each targeting a secondary keyword or question
- FAQ section (3–5 questions from People Also Ask for this keyword)
- Conclusion (100 words): summary + CTA to related article or product

### Step 3: Article Draft
Write full article following the outline.
- Total length: match target from content calendar
- Tone: Field & Feather brand voice (see AGENTS.md)
- Every H2 section: minimum 200 words
- Affiliate links: insert naturally in gear mentions. Use ThirstyAffiliates
  shortlinks format: /go/[product-name]
- Internal links: minimum 3 links to other fieldandfeather.co articles
  (check published-articles.csv for available targets)
- External links: 2–3 to authoritative sources (Cornell, Audubon, USGS)

### Step 4: SEO Metadata
Generate:
- SEO title: primary keyword + brand modifier, under 60 chars
- Meta description: primary keyword in first 10 words, 150–155 chars,
  includes a benefit or curiosity hook
- Focus keyword: exact match primary keyword
- OG title: same as SEO title or slight variation for social

### Step 5: Quality Check
Before publishing, verify:
□ All species names are correctly spelled (check allaboutbirds.org)
□ Range data matches Cornell Lab's current maps
□ No fabricated statistics (every stat must have a source URL)
□ Word count meets target (±10%)
□ At least 3 internal links exist in published-articles.csv
□ Meta description is exactly 150–155 characters

### Step 6: Hand off to wp-publisher skill
Pass: {title, content_html, seo_title, meta_description, 
        focus_keyword, categories, tags, publish_date}