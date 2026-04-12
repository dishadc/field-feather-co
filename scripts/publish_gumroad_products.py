#!/usr/bin/env python3
import csv
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_CSV = ROOT / "imports" / "gumroad_products.csv"
LINKS_CSV = ROOT / "data" / "product_links.csv"
MAP_CSV = ROOT / "data" / "gumroad_product_map.csv"

ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "").strip()
if not ACCESS_TOKEN:
    raise SystemExit("Missing GUMROAD_ACCESS_TOKEN env var")


def api_get(path, params):
    q = urllib.parse.urlencode(params)
    url = f"https://api.gumroad.com{path}?{q}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def api_post(path, params, retries=5):
    req = urllib.request.Request(
        f"https://api.gumroad.com{path}",
        data=urllib.parse.urlencode(params).encode(),
        method="POST",
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = e.read().decode(errors="ignore") if hasattr(e, "read") else ""
            if e.code == 429 and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            last_err = f"POST {path} failed {e.code}: {body[:200]}"
            break
    return {"success": False, "error": last_err or "unknown error"}


# existing products by custom permalink
existing = api_get("/v2/products", {"access_token": ACCESS_TOKEN}).get("products", [])
by_slug = {p.get("custom_permalink"): p for p in existing if p.get("custom_permalink")}

created = 0
reused = 0
errors = []
rows_out = []

for row in csv.DictReader(IMPORT_CSV.open()):
    slug = row["url_slug"].strip()
    status = row["status"].strip().lower()
    price_cents = int(round(float(row["price_usd"].strip()) * 100))

    product = by_slug.get(slug)
    if not product:
        payload = {
            "access_token": ACCESS_TOKEN,
            "name": row["name"].strip(),
            "description": row["description"].strip(),
            "price": str(price_cents),
            "custom_permalink": slug,
            "published": "true" if status == "ready" else "false",
        }
        resp = api_post("/v2/products", payload)
        if not resp.get("success", True) or not resp.get("product"):
            errors.append({"sku": row["sku"].strip(), "slug": slug, "error": resp.get("error", "create failed")})
            continue
        product = resp.get("product", {})
        created += 1
        time.sleep(0.6)
    else:
        reused += 1

    checkout = product.get("short_url") or product.get("url") or ""
    rows_out.append(
        {
            "sku": row["sku"].strip(),
            "channel": "gumroad",
            "checkout_url": checkout,
            "status": status,
            "product_id": product.get("id", ""),
            "slug": product.get("custom_permalink", slug),
            "price_cents": product.get("price", price_cents),
            "name": product.get("name", row["name"].strip()),
        }
    )

# update product_links.csv using gumroad rows
with LINKS_CSV.open() as f:
    current = list(csv.DictReader(f))

index = {r["sku"]: r for r in rows_out}
updated = []
for row in current:
    sku = row["sku"]
    if sku in index:
        g = index[sku]
        updated.append(
            {
                "sku": sku,
                "channel": "gumroad",
                "checkout_url": g["checkout_url"],
                "status": g["status"],
            }
        )
    else:
        updated.append(row)

with LINKS_CSV.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["sku", "channel", "checkout_url", "status"])
    w.writeheader()
    w.writerows(updated)

with MAP_CSV.open("w", newline="") as f:
    fields = ["sku", "product_id", "slug", "checkout_url", "status", "price_cents", "name"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in rows_out:
        w.writerow({k: r.get(k, "") for k in fields})

print(json.dumps({
    "created": created,
    "reused": reused,
    "errors": len(errors),
    "mapped": len(rows_out),
    "links_updated": sum(1 for r in updated if r.get("channel") == "gumroad" and r.get("checkout_url")),
}, indent=2))
if errors:
    print("sample_errors", json.dumps(errors[:5], indent=2))
