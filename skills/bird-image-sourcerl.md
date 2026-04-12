---
name: bird-image-sourcer
description: Source legally usable, attribution-correct bird images
version: 1.0.0
---
# Bird Image Sourcer

## Priority Order for Image Sources

### Source 1: Macaulay Library (Cornell Lab) — PREFERRED
URL: https://search.macaulaylibrary.org/catalog
API: https://api.ebird.org/v2/ (eBird API key required)
License: CC BY-NC-SA — free for non-commercial use WITH attribution
Attribution format: "Photo: [Photographer Name] / Macaulay Library"

Search procedure:
1. Query: species common name + "photo" in Macaulay Library
2. Filter: CC licensed, highest quality rating (4-5 stars)
3. Select horizontally-oriented image, min 1200px wide
4. Download via direct URL
5. Record: photographer name, ML catalogue number, species

### Source 2: Wikimedia Commons — FALLBACK
URL: https://commons.wikimedia.org/wiki/Special:Search
Filter: CC BY or CC BY-SA licenses ONLY (commercial use allowed)
Attribution: "Photo: [Author] / Wikimedia Commons / [License]"

### Source 3: iNaturalist — FALLBACK
URL: https://www.inaturalist.org/observations
Filter: CC BY or CC BY-SA only
Quality: Research grade observations only

## Image Processing After Download
1. Rename: [species-slug]-[source]-[date].jpg
2. Compress via ShortPixel API (target: under 150KB for web)
3. Generate alt text: "[Species common name] ([Scientific name]) 
   [brief description of pose/setting]"
4. Store attribution data for insertion into article caption

## Attribution Insertion
Add caption below image in article HTML:
<figure>
  <img src="[url]" alt="[alt text]" loading="lazy">
  <figcaption>Photo: [Photographer] / [Source] ([License])</figcaption>
</figure>