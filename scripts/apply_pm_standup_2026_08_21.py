#!/usr/bin/env python3
"""PM standup 2026-08-21 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-21"


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
            "Agent: Office re-scrape (1366 listings) + re-rank → data/office-top40.md",
            "Agent: Office A/B/C re-validated → planning/office-shortlist-refresh-2026-08-21.md",
            "Agent: Brand sprint day 1 prefill → planning/brand-sprint-day1-prefill-2026-08-21.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 72)",
            "Denis: Office Plovdiv — A/B/C still valid; pick 3 + contact landlords",
            "Denis: Brand sprint days 1–4 (no replies — day 63)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck (path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Office — confirm A/B/C from planning/office-shortlist-refresh-2026-08-21.md",
            "Denis: HQ Inbox batch approvals",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand day 1 → planning/brand-sprint-day1-prefill-2026-08-21.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → refine positioning in business/plan",
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
