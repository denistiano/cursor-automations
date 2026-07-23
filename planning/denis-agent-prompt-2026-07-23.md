# Denis batch agent prompt — 2026-07-23

Copy everything below the line into a new Cursor agent chat. Replace `[BRACKETED]` placeholders with your answers, then run.

---

You are helping Denis (founder, Vibe Coders Academy) clear **standup backlog** in one session. Repo: cursor-automations. Data: `data/hq.db`.

## Context

- Last standup: **2026-07-22**. No Denis inbox replies since **2026-06-10** (day 43+).
- **P1 blocker:** PO job — `jobs/product-owner` body is empty; fast-track at `planning/po-apply-fast-track-2026-07-21.md` (branch `09f0`).
- **Office:** Live re-check 2026-07-23 — Kapana **11108782** + широк център **10481212** still live (missed by 07-22 scrape). B expires **~11 days**. See `planning/office-shortlist-validation-2026-07-23.md`.
- **HQ Inbox:** 4 automations + 3 social drafts still `open`.
- **Brand sprint:** Days 1–4 unanswered since 2026-06-22 (31 days stale).
- **Path:** Landing vs deck not chosen — `planning/landing-vs-deck-decision-brief.md`.

## What we need to achieve

Unblock hiring (PO), office search (contact A+B this week), marketing automations, brand positioning, and public-facing asset path — then sync hq.db and post Slack confirmations.

## Denis inputs (fill before running)

```
PO apply: [EMAIL | FORM_URL | LINKEDIN_EASY_APPLY] — publish first on: [LINKEDIN | JOBS_BG | NETWORK]
PO JD: [approve expanded draft 2026-06-19 | PASTE_FULL_JD_TEXT]
Office visits: [Kapana 11108782, широк център 10481212, център 11036578] — budget: [<800 EUR all-in | OTHER]
HQ Inbox: [paste 7 approve lines from planning/hq-inbox-unlocks-2026-06-19.md]
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn DM | early bird] — brand: [approve draft | defer]
brand day1: ICP=[...] — NOT for=[...] — secret sauce=[...] — ops=[full-time PO | consultant | hybrid]
brand day2: visual=[A|B|C] — one-liner=[Стани част от AI революцията | EDIT] — CTA=[waitup|LinkedIn|info session] — tone OK=[yes|edits]
brand day3: channels=[rank 1-5] — facebook=[community|events|repost|skip] — rhythm=[2x/week|3x/week|minimal] — path=[deck-first|landing-first|hybrid]
brand day4: budget=[tier] — early bird=[price/seats or TBD] — plan=[approve 90-day draft | edits]
```

## How to execute (agent)

1. For each Denis input: update matching `actions/*` entry (`props.status=done`, `props.reply=...`).
2. If PO JD approved: write `business/jobs/product-owner.md` from `planning/po-jd-expanded-draft-2026-06-19.md` (with Denis edits), sync `jobs/product-owner` in hq.db.
3. If office picks confirmed: update `planning/office-plovdiv.md` + create lease comparison table in hq.db.
4. If path chosen: export deck scaffold OR minimal landing in `web/`.
5. Merge brand day1–4 into `planning/brand-marketing-plan-draft-2026-06-19.md` and `business/plan`.
6. Run: `python3 scripts/sync_actions.py && python3 scripts/build_site.py`
7. Upsert standup `2026-07-23` with Done / Today / Blockers / Agent next.
8. Post ≤15 line summary to `#vibe-standup` with prefix `🎯 *PM Agent* |`.

## Rules

- Never invent completed work.
- Do not publish compensation/legal terms without Denis text.
- Do not publish social content — drafts only.
