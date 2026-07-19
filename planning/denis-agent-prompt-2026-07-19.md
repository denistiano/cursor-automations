# Denis → agent batch prompt (2026-07-19)

Copy everything below the line into a new Cursor agent (or paste in `#vibe-standup` after filling brackets).

---

You are executing Denis's decisions for **Vibe Coders Academy** (repo: vibe-coding-101 / cursor-automations). Read `data/hq.db` (collections: `actions`, `tasks`, `standups`, `business`, `social`, `jobs`). After each decision below, update the matching `actions` entry (`props.status=done`, `props.reply=...`), sync related `tasks` list items, run `python3 scripts/sync_actions.py && python3 scripts/build_site.py`, and post a short summary to the relevant Slack channel with the correct agent prefix.

## Decisions (Denis fills brackets only)

**1. PO hiring (P1 blocker)**  
Apply method: `[email | Google Form URL | LinkedIn Easy Apply]`  
Publish first on: `[LinkedIn | jobs.bg | network]`  
JD: `[approve expanded draft 2026-06-19 | paste full JD text below]`  
`[optional: paste JD text]`  
→ Unblock: commit `business/jobs/product-owner.md`, sync `jobs/product-owner`, careers section in `web/`, LinkedIn announcement draft.

**2. Office Plovdiv**  
Visit shortlist: `[A,B,C from planning/office-shortlist-refresh-2026-07-19.md | paste 3 URLs]`  
Budget confirmed: `[<800 EUR/mo yes/no]`  
→ Unblock: lease comparison table in HQ, visit checklist.

**3. HQ Inbox**  
Social approvals: `[approve: linkedin-page-bio, linkedin-first-post, x-bio-and-first-post | edits: …]`  
Automations green-light: `[standup | competitor: SoftUni AI | plan update positioning | draft: … | defer]`  
→ Unblock: enable scheduled agent runs per approval.

**4. Brand sprint (or defer)**  
Day 1: `brand day1: ICP=[…] — NOT for=[…] — secret sauce=[…] — ops=[full-time PO | consultant | hybrid]`  
Days 2–4: `[complete now | defer entire sprint]`  
→ Unblock: `business/messaging`, marketing calendar draft.

**5. Landing vs deck**  
Path: `[deck-first | landing-first | hybrid one-pager]`  
CTA: `[waitlist | LinkedIn DM | early bird]`  
Early bird (if chosen): `price=[…] seats=[…] date=[…]`  
→ Unblock: landing scaffold OR deck export; fix “URL TBD” in social bios.

**6. Social accounts**  
Created handles: `LinkedIn=[…] X=[…] Facebook=[…]`  
→ Unblock: publish checklist after bios approved.

## Rules

- Do not invent completed work or pricing Denis did not provide.
- Minimal focused diffs; match repo conventions.
- Report what unblocked and what remains blocked after the run.
