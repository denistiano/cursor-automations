#!/usr/bin/env python3
"""PM standup 2026-07-10 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-10"


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
            "Agent: Office re-rank on 2026-07-06 scrape (1253 listings) → data/office-top40.md",
            "Agent: Office shortlist verification → planning/office-shortlist-refresh-2026-07-10.md (A/B/C still valid)",
            "Agent: Brand sprint day 1 decision brief → planning/brand-sprint-day1-decision-brief-2026-07-10.md",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–4 — no replies since 2026-06-19 (day 21)",
            "Denis: PO apply method + channels — no reply since 2026-06-05 (day 35); jobs/product-owner empty",
            "Denis: Office Plovdiv — shortlist ready; pick 3 visits",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 30+)",
            "Denis: Landing page OR deck — path not chosen",
        ],
        "today": [
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops (planning/brand-sprint-day1-decision-brief-2026-07-10.md)",
            "Denis: PO apply + channels + approve expanded JD (planning/po-jd-expanded-draft-2026-06-19.md)",
            "Denis: Office — confirm visits A/B/C (planning/office-shortlist-refresh-2026-07-10.md)",
        ],
        "blockers": [
            "Brand sprint days 1–4 unanswered — marketing plan frozen",
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body 0 bytes",
            "HQ Inbox — 7 approvals open (planning/hq-inbox-unlocks-2026-06-19.md)",
        ],
        "agent_next": [
            "After brand day1 → refine positioning in business/plan",
            "After PO channels + JD → careers page + LinkedIn announcement draft",
            "After office picks → landlord outreach from office-landlord-outreach pack",
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
