# Carryover analysis — 2026-08-10

Items carried from 2026-06-19 standup with **no Denis progress** in repo (61+ days).  
For each: top 3 priority-first steps + agent findings.

---

## 1. PO apply + publish channels (P1 — day 66)

**Evidence:** `jobs/product-owner` body = 0; `input-blocker-po-apply-method-publish-channels` still `in_progress`; no commits touching careers/JD since 2026-06-19.

**Top 3 steps:**

| # | Who | Step |
|---|-----|------|
| 1 | Denis | Reply: `PO apply: [email \| form URL \| LinkedIn Easy Apply] — publish first on: [LinkedIn \| jobs.bg \| network]` |
| 2 | Denis | Approve `planning/po-jd-expanded-draft-2026-06-19.md` OR paste official JD |
| 3 | Agent | Commit `business/jobs/product-owner.md`, sync hq.db, careers scaffold, LinkedIn announcement draft |

**Agent analysis:** Fastest path is **Google Form/Tally + LinkedIn post** (no company page required). Form fields suggested: name, email, LinkedIn URL, 2-sentence why PO, availability, salary expectation. Agent cannot create the form URL — Denis must create or delegate.

---

## 2. Office Plovdiv — pick A′/B′/C (P2 — day 61)

**Evidence:** No `office-plovdiv.md` lock; no landlord outreach commits; prior scrape (319 listings) had A/B missing — **stale data risk**.

**Top 3 steps:**

| # | Who | Step |
|---|-----|------|
| 1 | Denis | Confirm picks: `Office visits: A, B, C` from `planning/office-shortlist-refresh-2026-08-10.md` |
| 2 | Denis | Contact landlords (template in `planning/office-landlord-outreach-2026-06-15.md`) |
| 3 | Agent | Lease comparison table + visit checklist in HQ |

**Agent progress today:** Re-scraped 1333 listings; A′/B′/C all still active. C price now €35/mo (was €25.56). See `data/office-top40.md`.

---

## 3. Brand sprint days 1–4 (P1 day 1 — day 52)

**Evidence:** All 4 `input-task-brand-sprint-day-*` still `in_progress`; no `brand day1:` … `brand day4:` replies in repo.

**Top 3 steps:**

| # | Who | Step |
|---|-----|------|
| 1 | Denis | Complete **day 1 only** first — unblocks positioning for everything else |
| 2 | Denis | Reply: `brand day1: ICP=[…] — NOT for=[…] — secret sauce=[b1;b2;b3] — ops=[full-time PO \| consultant \| hybrid]` |
| 3 | Agent | Merge into `planning/brand-marketing-plan-draft-2026-06-19.md` + prep condensed day 2 prompt |

**Agent analysis:** Day 1 is the bottleneck. Suggested ICP draft (Denis edits): *"Mid-level BG developers already using Cursor who want a shipped capstone + automation pack in 6–8 weeks."* Do not assume — Denis must confirm.

---

## 4. HQ Inbox — 7 approvals (P2–P3 — day 61)

**Evidence:** All 7 `approve-*` actions still `open`; social accounts task blocked.

**Top 3 steps:**

| # | Who | Step |
|---|-----|------|
| 1 | Denis | Batch approve social bios (3 replies) — does not publish, only unlocks profile setup |
| 2 | Denis | Batch approve automations (4 replies) — enables scheduled agent runs |
| 3 | Denis | Create LinkedIn + X accounts after bios approved |

**One-shot:** See `planning/hq-inbox-unlocks-2026-06-19.md` batch block.

---

## 5. Landing vs deck path (P2 — day 66)

**Evidence:** Both `input-task-landing-page-*` and `input-task-presentation-document-*` `in_progress`; speaker notes exist; no landing scaffold.

**Top 3 steps:**

| # | Who | Step |
|---|-----|------|
| 1 | Denis | Pick path: `deck-first` \| `landing-first` \| `hybrid` |
| 2 | Denis | Pick CTA: waitlist \| LinkedIn \| early bird |
| 3 | Agent | Deck export OR minimal landing scaffold per choice |

**Agent analysis:** If Denis needs to pitch PO this week → **deck-first**. If waitlist is primary CTA → **hybrid one-pager** (hero + waitlist + careers link).
