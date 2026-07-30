#!/usr/bin/env python3
"""PM standup 2026-07-30 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-30"


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
            "Agent: Re-ranked office listings (1268 scraped 2026-07-27) → data/office-top40.md",
            "Agent: Validated shortlist A/B/C; alternate 10915009 delisted → planning/office-shortlist-validation-2026-07-30.md",
            "Agent: Carryover analysis → planning/carryover-analysis-2026-07-30.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-30.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 55)",
            "Denis: Office Plovdiv — A/B/C validated; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 50+)",
            "Denis: Landing page OR presentation deck — path not chosen",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD at planning/po-jd-expanded-draft-2026-06-19.md)",
            "Denis: Office — confirm visits A/B/C (planning/office-shortlist-validation-2026-07-30.md)",
            "Denis: HQ Inbox batch approve (planning/hq-inbox-unlocks-2026-06-19.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand sprint days 1–4 → HQ Inbox brand day templates",
        ],
        "agent_next": [
            "After PO channels + JD approved → business/jobs/product-owner.md + careers scaffold + LinkedIn draft",
            "After office picks → lease comparison table in HQ",
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
