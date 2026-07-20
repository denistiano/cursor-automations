#!/usr/bin/env python3
"""PM standup 2026-07-20 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-20"


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
            "Agent: Office re-scrape (1293 listings) + re-rank → data/office-top40.md",
            "Agent: A/B/C shortlist re-validated → planning/office-shortlist-refresh-2026-07-20.md",
            "Agent: Carryover analysis (31d gap) → planning/carryover-analysis-2026-07-20.md",
            "Agent: Brand day 1 starter → planning/brand-day1-starter-2026-07-20.md",
            "Agent: Denis batch agent prompt → planning/denis-agent-prompt-2026-07-20.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 45)",
            "Denis: Office Plovdiv — A/B/C re-validated; landlord outreach not started",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 40+)",
            "Denis: Landing page OR presentation deck (path not chosen)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD)",
            "Denis: Office — confirm A/B/C + send landlord messages",
            "Denis: HQ Inbox batch — 7 approvals",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand day 1 → planning/brand-day1-starter-2026-07-20.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks + quotes → lease comparison table in HQ",
            "After path choice → landing scaffold OR deck export",
            "After brand day 1 → merge into brand marketing plan draft",
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
