#!/usr/bin/env python3
"""PM standup 2026-07-25 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-25"


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
            "Agent: Office re-scrape (298 listings) + re-rank → data/office-top40.md",
            "Agent: Office shortlist validation — picks A+B delisted; revised 3 picks → planning/office-shortlist-validation-2026-07-25.md",
            "Agent: Carryover analysis for 5 stale Denis items → planning/carryover-analysis-2026-07-25.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-25.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 50)",
            "Denis: Office Plovdiv — revised shortlist ready; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 36)",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22; no answers (day 33)",
            "Denis: Landing page OR presentation deck (path not chosen since 2026-06-05)",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from planning/office-shortlist-validation-2026-07-25.md",
            "Denis: HQ Inbox — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office → previous picks A+B delisted; must re-pick",
            "Brand sprint days 1–4 unanswered — blocks marketing plan + CTA",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → refine positioning in business/plan",
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
