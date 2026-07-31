#!/usr/bin/env python3
"""PM standup 2026-06-21 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-21"


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
            "Agent: Office URL re-check — 3 picks live → planning/office-url-check-2026-06-21.md",
            "Agent: PO publish readiness (day 16) → planning/po-publish-readiness-2026-06-21.md",
            "Agent: Brand sprint day 3 prep → planning/brand-sprint-day3-prep-2026-06-21.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-21.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 16)",
            "Denis: Office Plovdiv — shortlist verified; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 11)",
            "Denis: Brand sprint — days 1–2 skipped; day 3 due today",
            "Denis: Landing page OR presentation deck (path tied to brand day 3)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint day 3 (+ optional catch-up days 1–2)",
            "Denis: HQ Inbox batch approve (7 items)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand day 3 → input-task-brand-sprint-day-3-channels-facebook-strategy-deck-landing-p",
            "Office picks → input-task-1-office-plovdiv-budget-area-constraints-visit-shortlist",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 3 (+ path) → merge brand plan + landing/deck scaffold",
            "After office picks → lease comparison table in HQ",
            "After HQ Inbox approvals → scheduled automations can run",
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
