#!/usr/bin/env python3
"""PM standup 2026-07-21 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-21"


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
            "Agent: A/B/C live re-check — pick C is hourly not monthly → planning/office-shortlist-validation-2026-07-21.md",
            "Agent: PO apply fast-track (2-reply unblock) → planning/po-apply-fast-track-2026-07-21.md",
            "Agent: Carryover analysis (1d since 2026-07-20) → planning/carryover-analysis-2026-07-21.md",
            "Agent: Denis batch agent prompt → planning/denis-agent-prompt-2026-07-21.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — no reply since 2026-06-05 (day 46); JD still empty",
            "Denis: Office Plovdiv — A/B live; C is per-session pricing; B listing expires ~13d",
            "Denis: HQ Inbox — 4 automations + 3 social drafts still open (day 41+)",
            "Denis: Landing page OR presentation deck — path not chosen",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + JD — 2 replies in planning/po-apply-fast-track-2026-07-21.md",
            "Denis: Office — confirm A+B; replace or negotiate C (hourly) — planning/office-shortlist-validation-2026-07-21.md",
            "Denis: HQ Inbox batch — 7 approvals (planning/hq-inbox-unlocks-2026-06-19.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office pick C → hourly pricing (€25.56/2–3h), not monthly lease",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand day 1 → planning/brand-day1-starter-2026-07-20.md (on branch 46aa; copy to repo)",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office A/B confirmed + quotes → lease comparison table in HQ",
            "After path choice → landing scaffold OR deck export to slides",
            "After brand day 1 → merge into brand marketing plan draft",
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
