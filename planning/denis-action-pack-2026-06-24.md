# Denis action pack — batch replies (2026-06-24)

**No Denis Slack replies since 2026-06-10 (day 14).** Copy blocks into `#vibe-standup`.

---

## 1. PO apply + JD (priority 1)

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
```

Refs: `planning/po-publish-readiness-2026-06-24.md`, `planning/po-jd-expanded-draft-2026-06-19.md`

---

## 2. Brand sprint — batch catch-up (all 4 days)

```
brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[hybrid]
brand day2: visual=[B] — one-liner=[…] — CTA=[LinkedIn DM] — tone OK=[yes]
brand day3: channels=[LI=1, FB=3] — facebook=[repost] — rhythm=[2x/week] — path=[hybrid]
brand day4: budget=[lean] — early bird=[defer] — plan=[approved]
```

Ref: `planning/brand-sprint-catchup-2026-06-24.md`

---

## 3. Office — pick 3 visits

```
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
```

Refs: `planning/office-url-check-2026-06-24.md`, `planning/office-shortlist-refresh-2026-06-19.md`

---

## 4. HQ Inbox

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

## 5. One-liner (blocks social + business copy)

```
One-liner: Ship real projects with Cursor and AI agents — practitioner-first, not theory slides.
```

---

## Combined reply (edit brackets)

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[hybrid]
brand day2: visual=[B] — one-liner=[…] — CTA=[LinkedIn DM] — tone OK=[yes]
brand day3: channels=[LI=1, FB=3] — facebook=[repost] — rhythm=[2x/week] — path=[hybrid]
brand day4: budget=[lean] — early bird=[defer] — plan=[approved]
Office visits: Kapana 11108782, широк център 10481212, зала 4734755
One-liner: [your approved one-liner]
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations
```

---

## Agent prompt template (copy-paste for another agent)

Use after Denis fills `[bracketed]` fields above:

```
You are the Business + Developer agent for Vibe Coders Academy. Denis (founder) has replied with decisions below. Apply them in the vibe-coding-101 repo and data/hq.db. Do not invent completed work.

## Denis inputs (paste his Slack reply here)
[PASTE DENIS COMBINED REPLY]

## What we need to achieve
1. Publish PO role: sync approved JD to jobs/product-owner + business/jobs/product-owner.md; scaffold careers section in web/; draft LinkedIn PO announcement in social collection.
2. Brand sprint: merge day 1–4 answers into planning/brand-marketing-plan-draft-2026-06-19.md; update business/plan and business/messaging (one-liner) in hq.db; resolve landing vs deck per day 3 path choice.
3. Office: lock Denis's 3 picks in planning/office-plovdiv.md; build lease comparison table in HQ.
4. HQ Inbox: mark approved automations/social drafts as done in actions collection; unblock social account creation task.
5. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py

## Missing input (Denis must still provide if blank)
- [ ] PO apply method URL (if not "form URL")
- [ ] Official JD text (if not "approve expanded draft")
- [ ] Brand day 1–4 bracket fields
- [ ] Approved one-liner
- [ ] Office visit picks (if different from default 3)

## How (if known)
- JD source: planning/po-jd-expanded-draft-2026-06-19.md
- Office shortlist: planning/office-shortlist-refresh-2026-06-19.md
- Brand merge target: planning/brand-marketing-plan-draft-2026-06-19.md
- Landing vs deck brief: planning/landing-vs-deck-decision-brief.md

Reply in Slack with what changed, what remains blocked, and links to new planning artifacts.
```
