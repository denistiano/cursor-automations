# Denis → agent batch prompt (2026-08-10)

Copy the block below into a new agent run. Replace `[…]` placeholders with your answers, then send.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear all open HQ Inbox blockers in one session.

## Context
- Repo: vibe-coding-101 / cursor-automations
- HQ data: data/hq.db (actions, jobs, business, social collections)
- Last Denis inbox replies: 2026-06-10 (61 days ago)
- Speaker notes ready: content/presentation/speaker-notes.md
- PO JD draft: planning/po-jd-expanded-draft-2026-06-19.md (NOT synced — needs approval)
- Office shortlist revalidated 2026-08-10: planning/office-shortlist-refresh-2026-08-10.md

## What we need to achieve
1. Unblock PO hiring (apply method + JD + first publish)
2. Lock office visit shortlist and prep landlord outreach
3. Approve HQ automations + social drafts (approval ≠ publish)
4. Complete brand sprint day 1 (minimum) to unblock marketing plan
5. Choose landing vs deck path + CTA

## Denis inputs (fill every bracket)

PO apply method: [email | Google Form URL | LinkedIn Easy Apply]
PO publish first on: [LinkedIn | jobs.bg | network]
PO JD: [approve expanded draft 2026-06-19 | paste full text below]
---
Office visits: [A, B, C | paste 3 listing URLs]
---
Path: [deck-first | landing-first | hybrid]
CTA: [waitlist | LinkedIn DM | early bird]
Brand visual: [approve draft | defer]
---
brand day1: ICP=[one sentence] — NOT for=[anti-audience] — secret sauce=[b1; b2; b3] — ops=[full-time PO | consultant | hybrid]
---
HQ approvals (paste lines you want executed):
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
standup
competitor: SoftUni AI
plan update positioning
draft: 2 linkedin posts about Cursor automations

## How to execute (agent)
1. Update matching actions in hq.db (props.status=done, props.reply=Denis text)
2. If PO JD approved → write business/jobs/product-owner.md, sync jobs/product-owner, careers scaffold in web/
3. If office picks → lock planning/office-plovdiv.md, lease comparison in HQ
4. If brand day1 → merge into planning/brand-marketing-plan-draft-2026-06-19.md
5. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
6. Post summary to #vibe-standup with prefix 🎯 *PM Agent* |

Rules: never invent completed work; mark unknowns; no pricing claims without Denis input.
```
