#!/usr/bin/env python3
"""Fetch Plovdiv office rental listings under a monthly budget (alo.bg search)."""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "office-listings.json"
MAX_EUR = 800
URLS = [
    "https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16",
    "https://www.alo.bg/searchq/?q=" + urllib.parse.quote("офис под наем пловdiv"),
]

# Curated samples when sites block bots (verify manually before visiting)
MANUAL_SAMPLES = [
    {
        "title": "Kapana office ~50 m² (alo.bg snippet, May 2026)",
        "priceEur": 400,
        "sqm": 50,
        "source": "manual-sample",
        "snippet": "Капана — 400 EUR/month, 50 m²; verify on alo.bg/imot.bg",
    },
    {
        "title": "Center office 50 m² (imot.bg sample)",
        "priceEur": 400,
        "sqm": 50,
        "source": "manual-sample",
        "snippet": "Идеален център — imot.bg listing ref Plv 90278 class; verify live",
    },
    {
        "title": "Dondukov garden area 70 m²",
        "priceEur": 420,
        "sqm": 70,
        "source": "manual-sample",
        "snippet": "бул. Шести септември 145 — 420 EUR без ДДС; verify on alo.bg",
    },
]


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "VibeCodersHQ/1.0 (office research; contact: denis)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_eur(snippet: str) -> float | None:
    m = re.search(r"(\d{2,4})\s*€", snippet.replace(",", ""))
    if m:
        return float(m.group(1))
    m = re.search(r"(\d{2,4})\s*евро", snippet, re.I)
    if m:
        return float(m.group(1))
    return None


def parse_sqm(snippet: str) -> float | None:
    m = re.search(r"(\d{2,4})\s*кв\.?\s*м", snippet, re.I)
    return float(m.group(1)) if m else None


def extract_listings(html: str) -> list[dict]:
    """Best-effort parse of alo.bg search snippets (HTML structure may change)."""
    listings: list[dict] = []
    # Split on premium/listing markers; alo.bg uses varied markup
    chunks = re.split(r"(?=🏢|Премиум офис|Офис под наем|Дава под [Нн]аем)", html)
    seen: set[str] = set()
    for chunk in chunks:
        if "пловдив" not in chunk.lower() and "plovdiv" not in chunk.lower():
            continue
        price = parse_eur(chunk)
        if price is None or price > MAX_EUR:
            continue
        sqm = parse_sqm(chunk)
        title_m = re.search(
            r"(Премиум офис[^<]{0,120}|Офис под наем[^<]{0,120}|Светъл[^<]{0,120})",
            chunk,
            re.I,
        )
        title = re.sub(r"\s+", " ", title_m.group(1)).strip() if title_m else "Office listing"
        key = f"{title}|{price}|{sqm}"
        if key in seen:
            continue
        seen.add(key)
        listings.append(
            {
                "title": title[:200],
                "priceEur": price,
                "sqm": sqm,
                "source": "alo.bg",
                "snippet": re.sub(r"<[^>]+>", " ", chunk)[:400].strip(),
            }
        )
    return sorted(listings, key=lambda x: (x["priceEur"], -(x["sqm"] or 0)))[:40]


def main() -> int:
    listings: list[dict] = []
    errors: list[str] = []
    for url in URLS:
        try:
            html = fetch_html(url)
            listings.extend(extract_listings(html))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{url}: {exc}")
    seen: set[str] = set()
    unique: list[dict] = []
    for row in sorted(listings, key=lambda x: (x["priceEur"], -(x["sqm"] or 0))):
        key = f"{row['title']}|{row['priceEur']}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    listings = unique[:40]
    ok = bool(listings)
    if not listings:
        listings = [dict(x) for x in MANUAL_SAMPLES]
    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "maxBudgetEur": MAX_EUR,
        "city": "Plovdiv",
        "searchUrls": URLS,
        "alsoCheck": [
            "https://www.imot.bg/obiavi/prodazhbi-imoti/naemi/plovdiv/ofisi/",
            "https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16",
        ],
        "ok": ok,
        "scrapeErrors": errors,
        "includesManualSamples": not ok,
        "count": len(listings),
        "listings": listings,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(listings)} listings under {MAX_EUR} EUR)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
