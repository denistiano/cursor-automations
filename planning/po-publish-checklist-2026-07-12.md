# PO publish checklist — decision + ship (2026-07-12)

**Blocker:** `input-blocker-po-apply-method-publish-channels` (priority 1, day **37** since last Denis reply)  
**JD draft:** `planning/po-jd-expanded-draft-2026-06-19.md` — **not** synced to hq.db (`jobs/product-owner` body still 0 bytes)  
**Repo check:** No Denis commits or inbox replies since 2026-06-10

---

## Top 3 steps (priority order)

1. **Pick apply method + first channel** — one line unlocks careers scaffold + LinkedIn post draft.
2. **Approve JD** — reply `approve expanded draft` OR paste official text (compensation/type placeholders remain).
3. **Agent ships** — `business/jobs/product-owner.md`, sync hq.db, careers section in `web/`, LinkedIn announcement draft.

---

## Apply method options (pick one)

| Method | Pros | Cons | Best if |
|--------|------|------|---------|
| **Google Form** | Fast, no ATS cost, easy to iterate | Manual triage | First 5–10 applicants |
| **Email** | Personal, low friction | Inbox chaos at scale | Network-first hire |
| **LinkedIn Easy Apply** | Reach, built-in funnel | Needs company page + JD live | Broad visibility |

**Suggested default (cautious):** Google Form → publish on **LinkedIn** first (PO role is founder-facing; network reach matters).

---

## Denis reply (HQ Inbox / Slack)

```
PO apply: Google Form https://forms.gle/[YOUR_ID] — publish first on: LinkedIn
PO JD: approve expanded draft
```

Optional same message: `remote=hybrid 2d/wk | type=part-time | comp=negotiable`

---

## What agent delivers after reply (≤1 session)

1. Commit `business/jobs/product-owner.md` from approved draft
2. Upsert `jobs/product-owner` in `data/hq.db`
3. Careers stub in `web/` (link from HQ nav when ready)
4. LinkedIn announcement post draft in `social/` collection
5. Mark `input-blocker-po-apply-method-publish-channels` + `#2 Publish & share PO` actions `done`

---

## Still blocked without this

- Careers page copy
- LinkedIn PO announcement
- Brand/social CTAs referencing “we’re hiring”
- PO interview pipeline
