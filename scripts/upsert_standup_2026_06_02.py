#!/usr/bin/env python3
"""Upsert 2026-06-02 standup into hq.db (cron PM run)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-02"
BODY_PATH = Path(__file__).resolve().parent.parent / "planning" / "standups" / f"{STANDUP_DATE}.md"


def main() -> None:
    init_db()
    body = BODY_PATH.read_text(encoding="utf-8") if BODY_PATH.exists() else ""
    with connect() as conn:
        entry_id = upsert_entry(
            conn,
            "standups",
            STANDUP_DATE,
            f"Standup — {STANDUP_DATE}",
            body=body,
            props={"date": STANDUP_DATE},
        )
        sections = {
            "done": [
                "Office listings refreshed under 800 EUR (data/office-listings.json, 2026-06-01)",
                "No other merged repo work since 2026-05-29 standup",
            ],
            "ongoing": [
                "Denis: PO apply method + first publish channel — in progress",
                "Denis: #1 Office Plovdiv — budget/area; visit shortlist",
                "Denis: Landing page OR presentation document — in progress",
                "Denis: #4 Social accounts (after bios) — in progress",
                "Denis: #2 Publish PO position — blocked on apply method",
            ],
            "today": [
                "Denis: HQ Inbox — batch replies + approve 4 automations",
                "Agent: Presentation outline + slide copy (content/presentation/)",
                "Agent: Social bios + first-post pack (content/social/)",
            ],
            "blockers": [
                "PO apply method + publish channel (priority 1 inbox)",
            ],
            "agent_next": [
                "After automation approvals → competitor + business plan cron runs",
                "After PO channels → careers copy + LinkedIn PO announcement",
                "Landing scaffold in web/ when Denis picks landing vs deck-first",
            ],
        }
        for section, lines in sections.items():
            replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])
        conn.commit()
    print(f"Upserted standup {STANDUP_DATE}")


if __name__ == "__main__":
    main()
