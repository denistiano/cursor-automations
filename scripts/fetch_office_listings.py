#!/usr/bin/env python3
"""Fetch Plovdiv office rental listings under a monthly budget (alo.bg + fallbacks)."""

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
ALO_CATEGORY = (
    "https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16"
)
URLS = [
    ALO_CATEGORY,
    "https://www.alo.bg/searchq/?q=" + urllib.parse.quote("офис под наем пловдив"),
]

MANUAL_SAMPLES = [
    {
        "title": "Kapana office ~50 m² (verify on alo.bg)",
        "priceEur": 400,
        "sqm": 50,
        "location": "Kapana, Plovdiv",
        "source": "manual-sample",
        "url": "https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16",
        "snippet": "Sample — confirm live listing before visiting.",
    },
    {
        "title": "Center office 50 m² (imot.bg sample)",
        "priceEur": 400,
        "sqm": 50,
        "location": "Center, Plovdiv",
        "source": "manual-sample",
        "url": "https://www.imot.bg/obiavi/prodazhbi-imoti/naemi/plovdiv/ofisi/",
        "snippet": "imot.bg ref Plv 90278 — verify live.",
    },
    {
        "title": "Dondukov garden area 70 m²",
        "priceEur": 420,
        "sqm": 70,
        "location": "Center, Plovdiv",
        "source": "manual-sample",
        "url": ALO_CATEGORY,
        "snippet": "бул. Шести септември — verify on alo.bg",
    },
]

PLOVDIV_RE = re.compile(r"пловдив|plovdiv", re.I)
OFFICE_HINT_RE = re.compile(r"офис|office|бизнес|магазин|шоурум|търгов", re.I)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; VibeCodersHQ/1.0; office research)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_eur(text: str) -> float | None:
    text = text.replace(",", "")
    m = re.search(r"(\d{2,4})\s*€", text)
    if m:
        return float(m.group(1))
    m = re.search(r"(\d{2,4})\s*евро", text, re.I)
    return float(m.group(1)) if m else None


def parse_sqm(text: str) -> float | None:
    m = re.search(r"(\d{1,4})\s*кв\.?\s*м", text, re.I)
    return float(m.group(1)) if m else None


def parse_location(text: str) -> str:
    m = re.search(
        r"list(?:vip|top)-item-address[^>]*>.*?([А-Яа-яA-Za-z0-9\s,\.\-]+,\s*Пловдив)",
        text,
        re.I | re.S,
    )
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"([А-Яа-яA-Za-z\s]+,\s*Пловдив)", text)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace('">', "").replace('"', "")
    return title[:200] if title else "Office listing"


def absolutize_url(path: str) -> str:
    if path.startswith("http"):
        return path
    return "https://www.alo.bg" + path


def is_office_relevant(title: str, snippet: str) -> bool:
    blob = f"{title} {snippet}".lower()
    if not PLOVDIV_RE.search(blob):
        return False
    if OFFICE_HINT_RE.search(blob):
        return True
    # Exclude obvious non-office (beauty salon, manicure) unless title says office
    exclude = re.compile(r"маникюр|салон за красота|палачинк|бургер|пица|бърза закуска|фризьор", re.I)
    if exclude.search(blob) and not re.search(r"офис", blob, re.I):
        return False
    return True


def parse_structured_blocks(html: str) -> list[dict]:
    """Parse alo.bg listvip / listtop listing cards."""
    listings: list[dict] = []
    pattern = re.compile(
        r'class="list(?:vip|top)-item[^"]*"[^>]*(?:id="adrows_(\d+)"[^>]*title="([^"]*)")?'
        r'|onclick="window\.location=\'([^\']+)\'"[^>]*class="listtop-item[^"]*"[^>]*id="adrows_(\d+)"[^>]*title="([^"]*)"',
        re.I,
    )
    # Split on listing container markers
    parts = re.split(
        r'(<div[^>]*class="list(?:vip|top)-item[^"]*"|onclick="window\.location=\'/[^\']+\'"[^>]*class="listtop-item)',
        html,
    )
    for i in range(1, len(parts), 2):
        block = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
        if not PLOVDIV_RE.search(block) and "Пловдив" not in block:
            continue

        path_m = re.search(r'href="(/[^"]+-\d{5,})"', block)
        onclick_m = re.search(r"window\.location='([^']+)'", block)
        path = (path_m.group(1) if path_m else None) or (onclick_m.group(1) if onclick_m else None)
        if not path:
            continue
        if re.search(r"barza-zakuska|salon-za-krasota|friziors|manikyur", path, re.I):
            continue

        title_m = re.search(r'list(?:vip|top)-item-title[^>]*>([^<]+)<', block) or re.search(
            r'title="([^"]+)"', block
        )
        title = clean_title(title_m.group(1) if title_m else "Office listing")

        price = parse_eur(block)
        sqm = parse_sqm(block)
        location = parse_location(block)
        snippet = re.sub(r"<[^>]+>", " ", block)
        snippet = re.sub(r"\s+", " ", snippet).strip()[:400]

        if not is_office_relevant(title, snippet):
            continue

        price_per_sqm = round(price / sqm, 2) if price and sqm else None

        listings.append(
            {
                "title": title,
                "priceEur": price,
                "sqm": sqm,
                "pricePerSqm": price_per_sqm,
                "location": location,
                "url": absolutize_url(path),
                "source": "alo.bg",
                "snippet": snippet,
            }
        )
    return listings


