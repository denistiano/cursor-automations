# PO publish readiness (2026-07-01)

**Status:** BLOCKED — day **26** since last Denis reply on PO apply (2026-06-05)  
**Blocker:** `input-blocker-po-apply-method-publish-channels` (priority 1)

---

## Gap (repo check)

| Item | Status |
|------|--------|
| `jobs/product-owner` body in hq.db | **0 bytes** |
| `business/jobs/product-owner.md` | **missing** |
| Expanded JD draft | Ready → `planning/po-jd-expanded-draft-2026-06-19.md` |
| Denis reply on apply method | **none since 2026-06-05** |
| Social drafts (LinkedIn PO post) | Exist but `approved=false` |
| Careers page scaffold | Blocked until JD + apply link |

---

## Top 3 steps (priority order)

1. **Denis:** Reply with apply method + first channel  
   `PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]`
2. **Denis:** Approve expanded JD draft OR paste official text  
   `PO JD: approve expanded draft 2026-06-19 OR [paste full text]`
3. **Agent (after 1–2):** Commit `business/jobs/product-owner.md`, sync hq.db, careers scaffold in `web/`, LinkedIn announcement draft

---

## Suggested default (cautious — Denis must confirm)

| Decision | Suggestion | Why |
|----------|------------|-----|
| Apply method | **Google Form** (Tally/free) | Structured CV intake; no LinkedIn company page needed yet |
| First channel | **LinkedIn** (Denis personal) | Aligns with task #2; social bios drafted |
| JD | Approve expanded draft with `[Denis: …]` placeholders filled | Fastest path; agent won't invent compensation |

---

## What blocks downstream

| Blocked work | Waiting on |
|--------------|------------|
| Careers page in `web/` | JD text + apply URL |
| LinkedIn PO announcement | JD + Denis profile (social accounts) |
| Publish checklist (`pm-agent-drafts-build` #2) | Apply method decision |
| PO interviews | Published listing |

---

## HQ Inbox reply template

```
PO apply: form URL — publish first on: LinkedIn
PO JD: approve expanded draft 2026-06-19
```

Refs: `planning/po-apply-decision-brief.md`, `planning/po-jd-expanded-draft-2026-06-19.md`
