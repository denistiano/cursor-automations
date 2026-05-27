#!/usr/bin/env python3
"""CLI for HQ database operations (agents and local dev)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_site import main as build_main
from hq_db import connect, init_db, json_dumps, json_loads, replace_list_items, upsert_entry
from seed_from_md import seed_all
from sync_actions import sync_all as sync_actions_all


def cmd_init(args: argparse.Namespace) -> None:
    init_db(force=args.force)
    print("Database initialized.")


def cmd_seed(args: argparse.Namespace) -> None:
    seed_all(force=args.force)


def cmd_build(_args: argparse.Namespace) -> None:
    build_main()


def cmd_sync_actions(_args: argparse.Namespace) -> None:
    sync_actions_all()


def cmd_show(args: argparse.Namespace) -> None:
    init_db()
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT e.collection, e.slug, e.title, e.status, e.owner, e.props
            FROM entries e
            WHERE e.collection=?
            ORDER BY e.sort_order, e.id
            """,
            (args.collection,),
        ).fetchall()
        for row in rows:
            props = json_loads(row["props"])
            print(f"- [{row['collection']}/{row['slug']}] {row['title']} status={row['status']} props={json.dumps(props)}")


def cmd_add_item(args: argparse.Namespace) -> None:
    init_db()
    with connect() as conn:
        entry = conn.execute(
            "SELECT id FROM entries WHERE collection=? AND slug=?",
            (args.collection, args.entry),
        ).fetchone()
        if not entry:
            raise SystemExit(f"Entry not found: {args.collection}/{args.entry}")
        items = conn.execute(
            "SELECT text, done, meta, sort_order FROM list_items WHERE entry_id=? AND section=? ORDER BY sort_order",
            (entry["id"], args.section),
        ).fetchall()
        payload = [
            {
                "text": row["text"],
                "done": bool(row["done"]),
                "meta": json_loads(row["meta"]),
                "sort_order": row["sort_order"],
            }
            for row in items
        ]
        payload.append({"text": args.text, "done": args.done, "meta": json.loads(args.meta or "{}")})
        replace_list_items(conn, entry["id"], args.section, payload)
        conn.commit()
    print(f"Added list item to {args.collection}/{args.entry}#{args.section}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Vibe Coding 101 HQ database CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_init = sub.add_parser("init", help="Create schema")
    p_init.add_argument("--force", action="store_true")
    p_init.set_defaults(func=cmd_init)

    p_seed = sub.add_parser("seed", help="Import legacy markdown into SQLite")
    p_seed.add_argument("--force", action="store_true")
    p_seed.set_defaults(func=cmd_seed)

    p_build = sub.add_parser("build", help="Export web/data/site.json")
    p_build.set_defaults(func=cmd_build)

    p_sync = sub.add_parser("sync-actions", help="Rebuild actions collection from tasks/blockers")
    p_sync.set_defaults(func=cmd_sync_actions)

    p_show = sub.add_parser("show", help="List entries in a collection")
    p_show.add_argument("collection")
    p_show.set_defaults(func=cmd_show)

    p_add = sub.add_parser("add-item", help="Append a list item to an entry")
    p_add.add_argument("collection")
    p_add.add_argument("entry")
    p_add.add_argument("text")
    p_add.add_argument("--section", default="items")
    p_add.add_argument("--done", action="store_true")
    p_add.add_argument("--meta", default="{}")
    p_add.set_defaults(func=cmd_add_item)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
