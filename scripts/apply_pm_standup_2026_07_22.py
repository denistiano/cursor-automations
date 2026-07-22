#!/usr/bin/env python3
"""PM standup 2026-07-22 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-22"


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
            "Agent: Re-ranked office listings (358 scraped 2026-07-20) → data/office-top40.md",
            "Agent: Office shortlist refresh — previous picks expired → planning/office-shortlist-refresh-2026-07-22.md",
            "Agent: Stale-item analysis + Denis action pack → planning/denis-action-pack-2026-07-22.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 47)",
            "Denis: Office Plovdiv — revised shortlist 2026-07-22; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 42)",
            "Denis: Brand sprint days 1–4 — no replies since added 2026-06-19",
            "Denis: Landing page OR presentation deck (path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-07-22.md",
            "Denis: Brand sprint day 1 — positioning & secret sauce",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Office → previous shortlist picks no longer listed; must re-pick",
            "Brand sprint day 1 never started — blocks marketing calendar",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After brand day 1 → merge into brand-marketing-plan-draft",
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
