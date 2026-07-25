# Carryover analysis — 2026-07-25

Items from **2026-06-19 standup** with no Denis progress evidence in repo (45 days since last inbox reply).

---

## 1. PO apply method + publish channels (P1 blocker)

**Days stale:** 50 (since 2026-06-05)  
**Evidence:** `jobs/product-owner` body = 0 bytes; `business/jobs/product-owner.md` missing; no commits touching PO publish flow.

**Top 3 steps:**

1. Denis replies: `PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]`
2. Denis approves `planning/po-jd-expanded-draft-2026-06-19.md` OR pastes official JD
3. Agent commits JD → careers scaffold in `web/` → LinkedIn announcement draft

**Suggested default:** Google Form + LinkedIn post (no Easy Apply until company page exists).

---

## 2. Office Plovdiv — visit shortlist (P2)

**Days stale:** 36 (since 2026-06-19 shortlist)  
**Evidence:** No landlord outreach commits; previous picks A+B now **delisted**.

**Top 3 steps:**

1. Denis picks 3 from `planning/office-shortlist-validation-2026-07-25.md` (revised picks)
2. Agent builds lease comparison table in HQ
3. Denis sends outreach using `planning/office-landlord-outreach-2026-06-15.md` template

**Agent progress today:** Fresh scrape (298 listings) + re-rank + validation doc.

---

## 3. HQ Inbox — automations + social drafts (P2)

**Days stale:** 36 (7 approvals open since 2026-06-10)  
**Evidence:** All 4 `approve-automation-*` and 3 `approve-social-*` actions still `status=open` in hq.db.

**Top 3 steps:**

1. Denis approves 4 automations (copy `slack_reply` from `planning/hq-inbox-unlocks-2026-06-19.md`)
2. Denis approves 3 social drafts (bios + first posts — does **not** publish)
3. Denis creates LinkedIn/X accounts after bios approved → unblocks task #4

---

## 4. Brand sprint days 1–4 (P1 day 1, P2 days 2–4)

**Days stale:** 33 (sprint ended 2026-06-22)  
**Evidence:** All 4 brand sprint `input` actions still `in_progress`; no `business/messaging` updates from Denis.

**Top 3 steps:**

1. Denis completes day 1 in HQ → Brand sprint tab: ICP, anti-audience, secret sauce, ops model
2. Denis completes days 2–3: visual direction, CTA, channel rank, deck/landing path
3. Denis completes day 4: budget tier + 90-day calendar sign-off

**Blocks:** Marketing plan finalization, social CTA, early bird pricing, Facebook strategy.

---

## 5. Landing page vs presentation deck (P2)

**Days stale:** 50 (since 2026-06-05)  
**Evidence:** No landing scaffold in `web/`; `content/presentation/speaker-notes.md` exists but no deck export.

**Top 3 steps:**

1. Denis picks path: `deck-first` | `landing-first` | `hybrid one-pager`
2. Denis picks CTA: waitlist | LinkedIn DM | early bird (needs price/seats)
3. Agent builds chosen asset; align social drafts CTA

**Suggested default:** Hybrid one-pager (hero + waitlist + careers) while deck built for live talks.

---

## Priority order for Denis today

1. PO apply (unblocks hiring pipeline)
2. Office picks (physical space decision)
3. HQ Inbox approvals (unblocks agent automations)

Brand sprint + landing/deck can batch in a single 30-min session via `planning/denis-agent-prompt-2026-07-25.md`.
