# Denis → agent prompt (copy-paste)

**Use:** Paste into a new agent session after filling `[PLACEHOLDERS]`. One shot unblocks PO, office, inbox, and brand sprint.

---

## Ready-to-run prompt

```
You are the Business + PM agent for Vibe Coders Academy (repo: cursor-automations).

Context: Vibe Coders Academy is a practitioner-first dev cohort in Plovdiv using Cursor, MCP, and automations. HQ data lives in data/hq.db. Denis is the owner. Do not invent completed work or official terms.

## Goals this session

1. **PO hiring** — After Denis inputs below, commit approved JD to business/jobs/product-owner.md, sync jobs/product-owner in hq.db, scaffold careers section in web/, draft LinkedIn PO announcement in social collection.

2. **Office Plovdiv** — After Denis confirms visit picks, lock finalists in planning/office-plovdiv.md, create lease comparison table in HQ, prep visit checklist (especially monthly vs per-session for listing 4734755).

3. **HQ Inbox** — After Denis approves automations + social drafts, update matching actions (props.status=done), note waitlist URL still TBD until landing/deck path chosen.

4. **Brand sprint** — After Denis replies to days 1–4, update business/messaging and business/plan entries; unblock creative brief and landing copy.

## Denis inputs (fill before running)

PO apply method: [EMAIL | FORM_URL | LINKEDIN_EASY_APPLY]
PO publish first on: [LINKEDIN | JOBS.BG | NETWORK]
PO JD: [APPROVE expanded draft 2026-06-19 | PASTE_FULL_TEXT_BELOW]
PO remote %: [___] | Type: [part-time/full-time/contract] | Compensation: [___ BGN/EUR range]

Office visits confirmed: [A=11108782, B′=11081121, C=4734755 | OR paste 3 URLs]

HQ Inbox batch (yes/no each):
- approve: linkedin-page-bio [Y/N]
- approve: linkedin-first-post [Y/N]
- approve: x-bio-and-first-post [Y/N]
- standup automation [Y/N]
- competitor research automation [Y/N]
- business plan automation [Y/N]
- social drafts automation [Y/N]

Brand sprint day 1: ICP=[___] NOT for=[___] secret sauce=[___] ops=[___]
Brand sprint day 2: visual=[A/B/C] one-liner=[___] CTA=[___] tone OK=[Y/N]
Brand sprint day 3: channels=[ranked list] facebook=[strategy] path=[deck-first|landing-first|hybrid]
Brand sprint day 4: budget tier=[___] early bird=[price/date/seats] plan=[approve draft Y/N]

Landing vs deck path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird]

## After changes

Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
Post summary to #vibe-standup prefixed: 🎯 *PM Agent* |
```
