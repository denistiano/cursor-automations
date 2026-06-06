#!/usr/bin/env python3
"""PM standup 2026-06-06 — upsert standup + sync completed agent tasks."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, entry_by_slug, init_db, json_loads, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-06"


def _items(conn, collection: str, slug: str, section: str = "items"):
    entry = entry_by_slug(conn, collection, slug)
    if not entry:
        raise SystemExit(f"Missing entry {collection}/{slug}")
    rows = conn.execute(
        "SELECT text, done, meta, sort_order FROM list_items WHERE entry_id=? AND section=? ORDER BY sort_order",
        (entry["id"], section),
    ).fetchall()
    return entry["id"], [
        {
            "text": r["text"],
            "done": bool(r["done"]),
            "meta": json_loads(r["meta"]),
            "sort_order": r["sort_order"],
        }
        for r in rows
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
            "Agent: Office visit shortlist draft → planning/office-plovdiv.md (5 Kapana/center picks; Denis to confirm)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — blocks careers copy + publish checklist",
            "Denis: #1 Office Plovdiv — review agent shortlist + HQ top-40; schedule 3–5 visits",
            "Denis: Landing page OR presentation deck (outline at content/presentation/outline.md)",
            "Denis: #4 Create social accounts (3 bios drafted — approve in HQ Inbox first)",
            "Denis: HQ Inbox — 4 automation + 3 social approve actions still open",
        ],
        "today": [
            "Denis: PO apply method + publish channels (email / form / LinkedIn + first channel)",
            "Denis: HQ Inbox — approve automations + social drafts",
            "Denis: Office — confirm or edit agent visit shortlist (5 picks in planning/office-plovdiv.md)",
        ],
        "blockers": [
            "PO apply method + publish channels → input-blocker-po-apply-method-publish-channels",
        ],
        "agent_next": [
            "After PO channels → PO publish checklist + careers page + LinkedIn announcement draft",
            "After social copy approved → Denis creates profiles; agent repurposes deck → posts",
            "Landing scaffold in web/ when Denis picks landing-first vs deck-first",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def patch_pm_tasks(conn) -> None:
    entry_id, items = _items(conn, "tasks", "pm-agent-drafts-build")
    for item in items:
        if "#8 Presentation outline" in item["text"]:
            item["done"] = True
        if "#4 Social page bios" in item["text"]:
            item["done"] = True
    replace_list_items(conn, entry_id, "items", items)


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        patch_pm_tasks(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
