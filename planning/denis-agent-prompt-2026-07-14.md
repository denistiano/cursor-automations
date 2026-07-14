# Denis → agent batch prompt (2026-07-14)

Copy the block below into a new Cursor agent chat **after** filling `[PLACEHOLDER]` fields from HQ Inbox replies.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear launch blockers. Repo: denistiano/cursor-automations (vibe-coding-101). Data: data/hq.db. Rules: never invent completed work; minimal focused diffs; run `python3 scripts/sync_actions.py && python3 scripts/build_site.py` after hq.db changes.

## Goal
Unblock PO hiring, brand positioning, HQ Inbox approvals, office visits, and landing/deck path so agents can ship careers page, social setup, and marketing assets.

## Context (already done by PM agent — 2026-07-14)
- PO expanded JD draft: planning/po-jd-expanded-draft-2026-06-19.md (NOT synced — awaiting approval)
- PO checklist + LinkedIn stub: planning/po-publish-checklist-2026-07-14.md
- Office A/B/C re-verified + re-ranked: planning/office-shortlist-refresh-2026-07-14.md
- Brand day 1 brief (+22 days): planning/brand-sprint-day1-decision-brief-2026-07-14.md
- Landing vs deck pack: planning/landing-path-decision-pack-2026-07-14.md
- HQ Inbox batch: planning/hq-inbox-impact-2026-07-14.md

## Denis inputs (fill before running — only missing pieces)
1. PO apply method + first channel: [PO_APPLY_REPLY e.g. Google Form URL — publish first on: LinkedIn]
2. PO JD: [approve expanded draft 2026-06-19 | paste full JD text]
3. Brand day 1: [BRAND_DAY1_REPLY or "use agent defaults from brief"]
4. HQ Inbox: [paste approve batch from hq-inbox-impact doc or "done in Slack"]
5. Office visits (3 picks): [OFFICE_PICKS e.g. Kapana 11108782, широк център 10481212, зала 4734755]
6. Path choice: [deck-first | landing-first | hybrid one-pager] — CTA: [waitlist | LinkedIn | early bird]

## Execute (in order; skip steps whose input is still blank)
1. If PO inputs present → write business/jobs/product-owner.md, sync jobs/product-owner in hq.db, careers scaffold in web/, LinkedIn PO announcement draft in social collection (props.approved=false).
2. If brand day 1 present → merge into planning/brand-marketing-plan-draft-2026-06-19.md + business/messaging; mark action props.status=done with props.reply.
3. If HQ Inbox batch confirmed → update matching actions + automations/social props.approved=true where applicable.
4. If office picks present → update planning/office-plovdiv.md, lease comparison table in hq.db office collection.
5. If path choice present → hybrid one-pager in web/ OR deck export notes per landing-path-decision-pack.
6. Update standup 2026-07-14 in planning/standups/ and hq.db; sync_actions + build_site; summarize what unblocked.
```
