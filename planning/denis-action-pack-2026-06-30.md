# Denis action pack — batch replies (2026-06-30)

**No Denis Slack replies since 2026-06-10 (day 20).** Copy blocks into `#vibe-standup`.

---

## 1. PO apply + JD (priority 1 — day 25)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
PO JD: approve expanded draft 2026-06-19 OR [paste full text]
```

Refs: `planning/po-publish-readiness-2026-06-30.md`, `planning/po-jd-expanded-draft-2026-06-19.md`

---

## 2. Office — pick 3 visits (re-checked 2026-06-30)

```
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
```

**Note:** Pick A still live on alo.bg but missing from latest scrape JSON — safe to contact.  
Refs: `planning/office-url-check-2026-06-30.md`, `planning/office-landlord-outreach-2026-06-15.md`

---

## 3. HQ Inbox (day 20)

```
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

Ref: `planning/hq-inbox-unlocks-2026-06-29.md`

---

## 4. Brand sprint catch-up (8 days overdue)

```
brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[full-time PO | consultant | hybrid]
brand day2: visual=[A|B|C] — one-liner=[…] — CTA=[waitlist|LinkedIn|info session] — tone OK
brand day3: channels=[…] — facebook=[…] — rhythm=[…] — path=[deck-first|landing-first|hybrid]
brand day4: budget=[lean|medium] — early bird=[price/date/seats OR defer] — plan=[approve draft]
```

Ref: `planning/brand-sprint-catchup-2026-06-30.md`

---

## 5. Landing vs deck

```
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft | defer]
```

Ref: `planning/landing-vs-deck-decision-brief.md`

---

## Combined reply (edit brackets)

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
brand day1: ICP=[your ICP] — NOT for=[anti-audience] — secret sauce=[3 bullets] — ops=[hybrid]
brand day2: visual=[A] — one-liner=[keep or edit] — CTA=[LinkedIn DM] — tone OK
brand day3: channels=[LinkedIn > X > FB] — facebook=[announcements only] — rhythm=[2/week] — path=[deck-first]
brand day4: budget=[lean] — early bird=[defer] — plan=[approve after merge]
Path: deck-first — CTA: LinkedIn — brand: defer
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

---

## Agent prompt for Denis (copy-paste to another agent)

Use this block after filling `[BRACKETED]` placeholders with your decisions:

```
You are helping Denis (founder, Vibe Coders Academy) clear his open HQ Inbox blockers in one batch.

Context: Practitioner-first AI coding cohort in Plovdiv. Course name locked: Vibe Coders Academy. Tagline: Стани част от AI революцията · Бъдещето е сега. Repo: denistiano/cursor-automations. HQ data in data/hq.db.

Denis decisions (fill before running):
- PO apply method: [email | form URL | LinkedIn Easy Apply]
- PO first publish channel: [LinkedIn | jobs.bg | network]
- PO JD: [approve expanded draft 2026-06-19 | paste full text below]
- Office visit picks (3 URLs or IDs): [e.g. Kapana 11108782, широк център 10481212, зала 4734755]
- Brand day1 ICP / NOT for / secret sauce / ops: […]
- Brand day2 visual / one-liner / CTA: […]
- Brand day3 channels / facebook / rhythm / path: […]
- Brand day4 budget / early bird / plan: […]
- Landing vs deck path + CTA: [deck-first | landing-first | hybrid] — CTA: […]
- HQ Inbox: approve all 4 automations + 3 social drafts? [yes/no per item]

What to achieve:
1. Update hq.db actions — mark matching input/approve actions done with Denis replies in props.reply.
2. Commit business/jobs/product-owner.md from planning/po-jd-expanded-draft-2026-06-19.md if JD approved.
3. Lock office finalists in planning/office-plovdiv.md; start lease comparison table.
4. Merge brand sprint answers into planning/brand-marketing-plan-draft-2026-06-19.md.
5. Run python3 scripts/sync_actions.py && python3 scripts/build_site.py.
6. Post summary to #vibe-standup with prefix 🎯 *PM Agent* | listing what unblocked.

Do not invent Denis decisions — only execute what is filled in above. Mark unknowns explicitly.
```
