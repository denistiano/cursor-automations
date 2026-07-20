# Denis batch agent prompt — 2026-07-20

Copy everything below the line into a new Cursor agent chat. Replace `[BRACKETED]` placeholders with your answers, then run.

---

You are helping Denis (founder, Vibe Coders Academy) clear **31 days of standup backlog** in one session. Repo: vibe-coding-101. Data: `data/hq.db`.

## Context

- Last standup in repo: **2026-06-19**. No Denis inbox replies since **2026-06-10**.
- **P1 blocker:** PO job — `jobs/product-owner` body is empty; expanded draft at `planning/po-jd-expanded-draft-2026-06-19.md`.
- **Office:** A/B/C picks re-validated 2026-07-20 — all live. See `planning/office-shortlist-refresh-2026-07-20.md`.
- **HQ Inbox:** 4 automations + 3 social drafts still `open`.
- **Brand sprint:** Days 1–4 unanswered since 2026-06-22. Day 1 starter: `planning/brand-day1-starter-2026-07-20.md`.
- **Path:** Landing vs deck not chosen — `planning/landing-vs-deck-decision-brief.md`.

## What we need to achieve

Unblock hiring (PO), office search, marketing automations, brand positioning, and public-facing asset path — then sync hq.db and post Slack confirmations.

## Denis inputs (fill before running)

```
PO apply: [EMAIL | FORM_URL | LINKEDIN_EASY_APPLY] — publish first on: [LINKEDIN | JOBS_BG | NETWORK]
PO JD: [approve expanded draft 2026-06-19 | PASTE_FULL_JD_TEXT]
Office visits: [Kapana 11108782, широк център 10481212, зала 4734755 | PASTE_3_URLS]
HQ Inbox: [paste 7 approve lines from planning/hq-inbox-unlocks-2026-06-19.md]
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn DM | early bird] — brand: [approve draft | defer]
brand day1: ICP=[...] — NOT for=[...] — secret sauce=[...] — ops=[full-time PO | consultant | hybrid]
brand day2: visual=[A|B|C] — one-liner=[Стани част от AI революцията | EDIT] — CTA=[waitlist|LinkedIn|info session] — tone OK=[yes|edits]
brand day3: channels=[rank 1-5] — facebook=[community|events|repost|skip] — rhythm=[2x/week|3x/week|minimal] — path=[deck-first|landing-first|hybrid]
brand day4: budget=[tier] — early bird=[price/seats or TBD] — plan=[approve 90-day draft | edits]
```

## How to execute (agent)

1. For each Denis input above: update matching `actions/*` entry (`props.status=done`, `props.reply=...`).
2. If PO JD approved: write `business/jobs/product-owner.md` from `planning/po-jd-expanded-draft-2026-06-19.md` (with Denis edits), sync `jobs/product-owner` in hq.db.
3. If office picks confirmed: update `planning/office-plovdiv.md` + create lease comparison table entry in hq.db.
4. If path chosen: either export deck scaffold OR minimal landing in `web/`.
5. Merge brand day1–4 into `planning/brand-marketing-plan-draft-2026-06-19.md` and `business/plan`.
6. Run: `python3 scripts/sync_actions.py && python3 scripts/build_site.py`
7. Upsert standup `2026-07-20` with Done / Today / Blockers / Agent next.
8. Post ≤15 line summary to `#vibe-standup` with prefix `🎯 *PM Agent* |`.

## Rules

- Never invent completed work.
- Do not publish compensation/legal terms without Denis text.
- Do not publish social content — drafts only.
