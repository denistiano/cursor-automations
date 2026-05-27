#!/usr/bin/env python3
"""Export data/hq.db + data/ui-config.json → web/data/site.json for GitHub Pages."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from hq_db import DB_PATH, ROOT, connect, init_db, json_loads, load_ui_config

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
    rows = conn.execute("SELECT key, value FROM meta").fetchall()
    return {row["key"]: row["value"] for row in rows}


def fetch_collections(conn) -> list[dict]:
    rows = conn.execute(
        "SELECT slug, label, description, icon, sort_order, config FROM collections ORDER BY sort_order"
    ).fetchall()
    return [
        {
            "slug": row["slug"],
            "label": row["label"],
            "description": row["description"],
            "icon": row["icon"],
            "sortOrder": row["sort_order"],
            "config": json_loads(row["config"]),
        }
        for row in rows
    ]


def entry_dict(row) -> dict:
    return {
        "id": row["id"],
        "collection": row["collection"],
        "parentId": row["parent_id"],
        "slug": row["slug"],
        "title": row["title"],
        "status": row["status"],
        "owner": row["owner"],
        "body": row["body"],
        "props": json_loads(row["props"]),
        "sortOrder": row["sort_order"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def fetch_entries(conn, collection: str | None = None) -> list[dict]:
    if collection:
        rows = conn.execute(
            "SELECT * FROM entries WHERE collection=? ORDER BY sort_order, id",
            (collection,),
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM entries ORDER BY collection, sort_order, id").fetchall()
    return [entry_dict(row) for row in rows]


def fetch_list_items(conn, entry_ids: list[int] | None = None) -> list[dict]:
    if entry_ids:
        placeholders = ",".join("?" for _ in entry_ids)
        rows = conn.execute(
            f"SELECT * FROM list_items WHERE entry_id IN ({placeholders}) ORDER BY entry_id, section, sort_order",
            entry_ids,
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM list_items ORDER BY entry_id, section, sort_order"
        ).fetchall()
    return [
        {
            "id": row["id"],
            "entryId": row["entry_id"],
            "section": row["section"],
            "text": row["text"],
            "done": bool(row["done"]),
            "meta": json_loads(row["meta"]),
            "sortOrder": row["sort_order"],
        }
        for row in rows
    ]


def fetch_tables(conn, entry_ids: list[int] | None = None) -> list[dict]:
    if entry_ids:
        placeholders = ",".join("?" for _ in entry_ids)
        table_rows = conn.execute(
            f"SELECT * FROM tables WHERE entry_id IN ({placeholders}) ORDER BY entry_id, sort_order",
            entry_ids,
        ).fetchall()
    else:
        table_rows = conn.execute("SELECT * FROM tables ORDER BY entry_id, sort_order").fetchall()

    tables = []
    for table in table_rows:
        rows = conn.execute(
            "SELECT cells, sort_order FROM table_rows WHERE table_id=? ORDER BY sort_order",
            (table["id"],),
        ).fetchall()
        tables.append(
            {
                "id": table["id"],
                "entryId": table["entry_id"],
                "name": table["name"],
                "columns": json_loads(table["columns"], []),
                "rows": [json_loads(row["cells"]) for row in rows],
                "sortOrder": table["sort_order"],
            }
        )
    return tables


def index_by_entry(items: list[dict], key: str = "entryId") -> dict[int, list]:
    grouped: dict[int, list] = {}
    for item in items:
        grouped.setdefault(item[key], []).append(item)
    return grouped


def compute_metrics(entries: list[dict], list_items: list[dict]) -> dict:
    task_entry_ids = {e["id"] for e in entries if e["collection"] == "tasks" and e["slug"] != "blockers" and e["slug"] != "project-status"}
    task_items = [i for i in list_items if i["entryId"] in task_entry_ids and i["section"] == "items"]
    standups = [e for e in entries if e["collection"] == "standups"]
    automations = [e for e in entries if e["collection"] == "automations"]
    social = [e for e in entries if e["collection"] == "social"]
    social_pending = sum(1 for e in social if not e["props"].get("approved"))

    return {
        "openTasks": sum(1 for i in task_items if not i["done"]),
        "doneTasks": sum(1 for i in task_items if i["done"]),
        "standups": len(standups),
        "automations": len(automations),
        "socialDrafts": len(social),
        "socialPending": social_pending,
        "entries": len(entries),
    }


def build_payload() -> dict:
    init_db()
    ui_config = load_ui_config()
    with connect() as conn:
        if conn.execute("SELECT COUNT(*) AS n FROM collections").fetchone()["n"] == 0:
            from seed_from_md import seed_all

            seed_all()

        meta = fetch_meta(conn)
        collections = fetch_collections(conn)
        entries = fetch_entries(conn)
        entry_ids = [e["id"] for e in entries]
        list_items = fetch_list_items(conn, entry_ids)
        tables = fetch_tables(conn, entry_ids)

        items_by_entry = index_by_entry(list_items)
        tables_by_entry = index_by_entry(tables)

        enriched_entries = []
        for entry in entries:
            enriched = dict(entry)
            enriched["listItems"] = items_by_entry.get(entry["id"], [])
            enriched["tables"] = tables_by_entry.get(entry["id"], [])
            enriched_entries.append(enriched)

        by_collection: dict[str, list] = {}
        for entry in enriched_entries:
            by_collection.setdefault(entry["collection"], []).append(entry)

        return {
            "meta": {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "generator": "scripts/build_site.py",
                "gitSha": git_sha(),
                "schemaVersion": meta.get("schema_version"),
                "dataModel": meta.get("data_model"),
            },
            "project": {
                "title": meta.get("project.title", "Course Business HQ"),
                "description": meta.get("project.description", ""),
            },
            "metrics": compute_metrics(entries, list_items),
            "ui": ui_config,
            "collections": collections,
            "entriesByCollection": by_collection,
        }


def main() -> None:
    payload = build_payload()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
