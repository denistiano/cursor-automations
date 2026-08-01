# PO publish readiness — 2026-08-01

**Blocker:** `input-blocker-po-apply-method-publish-channels` (priority 1, day 57)  
**Goal:** Unblock careers page, publish checklist, LinkedIn announcement draft

---

## Repo check (2026-08-01)

| Artifact | Status |
|----------|--------|
| `jobs/product-owner` in hq.db | **body length 0**, `position_text: ""` |
| `business/jobs/product-owner.md` | **missing** |
| `planning/po-jd-expanded-draft-2026-06-19.md` | Draft ready — Denis approval pending |
| `planning/po-jd-skeleton-2026-06-10.md` | Skeleton exists |
| Careers scaffold in `web/` | Not started |
| Social LinkedIn PO announcement | Blocked by JD + apply link |

---

## Top 3 steps (priority order)

1. **Denis:** `PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]`
2. **Denis:** Approve expanded JD (`planning/po-jd-expanded-draft-2026-06-19.md`) OR paste official text — fill `[Denis: ...]` placeholders (remote %, type, comp, duration)
3. **Agent:** Commit `business/jobs/product-owner.md`, sync hq.db, scaffold careers section in `web/`, draft LinkedIn announcement in `social` collection

---

## Suggested default (if Denis wants speed)

- **Apply:** Google Form (structured CV + 3 questions) → mailto/form link on careers page
- **First channel:** LinkedIn (Denis personal network) — aligns with task #2 Publish & share PO position
- **JD:** Approve expanded draft with comp/type filled in

---

## What Denis should reply (HQ Inbox)

```
PO apply: form URL — publish first on: LinkedIn
```

Optional same message: paste JD or `approve expanded JD with placeholders filled`.

---

## Unblocks after reply

1. `business/jobs/product-owner.md` + hq.db sync
2. Careers section in `web/`
3. LinkedIn announcement draft (`social` collection)
4. Publish checklist in `tasks/pm-agent-drafts-build`
