#!/usr/bin/env python3
import base64
import json
import math
import re
from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / 'web' / 'products.json'
SOURCE_DIR = ROOT / 'design' / 'preview-source'
TARGET_DIRS = [ROOT / 'web' / 'assets' / 'previews', ROOT / 'docs' / 'assets' / 'previews']

PALETTES = {
    'state': dict(bg1='#f6f1e8', bg2='#ded1be', accent='#476c64', accent2='#b86d4b', paper='#fffaf2', ink='#243130', chip='#e4eee8'),
    'migration': dict(bg1='#f7f1e6', bg2='#d8ccb7', accent='#315f53', accent2='#cf7c56', paper='#fffaf1', ink='#223036', chip='#e6efe9'),
    'warbler': dict(bg1='#f4ede3', bg2='#d9c6b3', accent='#2f5645', accent2='#d08a4f', paper='#fff9ef', ink='#213032', chip='#e2ede4'),
    'planner': dict(bg1='#f3efe8', bg2='#d4c7bb', accent='#42535f', accent2='#c38b5a', paper='#fffaf4', ink='#24303a', chip='#e8ecef'),
    'bundle': dict(bg1='#f5ede2', bg2='#d6c3ad', accent='#264b43', accent2='#c97a4a', paper='#fff9f0', ink='#213032', chip='#e5eee7'),
    'default': dict(bg1='#f5efe7', bg2='#d8cab8', accent='#35584f', accent2='#c57d57', paper='#fffaf1', ink='#233034', chip='#e4ede6'),
}

STATE_ACCENTS = {
    'california': ('Pacific Flyway', 'Monterey cypress + coastal cream', '#5f8f77'),
    'texas': ('Central Flyway', 'Hill country sage + warm stone', '#7b8763'),
    'florida': ('Atlantic flyway', 'Heron blue + palmetto green', '#5e9295'),
    'new-york': ('Atlantic flyway', 'Hudson slate + museum cream', '#6a758a'),
    'washington': ('Pacific flyway', 'Moss cedar + overcast pearl', '#5a7d6a'),
    'colorado': ('Mountain migration', 'Aspen gold + alpine spruce', '#8a8a5c'),
    'north-carolina': ('Coastal plain', 'Magnolia ivory + pine green', '#67806d'),
    'arizona': ('Sonoran routes', 'Adobe clay + agave shadow', '#9a7c5f'),
    'oregon': ('Pacific flyway', 'Fern green + misted linen', '#567a68'),
    'pennsylvania': ('Appalachian corridor', 'Woodland bronze + feather grey', '#726c5d'),
}


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def infer_family(sku: str) -> str:
    if 'STATE' in sku:
        return 'state'
    if 'MIGRATION' in sku:
        return 'migration'
    if 'WARBLER-BUNDLE' in sku:
        return 'bundle'
    if 'WARBLER' in sku:
        return 'warbler'
    if 'PLANNER' in sku or 'GOODNOTES' in sku:
        return 'planner'
    return 'default'


def collection_label(product: dict, family: str) -> str:
    if family == 'state':
        state_slug = slugify(product['sku'].split('DIGI-STATE-')[-1])
        return STATE_ACCENTS.get(state_slug, ('Regional archive', '', ''))[0]
    if family == 'migration':
        return 'Migration field notes'
    if family == 'warbler':
        return 'Warbler study collection'
    if family == 'planner':
        return 'GoodNotes atelier'
    if family == 'bundle':
        return 'Signature bundle'
    return 'Field notes edition'


def descriptor(product: dict, family: str) -> str:
    title = product['title']
    if family == 'state':
        state_slug = slugify(product['sku'].split('DIGI-STATE-')[-1])
        return STATE_ACCENTS.get(state_slug, ('', 'Premium printable checklist', ''))[1]
    if family == 'migration':
        m = re.search(r'v(\d+)$', title, re.I)
        version = m.group(1) if m else 'Edition'
        return f'Version {version} • premium migration insert'
    if family == 'warbler':
        return 'Editorial reference sheet with refined paper stack'
    if family == 'planner':
        return 'Luxury digital planner mockup with note-sheet layering'
    if family == 'bundle':
        return 'Collector set with layered stationery presentation'
    return 'Premium printable mockup'


