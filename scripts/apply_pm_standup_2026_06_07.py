#!/usr/bin/env python3
"""PM standup 2026-06-07 — upsert standup + sync agent deliverables."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, entry_by_slug, init_db, json_dumps, json_loads, replace_list_items, upsert_entry

STANDUP_DATE = "2026-06-07"
PO_JOB_PATH = Path(__file__).resolve().parent.parent / "business" / "jobs" / "product-owner.md"


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
            "Repo: 2026-06-06 office shortlist merged (planning/office-plovdiv.md)",
            "Agent: PO job draft → business/jobs/product-owner.md + planning/po-publish-checklist.md",
            "Agent: Landing vs deck decision brief → planning/landing-vs-deck.md",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — job text ready",
            "Denis: #1 Office Plovdiv — confirm agent shortlist; schedule visits",
            "Denis: Landing-first vs deck-first (planning/landing-vs-deck.md)",
            "Denis: #4 Create social accounts (approve 3 bios in HQ Inbox first)",
            "Denis: HQ Inbox — 4 automation + 3 social approve actions open since 2026-05-29",
        ],
        "today": [
            "Denis: PO apply method + publish channels",
            "Denis: HQ Inbox — approve automations + social drafts",
            "Denis: Office — confirm visit shortlist (planning/office-plovdiv.md)",
        ],
        "blockers": [
            "PO apply method + publish channels → input-blocker-po-apply-method-publish-channels",
            "Landing path → planning/landing-vs-deck.md",
        ],
        "agent_next": [
            "After PO channels → sync jobs/product-owner + LinkedIn PO announcement draft",
            "After office shortlist confirmed → visit call script for listing agents",
            "After landing path → public page scaffold or deck → social repurpose",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def sync_po_job(conn) -> None:
    if not PO_JOB_PATH.exists():
        return
    body = PO_JOB_PATH.read_text(encoding="utf-8")
    status = "Draft — awaiting Denis apply method + first publish channel"
    pos = body.split("## Position text")
    position_text = pos[1].split("---")[0].strip() if len(pos) > 1 else ""
    upsert_entry(
        conn,
        "jobs",
        "product-owner",
        "Product Owner",
        status=status,
        body=body,
        props={"position_text": position_text},
    )


def patch_pm_tasks(conn) -> None:
    entry_id, items = _items(conn, "tasks", "pm-agent-drafts-build")
    for item in items:
        if "#2 Publish checklist" in item["text"]:
            item["meta"]["reply"] = "Checklist drafted → planning/po-publish-checklist.md; blocked on Denis apply method"
        if "#1 Plovdiv office search brief" in item["text"]:
            item["done"] = True
    replace_list_items(conn, entry_id, "items", items)


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        sync_po_job(conn)
        patch_pm_tasks(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
