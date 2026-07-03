# PO publish readiness (2026-07-03)

**Status:** BLOCKED — Denis input required  
**Day count:** 23 since last Denis reply (2026-06-10)  
**Blocker:** `input-blocker-po-apply-method-publish-channels` (priority 1)

---

## Repo check (2026-07-03)

| Artifact | Status |
|----------|--------|
| `jobs/product-owner` in hq.db | body length **0** |
| `business/jobs/product-owner.md` | **missing** |
| Expanded JD draft | ✅ `planning/po-jd-expanded-draft-2026-06-19.md` |
| Skeleton JD | ✅ `planning/po-jd-skeleton-2026-06-10.md` |
| Decision brief | ✅ `planning/po-apply-decision-brief.md` |
| Social drafts (LinkedIn PO post) | exist but **unapproved** |

**No evidence of Denis progress** in repo since 2026-06-10.

---

## Top 3 steps (priority order)

1. **Denis — apply method + first channel** (2 min):
   ```
   PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
   ```
   **Suggested default:** Google Form/Tally + publish first on LinkedIn (Denis network).

2. **Denis — approve JD** (5 min):
   ```
   PO JD: approve expanded draft 2026-06-19 OR [paste full official text]
   ```
   Agent cannot invent compensation, employment type, or legal terms.

3. **Agent (after 1–2):**
   - Commit `business/jobs/product-owner.md` from approved draft
   - Sync hq.db `jobs/product-owner` body
   - Careers scaffold in `web/`
   - LinkedIn announcement draft (uses approved social bios when ready)

---

## What unblocks downstream

| Denis reply | Unblocks |
|-------------|----------|
| Apply method | Careers page CTA + mailto/form link |
| First channel | Publish checklist + `#2 Publish & share PO position` |
| JD approval | Official job text everywhere (HQ, web, boards) |

---

## Cautious assumptions (not confirmed)

- Denis still wants to hire a PO (vs consultant/hybrid from brand sprint)
- LinkedIn is acceptable first channel (personal profile OK until company page exists)
- Expanded draft is close enough to approve with bracket edits rather than full rewrite