def wrap_title(title: str):
    title = title.replace(', ', ' • ', 1)
    words = title.split()
    lines = []
    current = []
    count = 0
    for word in words:
        limit = 20 if len(lines) == 0 else 22
        add = len(word) + (1 if current else 0)
        if current and count + add > limit and len(lines) < 2:
            lines.append(' '.join(current))
            current = [word]
            count = len(word)
        else:
            current.append(word)
            count += add
    if current:
        lines.append(' '.join(current))
    if len(lines) > 3:
        merged = lines[:2]
        merged.append(' '.join(lines[2:]))
        lines = merged
    return lines[:3]


def make_data_uri(svg_text: str) -> str:
    encoded = base64.b64encode(svg_text.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{encoded}'


def build_svg(product: dict, source_svg: str) -> str:
    sku = product['sku']
    family = infer_family(sku)
    palette = PALETTES[family]
    title_lines = wrap_title(product['title'])
    title_y = 256
    title_parts = []
    for idx, line in enumerate(title_lines):
        title_parts.append(
            f'<text x="120" y="{title_y + idx * 70}" font-family="Georgia, serif" font-size="52" fill="{palette["ink"]}" font-weight="700">{escape(line)}</text>'
        )

    data_uri = make_data_uri(source_svg)
    label = collection_label(product, family)
    note = descriptor(product, family)
    price = f"${float(product['price']):.2f}"
    state_slug = slugify(sku.split('DIGI-STATE-')[-1]) if 'DIGI-STATE-' in sku else ''
    accent3 = STATE_ACCENTS.get(state_slug, ('', '', palette['accent']))[2] if family == 'state' else palette['accent']
    badge = 'Digital download • SVG/PDF preview'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1200" viewBox="0 0 1600 1200" role="img" aria-label="Premium mockup preview for {escape(product['title'])}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{palette['bg1']}"/>
      <stop offset="100%" stop-color="{palette['bg2']}"/>
    </linearGradient>
    <radialGradient id="glow" cx="35%" cy="26%" r="70%">
      <stop offset="0%" stop-color="#fffdf8" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="#fffdf8" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="cardEdge" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="#efe4d3" stop-opacity="0.9"/>
    </linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="18" stdDeviation="28" flood-color="#8f7d67" flood-opacity="0.22"/>
    </filter>
    <filter id="softShadow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="20" stdDeviation="22" flood-color="#8f7d67" flood-opacity="0.16"/>
    </filter>
    <filter id="innerGlow" x="-30%" y="-30%" width="160%" height="160%">
      <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#ffffff" flood-opacity="0.55"/>
    </filter>
    <clipPath id="heroClip">
      <rect x="0" y="0" width="520" height="720" rx="22"/>
    </clipPath>
    <pattern id="pinstripe" width="14" height="14" patternUnits="userSpaceOnUse" patternTransform="rotate(18)">
      <rect width="14" height="14" fill="transparent"/>
      <rect x="0" y="0" width="2" height="14" fill="#ffffff" opacity="0.16"/>
    </pattern>
  </defs>
  <rect width="1600" height="1200" fill="url(#bg)"/>
  <rect width="1600" height="1200" fill="url(#glow)"/>
  <rect x="0" y="0" width="1600" height="1200" fill="url(#pinstripe)" opacity="0.22"/>

  <g opacity="0.18" fill="none" stroke="{accent3}" stroke-width="2.2" stroke-linecap="round">
    <path d="M121 1031c48-63 78-137 89-220 10-70 8-137-6-201"/>
    <path d="M155 1002c44-54 76-122 91-192 8-36 12-79 10-128"/>
    <path d="M1413 176c-48 63-78 137-89 220-10 70-8 137 6 201"/>
    <path d="M1379 205c-44 54-76 122-91 192-8 36-12 79-10 128"/>
    <path d="M203 927c25-19 49-42 69-71 24-35 42-74 53-118" opacity="0.75"/>
    <path d="M1311 279c-25 19-49 42-69 71-24 35-42 74-53 118" opacity="0.75"/>
  </g>

  <ellipse cx="1135" cy="846" rx="344" ry="118" fill="#93816b" opacity="0.15"/>
  <ellipse cx="1080" cy="895" rx="262" ry="72" fill="#93816b" opacity="0.1"/>

  <g>
    <text x="120" y="112" font-family="Arial, sans-serif" font-size="20" letter-spacing="5" fill="{palette['accent']}" font-weight="700">FIELD &amp; FEATHER CO.</text>
    <text x="120" y="150" font-family="Arial, sans-serif" font-size="22" fill="#786d5f">Premium printable stationery mockup</text>

    <rect x="120" y="190" width="232" height="40" rx="20" fill="{palette['chip']}"/>
    <text x="145" y="216" font-family="Arial, sans-serif" font-size="18" fill="{palette['accent']}" font-weight="700">{escape(label.upper())}</text>

    {''.join(title_parts)}

    <text x="120" y="504" font-family="Arial, sans-serif" font-size="24" fill="#645b50">{escape(note)}</text>

    <g transform="translate(120 592)">
      <rect x="0" y="0" width="500" height="212" rx="26" fill="#fffaf3" opacity="0.76"/>
      <rect x="32" y="34" width="10" height="142" rx="5" fill="{palette['accent2']}" opacity="0.9"/>
      <text x="64" y="72" font-family="Georgia, serif" font-size="30" fill="{palette['ink']}" font-weight="700">Refined card presentation</text>
      <text x="64" y="114" font-family="Arial, sans-serif" font-size="22" fill="#5f5c55">Layered paper, gallery lighting, archival palette.</text>
      <text x="64" y="152" font-family="Arial, sans-serif" font-size="22" fill="#5f5c55">Built from the original sheet artwork for continuity.</text>
      <text x="64" y="190" font-family="Arial, sans-serif" font-size="20" fill="{palette['accent2']}" font-weight="700">{escape(badge)}</text>
    </g>

    <g transform="translate(120 978)">
      <text x="0" y="0" font-family="Georgia, serif" font-size="46" fill="{palette['ink']}" font-weight="700">{price}</text>
      <text x="138" y="0" font-family="Arial, sans-serif" font-size="23" fill="#6b655d">instant delivery • polished preview art</text>
    </g>
  </g>

  <g filter="url(#softShadow)" transform="translate(888 230) rotate(-7)">
    <rect x="80" y="58" width="510" height="715" rx="24" fill="#f7edde" opacity="0.9"/>
    <rect x="36" y="94" width="510" height="715" rx="24" fill="#f2e7d6" opacity="0.9"/>
  </g>

  <g filter="url(#shadow)" transform="translate(920 168) rotate(-7)">
    <rect x="0" y="0" width="520" height="720" rx="26" fill="{palette['paper']}"/>
    <rect x="18" y="18" width="484" height="684" rx="22" fill="url(#cardEdge)" opacity="0.46"/>
    <g clip-path="url(#heroClip)">
      <image href="{data_uri}" x="0" y="0" width="520" height="720" preserveAspectRatio="xMidYMid slice"/>
      <rect x="0" y="0" width="520" height="720" fill="#fff9f2" opacity="0.06"/>
    </g>
    <rect x="0.5" y="0.5" width="519" height="719" rx="26" fill="none" stroke="#dccfbd"/>
  </g>

  <g filter="url(#innerGlow)" transform="translate(820 760)">
    <rect x="0" y="0" width="238" height="164" rx="22" fill="#fff8ef" opacity="0.92"/>
    <text x="28" y="46" font-family="Arial, sans-serif" font-size="18" letter-spacing="3" fill="{palette['accent']}">CURATED DETAILS</text>
    <text x="28" y="84" font-family="Georgia, serif" font-size="26" fill="{palette['ink']}" font-weight="700">Editorial crop</text>
    <text x="28" y="116" font-family="Arial, sans-serif" font-size="18" fill="#60574f">soft depth</text>
    <text x="28" y="142" font-family="Arial, sans-serif" font-size="18" fill="#60574f">premium paper stack</text>
  </g>

  <circle cx="1324" cy="202" r="56" fill="#fff8ee" opacity="0.68"/>
  <circle cx="1324" cy="202" r="18" fill="{palette['accent2']}" opacity="0.45"/>
</svg>
'''


def main():
    products = json.loads(PRODUCTS_PATH.read_text())
    written = []
    for product in products:
        sku_slug = product['sku'].lower()
        source_path = SOURCE_DIR / f'{sku_slug}.svg'
        if not source_path.exists():
            raise FileNotFoundError(f'Missing source preview for {product["sku"]}: {source_path}')
        source_svg = source_path.read_text()
        output = build_svg(product, source_svg)
        for target_dir in TARGET_DIRS:
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / f'{sku_slug}.svg'
            target_path.write_text(output)
            written.append(str(target_path.relative_to(ROOT)))
    print(f'Generated {len(products)} premium preview mockups into {len(TARGET_DIRS)} targets ({len(written)} files).')


if __name__ == '__main__':
    main()
