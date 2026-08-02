#!/usr/bin/env python3
"""PM standup 2026-08-02 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-02"


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
            "Agent: Carryover analysis → planning/carryover-analysis-2026-08-02.md",
            "Agent: Office A/B′/C re-validated → planning/office-shortlist-validation-2026-08-02.md",
            "Agent: PO publish readiness checklist → planning/po-publish-readiness-2026-08-02.md",
            "Agent: Denis agent prompt → planning/denis-agent-prompt-2026-08-02.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 58)",
            "Denis: Office Plovdiv — pick A, B′, C + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 53)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Landing page OR presentation deck (path not chosen)",
        ],
        "today": [
            "Denis: PO apply + approve JD — planning/po-publish-readiness-2026-08-02.md",
            "Denis: Office visits — confirm A, B′, C per planning/office-shortlist-validation-2026-08-02.md",
            "Denis: HQ Inbox — approve social drafts + automations",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office alternate 10915009 no longer in listings; B′ (11081121) replaces stale B",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office visit picks → lease comparison table in HQ",
            "After inbox approvals → social account setup guide for Denis",
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
