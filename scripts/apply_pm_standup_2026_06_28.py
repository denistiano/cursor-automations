#!/usr/bin/env python3
"""PM standup 2026-06-28 — upsert standup + link planning artifacts."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-28"


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
            "Agent: Office re-scrape (1264 listings) + re-rank → data/office-top40.md",
            "Agent: URL check — picks A/B/C live → planning/office-url-check-2026-06-28.md",
            "Agent: PO publish readiness → planning/po-publish-readiness-2026-06-28.md",
            "Agent: Brand sprint catch-up → planning/brand-sprint-catchup-2026-06-28.md",
            "Agent: Denis action pack → planning/denis-action-pack-2026-06-28.md",
        ],
        "ongoing": [
            "Denis: PO apply + JD — no reply since 2026-06-10 (day 18); JD draft ready; hq.db empty",
            "Denis: Brand sprint days 1–4 — sprint ended 2026-06-22 (6 days overdue)",
            "Denis: Office Plovdiv — pick 3 + contact landlords (shortlist verified live)",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open (day 18)",
            "Denis: Landing vs deck — path not chosen; speaker notes ready",
        ],
        "today": [
            "Denis: PO apply + JD approve — unblocks careers + LinkedIn PO post",
            "Denis: Brand sprint day 1 minimum (or batch 1–4) — unblocks marketing plan",
            "Denis: HQ Inbox batch OR office pick 3 — unblocks automations / visits",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; planning/po-publish-readiness-2026-06-28.md",
            "Brand plan incomplete → planning/brand-sprint-catchup-2026-06-28.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md",
        ],
        "agent_next": [
            "After PO channels + JD approved → careers page + LinkedIn PO announcement draft",
            "After brand day 1+ → merge into business/plan + finalize marketing plan",
            "After office picks → lease comparison table in HQ",
            "After path choice → deck export OR landing scaffold",
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
