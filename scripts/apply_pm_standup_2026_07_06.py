#!/usr/bin/env python3
"""PM standup 2026-07-06 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-06"


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
            "Agent: Office re-scrape (1248 listings) + re-rank → data/office-top40.md",
            "Agent: Office URL check — picks A/B/C all HTTP 200 → planning/office-url-check-2026-07-06.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-07-06.md (Kapana 11108782 #1 @ €400)",
            "Agent: PO publish readiness brief (day 31) → planning/po-publish-readiness-2026-07-06.md",
            "Agent: Brand sprint catch-up (14 days overdue) → planning/brand-sprint-catchup-2026-07-06.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-07-06.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 31)",
            "Denis: Office Plovdiv — revised shortlist ready; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 26)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — 14 days overdue)",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-07-06.md",
            "Denis: HQ Inbox batch approve (planning/denis-action-pack-2026-07-06.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 → planning/brand-sprint-catchup-2026-07-06.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1–4 replies → merge into brand-marketing-plan-draft",
            "After path choice → landing scaffold OR deck export to slides",
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
