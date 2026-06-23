#!/usr/bin/env python3
"""PM standup 2026-06-23 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-23"


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
            "Agent: Office scrape refresh (1264 listings, 2026-06-22) → data/office-listings.json",
            "Agent: Shortlist URL re-check — 3 picks still live → planning/office-url-check-2026-06-23.md",
            "Agent: PO publish readiness (day 18) → planning/po-publish-readiness-2026-06-23.md",
            "Agent: Brand sprint catch-up pack → planning/brand-sprint-catchup-2026-06-23.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-23.md",
        ],
        "ongoing": [
            "Denis: PO apply method + publish channels (no reply since 2026-06-05 — day 18)",
            "Denis: Brand sprint days 1–4 — none answered; sprint ended 2026-06-22",
            "Denis: Office Plovdiv — shortlist verified; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 13)",
            "Denis: Landing vs deck path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels + JD approval",
            "Denis: Brand sprint catch-up — batch days 1–4 (min: day 4 budget/calendar)",
            "Denis: Office — confirm 3 visits from verified shortlist",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty (day 18)",
            "Brand plan → all 4 sprint inputs open; see planning/brand-sprint-catchup-2026-06-23.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand sprint replies → merge plan + unlock social CTA",
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
