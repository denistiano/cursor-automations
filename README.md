# Vibe Coders Academy — Course Business HQ

Central workspace for building a **course program business from scratch**: planning, business analysis, landing pages, automations, content, and project management.

**Data lives in SQLite** (`data/hq.db`). The GitHub Pages dashboard reads exported JSON. Agents update the database — not scattered markdown files.

**Planned public domain:** `vibe-coders.academy` — not active yet.

## Architecture

```
data/hq.db          ← source of truth (generic collections model)
data/schema.sql     ← 6 tables: collections, entries, list_items, tables, table_rows, meta
data/ui-config.json ← how each collection renders in the dashboard
        ↓
scripts/build_site.py  →  web/data/site.json  →  web/ (static UI)
        ↑
GitHub Actions on push
```

### Generic data model

| Table | Purpose |
|-------|---------|
| `collections` | Namespaces: tasks, standups, roadmap, business, office, research, jobs, names, automations, social |
| `entries` | Any record: title, body, status, owner, flexible `props` JSON |
| `list_items` | Checklists and bullet lists attached to entries (sections: `items`, `done`, `today`, …) |
| `tables` + `table_rows` | Structured tables (watchlists, phases, pricing, shortlists) |
| `meta` | Project title, description, schema version |

Add a new dashboard section by inserting a collection + entries — no schema migration required.

## Commands

```bash
# Export dashboard JSON (also run in CI)
python3 scripts/build_site.py

# One-time import from legacy markdown (if files exist)
python3 scripts/seed_from_md.py

# CLI helpers
python3 scripts/hq.py init
python3 scripts/hq.py show tasks
python3 scripts/hq.py add-item tasks blockers "New blocker text" --section items --meta '{"owner":"Denis"}'

# Local preview
python3 -m http.server 8080 --directory web
```

## What lives here

| Area | Collection | Purpose |
|------|------------|---------|
| Planning | `tasks`, `roadmap`, `standups` | TODOs, launch path, daily standups |
| Business | `business`, `names` | Plan, messaging, course name options |
| Ops | `office`, `jobs` | Office search, PO job posting |
| Research | `research` | Competitor watchlist and reports |
| Content | `social` | Draft posts (approval in `props.approved`) |
| Automations | `automations` | Cursor prompt inventory |
| Agent context | `.cursor/rules/` | Persistent agent instructions |
| MCP config | `.cursor/mcp.json` | Slack, Notion, Linear, Exa, Buffer |

Human setup docs (not in DB): `docs/slack-and-mcp-setup.md`, `docs/cursor-automations-playbook.md`.

## GitHub Pages HQ

Static dashboard in `web/` — sidebar navigation, search, collection-driven layouts.

Deploy workflow: `.github/workflows/deploy-pages.yml` (Python build → GitHub Pages).

## Getting started

```bash
cursor .
python3 scripts/build_site.py
python3 -m http.server 8080 --directory web
```

Follow **[Slack + MCP setup](docs/slack-and-mcp-setup.md)** for integrations.

---

*Private workspace — `data/hq.db` and generated `web/data/site.json` are versioned in git.*
