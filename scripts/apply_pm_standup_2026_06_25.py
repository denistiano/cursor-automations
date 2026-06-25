#!/usr/bin/env python3
"""PM standup 2026-06-25 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-25"


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
            "Agent: Shortlist A/B/C URL verification → planning/office-url-check-2026-06-25.md",
            "Agent: PO publish readiness (day 15) → planning/po-publish-readiness-2026-06-25.md",
            "Agent: Brand sprint catch-up (days 1–4 unanswered) → planning/brand-sprint-catchup-2026-06-25.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-25.md",
        ],
        "ongoing": [
            "Denis: PO apply + channels (no reply since 2026-06-10 — day 15)",
            "Denis: Office — shortlist verified; pick 3 + contact landlords",
            "Denis: Brand sprint days 1–4 — 0 replies; sprint ended 2026-06-22",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 15)",
            "Denis: Landing page OR deck — path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Office — confirm picks A/B/C (planning/office-url-check-2026-06-25.md)",
            "Denis: Brand sprint day 1 catch-up OR HQ Inbox batch",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 unanswered → blocks marketing plan merge",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → condensed day 2–4 prompts in #vibe-business",
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
