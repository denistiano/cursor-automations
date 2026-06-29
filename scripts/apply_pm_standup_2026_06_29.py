#!/usr/bin/env python3
"""PM standup 2026-06-29 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-29"


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
            "Agent: Office URL check — A/B/C still in 2026-06-22 scrape → planning/office-url-check-2026-06-29.md",
            "Agent: PO publish readiness audit (day 24) → planning/po-publish-readiness-2026-06-29.md",
            "Agent: Brand sprint catch-up pack → planning/brand-sprint-catchup-2026-06-29.md",
            "Agent: HQ Inbox + Denis action pack refresh → planning/hq-inbox-unlocks-2026-06-29.md, denis-action-pack-2026-06-29.md",
            "Repo: Automated office re-scrape 2026-06-22 (1264 listings)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 24)",
            "Denis: Office Plovdiv — shortlist verified live; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 19)",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22; no replies (day 7 overdue)",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD)",
            "Denis: Office — pick 3 + send landlord outreach",
            "Denis: HQ Inbox batch approve (denis-action-pack-2026-06-29.md §3)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint days 1–4 unanswered → planning/brand-sprint-catchup-2026-06-29.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → business/jobs/product-owner.md + careers scaffold",
            "After office picks → lease comparison table in HQ",
            "After brand day 1–4 replies → merge brand-marketing-plan-draft",
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
