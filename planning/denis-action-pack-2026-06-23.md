# Denis action pack — batch replies (2026-06-23)

**No Denis Slack replies since 2026-06-10 (day 13).** Copy blocks into `#vibe-standup` or use HQ Inbox.

---

## 1. PO apply + JD (priority 1 — day 18)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
PO JD: approve expanded draft 2026-06-19 OR [paste full text]
```

Refs: `planning/po-publish-readiness-2026-06-23.md`, `planning/po-jd-expanded-draft-2026-06-19.md`

---

## 2. Brand sprint catch-up (days 1–4 skipped)

```
brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[consultant|full-time PO|hybrid]
brand day2: visual=[A|B|C] — one-liner=[…] — CTA=[waitlist|LinkedIn|info session] — tone OK=[yes|edits]
brand day3: channels=[…] — facebook=[…] — rhythm=[…] — path=[deck-first|landing-first|hybrid]
brand day4: budget=[lean|standard|aggressive] — early bird=[…] — plan=[…]
```

Ref: `planning/brand-sprint-catchup-2026-06-23.md`

---

## 3. Office — pick 3 visits (URLs verified 2026-06-22)

```
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
```

Ref: `planning/office-url-check-2026-06-23.md`

---

## 4. HQ Inbox (7 items still open)

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

## 5. Landing vs deck

```
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft | defer]
```

Ref: `planning/landing-vs-deck-decision-brief.md`

---

## Combined reply (edit brackets — one paste)

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
brand day1: ICP=mid-level BG devs using Cursor — NOT for=career switchers zero code — secret sauce=ship not slide; agent ops; practitioner founder — ops=hybrid
brand day2: visual=A — one-liner=Стани част от AI революцията — CTA=LinkedIn — tone OK=yes
brand day3: channels=LinkedIn,Facebook,meetups — facebook=event announcements — rhythm=2×LI+1live/mo — path=deck-first
brand day4: budget=lean — early bird=defer — plan=2×LI+1live
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
Path: deck-first — CTA: LinkedIn — brand: defer
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
```

---

## Agent prompt for Denis (copy-paste to another agent)

Use this block after filling `[BRACKET]` placeholders:

```
You are helping Denis (founder, Vibe Coders Academy) clear his HQ Inbox blockers in one batch.

## Context
- Repo: vibe-coding-101 / cursor-automations — HQ in data/hq.db, planning artifacts in planning/
- Course: practitioner Cursor/agent cohort for working developers in Bulgaria (NOT beginner no-code)
- No Denis replies since 2026-06-10; PO apply blocked 18 days; brand sprint 19–22 Jun unanswered

## Denis inputs (fill before running)
PO apply method: [EMAIL | FORM URL | LINKEDIN EASY APPLY]
PO first publish channel: [LINKEDIN | JOBS.BG | NETWORK]
PO JD: [APPROVE planning/po-jd-expanded-draft-2026-06-19.md | PASTE TEXT BELOW]
[PASTE JD IF NOT APPROVING DRAFT]

Brand day1 ICP: [ONE SENTENCE]
Brand day1 NOT for: [ONE SENTENCE]
Brand day1 secret sauce: [3 BULLETS MAX]
Brand day1 ops model: [FULL-TIME PO | CONSULTANT | HYBRID]

Brand day2 visual: [A | B | C | CUSTOM URL]
Brand day2 one-liner: [TEXT]
Brand day2 CTA: [WAITLIST | LINKEDIN | INFO SESSION]
Brand day2 tone: [OK | EDITS: …]

Brand day3 channel rank: [ORDERED LIST]
Brand day3 Facebook purpose: [COMMUNITY | EVENTS | REPOST | SKIP]
Brand day3 content rhythm: [2×LI+1LIVE | 3×POSTS | MINIMAL]
Brand day3 path: [DECK-FIRST | LANDING-FIRST | HYBRID]

Brand day4 budget tier: [LEAN | STANDARD | AGGRESSIVE]
Brand day4 early bird: [PRICE/DATE/SEATS OR DEFER]
Brand day4 90-day plan: [RHYTHM SUMMARY]

Office visits (3 picks): [URL OR LISTING ID × 3]

Landing path: [DECK-FIRST | LANDING-FIRST | HYBRID]
Landing CTA: [WAITLIST | LINKEDIN | EARLY BIRD]

HQ approvals to mark done: [LIST approve: slugs]

## What to do
1. Update matching actions in data/hq.db — props.status=done, props.reply=Denis text
2. If PO JD approved: write business/jobs/product-owner.md from draft; sync jobs/product-owner entry
3. Merge brand sprint answers into planning/brand-marketing-plan-draft-2026-06-19.md
4. Lock office picks in planning/office-plovdiv.md
5. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
6. Reply with what unblocked and remaining blockers

Rules: never invent completed work; mark unknowns; minimal focused diffs.
```
