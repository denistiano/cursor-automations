#!/usr/bin/env python3
"""PM standup 2026-07-26 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-26"


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
            "Agent: Office listings re-ranked (358 → 234 candidates) → data/office-top40.md",
            "Agent: Shortlist validation — 2026-06-19 picks A+B delisted → planning/office-shortlist-validation-2026-07-26.md",
            "Agent: Carryover analysis (37-day gap) → planning/carryover-analysis-2026-07-26.md",
            "Agent: Denis batch agent prompt → planning/denis-agent-prompt-2026-07-26.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 51)",
            "Denis: Office Plovdiv — revised shortlist ready; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 37)",
            "Denis: Landing page OR presentation deck (path not chosen — day 51)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD)",
            "Denis: Office — pick 3 from planning/office-shortlist-validation-2026-07-26.md",
            "Denis: HQ Inbox batch approve",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office → 2026-06-19 picks A+B delisted; use revised shortlist",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table + landlord outreach",
            "After HQ inbox batch → run approved automations; refresh social drafts",
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
