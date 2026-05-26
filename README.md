# Vibe Coding 101 — Course Business HQ

Central workspace for building a **course program business from scratch**: planning, business analysis, landing pages, automations, content, and project management.

This repo is the single source of truth for strategy, research, and assets. **You (Denis)** are the boss and lecturer; **Cursor agents** act as project manager and business assistant.

## What lives here

| Area | Path | Purpose |
|------|------|---------|
| Planning & PM | `planning/` | Roadmaps, standups, todos, decisions |
| Business | `business/` | Business plans, financial models, positioning |
| Research | `research/` | Competitor analysis, market notes, citations |
| Content | `content/` | Social posts, newsletters, course copy drafts |
| Web | `web/` | GitHub Pages HQ dashboard and future landing page code |
| Automations | `docs/` | Playbooks, Slack/MCP setup, automation prompts |
| Agent context | `.cursor/rules/` | Persistent instructions for agents in this repo |
| MCP config | `.cursor/mcp.json` | Slack, Notion, Linear, Exa, Buffer |

## How we work

1. **Daily rhythm** — Short standup: done / todo / blockers. Artifacts go in `planning/standups/`.
2. **Deep work** — Competitor scans, business plans, and course design live under `research/` and `business/`.
3. **Ship in git** — Meaningful outputs are committed here so agents and future-you have full context.
4. **Automate with Cursor** — Slack-first interface; see [`docs/slack-and-mcp-setup.md`](docs/slack-and-mcp-setup.md) and [`docs/cursor-automations-playbook.md`](docs/cursor-automations-playbook.md).

## Cursor stack (quick reference)

- **This repo** — Attach as the automation repo for doc/code workflows.
- **No-repo automations** — Scheduled digests, competitor research, social drafting (MCP + web).
- **Rules** — `.cursor/rules/` for tone, brand, and PM conventions.
- **Skills** — Reusable agent skills in Cursor for recurring tasks.

## GitHub Pages HQ

This repo includes a no-framework static dashboard in `web/` for browsing the structured business context without opening every markdown file.

```bash
node scripts/build-site-data.js
python3 -m http.server 8080 --directory web
```

- UI: `web/index.html`, `web/styles.css`, `web/app.js`
- Structured data: `web/data/site.json`
- Data generator: `scripts/build-site-data.js`
- Deploy workflow: `.github/workflows/deploy-pages.yml`

The automation-owned markdown paths remain the source of truth. The dashboard reads generated JSON and does not move or rewrite `planning/`, `business/`, `research/`, `content/`, or `docs/automations/`.

## Getting started

```bash
# Already initialized — clone or open in Cursor
cursor .
```

Follow **[Slack + MCP setup](docs/slack-and-mcp-setup.md)** — Phase 1–4 (~1 hour).

## Status

- [x] Git repository initialized
- [x] Cursor rules, MCP config, templates
- [x] First standup + automation prompt files
- [x] GitHub Pages HQ dashboard scaffold
- [ ] Slack channels + Cursor integration (Denis)
- [ ] Cursor Automations live in UI (copy from `docs/automations/`)

---

*Private workspace — automation artifacts and dashboard data are versioned in git.*
