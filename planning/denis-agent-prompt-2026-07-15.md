# Denis → agent batch prompt (2026-07-15)

Copy-paste into a new Cursor agent run. Replace `[BRACKETED]` placeholders with your answers.

---

```
You are executing Denis's decisions for Vibe Coders Academy. Repo: denistiano/cursor-automations.

## Context
PM standup 2026-07-15. Multiple blockers open since 2026-06-10 (day 35). Agent artifacts are ready; only Denis inputs are missing.

## Goal
Process Denis's batch replies, update data/hq.db (actions → done, tasks unblocked), commit approved content, run python3 scripts/sync_actions.py && python3 scripts/build_site.py.

## Denis inputs (fill in)

### 1. PO hiring (priority 1)
PO apply method: [email | form URL | LinkedIn Easy Apply]
First publish channel: [LinkedIn | jobs.bg | network]
JD decision: [approve expanded draft 2026-06-19 | paste full JD text below]
[PASTE JD TEXT IF NOT APPROVING DRAFT]

### 2. Brand sprint day 1
ICP: [one sentence OR "defaults OK"]
NOT for: [anti-audience OR skip if defaults OK]
Secret sauce: [3 bullets OR skip if defaults OK]
Ops model: [full-time PO | consultant | hybrid OR skip if defaults OK]

### 3. Office Plovdiv
Visit picks: [A, B, C | paste 3 URLs]
Budget confirmed: [<800 EUR/mo | other: ___]

### 4. HQ Inbox
Approvals: [paste batch from planning/hq-inbox-impact-2026-07-15.md OR list which to approve]

### 5. Landing vs deck
Path: [deck-first | landing-first | hybrid]
CTA: [waitlist | LinkedIn | early bird]
Brand colors: [approve draft | defer]

## How to execute
1. For each input above, find matching action in hq.db actions collection; set props.status=done, props.reply=Denis text.
2. If PO JD approved → write business/jobs/product-owner.md from planning/po-jd-expanded-draft-2026-06-19.md (fill apply method).
3. If brand day1 answered → update business/plan positioning sections in hq.db.
4. If office picks given → update planning/office-plovdiv.md with finalists.
5. If path chosen → note in tasks; scaffold landing OR export deck per choice.
6. Upsert standup 2026-07-15 with what unblocked.
7. Run sync_actions.py && build_site.py; commit and push.

## Rules
- Never invent Denis decisions — only process filled placeholders.
- Preserve existing manual edits in hq.db.
- Follow .cursor/rules/pm-assistant.mdc.
```
