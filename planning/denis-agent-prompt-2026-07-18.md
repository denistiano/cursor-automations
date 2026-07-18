# Denis → agent handoff prompt (2026-07-18)

Copy-paste block for a follow-up agent run after Denis fills placeholders.

---

```
You are the Business + Developer agent for Vibe Coders Academy. Repo: cursor-automations.

## Goal
Unblock launch-critical Denis decisions captured today. After each reply, update matching `actions` in data/hq.db (props.status=done, props.reply=...) and execute downstream agent work. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py

## Context
- PO job post blocked 38+ days: jobs/product-owner body is empty; expanded JD draft at planning/po-jd-expanded-draft-2026-06-19.md
- Brand sprint day 1 overdue since 2026-06-22; starter at planning/brand-day1-starter-2026-07-18.md
- Office shortlist A/B/C re-validated 2026-07-18: planning/office-shortlist-refresh-2026-07-18.md
- HQ Inbox: 4 automations + 3 social drafts still open
- Landing vs deck undecided: planning/landing-vs-deck-decision-brief.md

## Denis inputs (fill before running)
PO_APPLY_METHOD=[email | form URL | LinkedIn Easy Apply]
PO_PUBLISH_CHANNEL=[LinkedIn | jobs.bg | network]
PO_JD=[approve expanded draft 2026-06-19 | paste full JD text]
BRAND_DAY1_ICP=[...]
BRAND_DAY1_NOT_FOR=[...]
BRAND_DAY1_SECRET_SAUCE=[bullet1; bullet2; bullet3]
BRAND_DAY1_OPS=[full-time PO | consultant | hybrid]
OFFICE_PICKS=[A,B,C | paste 3 URLs | budget update text]
HQ_APPROVALS=[list which approve:* and automation replies Denis sent]
PATH_CHOICE=[deck-first | landing-first | hybrid]
PRIMARY_CTA=[waitlist | LinkedIn | early bird]

## Execute (in order)
1. If PO_* filled → write business/jobs/product-owner.md, sync jobs/product-owner in hq.db, scaffold careers section in web/, draft LinkedIn PO announcement in social collection.
2. If BRAND_DAY1_* filled → merge positioning into business/plan and business/messaging; mark brand sprint day 1 action done; queue day 2 input.
3. If OFFICE_PICKS filled → create HQ lease comparison table + prepare landlord outreach from planning/office-landlord-outreach-2026-06-15.md.
4. If HQ_APPROVALS filled → mark matching approve actions done; note social account creation unblocked.
5. If PATH_CHOICE filled → deck export OR landing scaffold per planning/landing-vs-deck-decision-brief.md.

## Rules
- Never invent Denis decisions — only act on filled placeholders above.
- Do not publish externally; drafts and HQ updates only.
- Post summary to #vibe-standup with what unblocked and next steps.
```
