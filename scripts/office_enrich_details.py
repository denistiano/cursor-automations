#!/usr/bin/env python3
"""Fetch listing detail pages to enrich snippets for amenity/keyword scoring."""

from __future__ import annotations

import re
import time
import urllib.error

FETCH_DELAY_SEC = 0.4
MAX_DETAIL_CHARS = 12_000

STRIP_TAGS_RE = re.compile(r"<(script|style|noscript)[^>]*>.*?</\1>", re.I | re.S)
TAG_RE = re.compile(r"<[^>]+>")


def extract_detail_text(html: str) -> str:
    html = STRIP_TAGS_RE.sub(" ", html)
    text = TAG_RE.sub(" ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()[:MAX_DETAIL_CHARS]


def enrich_listing_detail(row: dict, fetch_html) -> dict:
    """Append detail-page text to snippet (mutates copy). fetch_html(url) -> str."""
    url = row.get("url") or ""
    if not url.startswith("http"):
        return row
    out = dict(row)
    try:
        html = fetch_html(url)
        extra = extract_detail_text(html)
        if extra:
            prev = (out.get("snippet") or "")[:2000]
            out["snippet"] = f"{prev} {extra}".strip()[:MAX_DETAIL_CHARS]
            out["detailEnriched"] = True
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        out["detailEnriched"] = False
    return out


def enrich_listings(
    listings: list[dict],
    fetch_html,
    urls: set[str] | None = None,
    limit: int = 80,
) -> list[dict]:
    by_url = {r["url"]: r for r in listings if r.get("url")}
    targets = list(urls or by_url.keys())[:limit]
    enriched: list[dict] = []
    for i, url in enumerate(targets):
        row = by_url.get(url)
        if not row:
            continue
        enriched.append(enrich_listing_detail(row, fetch_html))
        if i + 1 < len(targets):
            time.sleep(FETCH_DELAY_SEC)
    touched = {r["url"] for r in enriched}
    return [
        next((e for e in enriched if e.get("url") == r.get("url")), r)
        if r.get("url") in touched
        else r
        for r in listings
    ]
