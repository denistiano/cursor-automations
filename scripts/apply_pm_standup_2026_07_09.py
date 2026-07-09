#!/usr/bin/env python3
"""PM standup 2026-07-09 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-09"


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
            "Agent: Office re-rank (1253 listings) → data/office-top40.md; Kapana 11108782 still #1 location",
            "Agent: URL check A/B/C shortlist all HTTP 200 → planning/office-url-check-2026-07-09.md",
            "Agent: Stalled-item briefs (PO day 34, brand +17d, inbox day 29) → planning/po-publish-readiness-2026-07-09.md, brand-sprint-catchup-2026-07-09.md",
            "Agent: Denis action pack refresh → planning/denis-action-pack-2026-07-09.md",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–4 — 17 days overdue; draft plan ready",
            "Denis: PO apply + channels — no reply since 2026-06-05 (day 34); jobs/product-owner body empty",
            "Denis: Office Plovdiv — shortlist A/B/C live; no landlord contact logged",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 29)",
            "Denis: Landing vs deck path not chosen; speaker notes ready",
        ],
        "today": [
            "Denis: Brand sprint day 1 (or batch all 4) — planning/brand-sprint-catchup-2026-07-09.md",
            "Denis: PO apply + JD approve — planning/po-publish-readiness-2026-07-09.md",
            "Denis: HQ Inbox batch approve — planning/denis-action-pack-2026-07-09.md",
        ],
        "blockers": [
            "Brand sprint days 1–4 unanswered → blocks marketing plan merge",
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body 0 bytes",
            "HQ Inbox: 7 approvals still open",
        ],
        "agent_next": [
            "After brand day1 → merge positioning into business/plan",
            "After PO channels + JD → careers page + LinkedIn PO post draft",
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
