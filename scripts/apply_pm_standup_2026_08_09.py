#!/usr/bin/env python3
"""PM standup 2026-08-09 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-09"


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
            "Agent: Re-ranked office listings (319 scraped, 236 candidates) → data/office-top40.md",
            "Agent: Office shortlist refresh — June picks stale → planning/office-shortlist-refresh-2026-08-09.md",
            "Agent: PM standup + Denis action pack → planning/denis-action-pack-2026-08-09.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 60)",
            "Denis: Office Plovdiv — pick 3 from revised shortlist (old Kapana #1 delisted)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 60)",
            "Denis: Brand sprint day 1 — positioning & secret sauce (day 51 overdue)",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-08-09.md",
            "Denis: HQ Inbox batch — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand sprint day 1 still open → planning/brand-sprint-2026-06-19.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ + landlord outreach",
            "After path choice → landing scaffold OR deck export",
            "After brand day 1 reply → unlock days 2–4 + merge marketing plan draft",
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
