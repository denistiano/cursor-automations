#!/usr/bin/env python3
"""Apply Denis 2026-05-29 priority triage from #vibe-code to hq.db."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, entry_by_slug, init_db, json_dumps, json_loads, replace_list_items, upsert_entry

STANDUP_DATE = "2026-05-29"
DENIS_REPLY = (
    "Moved PO apply, Office Plovdiv, landing/presentation, and social accounts to ongoing "
    "(not Today). Denis moving to next priorities — see standup Today for agent + approval items."
)


def _patch_action(conn, slug: str, **prop_updates) -> None:
    row = entry_by_slug(conn, "actions", slug)
    if not row:
        return
    props = json_loads(row["props"])
    props.update(prop_updates)
    conn.execute(
        "UPDATE entries SET props=?, updated_at=datetime('now') WHERE id=?",
        (json_dumps(props), row["id"]),
    )


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
            "Denis triaged priorities in #vibe-code — PO, office, landing, social moved off Today into ongoing",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — in progress",
            "Denis: #1 Office Plovdiv — budget/area constraints; visit shortlist (HQ listings)",
            "Denis: Landing page on vibe-coders.academy OR presentation document — in progress",
            "Denis: #4 Create social accounts (after name + bios approved) — in progress",
        ],
        "today": [
            "Agent: Presentation outline + slide copy (content/presentation/) — one-liner approved",
            "Denis: HQ Inbox — approve automations (standup prep, competitor research, business plan, social drafts)",
            "Agent: Social page bios + first-post pack (draft) — supports Denis social setup",
        ],
        "blockers": [],
        "agent_next": [
            "After PO channels → careers page copy + LinkedIn announcement draft",
            "Office: keep planning/office-plovdiv.md brief aligned with Denis budget (<800 EUR) filters",
            "Public landing scaffold in web/ when Denis picks landing vs deck-first",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def patch_tasks(conn) -> None:
    entry_id, items = _items(conn, "tasks", "denis-decisions-manual")
    for needle, meta in (
        ("Landing page", {"inbox_status": "in_progress", "reply": "Ongoing — in progress (2026-05-29)"}),
        ("Presentation document", {"inbox_status": "in_progress", "reply": "Ongoing — in progress (2026-05-29)"}),
    ):
        for item in items:
            if needle in item["text"]:
                item["meta"] = {**item.get("meta", {}), **meta}
    replace_list_items(conn, entry_id, "items", items)

    entry_id, items = _items(conn, "tasks", "blockers")
    for item in items:
        if "PO apply" in item["text"]:
            item["meta"] = {
                **item.get("meta", {}),
                "inbox_status": "in_progress",
                "reply": "In progress — standup ongoing; method/channels still via HQ Inbox",
            }
    replace_list_items(conn, entry_id, "items", items)


def patch_actions(conn) -> None:
    ongoing_slugs = (
        "input-blocker-po-apply-method-publish-channels",
        "input-task-1-office-plovdiv-budget-area-constraints-visit-shortlist",
        "input-task-landing-page-on-vibe-coders-academy-denis-todo",
        "input-task-presentation-document-denis-todo",
        "input-task-4-create-social-accounts-after-name-bios-approved",
    )
    for slug in ongoing_slugs:
        _patch_action(
            conn,
            slug,
            status="in_progress",
            reply=DENIS_REPLY,
        )


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


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        patch_tasks(conn)
        patch_actions(conn)
        conn.commit()
    print(f"Applied Denis priorities → standup {STANDUP_DATE}")


if __name__ == "__main__":
    main()
