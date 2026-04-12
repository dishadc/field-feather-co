---
name: wordpress-publisher
description: Publish articles to WordPress via REST API with full SEO metadata
version: 2.0.0
---
# WordPress Publisher

## Authentication
Method: HTTP Basic Auth with Application Password
Header: Authorization: Basic base64(username:app_password)
Store credentials in MEMORY.md, never in skill files.

## Procedure

### Step 1: Upload Featured Image
1. Source bird image (see image-sourcer skill)
2. Upload to WP Media Library:
   POST https://fieldandfeather.co/wp-json/wp/v2/media
   Headers: Authorization, Content-Type: image/jpeg
   Body: raw image binary
3. Store returned media_id

### Step 2: Resolve Taxonomy IDs
GET https://fieldandfeather.co/wp-json/wp/v2/categories
GET https://fieldandfeather.co/wp-json/wp/v2/tags
Map article categories/tags to their WordPress integer IDs

### Step 3: Create Post
POST https://fieldandfeather.co/wp-json/wp/v2/posts
Body (JSON):
{
  "title": "[article title]",
  "slug": "[url-friendly-slug]",
  "content": "[full HTML article content]",
  "status": "future",
  "date": "[YYYY-MM-DDTHH:MM:SS]",
  "featured_media": [media_id],
  "categories": [[category_ids]],
  "tags": [[tag_ids]],
  "meta": {
    "rank_math_title": "[seo title]",
    "rank_math_description": "[meta description]",
    "rank_math_focus_keyword": "[primary keyword]",
    "rank_math_og_title": "[og title]"
  }
}

### Step 4: Verify Publication
GET https://fieldandfeather.co/wp-json/wp/v2/posts/[post_id]
Confirm: status=future, scheduled date correct, featured_image set

### Step 5: Update Records
Append to ./data/published-articles.csv:
[post_id, title, url, publish_date, primary_keyword, word_count,
 categories, has_affiliate=y/n, status=SCHEDULED]

Update ./data/content-calendar.csv: status=PUBLISHED for this item

### Error Handling
- 401 Unauthorized: credentials expired. Alert owner via Telegram.
- 422 Unprocessable: log error, save article as local .md file,
  retry next day
- Image upload fails: proceed without featured image, flag in
  decision-log.csv for owner review
- If WordPress hosting, credentials, or DNS are unavailable, use the temporary
  static publishing fallback on GitHub Pages instead of stopping:
  1. Temporary live base URL: https://dishadc.github.io/field-feather-co/
  2. Create article HTML at `./docs/blog/[slug]/index.html`
  3. Include full SEO metadata in the HTML head
  4. Ensure the page links back to `./docs/blog/index.html`
  5. Append to `./data/published-articles.csv` with the GitHub Pages article URL
     and status `LIVE_STATIC_TEMP`
  6. Update `./data/content-calendar.csv` to `PUBLISHED`
  7. Log the WordPress blocker and static fallback decision to
     `./data/decision-log.csv`
