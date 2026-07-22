# Denis action pack — batch replies (2026-07-22)

**No Denis Slack replies since 2026-06-10 (day 42).** Copy blocks into `#vibe-standup` or HQ Inbox.

---

## 1. PO apply + JD (priority 1 — day 47 stale)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
PO JD: approve expanded draft 2026-06-19 OR [paste full text]
```

Refs: `planning/po-apply-decision-brief.md`, `planning/po-jd-expanded-draft-2026-06-19.md`

**Top 3 steps:**
1. Pick apply method + first channel (one line).
2. Approve expanded JD draft OR paste official text.
3. Agent commits `business/jobs/product-owner.md`, syncs hq.db, drafts careers page + LinkedIn post.

---

## 2. Office — pick 3 visits (UPDATED — previous picks expired)

⚠️ Kapana 11108782 and широк център 10481212 are **no longer listed**. Use July refresh.

```
Office visits: Kapana 11237117, център 11036578, зала 4734755
```

Refs: `planning/office-shortlist-refresh-2026-07-22.md`, `planning/office-landlord-outreach-2026-06-15.md`

**Top 3 steps:**
1. Confirm budget still <€800/mo and ~20 seats (or reply with new constraints).
2. Pick 3 from revised shortlist (A/B/C above).
3. Agent locks finalists + lease comparison table; Denis sends outreach using BG template.

---

## 3. Brand sprint day 1 (NEW priority — 33 days stale)

```
brand day1: ICP=[mid-level BG devs using Cursor who want shipped capstone + automation pack] — NOT for=[career switchers with zero coding] — secret sauce=[cohort capstone repo; Cursor rules/skills/MCP stack; founder-led automation ops] — ops=[full-time PO | consultant | hybrid]
```

Ref: `planning/brand-sprint-2026-06-19.md`, `research/2026-06-19-brand-positioning-secret-sauce.md`

**Top 3 steps:**
1. Edit ICP + anti-audience (one sentence each).
2. Confirm or edit 3-bullet secret sauce.
3. Choose PO/ops model for next 90 days.

---

## 4. HQ Inbox (7 approvals still open)

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

## Combined agent prompt (copy-paste — fill brackets only)

```
You are helping Denis unblock Vibe Coders Academy launch tasks. Context: practitioner-first Cursor cohort in Plovdiv; tagline "Стани част от AI революцията"; no Denis replies since 2026-06-10.

Execute in order after Denis fills brackets:

1) PO HIRING — Apply method: [EMAIL | FORM_URL | LinkedIn Easy Apply]. Publish first on: [CHANNEL]. JD: [approve draft at planning/po-jd-expanded-draft-2026-06-19.md | paste text below]. Then: commit business/jobs/product-owner.md, sync jobs/product-owner in hq.db, scaffold web/ careers section, draft LinkedIn PO announcement.

2) OFFICE PLOVDIV — Budget: [<800 EUR/mo | OTHER]. Picks (3 URLs or IDs): [PICK_A, PICK_B, PICK_C]. Default if unsure: Kapana 11237117, център 11036578, зала 4734755 per planning/office-shortlist-refresh-2026-07-22.md. Then: lease comparison in HQ, outreach checklist.

3) BRAND SPRINT DAY 1 — ICP: […]. NOT for: […]. Secret sauce (3 bullets): […; …; …]. Ops model (90d): [full-time PO | consultant | hybrid]. Then: merge into brand-marketing-plan-draft + business/plan in hq.db.

4) HQ INBOX — Approvals: [list which of: linkedin-page-bio, linkedin-first-post, x-bio-and-first-post, standup automation, competitor research, business plan, social drafts]. Path for public assets: [deck-first | landing-first | hybrid]. CTA: [waitlist | LinkedIn | early bird]. Brand colors: [approve creative-brief A/B/C | defer].

5) EARLY BIRD (if ready) — Price: [EUR]. End date: [DATE]. Max seats: [N]. Legal line: [TEXT or defer].

Missing input from Denis (fill before running):
- PO apply method + channel: [___]
- PO JD approval or paste: [___]
- Office picks (3): [___]
- Brand day1 ICP / NOT for / secret sauce / ops: [___]
- Landing vs deck path + CTA: [___]
- HQ inbox approvals to run: [___]
```
