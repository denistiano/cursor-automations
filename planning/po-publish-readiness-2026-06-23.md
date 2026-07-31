# PO publish readiness (2026-06-23)

**Status:** BLOCKED — Denis input required  
**Days since last Denis reply on PO apply:** **18** (since 2026-06-05)  
**Blocker action:** `input-blocker-po-apply-method-publish-channels` (priority 1)

---

## Repo check (no assumptions)

| Artifact | State |
|----------|-------|
| `jobs/product-owner` in hq.db | **body length 0** |
| `business/jobs/product-owner.md` | **does not exist** |
| Expanded JD draft | Ready — `planning/po-jd-expanded-draft-2026-06-19.md` |
| Skeleton JD | `planning/po-jd-skeleton-2026-06-10.md` |
| Social drafts for PO announce | Blocked until apply link exists |

---

## Top 3 steps (priority order)

1. **Denis:** Choose apply method + first publish channel.
   ```
   PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
   ```
   *Suggested default:* Google Form + LinkedIn post (see `planning/po-apply-decision-brief.md`).

2. **Denis:** Approve expanded JD or paste official text.
   ```
   PO JD: approve expanded draft 2026-06-19 OR [paste full text]
   ```
   Placeholders in draft: compensation, employment type, remote %, years experience.

3. **Agent (after 1–2):** Commit `business/jobs/product-owner.md`, sync hq.db, careers scaffold in `web/`, LinkedIn announcement draft in `social` collection.

---

## What unblocks

- Task `#2 Publish & share PO position`
- Careers section in landing scaffold
- LinkedIn PO announcement (draft-only until Denis publishes)
- PM agent task `#2 Publish checklist + social announcement drafts`

---

## Decision brief

Full options matrix: `planning/po-apply-decision-brief.md`  
JD text: `planning/po-jd-expanded-draft-2026-06-19.md`
