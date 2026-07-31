# Denis action pack — batch replies (2026-06-22)

**No Denis Slack replies since 2026-06-10 (day 12).** Copy blocks into `#vibe-standup`.

---

## 1. Brand sprint — batch catch-up OR day 4 only

**Batch (recommended):** see `planning/brand-sprint-catchup-2026-06-22.md` Option A

**Day 4 only:**

```
brand day4: budget=lean — early bird=defer — plan=approved
```

---

## 2. PO apply + JD (priority 1)

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
```

Refs: `planning/po-publish-readiness-2026-06-22.md`, `planning/po-jd-expanded-draft-2026-06-19.md`

---

## 3. Office — pick 3 (URLs verified live 2026-06-22)

```
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
```

Ref: `planning/office-url-check-2026-06-22.md`

---

## 4. HQ Inbox (7 open approvals)

```
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

Ref: `planning/hq-inbox-unlocks-2026-06-19.md`

---

## Combined reply (edit brackets)

```
brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[hybrid]
brand day2: visual=[B] — one-liner=[…] — CTA=[LinkedIn] — tone OK=[yes]
brand day3: channels=[LI=1, FB=3] — facebook=[repost] — rhythm=[2x/week LI] — path=[hybrid]
brand day4: budget=[lean] — early bird=[defer] — plan=[approved]
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

---

## Copy-paste agent prompt (fill `[…]` only)

Use this in Cursor / another agent after Denis fills placeholders:

```
You are helping Denis (founder, Vibe Coders Academy) execute his open HQ inbox items in the vibe-coding-101 repo. Read data/hq.db (actions, tasks, standups) and these planning files before acting.

## Goal
Unblock launch path: brand plan sign-off, PO hiring publish, office visits, HQ automations, and social profile setup.

## Denis inputs (fill before running)
- Brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[full-time PO | consultant | hybrid]
- Brand day2: visual=[A|B|C] — one-liner=[…] — CTA=[waitlist|LinkedIn|info session] — tone OK=[yes|edits]
- Brand day3: channels=[ranked list] — facebook=[hub|events|repost|skip] — rhythm=[…] — path=[deck|landing|hybrid]
- Brand day4: budget=[lean|medium|aggressive] — early bird=[defer or €X/N seats/month] — plan=[approved|edits]
- PO apply: [email|form URL|LinkedIn Easy Apply] — publish first on: [LinkedIn|jobs.bg|network]
- PO JD: [approve expanded draft 2026-06-19 | paste full text below]
- Office visits: [3 listing IDs or URLs]
- HQ inbox: [list of approve: slugs + automation triggers Denis green-lit]

## After Denis inputs, do (in order)
1. Update matching actions in hq.db — props.status=done, props.reply=Denis text.
2. If PO JD approved: write business/jobs/product-owner.md from planning/po-jd-expanded-draft-2026-06-19.md (with Denis edits), sync jobs/product-owner in hq.db.
3. Merge brand sprint replies into planning/brand-marketing-plan-draft-2026-06-19.md and business/plan sections.
4. Lock office finalists in planning/office-plovdiv.md; add lease comparison table in HQ.
5. Run python3 scripts/sync_actions.py && python3 scripts/build_site.py
6. Post summary to #vibe-standup: what unblocked + next agent steps.

Rules: never invent completed work; mark unknowns; minimal focused diffs.
```
