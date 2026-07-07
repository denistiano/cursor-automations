#!/usr/bin/env python3
"""PM standup 2026-07-07 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-07"


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
            "Agent: Office re-scrape (1264 listings) + re-rank → data/office-top40.md",
            "Agent: URL check — picks A/B/C HTTP 200; B live but dropped from top40 → planning/office-url-check-2026-07-07.md",
            "Agent: PO publish readiness (day 27) → planning/po-publish-readiness-2026-07-07.md",
            "Agent: Brand sprint catch-up (15 days overdue) → planning/brand-sprint-catchup-2026-07-07.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-07.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-10 — day 27)",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22 (15 days overdue)",
            "Denis: Office Plovdiv — A/C in top40; B live but dropped; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 27)",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD)",
            "Denis: Brand sprint day 1 minimum (ICP + secret sauce) — or full catch-up batch",
            "Denis: Office — confirm 3 picks + start landlord outreach",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 unanswered → planning/brand-sprint-catchup-2026-07-07.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day1 → refine positioning in business/plan",
            "After office visit picks → lease comparison table in HQ",
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
