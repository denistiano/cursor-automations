#!/usr/bin/env python3
"""PM standup 2026-07-16 — upsert standup after 27-day gap since 2026-06-19."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-16"


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
            "Agent: Office re-scrape (1295 listings, +28 vs 2026-06-19) + re-rank → data/office-top40.md",
            "Agent: Kapana 11108782 still #1 location @ €400/mo — shortlist A/B/C unchanged",
            "Agent: PM standup 2026-07-16 + carryover analysis for 3 stalled Denis items",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–4 — started 2026-06-19, no replies (day 27)",
            "Denis: PO apply method + publish channel — no reply since 2026-06-05 (day 41)",
            "Denis: Office Plovdiv — pick 3 visits from planning/office-shortlist-refresh-2026-06-19.md",
            "Denis: HQ Inbox — 4 automations + 3 social drafts still open (day 37)",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops model (unblocks all marketing)",
            "Denis: PO apply + channels (+ approve JD in planning/po-jd-expanded-draft-2026-06-19.md)",
            "Denis: Office visits — reply A, B, C from refreshed shortlist",
        ],
        "blockers": [
            "Brand sprint incomplete — days 1–4 inbox actions still in_progress",
            "PO apply → jobs/product-owner body still 0 bytes; careers page blocked",
            "Early bird pricing deferred until Denis legal line (backlog)",
        ],
        "agent_next": [
            "After brand day1 → refine positioning in business/plan + unlock day 2 inbox",
            "After PO channels + JD → commit jobs/product-owner.md + careers scaffold",
            "After office picks → lease comparison table + landlord outreach from template",
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
