#!/usr/bin/env python3
"""Attach ranked top-10 lists to data/office-listings.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTINGS_PATH = ROOT / "data" / "office-listings.json"

sys.path.insert(0, str(ROOT / "scripts"))
from office_ranking import build_rankings  # noqa: E402


def main() -> int:
    if not LISTINGS_PATH.exists():
        print(f"Missing {LISTINGS_PATH} — run scripts/fetch_office_listings.py first", file=sys.stderr)
        return 1

    from office_ranking import enrich_listing, is_candidate

    payload = json.loads(LISTINGS_PATH.read_text(encoding="utf-8"))
    listings = payload.get("listings") or []
    payload["listings"] = [
        enrich_listing(r) if is_candidate(r) else r for r in listings
    ]
    payload["rankings"] = build_rankings(listings)
    LISTINGS_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    top = payload["rankings"]["top10"]
    print(
        f"Ranked {payload['rankings']['criteria']['candidateCount']} candidates → "
        f"overall {len(top['overall'])}, luxury {len(top['luxury'])}, "
        f"location {len(top['location'])}, price {len(top['price'])}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
