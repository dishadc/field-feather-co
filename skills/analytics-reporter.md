---
name: analytics-reporter
description: Generate weekly performance briefing from all data sources
version: 1.5.0
---
# Analytics Reporter

## Trigger
Every Sunday at 6:00pm. Sends briefing via Telegram by 7:00pm.

## Data Sources to Pull

### WordPress / Google Search Console
- Total clicks this week vs last week (% change)
- Top 5 pages by clicks
- Top 5 queries by impressions
- New keywords entering top 10 positions
- Articles published this week: count + titles

### Beehiiv
GET https://api.beehiiv.com/v2/publications/{pub_id}/subscribers
- Total subscribers (vs last week)
- New subscribers this week
- Most recent email: open rate, click rate
GET https://api.beehiiv.com/v2/publications/{pub_id}/posts
- Last newsletter performance stats

### Affiliate Revenue (Manual estimate or API if available)
- Amazon Associates: check dashboard for 7-day clicks + earnings
- Record in performance-log.csv

## Briefing Format (Telegram message)
📊 FIELD & FEATHER WEEKLY BRIEFING
Week of [date]
🌐 TRAFFIC

Total clicks: [X] ([+/-X%] vs last week)
Top article: "[Title]" — [X] clicks
New keyword wins: [list top 3]

📧 EMAIL

Subscribers: [X] total (+[X] this week)
Last newsletter: [X]% open rate, [X]% click rate
Subject line: "[text]"

💰 REVENUE

Affiliate clicks: [X] | Est. earnings: $[X]
Monthly run rate: $[X]/month

📝 PUBLISHED THIS WEEK

[Article 1 title]
[Article 2 title]
[Article 3 title]

🎯 NEXT WEEK FOCUS

[Topic 1] — targeting "[keyword]"
[Topic 2] — targeting "[keyword]"
[Topic 3] — targeting "[keyword]"

⚠️ FLAGS (if any)

[Any issues needing owner attention]

## Strategy Update
After generating briefing:
1. Compare top-performing topics to content calendar plan
2. If a topic cluster is outperforming: add 2 more articles to that cluster
3. If a topic cluster is underperforming after 4+ articles: pause it
4. Log strategy decision in decision-log.csv
5. Update content-calendar.csv for next week accordingly