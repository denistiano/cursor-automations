#!/usr/bin/env python3
"""PM standup 2026-08-19 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-19"


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
            "Agent: Office re-rank (281 listings, 205 candidates) → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-08-19.md (Jun A/B delisted)",
            "Agent: Brand sprint day 1 prefill → planning/brand-sprint-day1-prefill-2026-08-19.md",
            "Agent: Scheduled standup entry (2026-08-19)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 75)",
            "Denis: Brand sprint days 1–4 unanswered (since 2026-06-19 — day 61)",
            "Denis: Office Plovdiv — Jun shortlist stale; revised picks ready",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck (path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-08-19.md",
            "Denis: Brand sprint day 1 — edit prefill in planning/brand-sprint-day1-prefill-2026-08-19.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 → marketing plan blocked",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD → business/jobs/product-owner.md, careers scaffold, LinkedIn draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → refine business/plan positioning; prompt day 2",
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
