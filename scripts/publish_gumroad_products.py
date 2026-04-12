#!/usr/bin/env python3
import argparse
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


def load_token() -> str:
    tok = os.getenv("GUMROAD_ACCESS_TOKEN", "").strip()
    if tok:
        return tok
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith("GUMROAD_ACCESS_TOKEN="):
                return line.split("=", 1)[1].strip()
    return ""


def api_get(path: str, params: dict) -> dict:
    q = urllib.parse.urlencode(params)
    url = f"https://api.gumroad.com{path}?{q}"
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read().decode())


def api_post(path: str, params: dict, retries: int = 5) -> dict:
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


def api_put(path: str, params: dict, retries: int = 5) -> dict:
    req = urllib.request.Request(
        f"https://api.gumroad.com{path}",
        data=urllib.parse.urlencode(params).encode(),
        method="PUT",
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
            last_err = f"PUT {path} failed {e.code}: {body[:200]}"
            break
    return {"success": False, "error": last_err or "unknown error"}


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish/import Gumroad products and sync local link maps")
    parser.add_argument("--max-create", type=int, default=50, help="Maximum number of new products to create in this run")
    args = parser.parse_args()
    max_create = max(0, args.max_create)

    access_token = load_token()
    if not access_token:
        raise SystemExit("Missing GUMROAD_ACCESS_TOKEN env var (or .env entry)")

    existing = api_get("/v2/products", {"access_token": access_token}).get("products", [])
    by_slug = {p.get("custom_permalink"): p for p in existing if p.get("custom_permalink")}

    created = 0
    reused = 0
    errors = []
    rows_out = []
    payment_blocked = False

    # ready first, then draft
    import_rows = list(csv.DictReader(IMPORT_CSV.open()))
    import_rows.sort(
        key=lambda r: (
            0 if r.get("url_slug", "").strip() in by_slug else 1,
            0 if r.get("status", "").strip().lower() == "ready" else 1,
            r.get("sku", ""),
        )
    )

    for row in import_rows:
        slug = row["url_slug"].strip()
        status = row["status"].strip().lower()
        price_cents = int(round(float(row["price_usd"].strip()) * 100))

        product = by_slug.get(slug)
        if not product:
            if payment_blocked:
                continue
            if created >= max_create:
                continue

            payload = {
                "access_token": access_token,
                "name": row["name"].strip(),
                "description": row["description"].strip(),
                "price": str(price_cents),
                "custom_permalink": slug,
                "published": "true" if status == "ready" else "false",
            }
            resp = api_post("/v2/products", payload)
            if not resp.get("success", True) or not resp.get("product"):
                err = resp.get("error", "create failed")
                errors.append({"sku": row["sku"].strip(), "slug": slug, "error": err})
                if "429" in str(err):
                    break
                continue

            product = resp.get("product", {})
            created += 1
            by_slug[slug] = product
            time.sleep(0.6)
        else:
            reused += 1

        product_id = product.get("id", "")
        if product_id:
            endpoint = f"/v2/products/{product_id}/enable" if status == "ready" else f"/v2/products/{product_id}/disable"
            resp_state = api_put(endpoint, {"access_token": access_token})
            if not resp_state.get("success", True):
                err = (
                    resp_state.get("error")
                    or resp_state.get("message")
                    or f"state change failed for {product_id}"
                )
                errors.append({"sku": row["sku"].strip(), "slug": slug, "error": err})
                if "connect at least one payment method" in str(err).lower():
                    payment_blocked = True
                if "429" in str(err):
                    break
            else:
                product = resp_state.get("product", product)

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
                "published": str(bool(product.get("published", False))).lower(),
            }
        )

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
        fields = ["sku", "product_id", "slug", "checkout_url", "status", "price_cents", "name", "published"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows_out:
            w.writerow({k: r.get(k, "") for k in fields})

    print(
        json.dumps(
            {
                "created": created,
                "reused": reused,
                "errors": len(errors),
                "mapped": len(rows_out),
                "links_updated": sum(1 for r in updated if r.get("channel") == "gumroad" and r.get("checkout_url")),
                "max_create": max_create,
                "payment_method_blocked": payment_blocked,
            },
            indent=2,
        )
    )
    if errors:
        print("sample_errors", json.dumps(errors[:5], indent=2))


if __name__ == "__main__":
    main()
