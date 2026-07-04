#!/usr/bin/env python3
"""PM standup 2026-07-04 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-04"


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
            "Agent: Office re-rank confirmed (440 listings, 2026-06-29) → data/office-top40.md",
            "Agent: URL live-check — all shortlist picks still HTTP 200 → planning/office-url-check-2026-07-04.md",
            "Agent: PO publish readiness refresh (day 24) → planning/po-publish-readiness-2026-07-04.md",
            "Agent: Brand sprint catch-up (12 days overdue) → planning/brand-sprint-catchup-2026-07-04.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-04.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 24)",
            "Denis: Brand sprint days 1–4 (sprint ended 2026-06-22 — 12 days overdue)",
            "Denis: Office Plovdiv — pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 24)",
            "Denis: Landing page OR presentation deck (path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops model",
            "Denis: Office — pick 3 from planning/office-url-check-2026-07-04.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand day 1 → input-task-brand-sprint-day-1-positioning-secret-sauce-hq-brand-sprint",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 1 → refine positioning in business/plan",
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
