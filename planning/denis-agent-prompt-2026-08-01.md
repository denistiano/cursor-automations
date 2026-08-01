# Denis → agent prompt pack — 2026-08-01

Copy-paste the block below into a new Cursor agent run after filling `[...]` placeholders.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear his HQ Inbox blockers in one session.

## Context
- Repo: vibe-coding-101 / cursor-automations — HQ dashboard in web/, data in data/hq.db
- Course: practitioner-first AI/coding cohort in Plovdiv (Vibe Coders Academy)
- PO role needs to be published; office search active; brand sprint inputs overdue
- Agents must NOT invent completed work or official JD/legal text

## Denis inputs (fill before running)
PO_APPLY_METHOD=[email | form URL | LinkedIn Easy Apply]
PO_FIRST_CHANNEL=[LinkedIn | jobs.bg | network]
PO_JD=[paste approved JD text OR "approve planning/po-jd-expanded-draft-2026-06-19.md with: remote=X%, type=part-time, comp=RANGE, duration=6-8 weeks"]
OFFICE_VISITS=[A,B′,C | paste 3 URLs from planning/office-shortlist-validation-2026-08-01.md]
LANDING_PATH=[deck-first | landing-first | hybrid one-pager]
LANDING_CTA=[waitlist URL | LinkedIn DM | early bird — price/seats if early bird]
HQ_INBOX_BATCH=[yes — approve all 7 | list which to skip]
BRAND_DAY1=[ICP= — NOT for= — secret sauce= — ops=] (optional this run)

## What to achieve
1. Update hq.db actions: mark matching input/approve actions done with Denis replies in props.reply
2. If PO inputs provided: write business/jobs/product-owner.md, sync jobs/product-owner, scaffold careers in web/
3. If office picks provided: update planning/office-plovdiv.md with finalists + start lease comparison
4. If landing path provided: scaffold hero + CTA in web/ OR export deck notes per path
5. If HQ inbox batch=yes: set approve actions to done
6. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
7. Upsert standup 2026-08-01 with what unblocked

## How (if known)
- PO JD draft: planning/po-jd-expanded-draft-2026-06-19.md
- Office validation: planning/office-shortlist-validation-2026-08-01.md
- HQ inbox batch: planning/hq-inbox-unlocks-2026-06-19.md
- Landing brief: planning/landing-vs-deck-decision-brief.md
- Follow .cursor/rules/pm-assistant.mdc — never invent completed work

## Missing input (Denis must supply above)
- PO apply method + channel + JD approval
- Office visit confirmation (A/B′/C)
- Landing vs deck path + CTA
- HQ inbox approval batch (7 items)
- Brand sprint day 1 (optional — unblocks marketing plan)
```
