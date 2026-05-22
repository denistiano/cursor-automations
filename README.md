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
| Web | `web/` | Landing page / website code when we build it |
| Automations | `docs/` | Playbooks for Cursor Automations, MCP, SDK |
| Agent context | `.cursor/rules/` | Persistent instructions for agents in this repo |

## How we work

1. **Daily rhythm** — Short standup: done / todo / blockers. Artifacts go in `planning/standups/`.
2. **Deep work** — Competitor scans, business plans, and course design live under `research/` and `business/`.
3. **Ship in git** — Meaningful outputs are committed here so agents and future-you have full context.
4. **Automate with Cursor** — Background agents via [Cursor Automations](https://cursor.com/docs/cloud-agent/automations); see [`docs/cursor-automations-playbook.md`](docs/cursor-automations-playbook.md).

## Cursor stack (quick reference)

- **This repo** — Attach as the automation repo for doc/code workflows.
- **No-repo automations** — Scheduled digests, competitor research, social drafting (MCP + web).
- **Rules** — `.cursor/rules/` for tone, brand, and PM conventions.
- **Skills** — Reusable agent skills in Cursor for recurring tasks.

## Getting started

```bash
# Already initialized — clone or open in Cursor
cursor .
```

Open the automations playbook and pick the first automation to enable (recommended: **Morning standup prep**).

## Status

- [x] Git repository initialized
- [ ] First daily standup template
- [ ] Competitor research template
- [ ] Cursor Automations configured (see playbook)

---

*Private workspace — no remote configured yet.*
