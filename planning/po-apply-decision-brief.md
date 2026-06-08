# PO position — apply method & publish channels (decision brief)

**Date:** 2026-06-08  
**Blocker:** `input-blocker-po-apply-method-publish-channels` (priority 1)  
**Goal:** Unblock agent work on careers page copy, publish checklist, LinkedIn announcement draft

---

## Gap found (repo check)

- `jobs/product-owner` in `data/hq.db` has **empty body** and `position_text: ""`
- `business/jobs/product-owner.md` **does not exist** in repo (task marked done 2026-05-27 — content may never have been committed)
- **Agent cannot invent official JD text.** Denis must paste or approve PO job description before publish.

---

## Apply method options (pick one)

| Method | Pros | Cons | Agent can automate |
|--------|------|------|-------------------|
| **Email** (`careers@vibe-coders.academy` or personal) | Fastest; no extra tooling | Manual triage; no tracking | Careers page + mailto link |
| **Google Form / Tally** | Structured CV + questions; free | Another URL to maintain | Embed link on careers page |
| **LinkedIn Easy Apply** | Reach; familiar for PO candidates | Needs LinkedIn company page + paid job post? | Announcement post + link |

**Suggested default (if Denis wants speed):** Google Form for structured intake + LinkedIn post pointing to form (no Easy Apply until company page exists).

---

## Publish channel options (pick first channel)

| Channel | Ready? | Blocker |
|---------|--------|---------|
| **LinkedIn** (Denis personal + later company page) | Social drafts exist; profiles not created | Denis approves bios; creates accounts |
| **Bulgarian boards** (jobs.bg, etc.) | Not set up | Denis picks board + account |
| **Network / Slack / dev communities** | Ready now | Needs final JD + apply link |

**Suggested first channel:** LinkedIn (Denis network) — aligns with `#2 Publish & share PO position`.

---

## What Denis should reply (HQ Inbox template)

```
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
```

Optional: paste PO JD in same reply or confirm agent should draft from `business/plan` + syllabus (Denis review required).

---

## Unblocks after reply

1. Agent writes `business/jobs/product-owner.md` + syncs `jobs/product-owner` in hq.db
2. Careers section scaffold in `web/`
3. LinkedIn announcement draft in `social` collection
4. Publish checklist in `tasks/pm-agent-drafts-build`
