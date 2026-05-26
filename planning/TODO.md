# TODO — Vibe Coding 101

## Now — Denis (manual, ~1 hour)

- [ ] Create Slack channels: `#vibe-standup`, `#vibe-research`, `#vibe-business`, `#vibe-social`, `#vibe-inbox`
- [ ] Connect Slack at [cursor.com/dashboard/integrations](https://www.cursor.com/dashboard/integrations)
- [ ] Connect MCPs: Slack + Exa minimum ([setup guide](../docs/slack-and-mcp-setup.md))
- [ ] Create automation: Morning standup ([prompt](../docs/automations/01-morning-standup.md))
- [ ] Fill `research/competitors/COMPETITORS.md` (5–10 names)
- [ ] Fill `business/approved-messaging.md` (title + one-liner)

## Now — Agent (after Denis unblocks)

- [ ] First competitor report when COMPETITORS.md has entries
- [ ] Draft 3 LinkedIn posts after messaging approved
- [ ] Expand `business/plan-v1.md` executive summary

## Done

- [x] Git repo + README
- [x] Automations playbook
- [x] `.cursor/rules/` (PM, brand, research, social)
- [x] `.cursor/mcp.json` + `.env.example`
- [x] Templates + first standup (2026-05-22)
- [x] Slack/MCP setup doc + 4 automation prompt files
- [x] GitHub Pages HQ dashboard scaffold (`web/`) + JSON data generator (`scripts/build-site-data.js`)

## Next

- [ ] Automations 02–04 in Cursor UI
- [ ] GitHub remote + attach repo to automations
- [ ] Buffer MCP + publish automation (draft-only until approved)
- [ ] Enable GitHub Pages with GitHub Actions source after this dashboard PR merges
- [ ] Public landing page in `web/` (separate from HQ dashboard)

## Blockers

- Slack channels + Cursor integration required before automations fire
- GitHub remote optional for local agent work; required for cloud automation repo attach
