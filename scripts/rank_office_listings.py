#!/usr/bin/env python3
"""Attach ranked top-10 lists to data/office-listings.json (with optional detail enrichment)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTINGS_PATH = ROOT / "data" / "office-listings.json"
REPORT_PATH = ROOT / "data" / "office-top40.md"

sys.path.insert(0, str(ROOT / "scripts"))
from office_ranking import (  # noqa: E402
    build_rankings,
    collect_urls_for_detail_enrichment,
    enrich_listing,
    is_candidate,
    top_n,
)
from office_enrich_details import enrich_listings  # noqa: E402


def provisional_rankings(listings: list[dict]) -> dict[str, list[dict]]:
    return {
        "luxury": top_n(listings, "luxury"),
        "location": top_n(listings, "location"),
        "price": top_n(listings, "priceValue"),
        "overall": top_n(listings, "overall"),
    }


def write_top40_report(payload: dict) -> None:
    top10 = payload.get("rankings", {}).get("top10", {})
    labels = {
        "overall": "Overall (training + location + amenities + value)",
        "location": "Best location (Kapana / center)",
        "luxury": "Most luxurious",
        "price": "Best price (usable m² per euro)",
    }
    lines = [
        "# Plovdiv office — top 10 × 4 (40 suggestions)",
        "",
        f"Generated: {payload.get('generatedAt', '—')}",
        f"Listings scraped: {payload.get('count', '—')} | "
        f"Candidates ≥40 m²: {payload.get('rankings', {}).get('criteria', {}).get('candidateCount', '—')}",
        "",
        "Amenity bonus: kitchen and/or leisure room explicitly mentioned in listing text.",
        "",
    ]
    for key, heading in labels.items():
        rows = top10.get(key) or []
        lines.append(f"## {heading}")
        lines.append("")
        if not rows:
            lines.append("_No matches._")
            lines.append("")
            continue
        for row in rows:
            lines.append(format_report_row(row, key))
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def format_report_row(row: dict, category: str) -> str:
    rank = row.get("rank", "?")
    title = (row.get("title") or "Listing").replace("|", "/")
    url = row.get("url") or ""
    price = row.get("priceEur")
    sqm = row.get("sqm")
    loc = row.get("location") or "Plovdiv"
    price_s = f"€{price}/mo" if price is not None else "price TBD"
    sqm_s = f"{sqm} m²" if sqm else "m² TBD"
    score_key = "priceValue" if category == "price" else category
    score = row.get("scores", {}).get(score_key)
    score_s = f" · score {score:.2f}" if score is not None else ""
    perks: list[str] = []
    am = row.get("amenities") or {}
    if am.get("hasKitchen"):
        perks.append("kitchen")
    if am.get("hasLeisureRoom"):
        perks.append("leisure room")
    perk_s = f" · **{' + '.join(perks)}**" if perks else ""
    budget = "" if row.get("withinSoftBudget", True) else " · *over €800*"
    link = f"[{title}]({url})" if url else title
    return f"{rank}. {link} — {price_s}, {sqm_s}, {loc}{score_s}{perk_s}{budget}"


def main() -> int:
    if not LISTINGS_PATH.exists():
        print(f"Missing {LISTINGS_PATH} — run scripts/fetch_office_listings.py first", file=sys.stderr)
        return 1

    payload = json.loads(LISTINGS_PATH.read_text(encoding="utf-8"))
    listings = payload.get("listings") or []

    first_pass = provisional_rankings(listings)
    detail_urls = collect_urls_for_detail_enrichment(first_pass)
    if detail_urls:
        try:
            from fetch_office_listings import fetch_html

            print(f"Enriching {len(detail_urls)} listing detail pages for amenity keywords…")
            listings = enrich_listings(listings, fetch_html, urls=set(detail_urls), limit=len(detail_urls))
            payload["detailEnrichedCount"] = sum(1 for r in listings if r.get("detailEnriched"))
        except ImportError as exc:
            print(f"Detail enrichment skipped: {exc}", file=sys.stderr)

    payload["listings"] = [
        enrich_listing(r) if is_candidate(r) else r for r in listings
    ]
    payload["rankings"] = build_rankings(listings)
    write_top40_report(payload)

    LISTINGS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    top = payload["rankings"]["top10"]
    unique = payload["rankings"]["criteria"].get("top10UniqueUrls", "?")
    print(
        f"Ranked {payload['rankings']['criteria']['candidateCount']} candidates → "
        f"40 picks ({unique} unique URLs) → {REPORT_PATH.relative_to(ROOT)}"
    )
    for key in ("overall", "location", "luxury", "price"):
        print(f"  {key}: {len(top[key])} listings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
