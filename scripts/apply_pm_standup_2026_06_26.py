#!/usr/bin/env python3
"""PM standup 2026-06-26 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-26"


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
            "Agent: Office URL re-check (3 picks live) → planning/office-url-check-2026-06-26.md",
            "Agent: PO publish readiness pack → planning/po-publish-readiness-2026-06-26.md",
            "Agent: Brand sprint catch-up batch → planning/brand-sprint-catchup-2026-06-26.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-26.md",
        ],
        "ongoing": [
            "Denis: PO apply + channels (no reply since 2026-06-05 — day 21)",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22",
            "Denis: Office — pick 3 verified listings + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 16)",
            "Denis: Landing vs deck — path tied to brand day 3",
        ],
        "today": [
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Brand sprint batch reply (days 1–4)",
            "Denis: Office pick 3 + HQ Inbox approvals",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand plan → days 1–4 unanswered since sprint end 2026-06-22",
            "HQ Inbox → 7 approvals still open",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand batch reply → merge plan; deck export + FB copy",
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
