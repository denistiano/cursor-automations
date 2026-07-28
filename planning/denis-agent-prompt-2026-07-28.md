# Denis → agent prompt (copy-paste, 2026-07-28)

Fill in `[brackets]` and paste into Cursor / #vibe-code for a single agent run.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear a 39-day backlog of founder decisions. Repo: cursor-automations / vibe-coding-101. Data: data/hq.db (actions, tasks, standups).

## Goal
Unblock hiring (PO), office lease shortlist, brand positioning, and HQ automations so agents can ship careers page, social setup, and landing/deck assets.

## Context (already done by agents — do NOT redo)
- PO expanded JD draft: planning/po-jd-expanded-draft-2026-06-19.md (NOT synced — jobs/product-owner body is empty)
- Office scrape 2026-07-28: 1274 listings; picks A/B/C still valid — planning/office-shortlist-validation-2026-07-28.md
- Brand sprint plan + research: planning/brand-sprint-2026-06-19.md, content/brand/creative-brief.md
- HQ Inbox batch template: planning/hq-inbox-unlocks-2026-06-19.md
- Landing vs deck brief: planning/landing-vs-deck-decision-brief.md

## Denis inputs (REPLACE BRACKETS)
1. PO apply method: [email | form URL | LinkedIn Easy Apply]
2. PO first publish channel: [LinkedIn | jobs.bg | network]
3. PO JD: [approve expanded draft 2026-06-19 | paste JD below]
4. Office visits (3 listing IDs or URLs): [11108782, 10481212, 4734755]
5. Brand sprint day 1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[full-time PO | consultant | hybrid]
6. Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft | defer]
7. HQ Inbox: [paste approve batch from hq-inbox-unlocks OR "skip for now"]

## What to do after Denis inputs
1. Update matching actions in data/hq.db (props.status=done, props.reply=…) for each answered item
2. If PO JD approved: write business/jobs/product-owner.md, sync jobs/product-owner, add careers scaffold in web/
3. If office picks confirmed: update planning/office-plovdiv.md + lease comparison table in HQ
4. If brand day1 answered: merge into business/plan positioning sections
5. Upsert standup 2026-07-28 with what unblocked
6. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
7. Summarize what unblocked and remaining blockers (max 15 lines)

Rules: never invent Denis decisions; mark unknowns; minimal focused diffs.
```
