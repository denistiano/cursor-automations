#!/usr/bin/env python3
"""PM standup 2026-06-20 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-20"


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
            "Agent: Office URL check — 3 recommended picks still live → planning/office-url-check-2026-06-20.md",
            "Agent: PO publish readiness pack (day 15) → planning/po-publish-readiness-2026-06-20.md",
            "Agent: Brand sprint day 2 prep → planning/brand-sprint-day2-prep-2026-06-20.md",
            "Agent: Denis action pack refresh → planning/denis-action-pack-2026-06-20.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 15)",
            "Denis: Office Plovdiv — shortlist ready; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 10)",
            "Denis: Brand sprint — day 1 skipped; day 2 visual + CTA due today",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: Brand sprint day 2 — visual direction + CTA",
            "Denis: PO apply + channels + approve expanded JD",
            "Denis: Office — pick 3 (URLs verified) + landlord outreach",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand sprint day 1 skipped — batch with day 2 or reply separately",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After brand day 2 → update creative brief + align landing/deck path",
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
