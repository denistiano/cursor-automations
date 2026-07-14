#!/usr/bin/env python3
"""PM standup 2026-07-14 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-07-14"


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
            "Agent: Office re-rank (1288 listings) → data/office-top40.md",
            "Agent: Office shortlist refresh → planning/office-shortlist-refresh-2026-07-14.md",
            "Agent: PO publish checklist (day 39) → planning/po-publish-checklist-2026-07-14.md",
            "Agent: Brand day 1 brief (+22 days) → planning/brand-sprint-day1-decision-brief-2026-07-14.md",
            "Agent: HQ Inbox + landing path packs → planning/hq-inbox-impact-2026-07-14.md, landing-path-decision-pack-2026-07-14.md",
            "Agent: Denis batch prompt → planning/denis-agent-prompt-2026-07-14.md",
        ],
        "ongoing": [
            "Denis: PO apply + publish channel (no reply since 2026-06-05 — day 39)",
            "Denis: Brand sprint days 1–4 unanswered (sprint ended 2026-06-22 — +22 days)",
            "Denis: Office A/B/C verified — confirm + landlord outreach",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 34)",
            "Denis: Landing page OR deck — path not chosen (day 39)",
        ],
        "today": [
            "Denis: PO apply + approve JD (planning/po-publish-checklist-2026-07-14.md)",
            "Denis: Brand day 1 reply (planning/brand-sprint-day1-decision-brief-2026-07-14.md)",
            "Denis: HQ Inbox batch (planning/hq-inbox-impact-2026-07-14.md)",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; jobs/product-owner body empty",
            "Brand day 1 → input-task-brand-sprint-day-1-positioning-secret-sauce-hq-brand-sprint",
            "Landing vs deck → planning/landing-path-decision-pack-2026-07-14.md",
        ],
        "agent_next": [
            "After PO + JD → careers page + LinkedIn PO announcement draft",
            "After brand day 1 → merge marketing plan + business/messaging",
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
