#!/usr/bin/env python3
"""PM standup 2026-06-24 — upsert standup + restore blockers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-24"


def restore_blockers(conn) -> None:
    blockers_id = upsert_entry(
        conn,
        "tasks",
        "blockers",
        "Blockers",
        sort_order=900,
        props={"kind": "blockers"},
    )
    blockers = [
        {
            "text": "PO apply method + publish channels",
            "meta": {
                "owner": "Denis → pick apply method + first channel",
                "inbox_status": "in_progress",
            },
        },
        {
            "text": "Brand sprint days 1–4 incomplete",
            "meta": {
                "owner": "Denis → batch catch-up in #vibe-standup",
                "inbox_status": "in_progress",
            },
        },
        {
            "text": "Course one-liner TBD",
            "meta": {
                "owner": "Denis → One-liner: …",
                "inbox_status": "open",
            },
        },
        {
            "text": "Landing page vs presentation deck path",
            "meta": {
                "owner": "Denis → path via brand day 3 or standalone",
                "inbox_status": "in_progress",
            },
        },
    ]
    replace_list_items(conn, blockers_id, "items", blockers)


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
            "Agent: Office URL re-check (3 picks HTTP 200) → planning/office-url-check-2026-06-24.md",
            "Agent: PO publish readiness (day 19, JD empty) → planning/po-publish-readiness-2026-06-24.md",
            "Agent: Brand sprint post-sprint catch-up → planning/brand-sprint-catchup-2026-06-24.md",
            "Agent: Denis action pack + agent prompt → planning/denis-action-pack-2026-06-24.md",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–4 skipped — sprint ended 2026-06-22",
            "Denis: PO apply + publish channels (no reply since 2026-06-05 — day 19)",
            "Denis: Office Plovdiv — pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 14)",
            "Denis: Course one-liner TBD",
            "Denis: Landing vs deck path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint batch catch-up OR minimum viable days 1+3+one-liner",
            "Denis: HQ Inbox batch approve",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner empty",
            "Brand sprint days 1–4 → marketing plan, FB strategy, CTA",
            "One-liner → input-one-liner",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO approved → careers page + LinkedIn PO draft",
            "After brand sprint → merge marketing plan + business/plan in hq.db",
            "After office picks → lease comparison table in HQ",
            "After HQ inbox → social profile setup; align draft CTAs",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def main() -> None:
    init_db()
    with connect() as conn:
        restore_blockers(conn)
        upsert_standup(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
