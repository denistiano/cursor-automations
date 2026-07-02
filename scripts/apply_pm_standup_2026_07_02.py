#!/usr/bin/env python3
"""PM standup 2026-07-02 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-02"


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
            "Agent: Office re-rank (440 listings, 284 candidates) → data/office-top40.md",
            "Agent: URL check + scrape gap (Kapana 11108782 live, missing from JSON) → planning/office-url-check-2026-07-02.md",
            "Agent: PO publish readiness (day 27) → planning/po-publish-readiness-2026-07-02.md",
            "Agent: Brand sprint catch-up (10 days overdue) → planning/brand-sprint-catchup-2026-07-02.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-02.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 27)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — 10 days overdue)",
            "Denis: Office Plovdiv — revised shortlist; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 22)",
            "Denis: Landing page OR presentation deck (path tied to brand day 3)",
        ],
        "today": [
            "Denis: PO apply + channels + JD approval — planning/po-publish-readiness-2026-07-02.md",
            "Denis: Brand sprint day 1 minimum (ICP + ops) — planning/brand-sprint-catchup-2026-07-02.md",
            "Denis: Office — pick 3 from planning/office-url-check-2026-07-02.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 → input-task-brand-sprint-day-*",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md (brand day 3 path)",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 1 → merge ICP into business/plan",
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
