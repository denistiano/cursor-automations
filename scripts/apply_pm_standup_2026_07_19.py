#!/usr/bin/env python3
"""PM standup 2026-07-19 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-19"


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
            "Agent: Office re-scrape (1295 listings) + re-rank → data/office-top40.md",
            "Agent: Office shortlist re-validated → planning/office-shortlist-refresh-2026-07-19.md",
            "Agent: Carryover analysis → planning/carryover-analysis-2026-07-19.md",
            "Agent: Brand day 1 starter → planning/brand-day1-starter-2026-07-19.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-19.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 39+)",
            "Denis: Office Plovdiv — picks A/B/C re-validated; contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels + JD approval",
            "Denis: Office — confirm A/B/C from planning/office-shortlist-refresh-2026-07-19.md",
            "Denis: Brand day 1 (15 min) OR batch via planning/denis-agent-prompt-2026-07-19.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "HQ Inbox → planning/hq-inbox-unlocks-2026-06-19.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → business/messaging + social CTA alignment",
            "After path choice → landing scaffold OR deck export",
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
