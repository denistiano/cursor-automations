# Denis action pack — 2026-06-14

Batch replies for HQ Inbox. Paste each block in #vibe-standup (or reply via HQ copy buttons).

---

## 1. PO apply + JD (priority 1 blocker)

```
PO JD: [paste full text | approve skeleton expansion]
PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [LinkedIn | jobs.bg | network]
```

**Suggested minimum (if you want speed):** Google Form URL + publish first on LinkedIn (personal network).

---

## 2. Office — pick 3 visits

```
Office visits: [1, 2, 3] from planning/office-visit-shortlist-refresh-2026-06-10.md
```

| # | Listing | €/mo | m² |
|---|---------|------|-----|
| 1 | [В сърцето на Капана](https://www.alo.bg/v-sarceto-na-kapana-za-parvi-naemateli-za-razlichni-deinosti-10915009) | 550 | 64 |
| 2 | [Kapana — бизнес пространство](https://www.alo.bg/kapana-za-parvi-naemateli-prostranstvo-za-biznes-i-vdahnovenie-11104973) | 750 | 80 |
| 3 | [Зала за обучения](https://www.alo.bg/zala-pod-naem-za-provejdane-na-obucheniya-i-seminari-4734755) | ~26* | 42 |
| 4 | [Зала — курсове](https://www.alo.bg/zala-pod-naem-obucheniya-seminari-kursove-plovdiv-7944729) | 100* | TBD |
| 5 | [Офис широк център](https://www.alo.bg/ofis-pod-naem-shirok-centar-10481212) | 400 | 90 |

\* Confirm monthly vs session pricing before visits.

---

## 3. Landing vs deck path

```
Path: [deck-first | landing-first | hybrid] — CTA: [waitlist | LinkedIn | early bird] — brand: [approve draft | defer]
```

---

## 4. HQ Inbox — social + automations

```
approve: linkedin-page-bio
approve: linkedin-first-post
approve: x-bio-and-first-post
```

---

## Agent prompt (copy-paste — fill `[...]` only)

```
You are helping Denis (founder, Vibe Coders Academy) clear his HQ Inbox in one session. Repo: denistiano/cursor-automations. Data: data/hq.db (collections: actions, tasks, jobs, social).

## Goal
Unblock PO hiring, office visits, public-facing assets, and social launch prep — using only Denis's decisions below.

## Denis inputs (fill before running)
- PO JD: [paste full job description OR write "expand skeleton in planning/po-jd-skeleton-2026-06-10.md"]
- PO apply method: [email address | Google Form URL | LinkedIn Easy Apply]
- PO publish first on: [LinkedIn personal | jobs.bg | network only]
- Office visit picks (numbers 1–5): [e.g. 1, 2, 5]
- Landing vs deck: [deck-first | landing-first | hybrid one-pager]
- Primary CTA: [waitlist URL | LinkedIn DM | early bird — if early bird: price/seats/legal line]
- Social bios approved: [yes — all three drafts | edits: ...]
- Brand colors: [approve agent draft | defer]

## Execute (in order)
1. Write business/jobs/product-owner.md from JD; sync jobs/product-owner in hq.db; add careers section stub in web/.
2. Create publish checklist + LinkedIn announcement draft in social collection (draft-only).
3. For office picks: add visit-priority table to planning/office-plovdiv.md with landlord call script (monthly all-in, deposit, capacity ~20).
4. Per landing/deck choice: either export content/presentation/speaker-notes.md from outline.md OR scaffold minimal marketing landing in web/ (hero + waitlist + careers link).
5. Mark matching actions done in hq.db (props.status=done, props.reply=Denis inputs); update tasks list_items.
6. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
7. Reply with: files changed, what still needs Denis manual action (LinkedIn account creation, actual job post publish, physical visits).

## Constraints
- Never invent compensation, equity, pricing, or launch dates.
- Social: draft-only; no publishing.
- Match existing repo conventions; minimal focused diffs.
```
