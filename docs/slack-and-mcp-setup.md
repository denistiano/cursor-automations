# Slack + MCP implementation checklist

**Goal:** Slack is the daily interface; this repo + Cursor Automations do the work.

## Phase 1 — Slack workspace (15 min)

Create **public** channels (Cursor automations only see public channels today):

| Channel | Purpose | Trigger examples |
|---------|---------|------------------|
| `#vibe-standup` | Daily PM | `standup`, or cron-only posts |
| `#vibe-research` | Competitor / market | `competitor: Maven`, `research: X` |
| `#vibe-business` | Plans & analysis | `plan`, `business update` |
| `#vibe-social` | Content drafts | `draft: 3 linkedin posts` |
| `#vibe-inbox` | Ad-hoc `@Cursor` | `@Cursor …` |

Invite the **Cursor** app to each channel (`/invite @Cursor`).

## Phase 2 — Cursor integrations (20 min)

1. [Cursor → Integrations](https://www.cursor.com/dashboard/integrations) → **Connect Slack**
2. [Cloud Agents dashboard](https://www.cursor.com/dashboard/cloud-agents) → enable privacy/display settings you want
3. In `#vibe-inbox`, run `@Cursor settings` → set default repo to **vibe-coding-101** (when GitHub is connected) or use local path for now

## Phase 3 — MCP in Cursor IDE (15 min)

Open **Cursor Settings → MCP**. Connect (OAuth where prompted):

| MCP | How | Required? |
|-----|-----|-----------|
| **Slack** | Marketplace → [Slack plugin](https://cursor.com/marketplace/slack) or `.cursor/mcp.json` | Recommended |
| **Notion** | Marketplace / `https://mcp.notion.com/sse` | Optional |
| **Linear** | Marketplace / `https://mcp.linear.app/sse` | Optional |
| **Exa** | URL in `.cursor/mcp.json` | For research |
| **Buffer** | Copy `.env.example` → `.env`, add token | When ready to post |

**Cloud automations:** Repeat MCP enablement in [cursor.com/agents](https://cursor.com/agents) → MCP dropdown (same servers for background agents).

## Phase 4 — Automations (30 min)

Create four automations at [cursor.com/automations/new](https://cursor.com/automations/new). Copy prompts from:

- `docs/automations/01-morning-standup.md`
- `docs/automations/02-competitor-research.md`
- `docs/automations/03-business-plan.md`
- `docs/automations/04-social-content.md`

**Shared settings:**

- **Repo:** `vibe-coding-101` (attach when GitHub remote exists; until then use local sync or push to GitHub first)
- **Slack trigger → From:** `Anyone in the channel`
- **Memories:** On for standup + research
- **Model:** Default or Sonnet-class for plans; Haiku OK for digests if cost-sensitive

## Phase 5 — Seed data (10 min)

1. Edit `research/competitors/COMPETITORS.md` — add real competitors
2. Edit `business/approved-messaging.md` — title + one-liner
3. Post `standup` in `#vibe-standup` to test Slack trigger (after automation exists)

## Verification

- [ ] Cursor app in all `#vibe-*` channels
- [ ] MCP Slack + Exa show green/connected in Settings
- [ ] Morning automation ran once (check `planning/standups/`)
- [ ] `competitor: test` in `#vibe-research` produced a file (or agent reply)
- [ ] Social draft created with `approved: false`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| "Link Cursor account" when posting | You're using `@Cursor`; use plain message for automations |
| Automation doesn't fire | Check trigger channel, keyword filter, "Anyone in channel" |
| Bot message doesn't trigger 2nd automation | Known limitation — you post the follow-up, or use cron/webhook |
| MCP works locally but not in automation | Enable same MCP on cloud agents dashboard |

See also: [`cursor-automations-playbook.md`](cursor-automations-playbook.md)
