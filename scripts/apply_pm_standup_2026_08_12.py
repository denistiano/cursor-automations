#!/usr/bin/env python3
"""PM standup 2026-08-12 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-12"


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
            "Agent: Office re-scrape (135 listings — degraded vs 1315 on 2026-08-11) + re-rank → data/office-top40.md",
            "Agent: A′/B′/C revalidated + backups D/E/F → planning/office-shortlist-refresh-2026-08-12.md",
            "Agent: Carryover analysis → planning/carryover-analysis-2026-08-12.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-08-12.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 68)",
            "Denis: Office Plovdiv — A′/B′/C still live; pick 3 + contact landlords",
            "Denis: Brand sprint days 1–4 unanswered (day 54)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 63)",
            "Denis: Landing page OR presentation deck (path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels + JD approve",
            "Denis: Office — confirm A′/B′/C from planning/office-shortlist-refresh-2026-08-12.md",
            "Denis: HQ Inbox batch — 7 approvals (planning/hq-inbox-unlocks-2026-06-19.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint day 1 → input-task-brand-sprint-day-1-positioning-secret-sauce-hq-brand-sprint",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ + landlord outreach",
            "After brand day 1 → unblock days 2–4 + merge marketing plan",
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
