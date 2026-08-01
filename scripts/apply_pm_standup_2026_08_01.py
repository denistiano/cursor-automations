#!/usr/bin/env python3
"""PM standup 2026-08-01 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-01"


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
            "Agent: Office shortlist A/C re-validated → planning/office-shortlist-validation-2026-08-01.md (B′ swap)",
            "Agent: PO publish readiness check → planning/po-publish-readiness-2026-08-01.md",
            "Agent: Carryover analysis (day 43+) → planning/carryover-analysis-2026-08-01.md",
            "Agent: Denis agent prompt pack → planning/denis-agent-prompt-2026-08-01.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 57)",
            "Denis: Office Plovdiv — confirm A + B′ + C; contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 52)",
            "Denis: Brand sprint days 1–4 unanswered (day 40 since sprint end)",
            "Denis: Landing page OR presentation deck — path not chosen",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — confirm visits A + B′ + C",
            "Denis: HQ Inbox — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand sprint days 1–4 → marketing plan incomplete",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
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
