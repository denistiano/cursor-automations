#!/usr/bin/env python3
"""PM standup 2026-07-28 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-28"


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
            "Agent: Office re-scrape (1274 listings) + re-rank → data/office-top40.md",
            "Agent: Shortlist validation — A/B/C still listed; alt Kapana delisted → planning/office-shortlist-validation-2026-07-28.md",
            "Agent: Carryover analysis (39-day gap) → planning/carryover-analysis-2026-07-28.md",
            "Agent: Denis batch agent prompt → planning/denis-agent-prompt-2026-07-28.md",
        ],
        "ongoing": [
            "Denis: PO apply + JD approve — no reply since 2026-06-10 (day 48); jobs/product-owner empty",
            "Denis: Office Plovdiv — A/B/C valid; pick 3 + contact landlords",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts still open",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD (planning/po-jd-expanded-draft-2026-06-19.md)",
            "Denis: Office — confirm visits 11108782, 10481212, 4734755",
            "Denis: HQ Inbox batch approve (planning/hq-inbox-unlocks-2026-06-19.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 → all input actions in_progress since 2026-06-19",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After path choice → landing scaffold OR deck export",
            "After brand day1 → refine positioning in business/plan",
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
