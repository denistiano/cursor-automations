# PO publish readiness — 2026-06-24

**Blocker:** PO apply method + first publish channel (priority 1)  
**Days without Denis reply on PO apply:** 19 (since 2026-06-05)  
**JD status:** Expanded draft ready; `jobs/product-owner` body still **0 bytes** in hq.db

---

## Repo evidence (no progress since 2026-06-19)

| Check | Status |
|-------|--------|
| `business/jobs/product-owner.md` | **Missing** |
| `jobs/product-owner` in hq.db | body empty |
| Git commits touching PO/JD | **None** since `f358977` (2026-06-19) |
| Denis Slack inbox replies | **None** since 2026-06-10 |

---

## Top 3 steps (priority order)

### 1. Denis — apply method + first channel (5 min)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
```

**Suggested default:** Google Form URL + publish first on LinkedIn.  
Ref: `planning/po-apply-decision-brief.md`

### 2. Denis — approve or paste JD (10 min)

```
PO JD: approve expanded draft 2026-06-19
```

OR paste full official text. Ref: `planning/po-jd-expanded-draft-2026-06-19.md`

### 3. Agent — after 1–2 (automated)

- Commit `business/jobs/product-owner.md` + sync hq.db
- Careers section scaffold in `web/`
- LinkedIn PO announcement draft in `social` collection

---

## What blocks downstream

| Waiting on PO | Task |
|---------------|------|
| Careers page | `#6 + #7 + #11 Scaffold web/ landing + careers` |
| LinkedIn PO post | `#2 Publish checklist + social announcement drafts` |
| Brand sprint hiring story | PO/consultant model in day 1 reply |
