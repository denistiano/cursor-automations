#!/usr/bin/env python3
"""PM standup 2026-06-27 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-27"


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
            "Agent: Office re-rank from 2026-06-22 scrape (1264 listings) → data/office-top40.md",
            "Agent: Shortlist URL check — A/B/C live → planning/office-url-check-2026-06-27.md",
            "Agent: PO publish readiness → planning/po-publish-readiness-2026-06-27.md",
            "Agent: Brand sprint catch-up → planning/brand-sprint-catchup-2026-06-27.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-27.md",
        ],
        "ongoing": [
            "Denis: PO apply + JD — no reply since 2026-06-05 (day 22); jobs/product-owner empty",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22; all inbox actions in_progress",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 17)",
            "Denis: Office — 3 picks verified; contact landlords + schedule visits",
            "Denis: Landing vs deck path — tied to brand day 3",
        ],
        "today": [
            "Denis: PO apply + approve expanded JD (planning/po-publish-readiness-2026-06-27.md)",
            "Denis: Brand sprint day 1 or catch-up batch (planning/brand-sprint-catchup-2026-06-27.md)",
            "Denis: HQ Inbox — LinkedIn bio + first post + standup automation",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels (day 22)",
            "Brand sprint days 1–4 unanswered — blocks marketing plan sign-off",
            "HQ Inbox 7 approvals — blocks automations + social account creation",
        ],
        "agent_next": [
            "After PO channels + JD → business/jobs/product-owner.md + careers scaffold",
            "After brand day 1 → merge positioning into business/plan",
            "After office picks → lease comparison table in HQ",
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
