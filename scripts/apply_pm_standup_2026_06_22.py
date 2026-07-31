#!/usr/bin/env python3
"""PM standup 2026-06-22 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-22"


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
            "Agent: Office URL re-check (3 picks HTTP 200) → planning/office-url-check-2026-06-22.md",
            "Agent: PO publish readiness (day 17, JD empty) → planning/po-publish-readiness-2026-06-22.md",
            "Agent: Brand sprint catch-up pack → planning/brand-sprint-catchup-2026-06-22.md",
            "Agent: Denis action pack + agent prompt → planning/denis-action-pack-2026-06-22.md",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–3 skipped; day 4 due today",
            "Denis: PO apply + publish channels (no reply since 2026-06-05 — day 17)",
            "Denis: Office Plovdiv — pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 12)",
            "Denis: Landing vs deck path not chosen",
        ],
        "today": [
            "Denis: Brand sprint batch catch-up + day 4 OR day 4 only",
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: HQ Inbox batch approve",
        ],
        "blockers": [
            "Brand sprint days 1–4 incomplete → marketing plan, FB strategy, CTA",
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After brand sprint → merge marketing plan + business/plan in hq.db",
            "After PO approved → careers page + LinkedIn PO draft",
            "After office picks → lease comparison table in HQ",
            "After HQ inbox → social profile setup; align draft CTAs",
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
