#!/usr/bin/env python3
"""PM standup 2026-06-19 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-19"


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
            "Agent: Office re-scrape (1267 listings) + re-rank → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-06-19.md (Kapana 11108782 #1 @ €400)",
            "Agent: PO expanded JD draft → planning/po-jd-expanded-draft-2026-06-19.md",
            "Agent: Speaker notes export → content/presentation/speaker-notes.md",
            "Agent: HQ Inbox unlocks + Denis action pack → planning/hq-inbox-unlocks-2026-06-19.md, denis-action-pack-2026-06-19.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 14)",
            "Denis: Office Plovdiv — revised shortlist ready; pick 3 + contact landlords",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 9)",
            "Denis: Landing page OR presentation deck (speaker notes ready; path not chosen)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — pick 3 from planning/office-shortlist-refresh-2026-06-19.md",
            "Denis: HQ Inbox — approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office picks → lease comparison table in HQ",
            "After path choice → landing scaffold OR deck export to slides",
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
