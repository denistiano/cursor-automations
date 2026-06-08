#!/usr/bin/env python3
"""PM standup 2026-06-08 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-08"


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
            "Agent: Office visit shortlist → planning/office-visit-shortlist-2026-06-08.md",
            "Agent: PO apply decision brief → planning/po-apply-decision-brief.md (flagged empty PO JD)",
            "Agent: Re-ran office ranking (no new scrape since 2026-06-03)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05)",
            "Denis: Office Plovdiv — shortlist ready; pick 3–5 visits",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck (outline ready)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + publish channels (+ PO JD if missing)",
            "Denis: Office — confirm visit shortlist or reply with picks",
            "Denis: HQ Inbox — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck — Denis path choice",
        ],
        "agent_next": [
            "After PO channels + JD → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "Landing scaffold in web/ when Denis picks landing-first vs deck-first",
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
