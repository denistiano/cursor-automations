# Denis agent prompt — batch input (2026-07-25)

Copy everything below the `---` line into a new agent chat. Fill in `[BRACKETS]` only.

---

You are helping Denis (founder, Vibe Coders Academy) clear **all open HQ Inbox inputs** in one session. Repo: `denistiano/cursor-automations`. Data store: `data/hq.db` (actions collection).

## Goal

Unblock the PM pipeline so agents can: publish PO role, scaffold careers page, finalize marketing plan, and pick office space.

## Context

- **Course:** Vibe Coders Academy — practitioner-first AI/coding cohort in Plovdiv
- **Last Denis inbox reply:** 2026-06-10 (45 days ago)
- **Open blockers:** PO apply method, office visits, HQ approvals, brand sprint days 1–4, landing vs deck path
- **Artifacts ready:** PO JD draft (`planning/po-jd-expanded-draft-2026-06-19.md`), office shortlist (`planning/office-shortlist-validation-2026-07-25.md`), speaker notes (`content/presentation/speaker-notes.md`), social bios (HQ Inbox drafts)

## Denis inputs needed (fill every bracket)

### 1. PO hiring (P1 blocker)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
JD: [approve expanded draft in planning/po-jd-expanded-draft-2026-06-19.md | paste official text below]
[Optional pasted JD text]
Compensation: [range + type: part-time/full-time/contract]
Remote: [X% remote]
```

### 2. Office Plovdiv (revised shortlist — old picks delisted)

```
Office visits: [A, B, C from planning/office-shortlist-validation-2026-07-25.md | paste 3 URLs]
Budget ceiling: [confirm €800/mo or adjust]
Must-have: [Kapana only | center OK | training room required]
```

### 3. HQ Inbox approvals (copy-paste each to Slack or confirm here)

```
Automations: approve all 4 (standup, research, business plan, social drafts) — [yes/no per item]
Social drafts: approve linkedin-page-bio, linkedin-first-post, x-bio-and-first-post — [yes/no per item]
```

### 4. Brand sprint (days 1–4 — overdue since 2026-06-22)

```
brand day1: ICP=[target audience] — NOT for=[anti-audience] — secret sauce=[differentiator] — ops=[consultant vs FT PO model]
brand day2: visual=[A/B/C or describe] — one-liner=[tagline] — CTA=[primary call to action] — tone OK=[yes/no]
brand day3: channels=[rank: LinkedIn, FB, X, ...] — facebook=[strategy] — rhythm=[posting cadence] — path=[deck-first | landing-first | hybrid]
brand day4: budget=[tier €] — early bird=[price/date/seats or defer] — plan=[approve 90-day calendar draft | changes]
```

### 5. Landing vs deck

```
Path: [deck-first | landing-first | hybrid one-pager] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft colors | defer]
```

## What the agent should do after Denis fills brackets

1. Update matching `actions` in `data/hq.db` — set `props.status=done`, store replies in `props.reply`
2. If PO approved: write `business/jobs/product-owner.md`, sync `jobs/product-owner`, scaffold careers in `web/`
3. If office picks received: lease comparison table + outreach pack
4. If brand sprint complete: merge into `business/plan` and `business/messaging`
5. Run `python3 scripts/sync_actions.py && python3 scripts/build_site.py`
6. Post summary to #vibe-standup with prefix `🎯 *PM Agent* |`

## Rules

- Never invent completed work or pricing/legal terms
- Mark unknowns explicitly
- Max 3 items in standup Today after processing
