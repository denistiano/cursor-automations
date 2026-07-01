#!/usr/bin/env python3
"""PM standup 2026-07-01 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-01"


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
            "Agent: Office re-rank after 2026-06-29 scrape (440 listings) → data/office-top40.md",
            "Agent: URL re-check + shortlist refresh → planning/office-url-check-2026-07-01.md, office-shortlist-refresh-2026-07-01.md",
            "Agent: PO publish readiness → planning/po-publish-readiness-2026-07-01.md",
            "Agent: Brand sprint catch-up (9 days overdue) → planning/brand-sprint-catchup-2026-07-01.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-01.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 26)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — 9 days overdue)",
            "Denis: Office Plovdiv — revised shortlist; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 21)",
            "Denis: Landing page OR presentation deck (path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops model",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-07-01.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty (day 26)",
            "Brand sprint days 1–4 → planning/brand-sprint-catchup-2026-07-01.md",
            "Office Kapana 11108782 live but scrape gap — Denis confirms pick A",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 1 → refine business/plan positioning",
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
