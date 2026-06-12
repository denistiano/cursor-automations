#!/usr/bin/env python3
"""PM standup 2026-06-12 — upsert standup + sync office tables from 06-11 refresh."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from apply_pm_standup_2026_06_11 import STANDUP_DATE as PREV_DATE, sync_office_tables
from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-12"


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
            "Agent: Recovered 2026-06-11 artifacts (PO checklist, inbox batch, office lease table)",
            "Agent: PO apply form draft → planning/po-apply-form-draft-2026-06-12.md",
            "Agent: Office landlord script + picks 1,5,3 → planning/office-landlord-call-script-2026-06-12.md",
            "Agent: HQ Inbox 3-message batch → planning/hq-inbox-batch-2026-06-12.md",
            "Agent: Deck Slides paste pack → planning/deck-google-slides-paste-2026-06-12.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05)",
            "Denis: Office Plovdiv — agent recommends 1,5,3; Denis confirm + landlord calls",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck — paste pack ready; path not chosen",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + JD — hq-inbox-batch Message 1",
            "Denis: HQ Inbox approvals — Message 3 (7 items)",
            "Denis: Office — confirm Office visits: 1,5,3 or override",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; form draft + checklist ready",
            "Landing vs deck → deck paste pack available; not blocking Today",
        ],
        "agent_next": [
            "After PO channels + JD → business/jobs/product-owner.md + careers in web/",
            "After office picks → lease comparison visit rows + office-plovdiv.md notes",
            "After path choice → landing scaffold OR deck polish export",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def main() -> None:
    init_db()
    with connect() as conn:
        # Ensure 06-11 standup exists if DB was stale
        upsert_entry(
            conn,
            "standups",
            PREV_DATE,
            f"Standup — {PREV_DATE}",
            props={"date": PREV_DATE},
        )
        upsert_standup(conn)
        sync_office_tables(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
