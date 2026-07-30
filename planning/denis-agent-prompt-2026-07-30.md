# Denis → agent batch prompt (2026-07-30)

Copy the block below into a new agent run after filling in `[PLACEHOLDER]` sections.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear launch blockers in the vibe-coding-101 / cursor-automations repo.

## Context
- Practitioner-first AI coding cohort (Cursor, agents, MCP, automations) in Plovdiv, Bulgaria
- Course name locked: Vibe Coders Academy · domain vibe-coders.academy registered
- HQ data: data/hq.db · planning artifacts in planning/
- Last standup: 2026-06-19 · 41-day gap · no Denis inbox replies since 2026-06-10
- Agent has refreshed office data (1268 listings, 2026-07-27) and validated shortlist A/B/C

## Goal
Unblock PO hiring, office search, public-facing assets, and automations in one coordinated pass.

## Denis inputs (fill before running)

### 1. PO hiring (P1 blocker)
- Apply method: [PLACEHOLDER: email | Google Form URL | LinkedIn Easy Apply]
- First publish channel: [PLACEHOLDER: LinkedIn personal | jobs.bg | network/Slack]
- JD decision: [PLACEHOLDER: approve planning/po-jd-expanded-draft-2026-06-19.md | paste official JD below]

[PASTE OFFICIAL JD HERE IF NOT APPROVING DRAFT]

### 2. Office Plovdiv
- Visit picks: [PLACEHOLDER: A,B,C | or paste 3 alo.bg URLs]
- Notes on training hall (4734755) pricing: [PLACEHOLDER: monthly confirmed yes/no | skip C]
- Alternate if A unavailable: [PLACEHOLDER: 10769362 Kapana €450 | other URL]

### 3. HQ Inbox approvals
- Social drafts approved: [PLACEHOLDER: yes — linkedin-page-bio, linkedin-first-post, x-bio-and-first-post | no — list edits]
- Automations green-lit: [PLACEHOLDER: all four | standup only | list which]
- Social accounts created: [PLACEHOLDER: LinkedIn done | X done | not yet]

### 4. Go-to-market path
- Path choice: [PLACEHOLDER: deck-first | landing-first | hybrid one-pager]
- Primary CTA: [PLACEHOLDER: waitlist URL | LinkedIn DM | early bird — needs price/seats]
- Brand colors/logo: [PLACEHOLDER: approve draft | defer | paste direction]

### 5. Brand sprint (optional — sprint ended 2026-06-22)
- Day 1: ICP=[PLACEHOLDER] NOT for=[PLACEHOLDER] secret sauce=[PLACEHOLDER] ops model=[PLACEHOLDER]
- Day 2: visual=[PLACEHOLDER] one-liner=[PLACEHOLDER] CTA=[PLACEHOLDER]
- Day 3: channels=[PLACEHOLDER] facebook=[PLACEHOLDER] rhythm=[PLACEHOLDER] path=[PLACEHOLDER]
- Day 4: budget tier=[PLACEHOLDER] early bird=[PLACEHOLDER] 90-day plan=[PLACEHOLDER]

## What the agent should do after inputs
1. Update matching actions in data/hq.db (props.status=done, props.reply=...) for each answered input
2. If PO approved: write business/jobs/product-owner.md, sync jobs/product-owner, scaffold careers in web/
3. If office picks confirmed: update planning/office-plovdiv.md + lease comparison in HQ
4. If path chosen: deck export OR landing scaffold per planning/landing-vs-deck-decision-brief.md
5. If brand sprint answered: merge into planning/brand-marketing-plan-draft-2026-06-19.md + business/plan
6. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
7. Post ≤15 line summary to #vibe-standup with what unblocked and next agent steps

## Rules
- Never invent completed work or pricing/legal terms
- Mark unknowns explicitly
- Minimal focused diffs; match repo conventions
```
