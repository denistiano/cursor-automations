#!/usr/bin/env python3
"""Fetch Plovdiv office rental listings (alo.bg + imot.bg) matching search criteria."""

from __future__ import annotations

import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "office-listings.json"
MAX_EUR = 800
FETCH_DELAY_SEC = 0.35

ALO_CATEGORY = (
    "https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16"
)
ALO_SEARCH = "https://www.alo.bg/searchq/?q=" + urllib.parse.quote("офис под наем пловдив")
IMOT_OFFICES = "https://www.imot.bg/obiavi/naemi/grad-plovdiv/ofis"

SEARCH_SOURCES: list[tuple[str, str]] = [
    ("alo.bg", ALO_CATEGORY),
    ("alo.bg", ALO_SEARCH),
    ("imot.bg", IMOT_OFFICES),
]

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

MANUAL_SAMPLES = [
    {
        "title": "Kapana office ~50 m² (verify on alo.bg)",
        "priceEur": 400,
        "sqm": 50,
        "location": "Kapana, Plovdiv",
        "source": "manual-sample",
        "url": ALO_CATEGORY,
        "snippet": "Sample — confirm live listing before visiting.",
    },
]

PLOVDIV_RE = re.compile(r"пловдив|plovdiv", re.I)
OFFICE_HINT_RE = re.compile(r"офис|office|бизнес|магазин|шоурум|търгов", re.I)
EXCLUDED_PATH_RE = re.compile(r"barza-zakuska|salon-za-krasota|friziors|manikyur", re.I)
EXCLUDED_TEXT_RE = re.compile(r"фризьор|маникюр|бърза закуска|палачинк", re.I)
IMOT_OFFICE_SLUG_RE = re.compile(
    r"(obiava-2h\d+-dava-pod-naem-ofis-grad-plovdiv-[^\"#]+)", re.I
)


