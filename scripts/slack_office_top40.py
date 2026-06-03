#!/usr/bin/env python3
"""Print Slack-formatted top-40 office lists with links (for agent copy-paste)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTINGS_PATH = ROOT / "data" / "office-listings.json"

LABELS = {
    "overall": "Overall",
    "location": "Best location",
    "luxury": "Most luxurious",
    "price": "Best price",
}


def format_slack_row(row: dict) -> str:
    title = (row.get("title") or "Listing")[:70]
    url = row.get("url") or ""
    price = row.get("priceEur")
    sqm = row.get("sqm")
    loc = (row.get("location") or "Plovdiv")[:30]
    price_s = f"€{price}" if price is not None else "€?"
    sqm_s = f"{sqm}m²" if sqm else "?m²"
    perks = []
    am = row.get("amenities") or {}
    if am.get("hasKitchen"):
        perks.append("🍳")
    if am.get("hasLeisureRoom"):
        perks.append("☕")
    perk_s = " ".join(perks) + " " if perks else ""
    rank = row.get("rank", "?")
    if url:
        line = f"{rank}. {perk_s}<{url}|{title}> — {price_s}/mo · {sqm_s} · {loc}"
    else:
        line = f"{rank}. {perk_s}{title} — {price_s}/mo · {sqm_s} · {loc}"
    if row.get("withinSoftBudget") is False:
        line += " _(over €800)_"
    return line


def main() -> int:
    payload = json.loads(LISTINGS_PATH.read_text(encoding="utf-8"))
    top10 = payload.get("rankings", {}).get("top10", {})
    for key, label in LABELS.items():
        print(f"### {label}")
        for row in top10.get(key, []):
            print(format_slack_row(row))
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
