#!/usr/bin/env python3
import argparse
import base64
import hashlib
import json
import os
import secrets
import urllib.parse
import urllib.request

AUTH_BASE = "https://www.etsy.com/oauth/connect"
TOKEN_URL = "https://api.etsy.com/v3/public/oauth/token"


def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip('=')


def generate_pkce() -> tuple[str, str]:
    verifier = b64url(secrets.token_bytes(32))
    challenge = b64url(hashlib.sha256(verifier.encode()).digest())
    return verifier, challenge


def build_auth_url(client_id: str, redirect_uri: str, scopes: str, state: str, challenge: str) -> str:
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scopes,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return AUTH_BASE + "?" + urllib.parse.urlencode(params)


def post_form(url: str, data: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode(),
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def cmd_start(args):
    client_id = args.client_id or os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
    redirect_uri = args.redirect_uri or os.getenv("ETSY_REDIRECT_URI", "http://localhost:9876/callback")
    scopes = args.scopes or "shops_r shops_w listings_r listings_w transactions_r"
    if not client_id:
        raise SystemExit("Missing Etsy client_id (ETSY_CLIENT_ID or ETSY_API_KEY)")

    verifier, challenge = generate_pkce()
    state = secrets.token_urlsafe(24)
    url = build_auth_url(client_id, redirect_uri, scopes, state, challenge)

    out = {
        "authorize_url": url,
        "state": state,
        "code_verifier": verifier,
        "redirect_uri": redirect_uri,
        "scopes": scopes,
    }
    print(json.dumps(out, indent=2))


def cmd_exchange(args):
    client_id = args.client_id or os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
    redirect_uri = args.redirect_uri or os.getenv("ETSY_REDIRECT_URI", "http://localhost:9876/callback")
    code = args.code
    verifier = args.code_verifier

    if not client_id or not code or not verifier:
        raise SystemExit("Need client_id, code, and code_verifier")

    payload = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code": code,
        "code_verifier": verifier,
    }
    token = post_form(TOKEN_URL, payload)
    print(json.dumps(token, indent=2))


def cmd_refresh(args):
    client_id = args.client_id or os.getenv("ETSY_CLIENT_ID") or os.getenv("ETSY_API_KEY")
    refresh_token = args.refresh_token or os.getenv("ETSY_REFRESH_TOKEN")
    if not client_id or not refresh_token:
        raise SystemExit("Need client_id and refresh_token")
    payload = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "refresh_token": refresh_token,
    }
    token = post_form(TOKEN_URL, payload)
    print(json.dumps(token, indent=2))


def main():
    p = argparse.ArgumentParser(description="Etsy OAuth helper")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("start", help="Generate Etsy authorize URL + PKCE values")
    s.add_argument("--client-id")
    s.add_argument("--redirect-uri")
    s.add_argument("--scopes")
    s.set_defaults(func=cmd_start)

    e = sub.add_parser("exchange", help="Exchange authorization code for tokens")
    e.add_argument("--client-id")
    e.add_argument("--redirect-uri")
    e.add_argument("--code", required=True)
    e.add_argument("--code-verifier", required=True)
    e.set_defaults(func=cmd_exchange)

    r = sub.add_parser("refresh", help="Refresh Etsy access token")
    r.add_argument("--client-id")
    r.add_argument("--refresh-token")
    r.set_defaults(func=cmd_refresh)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
