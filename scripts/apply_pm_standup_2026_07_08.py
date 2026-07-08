#!/usr/bin/env python3
"""PM standup 2026-07-08 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-08"


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
            "Agent: Office re-scrape (1270 listings) + re-rank → data/office-top40.md",
            "Agent: Office URL check A/B/C HTTP 200 → planning/office-url-check-2026-07-08.md",
            "Agent: PO publish readiness brief (day 33) → planning/po-publish-readiness-2026-07-08.md",
            "Agent: Brand sprint catch-up guide (16 days overdue) → planning/brand-sprint-catchup-2026-07-08.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-08.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 33)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — 16 days overdue)",
            "Denis: Office Plovdiv — A/C in top40; B (10481212) live but dropped from top40",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 28)",
            "Denis: Landing page OR presentation deck (path not chosen since 2026-06-05)",
        ],
        "today": [
            "Denis: PO apply + JD approval — planning/po-publish-readiness-2026-07-08.md",
            "Denis: Brand sprint day 1 minimum — planning/brand-sprint-catchup-2026-07-08.md",
            "Denis: Office — confirm 3 visits + contact landlords — planning/office-url-check-2026-07-08.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint → 4 daily inputs open; see planning/brand-sprint-catchup-2026-07-08.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md (brand day 3)",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 1 → refine positioning in business/plan + PO JD tone",
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
