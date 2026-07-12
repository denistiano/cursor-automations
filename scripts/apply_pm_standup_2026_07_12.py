#!/usr/bin/env python3
"""PM standup 2026-07-12 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-12"


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
            "Agent: Office A/B/C re-verify (all 200) → planning/office-shortlist-verify-2026-07-12.md",
            "Agent: PO publish checklist → planning/po-publish-checklist-2026-07-12.md",
            "Agent: HQ Inbox impact summary → planning/hq-inbox-impact-2026-07-12.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-12.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 37)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — +20 days)",
            "Denis: Office Plovdiv — A/B/C verified; pick + contact landlords (day 27)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 32)",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: brand day1 reply — planning/brand-sprint-day1-decision-brief-2026-07-11.md",
            "Denis: PO apply + JD approve — planning/po-publish-checklist-2026-07-12.md",
            "Denis: HQ Inbox batch + Office visits A,B,C — planning/denis-agent-prompt-2026-07-12.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand day 1 → input-task-brand-sprint-day-1-positioning-secret-sauce-hq-brand-sprint",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO + brand day1 → careers page + LinkedIn PO draft + brand plan merge",
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