def extract_listings_legacy(html: str) -> list[dict]:
    """Fallback chunk parser for premium / inline snippets."""
    listings: list[dict] = []
    chunks = re.split(r"(?=🏢|Премиум офис|Офис под наем|Дава под [Нн]аем)", html)
    seen: set[str] = set()
    for chunk in chunks:
        if not PLOVDIV_RE.search(chunk):
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
        title = clean_title(title_m.group(1) if title_m else "Office listing")
        if not is_office_relevant(title, chunk):
            continue
        path_m = re.search(r'href="(/[^"]+-\d{5,})"', chunk)
        key = f"{title}|{price}|{sqm}"
        if key in seen:
            continue
        seen.add(key)
        listings.append(
            {
                "title": title,
                "priceEur": price,
                "sqm": sqm,
                "pricePerSqm": round(price / sqm, 2) if sqm else None,
                "location": parse_location(chunk),
                "url": absolutize_url(path_m.group(1)) if path_m else "",
                "source": "alo.bg",
                "snippet": re.sub(r"<[^>]+>", " ", chunk)[:400].strip(),
            }
        )
    return listings


def merge_listings(*groups: list[dict]) -> list[dict]:
    """Merge listing groups; prefer rows with URLs and cleaner titles."""
    by_key: dict[str, dict] = {}
    for group in groups:
        for row in group:
            price = row.get("priceEur")
            sqm = row.get("sqm")
            title_key = re.sub(r"[^a-z0-9]", "", (row.get("title") or "").lower())[:40]
            key = f"{price}|{sqm}|{title_key}"
            existing = by_key.get(key)
            if not existing:
                by_key[key] = row
                continue
            # Prefer entry with URL, longer title, or location
            score = lambda r: (
                (2 if r.get("url") else 0)
                + (1 if r.get("location") else 0)
                + len(r.get("title") or "")
            )
            if score(row) > score(existing):
                by_key[key] = row
    return list(by_key.values())


def reject_listing(row: dict) -> bool:
    url = (row.get("url") or "").lower()
    if re.search(r"barza-zakuska|salon-za-krasota|friziors|manikyur", url):
        return True
    blob = f"{row.get('title', '')} {row.get('snippet', '')}".lower()
    if re.search(r"фризьор|маникюр|бърза закуска|палачинк", blob) and not re.search(r"\bофис\b", blob[:120]):
        return True
    return False


def normalize_listing(row: dict) -> dict | None:
    price = row.get("priceEur")
    if price == 0:
        price = None
        row["priceEur"] = None
    sqm = row.get("sqm")
    if price and sqm:
        row["pricePerSqm"] = round(price / sqm, 2)
    row["title"] = clean_title(row.get("title") or "Office listing")
    if row.get("url"):
        row["url"] = absolutize_url(row["url"])
    return None if reject_listing(row) else row


def filter_by_budget(listings: list[dict], max_eur: int) -> tuple[list[dict], list[dict]]:
    """Return (within budget, over budget or unknown price)."""
    within: list[dict] = []
    other: list[dict] = []
    for row in listings:
        price = row.get("priceEur")
        if price is None:
            other.append(row)
        elif price <= max_eur:
            within.append(row)
        else:
            other.append(row)
    return within, other


def main() -> int:
    structured: list[dict] = []
    legacy: list[dict] = []
    errors: list[str] = []
    for url in URLS:
        try:
            html = fetch_html(url)
            structured.extend(parse_structured_blocks(html))
            legacy.extend(extract_listings_legacy(html))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{url}: {exc}")

    all_rows = [r for r in (normalize_listing(r) for r in merge_listings(structured, legacy)) if r]
    within, over = filter_by_budget(all_rows, MAX_EUR)
    # Prefer budget listings; include over-budget only if we have few matches
    listings = within if len(within) >= 3 else within + over[: max(0, 10 - len(within))]
    listings = sorted(
        listings,
        key=lambda x: (
            x["priceEur"] if x.get("priceEur") is not None else 99999,
            -(x.get("sqm") or 0),
        ),
    )[:60]

    ok = bool(within)
    if not listings:
        listings = [dict(x) for x in MANUAL_SAMPLES]
        ok = False

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "maxBudgetEur": MAX_EUR,
        "city": "Plovdiv",
        "searchUrls": URLS,
        "alsoCheck": [
            {"label": "imot.bg — Plovdiv offices", "url": "https://www.imot.bg/obiavi/prodazhbi-imoti/naemi/plovdiv/ofisi/"},
            {"label": "alo.bg — offices Plovdiv", "url": ALO_CATEGORY},
            {"label": "alo.bg — search", "url": "https://www.alo.bg/searchq/?q=" + urllib.parse.quote("офис под наем пловдив")},
        ],
        "ok": ok,
        "scrapeErrors": errors,
        "includesManualSamples": not ok,
        "count": len(listings),
        "countWithinBudget": len(within),
        "listings": listings,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(listings)} listings, {len(within)} under {MAX_EUR} EUR)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
