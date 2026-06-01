#!/usr/bin/env python3
"""PM standup 2026-06-01 — upsert standup sections in hq.db."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-01"


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
            "_(none on master since 2026-05-29 — no merged repo commits)_",
            "Scheduled: Morning standup prep automation ran (cron 04:00 UTC)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — in progress",
            "Denis: #1 Office Plovdiv — budget/area constraints; visit shortlist (689 listings in HQ)",
            "Denis: Landing page on vibe-coders.academy OR presentation document — in progress",
            "Denis: #4 Create social accounts (after name + bios approved) — in progress",
        ],
        "today": [
            "Agent: Presentation outline + slide copy (content/presentation/) — open since 2026-05-29",
            "Denis: HQ Inbox — approve automations + reply PO apply blocker (P1)",
            "Agent: Social page bios + first-post pack (draft)",
        ],
        "blockers": [
            "PO apply: How candidates apply + where to publish first → input-blocker-po-apply-method-publish-channels",
        ],
        "agent_next": [
            "Ship presentation outline + social bios (Today)",
            "After PO channels → careers page copy + LinkedIn announcement draft",
            "Office: Monday scrape may refresh data/office-listings.json",
            "Public landing scaffold in web/ when Denis picks landing vs deck-first",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        conn.commit()
    print(f"Standup {STANDUP_DATE} applied")


if __name__ == "__main__":
    main()
