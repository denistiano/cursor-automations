#!/usr/bin/env python3
"""PM standup 2026-08-15 — upsert standup entry in hq.db."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-15"


def upsert_standup(conn) -> None:
    entry_id = upsert_entry(
        conn,
        "standups",
        STANDUP_DATE,
        f"Standup — {STANDUP_DATE}",
        props={"date": STANDUP_DATE},
    )
    sections = {
        "done": [
            "Agent: Re-ran office ranking → data/office-top40.md (231 listings, 175 ≥40 m²)",
            "Agent: Verified Aug 13 office picks A/B/C still in top rankings",
            "Agent: Brand sprint day 1 pre-fill → planning/brand-sprint-day1-prefill-2026-08-15.md",
            "Agent: PM standup 2026-08-15 + stalled-item analysis",
        ],
        "ongoing": [
            "Denis: PO apply + JD — jobs/product-owner body 0 bytes (day 71)",
            "Denis: Brand sprint days 1–4 — never answered",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Office Plovdiv — Aug 13 picks valid; no visit confirmations",
            "Denis: Landing vs deck path not chosen",
            "Denis: Social accounts — blocked on bio approvals",
        ],
        "today": [
            "Denis: Brand sprint day 1 — edit + send pre-fill",
            "Denis: PO apply + channels + approve JD",
            "Denis: Office — confirm A/B/C from Aug 13 shortlist",
        ],
        "blockers": [
            "Brand plan incomplete until sprint days 1–4 answered",
            "PO careers page blocked until apply method + JD approved",
            "Early bird pricing deferred until Denis legal line",
        ],
        "agent_next": [
            "After brand day1 → merge into business/plan + unlock days 2–4",
            "After PO channels + JD → business/jobs/product-owner.md + careers scaffold",
            "After office picks → lease comparison table in HQ",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
