#!/usr/bin/env python3
"""PM standup 2026-06-09 — upsert standup after listings refresh + planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-09"


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
            "Agent: Re-ranked offices (329 scraped → 236 candidates) → data/office-top40.md",
            "Agent: Visit shortlist update → planning/office-visit-shortlist-2026-06-09.md",
            "Agent: PO JD draft scaffold (DRAFT) → planning/po-jd-draft-scaffold.md",
            "Agent: Landing vs deck brief → planning/landing-vs-deck-brief.md",
        ],
        "ongoing": [
            "Denis: PO apply method + channels (no reply since 2026-06-05; JD empty in hq.db)",
            "Denis: Office Plovdiv — updated shortlist; 3 prior Kapana picks delisted",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck (brief ready)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve/edit JD scaffold)",
            "Denis: Office — confirm picks from office-visit-shortlist-2026-06-09.md",
            "Denis: HQ Inbox — approve social copy + automations",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-brief.md",
        ],
        "agent_next": [
            "After PO channels + approved JD → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "Landing/waitlist scaffold in web/ when Denis picks landing-first or hybrid",
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
