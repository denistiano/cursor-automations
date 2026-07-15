#!/usr/bin/env python3
"""PM standup 2026-07-15 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-15"


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
            "Agent: Office re-rank (1288 listings, 753 candidates) → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-07-15.md",
            "Agent: Brand sprint day 1 brief → planning/brand-sprint-day1-decision-brief-2026-07-15.md",
            "Agent: PO publish checklist → planning/po-publish-checklist-2026-07-15.md",
            "Agent: HQ Inbox impact + landing path pack + Denis batch prompt",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 35)",
            "Denis: Office Plovdiv — A/B/C verified; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 35)",
            "Denis: Brand sprint days 1–4 unanswered (+23 days since sprint ended)",
            "Denis: Landing page OR presentation deck — path not chosen (day 40)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint day 1 (or defaults OK in brief)",
            "Denis: HQ Inbox batch approve + office visit picks A/B/C",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; business/jobs/product-owner.md missing",
            "Brand day 1 → input-task-brand-sprint-day-1; sprint +23 days overdue",
            "Landing vs deck → planning/landing-path-decision-pack-2026-07-15.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 1 → merge positioning into business/plan + social CTAs",
            "After office picks → landlord outreach + lease comparison table",
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
