# Denis → agent batch prompt (2026-08-12)

Copy-paste the block below into a new Cursor agent (or Slack `@Cursor`) after filling in `[PLACEHOLDERS]`.

---

```
You are helping Denis unblock Vibe Coders Academy launch tasks. Repo: denistiano/cursor-automations (vibe-coding-101). Read data/hq.db and planning/ docs for context.

## Goal
Clear Denis's open HQ Inbox inputs in one batch so agents can ship careers page, office lease comparison, brand plan merge, and landing/deck scaffold.

## Denis inputs (fill before running)

1. PO apply method + first channel:
   PO apply: [EMAIL | FORM_URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]

2. PO job description:
   [APPROVE po-jd-expanded-draft-2026-06-19.md | PASTE_OFFICIAL_JD_HERE]

3. Office visit shortlist (from planning/office-shortlist-refresh-2026-08-12.md):
   Office visits: [A, B, C | paste 3 URLs]

4. Brand sprint day 1 (#vibe-business):
   brand day1: ICP=[___] — NOT for=[___] — secret sauce=[___] — ops=[consultant | FT | hybrid]

5. Launch path:
   Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird]

6. HQ Inbox batch (paste all 7 if approving):
   approve: linkedin-page-bio
   approve: linkedin-first-post
   approve: x-bio-and-first-post
   standup
   competitor: SoftUni AI
   plan update positioning
   draft: 2 linkedin posts about Cursor automations

## What to do after Denis fills inputs

1. Update matching actions in hq.db (props.status=done, props.reply=Denis text).
2. If PO approved: write business/jobs/product-owner.md, sync jobs/product-owner, scaffold careers in web/.
3. If office picks confirmed: lease comparison table in HQ + update planning/office-plovdiv.md.
4. If brand day1 received: merge into planning/brand-marketing-plan-draft-2026-06-19.md.
5. If path chosen: deck export OR landing scaffold per planning/landing-vs-deck-decision-brief.md.
6. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
7. Post summary to #vibe-standup with what unblocked.

Rules: never invent completed work; minimal focused diffs; ask only if a placeholder is still empty.
```
