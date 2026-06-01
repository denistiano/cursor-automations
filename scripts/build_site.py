#!/usr/bin/env python3
"""Export data/hq.db → web/data/site.json (query/action-centric inbox UI)."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from hq_db import ROOT, connect, init_db, json_loads, load_ui_config

OUTPUT_PATH = ROOT / "web" / "data" / "site.json"


def git_sha() -> str | None:
    if sha := __import__("os").environ.get("GITHUB_SHA"):
        return sha
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def fetch_meta(conn) -> dict:
    return {row["key"]: row["value"] for row in conn.execute("SELECT key, value FROM meta").fetchall()}


def entry_dict(row) -> dict:
    props = json_loads(row["props"])
    return {
        "id": row["id"],
        "collection": row["collection"],
        "slug": row["slug"],
        "title": row["title"],
        "status": row["status"],
        "body": row["body"],
        "props": props,
        "sortOrder": row["sort_order"],
        "updatedAt": row["updated_at"],
    }


def action_card(entry: dict) -> dict:
    p = entry["props"]
    return {
        "id": entry["id"],
        "slug": entry["slug"],
        "title": entry["title"],
        "kind": p.get("kind", "input"),
        "role": p.get("role", "pm"),
        "priority": p.get("priority", 2),
        "status": p.get("status", "open"),
        "slackChannel": p.get("slack_channel", ""),
        "slackReply": p.get("slack_reply", ""),
        "slackTrigger": p.get("slack_trigger", ""),
        "prompt": p.get("prompt") or entry.get("body", ""),
        "batchPrompt": p.get("batch_prompt", ""),
        "hint": p.get("hint", ""),
        "inputLabel": p.get("input_label", ""),
        "inputExample": p.get("input_example", ""),
        "source": p.get("source", {}),
        "updatedAt": entry.get("updatedAt"),
    }


def compile_actions(entries: list[dict]) -> list[dict]:
    cards = [action_card(e) for e in entries if e["collection"] == "actions"]
    open_first = sorted(
        cards,
        key=lambda c: (
            0 if c["status"] == "open" else 1,
            c["priority"],
            c["title"],
        ),
    )
    return open_first


def group_by_role(actions: list[dict], ui_config: dict) -> dict:
    roles_cfg = ui_config.get("roles", {})
    grouped = {role: {"meta": meta, "actions": [], "prompts": []} for role, meta in roles_cfg.items()}
    for action in actions:
        role = action.get("role", "pm")
        if role not in grouped:
            grouped[role] = {"meta": {"label": role.title(), "channel": ""}, "actions": [], "prompts": []}
        if action["kind"] == "prompt":
            grouped[role]["prompts"].append(action)
        else:
            grouped[role]["actions"].append(action)
    return grouped


def fetch_tables_for_entries(conn, entry_ids: list[int]) -> dict[int, list]:
    if not entry_ids:
        return {}
    placeholders = ",".join("?" for _ in entry_ids)
    table_rows = conn.execute(
        f"SELECT * FROM tables WHERE entry_id IN ({placeholders}) ORDER BY entry_id, sort_order",
        entry_ids,
    ).fetchall()
    grouped: dict[int, list] = {}
    for table in table_rows:
        rows = conn.execute(
            "SELECT cells FROM table_rows WHERE table_id=? ORDER BY sort_order",
            (table["id"],),
        ).fetchall()
        grouped.setdefault(table["entry_id"], []).append(
            {
                "name": table["name"],
                "columns": json_loads(table["columns"], []),
                "rows": [json_loads(r["cells"]) for r in rows],
            }
        )
    return grouped


def build_reference(by_collection: dict, tables_by_entry: dict[int, list]) -> dict:
    research = by_collection.get("research", [])
    competitors = next((e for e in research if e["slug"] == "competitors"), None)
    if competitors:
        competitors = dict(competitors)
        competitors["tables"] = tables_by_entry.get(competitors["id"], [])
    roadmap = by_collection.get("roadmap", [])
    tracks = next((e for e in roadmap if e["slug"] == "tracks"), None)
    if tracks:
        tracks = dict(tracks)
        tracks["tables"] = tables_by_entry.get(tracks["id"], [])
    messaging = next((e for e in by_collection.get("business", []) if e["slug"] == "messaging"), None)
    return {
        "competitors": competitors,
        "roadmapTracks": tracks,
        "messaging": messaging,
    }


def compute_metrics(actions: list[dict]) -> dict:
    open_actions = [a for a in actions if a["status"] in ("open", "in_progress") and a["kind"] != "prompt"]
    inputs = [a for a in open_actions if a["kind"] == "input"]
    approvals = [a for a in open_actions if a["kind"] == "approve"]
    return {
        "openActions": len(open_actions),
        "needsInput": len(inputs),
        "needsApproval": len(approvals),
        "prompts": len([a for a in actions if a["kind"] == "prompt"]),
    }


def task_column(done: bool, meta: dict) -> str:
    status = (meta or {}).get("inbox_status")
    if done or status == "done":
        return "done"
    if status == "backlog":
        return "backlog"
    if status == "in_progress":
        return "in_progress"
    return "todo"


def list_item_card(item: dict, group: dict) -> dict:
    meta = item.get("meta") or {}
    col = task_column(item["done"], meta)
    return {
        "id": item.get("id"),
        "text": item["text"],
        "done": item["done"],
        "column": col,
        "owner": meta.get("owner", group.get("owner", "")),
        "meta": meta,
    }


def build_task_boards(task_entries: list[dict]) -> list[dict]:
    boards = []
    for entry in sorted(task_entries, key=lambda e: e.get("sortOrder", 0)):
        items = [list_item_card(i, entry) for i in entry.get("listItems", []) if i["section"] == "items"]
        columns: dict[str, list] = {"backlog": [], "todo": [], "in_progress": [], "done": []}
        for item in items:
            columns.setdefault(item["column"], []).append(item)
        boards.append(
            {
                "slug": entry["slug"],
                "title": entry["title"],
                "owner": entry.get("owner"),
                "kind": (entry.get("props") or {}).get("kind", "group"),
                "columns": columns,
                "counts": {k: len(v) for k, v in columns.items()},
            }
        )
    return boards


def build_standups(standup_entries: list[dict], limit: int = 5) -> list[dict]:
    ordered = sorted(standup_entries, key=lambda e: e["slug"], reverse=True)[:limit]
    result = []
    for entry in ordered:
        sections: dict[str, list[str]] = {}
        for item in entry.get("listItems", []):
            sections.setdefault(item["section"], []).append(item["text"])
        result.append({"slug": entry["slug"], "title": entry["title"], "sections": sections})
    return result


def build_planning(by_collection: dict, tables_by_entry: dict[int, list]) -> dict:
    roadmap_entries = by_collection.get("roadmap", [])
    office_entries = by_collection.get("office", [])
    office_entry = office_entries[0] if office_entries else None

    tracks = next((e for e in roadmap_entries if e["slug"] == "tracks"), None)
    phases = next((e for e in roadmap_entries if e["slug"] == "phases"), None)
    near_term = next((e for e in roadmap_entries if e["slug"] == "near-term"), None)
    overview = next((e for e in roadmap_entries if e["slug"] == "overview"), None)

    def with_tables(entry: dict | None) -> dict | None:
        if not entry:
            return None
        out = dict(entry)
        out["tables"] = tables_by_entry.get(entry["id"], [])
        return out

    listings_path = ROOT / "data" / "office-listings.json"
    office_listings = {}
    if listings_path.exists():
        office_listings = json.loads(listings_path.read_text(encoding="utf-8"))

    office_brief = ""
    if office_entry and office_entry.get("body"):
        office_brief = office_entry["body"]
    else:
        brief_path = ROOT / "planning" / "office-plovdiv.md"
        if brief_path.exists():
            office_brief = brief_path.read_text(encoding="utf-8")

    office_tables = tables_by_entry.get(office_entry["id"], []) if office_entry else []
    criteria = next((t for t in office_tables if t["name"] == "criteria"), None)
    shortlist = next((t for t in office_tables if t["name"] == "shortlist"), None)

    return {
        "overview": overview,
        "tracks": with_tables(tracks),
        "phases": with_tables(phases),
        "nearTerm": near_term,
        "office": office_entry,
        "officeBrief": office_brief,
        "officeCriteria": criteria,
        "officeShortlist": shortlist,
        "officeListings": office_listings,
        "standups": build_standups(by_collection.get("standups", [])),
    }


def build_research_export(by_collection: dict, tables_by_entry: dict[int, list]) -> dict:
    entries = []
    for entry in sorted(by_collection.get("research", []), key=lambda e: e["slug"]):
        body = entry.get("body") or ""
        enriched = {
            "slug": entry["slug"],
            "title": entry["title"],
            "props": entry.get("props") or {},
            "excerpt": body[:1200] + ("…" if len(body) > 1200 else ""),
            "bodyLength": len(body),
            "tables": tables_by_entry.get(entry["id"], []),
        }
        entries.append(enriched)
    return {"entries": entries}


def build_payload() -> dict:
    init_db()
    from sync_actions import sync_actions

    ui_config = load_ui_config()
    with connect() as conn:
        sync_actions(conn)
        conn.commit()

        meta = fetch_meta(conn)
        rows = conn.execute("SELECT * FROM entries ORDER BY collection, sort_order, id").fetchall()
        entries = [entry_dict(r) for r in rows]

        entry_ids = [e["id"] for e in entries]
        list_items = []
        if entry_ids:
            placeholders = ",".join("?" for _ in entry_ids)
            for row in conn.execute(
                f"SELECT * FROM list_items WHERE entry_id IN ({placeholders}) ORDER BY entry_id, section, sort_order",
                entry_ids,
            ).fetchall():
                list_items.append(
                    {
                        "entryId": row["entry_id"],
                        "section": row["section"],
                        "text": row["text"],
                        "done": bool(row["done"]),
                        "meta": json_loads(row["meta"]),
                    }
                )

        by_collection: dict[str, list] = {}
        for entry in entries:
            enriched = dict(entry)
            enriched["listItems"] = [i for i in list_items if i["entryId"] == entry["id"]]
            by_collection.setdefault(entry["collection"], []).append(enriched)

        tables_by_entry = fetch_tables_for_entries(conn, entry_ids)
        actions = compile_actions(entries)
        roles = group_by_role(actions, ui_config)
        inbox = [a for a in actions if a["kind"] != "prompt" and a["status"] in ("open", "in_progress")]
        inbox_batch = __import__("sync_actions", fromlist=["build_inbox_batch"]).build_inbox_batch(actions)

        task_boards = build_task_boards(by_collection.get("tasks", []))
        task_totals = {
            col: sum(b["counts"].get(col, 0) for b in task_boards)
            for col in ("backlog", "todo", "in_progress", "done")
        }

        return {
            "meta": {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "generator": "scripts/build_site.py",
                "gitSha": git_sha(),
                "schemaVersion": meta.get("schema_version"),
                "dataModel": "hq-sections-v3",
            },
            "project": {
                "title": meta.get("project.title", "Course Business HQ"),
                "description": meta.get("project.description", ""),
            },
            "metrics": {**compute_metrics(actions), "tasks": task_totals},
            "ui": ui_config,
            "inbox": inbox,
            "inboxBatch": inbox_batch,
            "actions": actions,
            "roles": roles,
            "reference": build_reference(by_collection, tables_by_entry),
            "tasks": {"boards": task_boards, "totals": task_totals},
            "planning": build_planning(by_collection, tables_by_entry),
            "researchHub": build_research_export(by_collection, tables_by_entry),
        }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)} ({len(payload['inbox'])} open actions)")


if __name__ == "__main__":
    main()
