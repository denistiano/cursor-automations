# Denis → agent batch prompt (2026-07-13)

Copy the block below into a new Cursor agent chat **after** filling `[PLACEHOLDER]` fields from HQ Inbox replies.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear launch blockers. Repo: denistiano/cursor-automations (vibe-coding-101). Data: data/hq.db. Rules: never invent completed work; minimal focused diffs; run `python3 scripts/sync_actions.py && python3 scripts/build_site.py` after hq.db changes.

## Goal
Unblock PO hiring, office visits, brand positioning, and HQ Inbox approvals so agents can ship careers page, social setup, and marketing assets.

## Context (already done by PM agent)
- PO expanded JD draft: planning/po-jd-expanded-draft-2026-06-19.md (NOT synced — awaiting approval)
- Office A/B/C verified live 2026-07-13: planning/office-shortlist-verify-2026-07-13.md
- Brand day 1 brief with suggested defaults: planning/brand-sprint-day1-decision-brief-2026-07-13.md
- Landing vs deck brief: planning/landing-vs-deck-decision-brief.md
- HQ Inbox batch: planning/hq-inbox-impact-2026-07-13.md

## Denis inputs (fill before running)
1. PO apply method + first channel: [PO_APPLY_REPLY]
2. PO JD: [approve expanded draft 2026-06-19 | paste full JD text]
3. Office visits (3 picks): [OFFICE_PICKS e.g. Kapana 11108782, широк център 10481212, зала 4734755]
4. Brand day 1: [BRAND_DAY1_REPLY or "use agent defaults from brief"]
5. Path choice: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird]
6. HQ Inbox: [paste approve batch from hq-inbox-impact doc or "done in Slack"]

## Execute (in order, skip if input missing)
1. If PO inputs present → write business/jobs/product-owner.md, sync jobs/product-owner, careers scaffold in web/, LinkedIn PO announcement draft in social collection.
2. If office picks present → update planning/office-plovdiv.md, lease comparison table entry in hq.db office collection.
3. If brand day 1 present → merge into planning/brand-marketing-plan-draft-2026-06-19.md + business/messaging props; mark matching action props.status=done with props.reply.
4. If path choice present → deck export notes OR web/ landing hero scaffold per landing-vs-deck brief.
5. For each HQ Inbox approval Denis confirms → update actions + automations/social props.approved=true where applicable.
6. Update today's standup in planning/standups/ and hq.db; sync_actions + build_site; summarize what unblocked.
```
