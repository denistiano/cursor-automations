#!/usr/bin/env python3
"""Shared SQLite helpers for the generic HQ data model."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "hq.db"
SCHEMA_PATH = ROOT / "data" / "schema.sql"
UI_CONFIG_PATH = ROOT / "data" / "ui-config.json"


def json_loads(value: str | None, default: Any = None) -> Any:
    if not value:
        return default if default is not None else {}
    return json.loads(value)


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: Path | None = None, force: bool = False) -> None:
    path = db_path or DB_PATH
    if path.exists() and not force:
        with connect(path) as conn:
            if conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='collections'"
            ).fetchone():
                return
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with connect(path) as conn:
        conn.executescript(schema)
        conn.commit()


def set_meta(conn: sqlite3.Connection, key: str, value: str) -> None:
    conn.execute(
        "INSERT INTO meta(key, value) VALUES(?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )


def upsert_collection(
    conn: sqlite3.Connection,
    slug: str,
    label: str,
    description: str = "",
    icon: str = "folder",
    sort_order: int = 0,
    config: dict | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO collections(slug, label, description, icon, sort_order, config)
        VALUES(?, ?, ?, ?, ?, ?)
        ON CONFLICT(slug) DO UPDATE SET
          label=excluded.label,
          description=excluded.description,
          icon=excluded.icon,
          sort_order=excluded.sort_order,
          config=excluded.config
        """,
        (slug, label, description, icon, sort_order, json_dumps(config or {})),
    )


def upsert_entry(
    conn: sqlite3.Connection,
    collection: str,
    slug: str,
    title: str,
    *,
    parent_id: int | None = None,
    status: str | None = None,
    owner: str | None = None,
    body: str = "",
    props: dict | None = None,
    sort_order: int = 0,
) -> int:
    conn.execute(
        """
        INSERT INTO entries(collection, parent_id, slug, title, status, owner, body, props, sort_order, updated_at)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ON CONFLICT(collection, slug) DO UPDATE SET
          parent_id=excluded.parent_id,
          title=excluded.title,
          status=excluded.status,
          owner=excluded.owner,
          body=excluded.body,
          props=excluded.props,
          sort_order=excluded.sort_order,
          updated_at=datetime('now')
        """,
        (
            collection,
            parent_id,
            slug,
            title,
            status,
            owner,
            body,
            json_dumps(props or {}),
            sort_order,
        ),
    )
    row = conn.execute(
        "SELECT id FROM entries WHERE collection=? AND slug=?",
        (collection, slug),
    ).fetchone()
    return int(row["id"])


def replace_list_items(
    conn: sqlite3.Connection,
    entry_id: int,
    section: str,
    items: list[dict],
) -> None:
    conn.execute(
        "DELETE FROM list_items WHERE entry_id=? AND section=?",
        (entry_id, section),
    )
    for index, item in enumerate(items):
        conn.execute(
            """
            INSERT INTO list_items(entry_id, section, text, done, meta, sort_order)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                entry_id,
                section,
                item.get("text", ""),
                1 if item.get("done") else 0,
                json_dumps(item.get("meta") or {}),
                item.get("sort_order", index),
            ),
        )


def replace_table(
    conn: sqlite3.Connection,
    entry_id: int,
    name: str,
    columns: list[str],
    rows: list[dict],
    sort_order: int = 0,
) -> int:
    conn.execute(
        "DELETE FROM table_rows WHERE table_id IN (SELECT id FROM tables WHERE entry_id=? AND name=?)",
        (entry_id, name),
    )
    conn.execute(
        "DELETE FROM tables WHERE entry_id=? AND name=?",
        (entry_id, name),
    )
    conn.execute(
        "INSERT INTO tables(entry_id, name, columns, sort_order) VALUES(?, ?, ?, ?)",
        (entry_id, name, json_dumps(columns), sort_order),
    )
    table_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    for index, row in enumerate(rows):
        cells = {col: row.get(col, "") for col in columns}
        conn.execute(
            "INSERT INTO table_rows(table_id, cells, sort_order) VALUES(?, ?, ?)",
            (table_id, json_dumps(cells), index),
        )
    return int(table_id)


def entry_by_slug(conn: sqlite3.Connection, collection: str, slug: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM entries WHERE collection=? AND slug=?",
        (collection, slug),
    ).fetchone()


def load_ui_config() -> dict:
    return json.loads(UI_CONFIG_PATH.read_text(encoding="utf-8"))
