#!/usr/bin/env python3
"""PM standup 2026-08-13 — upsert standup after 55-day gap."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-13"


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
            "Agent: Re-ranked office (Aug 10 scrape, 231 listings) → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-08-13.md",
            "Agent: PM standup 2026-08-13 (55 days since 2026-06-19)",
        ],
        "ongoing": [
            "Denis: PO apply + JD — jobs/product-owner body 0 bytes (no reply since 2026-06-10)",
            "Denis: Brand sprint days 1–4 — never answered (sprint 19–22 Jun)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Office Plovdiv — no visit picks; June shortlist stale",
            "Denis: Landing vs deck path not chosen",
            "Denis: Social accounts blocked on bio approvals",
        ],
        "today": [
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops model",
            "Denis: PO apply + channels + approve JD",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-08-13.md",
        ],
        "blockers": [
            "Brand plan incomplete until sprint days 1–4 answered",
            "PO careers blocked until apply method + JD approved",
            "Early bird pricing deferred until Denis legal line",
        ],
        "agent_next": [
            "After brand day1 → refine positioning in business/plan",
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
