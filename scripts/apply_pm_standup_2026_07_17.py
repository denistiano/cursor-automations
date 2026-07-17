#!/usr/bin/env python3
"""PM standup 2026-07-17 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-17"


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
            "Agent: Re-ranked office top40 from data/office-listings.json (1288 listings, 2026-07-13 snapshot) → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-07-17.md (Kapana 11108782 still #1 @ €400)",
            "Agent: Carryover analysis (28d since last HQ standup) → planning/carryover-analysis-2026-07-17.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — no hq.db reply since 2026-06-10 (day 37+); jobs/product-owner body empty",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Office Plovdiv — A/B/C re-validated; pick + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts still open",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops (HQ → Brand sprint)",
            "Denis: Office — confirm A/B/C or budget update from planning/office-shortlist-refresh-2026-07-17.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; see planning/po-jd-expanded-draft-2026-06-19.md",
            "Brand plan incomplete until sprint days 1–4 answered",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → business/jobs/product-owner.md + careers scaffold",
            "After brand day1 → merge positioning into business/plan",
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
