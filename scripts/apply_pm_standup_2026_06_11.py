#!/usr/bin/env python3
"""PM standup 2026-06-11 — upsert standup + sync office shortlist from 2026-06-10 refresh."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, entry_by_slug, replace_list_items, replace_table, upsert_entry

STANDUP_DATE = "2026-06-11"

REVISED_SHORTLIST = [
    {
        "num": "1",
        "address": "В сърцето на Капана — https://www.alo.bg/v-sarceto-na-kapana-za-parvi-naemateli-za-razlichni-deinosti-10915009",
        "rent": "550",
        "notes": "64 m²; best location; kitchen; flexible use",
        "visit": "Denis pick?",
    },
    {
        "num": "2",
        "address": "Kapana бизнес пространство — https://www.alo.bg/kapana-za-parvi-naemateli-prostranstvo-za-biznes-i-vdahnovenie-11104973",
        "rent": "750",
        "notes": "80 m²; Kapana; kitchen; confirm ≤800 all-in",
        "visit": "Denis pick?",
    },
    {
        "num": "3",
        "address": "Зала обучения/семинари — https://www.alo.bg/zala-pod-naem-za-provejdane-na-obucheniya-i-seminari-4734755",
        "rent": "~26*",
        "notes": "42 m²; training hall; *per-session — confirm monthly",
        "visit": "Denis pick?",
    },
    {
        "num": "4",
        "address": "Зала курсове Пловдив — https://www.alo.bg/zala-pod-naem-obucheniya-seminari-kursove-plovdiv-7944729",
        "rent": "100*",
        "notes": "m² TBD; training keywords; *confirm monthly package",
        "visit": "Denis pick?",
    },
    {
        "num": "5",
        "address": "Офис широк център — https://www.alo.bg/ofis-pod-naem-shirok-centar-10481212",
        "rent": "400",
        "notes": "90 m²; best value center; kitchen; capacity check",
        "visit": "Denis pick?",
    },
]

LEASE_COMPARISON = [
    {
        "listing": "1 — Капана сърцето",
        "rent_eur": "550",
        "sqm": "64",
        "monthly_all_in": "TBD visit",
        "capacity_20": "TBD",
        "deposit": "TBD",
        "notes": "Top location score",
    },
    {
        "listing": "2 — Kapana бизнес",
        "rent_eur": "750",
        "sqm": "80",
        "monthly_all_in": "TBD visit",
        "capacity_20": "TBD",
        "deposit": "TBD",
        "notes": "At budget edge",
    },
    {
        "listing": "3 — Зала обучения",
        "rent_eur": "~26/session",
        "sqm": "42",
        "monthly_all_in": "TBD visit",
        "capacity_20": "TBD",
        "deposit": "TBD",
        "notes": "Purpose-built; verify monthly",
    },
    {
        "listing": "4 — Зала курсове",
        "rent_eur": "100*",
        "sqm": "TBD",
        "monthly_all_in": "TBD visit",
        "capacity_20": "TBD",
        "deposit": "TBD",
        "notes": "New find 2026-06-10",
    },
    {
        "listing": "5 — Широк център",
        "rent_eur": "400",
        "sqm": "90",
        "monthly_all_in": "TBD visit",
        "capacity_20": "TBD",
        "deposit": "TBD",
        "notes": "Best €/m² in center",
    },
]


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
            "Agent: PO publish checklist → planning/po-publish-checklist-2026-06-11.md",
            "Agent: HQ Inbox batch → planning/hq-inbox-batch-2026-06-11.md",
            "Agent: Office shortlist + lease comparison table synced in HQ",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel (no reply since 2026-06-05)",
            "Denis: Office Plovdiv — revised shortlist; pick 3 visits",
            "Denis: HQ Inbox — 4 automations + 3 social drafts open",
            "Denis: Landing page OR presentation deck (decision brief ready)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: PO apply + JD in one HQ Inbox reply",
            "Denis: HQ Inbox batch — approve automations + social copy",
            "Denis: Office — pick 3 from revised shortlist",
        ],
        "blockers": [
            "PO apply → input-blocker-po-apply-method-publish-channels; JD empty — po-jd-skeleton-2026-06-10.md",
            "Landing vs deck → planning/landing-vs-deck-decision-brief.md (ongoing, not Today)",
        ],
        "agent_next": [
            "After PO channels + JD → business/jobs/product-owner.md + careers in web/",
            "After office picks → lease comparison filled + visit notes",
            "After path choice → landing scaffold OR deck export",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def sync_office_tables(conn) -> None:
    office = entry_by_slug(conn, "office", "plovdiv")
    if not office:
        return
    entry_id = int(office["id"])
    replace_table(
        conn,
        entry_id,
        "shortlist",
        ["num", "address", "rent", "notes", "visit"],
        REVISED_SHORTLIST,
    )
    replace_table(
        conn,
        entry_id,
        "lease_comparison",
        ["listing", "rent_eur", "sqm", "monthly_all_in", "capacity_20", "deposit", "notes"],
        LEASE_COMPARISON,
    )


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        sync_office_tables(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
