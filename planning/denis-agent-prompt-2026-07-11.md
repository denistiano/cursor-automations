# Denis → agent batch prompt (2026-07-11)

Copy everything below the line into a new agent chat. Replace `[…]` placeholders with your decisions, then run.

---

You are helping Denis (founder, Vibe Coders Academy) clear **all open HQ Inbox blockers** in one pass. Repo: `denistiano/cursor-automations`. After each Slack-style reply, update matching `actions` in `data/hq.db` (`props.status=done`, `props.reply=…`), sync tasks/standups, run `python3 scripts/sync_actions.py && python3 scripts/build_site.py`, and execute downstream agent work described below.

## Context

Vibe Coders Academy is a practitioner-first Cursor/agent engineering cohort in Plovdiv, Bulgaria — **not** SoftUni-style no-code vibe coding. HQ dashboard at `web/` tracks tasks via `actions` collection. Last Denis inbox replies: **2026-06-10**. Priority blockers have been open **31–36 days**.

**Goal this session:** Unblock PO hiring, brand positioning, office visits, social launch, and automation approvals so agents can ship careers page, landing/deck, and marketing calendar.

## Denis inputs (fill every `[…]`)

### Priority 1 — PO apply + JD (blocks careers + LinkedIn PO post)

```
PO apply: [email | Google Form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
PO JD: [approve expanded draft planning/po-jd-expanded-draft-2026-06-19.md | paste full JD text]
```

Optional: remote %, employment type, compensation range for JD placeholders.

### Priority 1 — Brand sprint day 1 (sprint +19d overdue)

```
brand day1: ICP=[one sentence] — NOT for=[who we turn away] — secret sauce=[bullet1; bullet2; bullet3] — ops=[full-time PO | consultant | hybrid]
```

Suggested starting point in `planning/brand-sprint-day1-decision-brief-2026-07-11.md` — edit before sending.

### Priority 2 — Office Plovdiv (A/B/C verified live 2026-07-11)

```
Office visits: [A, B, C | paste 3 URLs]
```

See `planning/office-shortlist-verify-2026-07-11.md`. Outreach: `planning/office-landlord-outreach-2026-06-15.md`.

### Priority 2 — Landing vs deck path

```
Path: [deck-first | landing-first | hybrid one-pager] — CTA: [waitlist | LinkedIn DM | early bird] — brand: [approve draft | defer]
```

See `planning/landing-vs-deck-decision-brief.md`.

### Priority 2 — HQ Inbox batch (7 items, copy-paste all if ready)

```
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

### Priority 2 — Brand sprint days 2–4 (if time)

```
brand day2: visual=[A|B|C|URL] — one-liner=[…] — CTA=[waitlist|LinkedIn|info session] — tone OK=[yes|edits]
brand day3: channels=[ranked list] — facebook=[community|events|repost|skip] — rhythm=[2x/wk|3x/wk|minimal] — path=[deck|landing|hybrid]
brand day4: budget=[lean|medium] — early bird=[price/seats or defer] — plan=[approve 90-day draft | edits]
```

## What the agent must deliver after inputs

1. **PO:** `business/jobs/product-owner.md` + sync `jobs/product-owner` in hq.db + careers scaffold in `web/` + LinkedIn announcement draft
2. **Brand:** Merge day 1–4 answers into `planning/brand-marketing-plan-draft-2026-06-19.md` + `business/plan` sections
3. **Office:** Finalists in `planning/office-plovdiv.md` + lease comparison in HQ
4. **Path:** Deck export OR landing scaffold per Denis choice
5. **Social:** Mark approved drafts; unblock task #4 create accounts
6. **Automations:** Mark approved; note enabled triggers
7. **Standup:** Upsert `2026-07-11` with Done / Today (max 3) / Blockers / Agent next
8. Post ≤15-line summary to `#vibe-standup` (or `#all-denistiano` if standup channel unavailable)

**Rules:** Never invent completed work. Only mark actions `done` when matching reply text is provided above.
