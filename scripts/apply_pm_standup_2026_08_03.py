#!/usr/bin/env python3
"""PM standup 2026-08-03 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-08-03"


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
            "Agent: Re-ranked office listings (1268 scraped, 745 ≥40 m²) → data/office-top40.md",
            "Agent: Verified office shortlist A/B/C still live; alternate 10915009 delisted → planning/office-shortlist-refresh-2026-08-03.md",
            "Agent: Scheduled standup 2026-08-03 (45-day gap since 2026-06-19)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05 — day 59); jobs/product-owner body still empty",
            "Denis: Office Plovdiv — pick 3 visits from refreshed shortlist",
            "Denis: HQ Inbox — 4 automations + 3 social drafts still open (day 54)",
            "Denis: Landing page OR presentation deck — path not chosen since 2026-06-05",
            "Denis: Brand sprint days 1–4 — no replies in #vibe-business",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + channels (+ approve expanded JD or paste text)",
            "Denis: Office — confirm visits A/B/C (Kapana 11108782, широк център 10481212, training hall 4734755)",
            "Denis: HQ Inbox — batch approve automations + social copy",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; see planning/po-jd-expanded-draft-2026-06-19.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
            "Brand sprint day 1 → input-task-brand-sprint-day-1-positioning-secret-sauce-hq-brand-sprint",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn announcement draft",
            "After office visit picks → lease comparison table + landlord outreach",
            "Fix office-listings workflow to commit data/office-top40.md alongside JSON",
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
