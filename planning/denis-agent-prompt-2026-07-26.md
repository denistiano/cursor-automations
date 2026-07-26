# Denis → agent batch prompt (2026-07-26)

Copy the block below into a new Cursor agent (or `#vibe-code`) after filling `[PLACEHOLDERS]`.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear launch blockers. Repo: vibe-coding-101. Read data/hq.db and planning/ artifacts before acting.

## Context
Practitioner-first AI/cohort academy in Plovdiv. HQ is action-centric (actions collection). No Denis inbox replies since 2026-06-10. Last standup: 2026-06-19. Today: 2026-07-26.

## Goals (in priority order)
1. Unblock PO hire — publish JD + apply flow
2. Lock office visit shortlist — contact landlords
3. Unlock HQ automations + social drafts
4. Choose landing vs deck path
5. Close brand sprint inputs (or collapse to one brand direction)

## Denis inputs (fill before running)
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
PO JD: [approve expanded draft 2026-06-19 | paste full JD text]
Office visits: [11237117, 11036578, 11224213 | paste 3 URLs]
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft | defer]
HQ Inbox batch:
  approve: linkedin-page-bio
  approve: linkedin-first-post
  approve: x-bio-and-first-post
  standup
  competitor: SoftUni AI
  plan update positioning
  draft: 2 linkedin posts about Cursor automations
Brand day1 (if doing sprint): ICP=[___] NOT for=[___] secret sauce=[___] ops=[___]

## What to do after Denis fills inputs
1. Update matching actions in hq.db (props.status=done, props.reply=Denis text)
2. PO: commit business/jobs/product-owner.md, sync jobs/product-owner, careers scaffold in web/
3. Office: lock picks in planning/office-plovdiv.md, draft landlord outreach
4. Path: landing scaffold OR deck export per choice
5. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
6. Post summary to #vibe-standup with what unblocked and next agent steps

## Rules
- Never invent completed work or official pricing/compensation
- Mark unknowns explicitly
- Minimal focused diffs; match repo conventions
```
