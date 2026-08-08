#!/usr/bin/env python3
"""PM standup 2026-08-08 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-08"


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
            "Agent: Re-validated office A′/B′/C still in scrape (2026-08-03 data)",
            "Agent: Carryover analysis (1d; PO day 64) → planning/carryover-analysis-2026-08-08.md",
            "Agent: Denis agent prompt pack → planning/denis-agent-prompt-2026-08-08.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 64)",
            "Denis: Office Plovdiv — pick 3 from revised shortlist (A′/B′/C)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 59+)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Landing page OR presentation deck (path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from data/office-top40.md (A′/B′/C)",
            "Denis: HQ Inbox — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office — previous Kapana pick 11108782 removed; A′/B′/C still listed",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After inbox approvals → remind Denis task #4 create social accounts",
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
