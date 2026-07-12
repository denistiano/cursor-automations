# Office shortlist A/B/C — live verify (2026-07-12)

**Task:** `input-task-1-office-plovdiv-budget-area-constraints-visit-shortlist`  
**Last full scrape:** 2026-06-19 (23 days stale — URL picks still valid)  
**Previous verify:** 2026-07-11 (all 200)  
**Source:** `planning/office-shortlist-refresh-2026-06-19.md`

---

## URL verify (2026-07-12)

| Pick | Listing | HTTP | Notes |
|------|---------|------|-------|
| **A** | [Kapana 11108782](https://www.alo.bg/ofis-pod-naem-na-top-lokaciya-v-kapana-11108782) | 200 | €400/mo, 50 m², kitchen — still #1 Kapana in cached rank |
| **B** | [Широк център 10481212](https://www.alo.bg/ofis-pod-naem-shirok-centar-10481212) | 200 | €400/mo, 90 m² — best m²/€ |
| **C** | [Зала обучения 4734755](https://www.alo.bg/zala-pod-naem-za-provejdane-na-obucheniya-i-seminari-4734755) | 200 | €25.56/mo listed — **confirm monthly vs per-session** (YMCA Plovdiv) |

All three URLs respond. No Denis `Office visits:` reply since 2026-06-15 standup (**day 27** on office picks).

---

## Top 3 steps for Denis

1. **Confirm picks:** `Office visits: A, B, C` (or swap one URL from `data/office-top40.md`).
2. **Send landlord messages** — Bulgarian template in `planning/office-landlord-outreach-2026-06-15.md`; ask C about monthly package.
3. **Book visits** — A (Kapana) first; B if need more m²; C if cohort needs dedicated training room.

---

## Denis reply (HQ Inbox)

```
Office visits: A, B, C
```

---

## Agent next (after Denis confirms)

1. Lock finalists in `planning/office-plovdiv.md`
2. Lease comparison table in HQ
3. Fresh scrape on request (`python3 scripts/fetch_office_listings.py`)
