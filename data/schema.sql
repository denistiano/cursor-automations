PRAGMA foreign_keys = ON;

-- Generic HQ data model: collections → entries → list_items / tables
-- See data/ui-config.json for how each collection renders in the dashboard.

CREATE TABLE IF NOT EXISTS meta (
  key TEXT PRIMARY KEY,
  value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS collections (
  slug TEXT PRIMARY KEY,
  label TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  icon TEXT NOT NULL DEFAULT 'folder',
  sort_order INTEGER NOT NULL DEFAULT 0,
  config TEXT NOT NULL DEFAULT '{}'  -- JSON: layout hints for UI/export
);

CREATE TABLE IF NOT EXISTS entries (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  collection TEXT NOT NULL REFERENCES collections(slug) ON DELETE CASCADE,
  parent_id INTEGER REFERENCES entries(id) ON DELETE CASCADE,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  status TEXT,
  owner TEXT,
  body TEXT NOT NULL DEFAULT '',
  props TEXT NOT NULL DEFAULT '{}',  -- JSON blob for flexible fields
  sort_order INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now')),
  UNIQUE(collection, slug)
);

CREATE TABLE IF NOT EXISTS list_items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entry_id INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
  section TEXT NOT NULL DEFAULT 'default',
  text TEXT NOT NULL,
  done INTEGER NOT NULL DEFAULT 0,
  meta TEXT NOT NULL DEFAULT '{}',  -- JSON: priority, roadmap_ref, owner, etc.
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS tables (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entry_id INTEGER NOT NULL REFERENCES entries(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  columns TEXT NOT NULL DEFAULT '[]',  -- JSON array of column keys
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS table_rows (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  table_id INTEGER NOT NULL REFERENCES tables(id) ON DELETE CASCADE,
  cells TEXT NOT NULL DEFAULT '{}',  -- JSON object keyed by column
  sort_order INTEGER NOT NULL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_entries_collection ON entries(collection);
CREATE INDEX IF NOT EXISTS idx_entries_parent ON entries(parent_id);
CREATE INDEX IF NOT EXISTS idx_list_items_entry ON list_items(entry_id);
CREATE INDEX IF NOT EXISTS idx_tables_entry ON tables(entry_id);
CREATE INDEX IF NOT EXISTS idx_table_rows_table ON table_rows(table_id);
