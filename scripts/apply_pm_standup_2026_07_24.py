#!/usr/bin/env python3
"""PM standup 2026-07-24 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-24"


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
            "Agent: Live office re-check — A/B/C still live; B ~10 days → planning/office-shortlist-validation-2026-07-24.md",
            "Agent: Carryover analysis (1d since 2026-07-23) → planning/carryover-analysis-2026-07-24.md",
            "Agent: Denis batch agent prompt → planning/denis-agent-prompt-2026-07-24.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 49)",
            "Denis: Office Plovdiv — B (10481212) expires ~10 days; no landlord contact in repo",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 44+)",
            "Denis: Brand sprint days 1–4 unanswered (32 days since sprint ended)",
            "Denis: Landing page OR presentation deck — path not chosen",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + JD — 2 replies in planning/po-apply-fast-track-2026-07-21.md",
            "Denis: Office — confirm 3 picks + contact B today — planning/office-shortlist-validation-2026-07-24.md",
            "Denis: Brand sprint day 1 — suggested defaults in planning/carryover-analysis-2026-07-24.md",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office B urgency → 10481212 valid ~10 days",
            "Brand day 1 → blocks days 2–4, social strategy, marketing calendar",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks confirmed → lease comparison table in HQ",
            "After brand day 1 reply → merge into brand marketing plan draft",
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