def fetch_html(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "bg-BG,bg;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_eur(text: str) -> float | None:
    text = text.replace(",", "").replace("\xa0", " ")
    m = re.search(r"(\d[\d\s]{1,6})\s*€", text)
    if m:
        return float(m.group(1).replace(" ", ""))
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
    m = re.search(r"([А-Яа-яA-Za-z\s\-]+,\s*Пловдив)", text)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = re.search(r"grad-plovdiv-([a-z0-9\-]+)", text, re.I)
    if m:
        area = m.group(1).replace("-", " ").title()
        return f"{area}, Plovdiv"
    return ""


def clean_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    title = title.replace('">', "").replace('"', "")
    return title[:200] if title else "Office listing"


def absolutize_alo_url(path: str) -> str:
    path = path.split("#")[0]
    if path.startswith("http"):
        return path
    return "https://www.alo.bg" + path


def absolutize_imot_url(path: str) -> str:
    path = path.split("#")[0]
    if path.startswith("http"):
        return path
    if path.startswith("//"):
        return "https:" + path
    if path.startswith("/"):
        return "https://www.imot.bg" + path
    return "https://www.imot.bg/" + path


def is_office_relevant(title: str, snippet: str) -> bool:
    blob = f"{title} {snippet}".lower()
    if not PLOVDIV_RE.search(blob):
        return False
    if OFFICE_HINT_RE.search(blob):
        return True
    exclude = re.compile(
        r"маникюр|салон за красота|палачинк|бургер|пица|бърза закуска|фризьор", re.I
    )
    if exclude.search(blob) and not re.search(r"офис", blob, re.I):
        return False
    return True


def reject_listing(row: dict) -> bool:
    url = (row.get("url") or "").lower()
    if EXCLUDED_PATH_RE.search(url):
        return True
    blob = f"{row.get('title', '')} {row.get('snippet', '')}".lower()
    if EXCLUDED_TEXT_RE.search(blob) and not re.search(r"\bофис\b", blob[:120]):
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
        src = (row.get("source") or "").lower()
        if "imot" in src:
            row["url"] = absolutize_imot_url(row["url"])
        else:
            row["url"] = absolutize_alo_url(row["url"])
    return None if reject_listing(row) else row


def fits_criteria(row: dict, max_eur: int) -> bool:
    price = row.get("priceEur")
    if price is not None and price > max_eur:
        return False
    return True


def merge_listings(*groups: list[dict]) -> list[dict]:
    by_key: dict[str, dict] = {}
    for group in groups:
        for row in group:
            url = row.get("url") or ""
            url_key = re.sub(r"[^a-z0-9]", "", url.lower())[-24:]
            title_key = re.sub(r"[^a-z0-9]", "", (row.get("title") or "").lower())[:40]
            price = row.get("priceEur")
            sqm = row.get("sqm")
            key = url_key or f"{row.get('source')}|{price}|{sqm}|{title_key}"
            existing = by_key.get(key)
            if not existing:
                by_key[key] = row
                continue

            def score(r: dict) -> int:
                return (
                    (4 if r.get("url") else 0)
                    + (2 if r.get("location") else 0)
                    + (1 if r.get("priceEur") is not None else 0)
                    + len(r.get("title") or "")
                )

            if score(row) > score(existing):
                by_key[key] = row
    return list(by_key.values())


def parse_alo_page(html: str) -> list[dict]:
    """Parse one alo.bg results page (category or search)."""
    listings: list[dict] = []
    blocks = re.split(r'id="adrows_(\d+)"', html)
    for i in range(1, len(blocks), 2):
        block = f'id="adrows_{blocks[i]}' + (blocks[i + 1][:12000] if i + 1 < len(blocks) else "")
        if not PLOVDIV_RE.search(block) and "Пловдив" not in block:
            continue

        path_m = re.search(r'href="(/[^"]+-\d{5,})"', block) or re.search(
            r"window\.location='([^']+)'", block
        )
        if not path_m:
            continue
        path = path_m.group(1).split("#")[0]
        if EXCLUDED_PATH_RE.search(path):
            continue

        title_m = re.search(r'list(?:vip|top)-item-title[^>]*>([^<]+)<', block) or re.search(
            r'title="([^"]+)"', block
        )
        title = clean_title(title_m.group(1) if title_m else "Office listing")
        snippet = re.sub(r"<[^>]+>", " ", block)
        snippet = re.sub(r"\s+", " ", snippet).strip()[:400]

        if not is_office_relevant(title, snippet):
            continue

        price = parse_eur(block)
        sqm = parse_sqm(block)
        location = parse_location(block)
        listings.append(
            {
                "title": title,
                "priceEur": price,
                "sqm": sqm,
                "pricePerSqm": round(price / sqm, 2) if price and sqm else None,
                "location": location,
                "url": absolutize_alo_url(path),
                "source": "alo.bg",
                "snippet": snippet,
            }
        )
    return listings


def alo_page_url(base_url: str, page: int) -> str:
    if page <= 1:
        return base_url
    sep = "&" if "?" in base_url else "?"
    return f"{base_url}{sep}page={page}"


def discover_alo_last_page(html: str) -> int:
    pages = [int(p) for p in re.findall(r"page=(\d+)", html)]
    return max(pages) if pages else 1


def fetch_alo_source(base_url: str) -> tuple[list[dict], list[str]]:
    listings: list[dict] = []
    errors: list[str] = []
    seen_ids: set[str] = set()
    last_page_hint = 1

    page = 1
    while page <= max(last_page_hint, 1) + 2:
        url = alo_page_url(base_url, page)
        try:
            html = fetch_html(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            if page == 1:
                errors.append(f"{url}: {exc}")
            break
        if page == 1:
            last_page_hint = discover_alo_last_page(html)

        page_ids = set(re.findall(r'id="adrows_(\d+)"', html))
        if not page_ids:
            break
        new_ids = page_ids - seen_ids
        if not new_ids and page > 1:
            break
        seen_ids |= page_ids
        listings.extend(parse_alo_page(html))

        if page >= last_page_hint and not new_ids:
            break
        page += 1
        time.sleep(FETCH_DELAY_SEC)

    return listings, errors


def title_from_imot_slug(slug: str) -> str:
    part = slug.split("-grad-plovdiv-")[-1] if "-grad-plovdiv-" in slug else slug
    part = re.sub(r"^dava-pod-naem-ofis-", "", part, flags=re.I)
    return clean_title(part.replace("-", " "))


def parse_imot_page(html: str) -> list[dict]:
    listings: list[dict] = []
    slugs = list(dict.fromkeys(IMOT_OFFICE_SLUG_RE.findall(html)))
    for slug in slugs:
        idx = html.find(slug)
        if idx < 0:
            continue
        block = html[idx : idx + 2800]
        text = re.sub(r"<[^>]+>", " ", block)
        text = re.sub(r"\s+", " ", text)

        price = parse_eur(text)
        sqm = parse_sqm(text)
        title = title_from_imot_slug(slug)
        location = parse_location(slug + " " + text)
        listings.append(
            {
                "title": title,
                "priceEur": price,
                "sqm": sqm,
                "pricePerSqm": round(price / sqm, 2) if price and sqm else None,
                "location": location,
                "url": absolutize_imot_url(slug),
                "source": "imot.bg",
                "snippet": text[:400].strip(),
            }
        )
    return listings


def imot_page_url(base_url: str, page: int) -> str:
    if page <= 1:
        return base_url
    return base_url.rstrip("/") + f"/p-{page}"


def discover_imot_last_page(html: str, base_url: str) -> int:
    pages = [1]
    prefix = base_url.rstrip("/")
    for m in re.finditer(rf'href="(?:https:)?//www\.imot\.bg{re.escape(prefix)}/p-(\d+)"', html):
        pages.append(int(m.group(1)))
    for m in re.finditer(rf'href="{re.escape(prefix)}/p-(\d+)"', html):
        pages.append(int(m.group(1)))
    return max(pages) if pages else 1


def fetch_imot_source(base_url: str) -> tuple[list[dict], list[str]]:
    listings: list[dict] = []
    errors: list[str] = []
    seen_slugs: set[str] = set()
    last_page_hint = 1

    page = 1
    while page <= max(last_page_hint, 1) + 1:
        url = imot_page_url(base_url, page)
        try:
            html = fetch_html(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
            if page == 1:
                errors.append(f"{url}: {exc}")
            break
        if page == 1:
            last_page_hint = discover_imot_last_page(html, base_url)

        slugs = set(IMOT_OFFICE_SLUG_RE.findall(html))
        if not slugs:
            break
        new_slugs = slugs - seen_slugs
        if not new_slugs and page > 1:
            break
        seen_slugs |= slugs
        listings.extend(parse_imot_page(html))

        if page >= last_page_hint and not new_slugs:
            break
        page += 1
        time.sleep(FETCH_DELAY_SEC)

    return listings, errors


def filter_by_budget(listings: list[dict], max_eur: int) -> tuple[list[dict], list[dict]]:
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
    all_raw: list[dict] = []
    errors: list[str] = []
    scrape_stats: dict[str, dict[str, int]] = {}

    for source_name, url in SEARCH_SOURCES:
        if source_name == "imot.bg":
            rows, src_errors = fetch_imot_source(url)
        else:
            rows, src_errors = fetch_alo_source(url)
        errors.extend(src_errors)
        scrape_stats[url] = {"scraped": len(rows)}
        all_raw.extend(rows)
        time.sleep(FETCH_DELAY_SEC)

    normalized = [
        r for r in (normalize_listing(r) for r in merge_listings(all_raw)) if r
    ]
    matching = [r for r in normalized if fits_criteria(r, MAX_EUR)]
    within, unknown_price = filter_by_budget(matching, MAX_EUR)

    listings = sorted(
        matching,
        key=lambda x: (
            x["priceEur"] if x.get("priceEur") is not None else 99999,
            -(x.get("sqm") or 0),
        ),
    )

    ok = bool(listings)
    if not listings:
        listings = [dict(x) for x in MANUAL_SAMPLES]
        ok = False

    payload = {
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "maxBudgetEur": MAX_EUR,
        "city": "Plovdiv",
        "searchUrls": [u for _, u in SEARCH_SOURCES],
        "alsoCheck": [
            {
                "label": "imot.bg — Plovdiv offices (rent)",
                "url": IMOT_OFFICES,
            },
            {
                "label": "alo.bg — offices Plovdiv",
                "url": ALO_CATEGORY,
            },
            {
                "label": "alo.bg — search",
                "url": ALO_SEARCH,
            },
        ],
        "ok": ok,
        "scrapeErrors": errors,
        "scrapeStats": scrape_stats,
        "includesManualSamples": not ok,
        "count": len(listings),
        "countWithinBudget": len(within),
        "countUnknownPrice": len(unknown_price),
        "listings": listings,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUTPUT.relative_to(ROOT)} ({len(listings)} listings, "
        f"{len(within)} priced ≤{MAX_EUR} EUR, {len(unknown_price)} unknown price)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
