#!/usr/bin/env python3
"""PM standup 2026-07-27 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-27"


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
            "Agent: Office shortlist validation vs 2026-07-20 scrape → planning/office-shortlist-validation-2026-07-27.md",
            "Agent: Carryover analysis (38-day gap) → planning/carryover-analysis-2026-07-27.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-27.md",
            "Repo: Automated office listing refreshes continue (scrape in JSON: 2026-07-20)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 52)",
            "Denis: Office Plovdiv — old picks delisted; revised shortlist ready",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 52)",
            "Denis: Landing page OR presentation deck — path not chosen",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Office — pick 3 from planning/office-shortlist-validation-2026-07-27.md",
            "Denis: HQ Inbox batch (planning/denis-action-pack-2026-06-19.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office → 3/4 prior picks delisted; revised IDs 11078372, 11063950, 4734755",
            "Brand sprint → days 1–4 input actions open",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After path choice → landing scaffold OR deck export",
            "After brand sprint replies → merge into brand-marketing-plan draft",
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
