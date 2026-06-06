# Office Plovdiv — search brief

**Budget:** ~**800 EUR / month** soft cap (Denis may go higher for an exceptional space)  
**City:** Plovdiv — **central** (Kapana, center, Dondukov garden area)  
**Use:** **training room for ~20 students** — aim **40–120+ m²** (listings marked 20 m² are not viable)  
**Look:** spacious, presentable (“luxurious” where it makes sense)  

## Sources (automated + manual)

| Source | URL | Notes |
|--------|-----|-------|
| alo.bg search | https://www.alo.bg/searchq/?q=офис%20под%20наем%20пловдив | Scraped (all pages) → `data/office-listings.json` |
| alo.bg category | https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16 | Scraped (all pages) |
| imot.bg | https://www.imot.bg/obiavi/naemi/grad-plovdiv/ofis | Scraped (all pages) |

## Agent output

- GitHub Action: `.github/workflows/office-listings.yml` (Mondays 06:00 UTC)
- Scrape: `python3 scripts/fetch_office_listings.py` (alo.bg + imot.bg, all pages)
- Rank: `python3 scripts/rank_office_listings.py` (or run automatically after fetch)
- HQ **Office search** tab: top-10 tabs — **Overall**, **Location**, **Luxury**, **Best price**, plus full grid

## Rankings (automated)

Heuristic scores on scraped listings (not visit-verified):

| List | What it favors |
|------|----------------|
| Overall | Training fit + central location + quality signals + value |
| Location | Kapana, center, Old Town, Dondukov, etc. |
| Luxury | Higher €/m², premium keywords, larger polished spaces |
| Best price | Low rent with usable m² (still ≥40 m² candidates) |

**Amenity boost:** listings that explicitly mention a **kitchen** and/or **leisure room** in the description rank higher (detail pages scraped for top picks).

## Denis next steps

1. Open HQ → **Office search** → review the four top-10 lists.
2. Shortlist 3–5 for visits; confirm real capacity, photos, and VAT/deposit.
3. Reply in Slack when ready to lock a lease target.

## Suggested visit shortlist (agent draft — Denis to confirm)

_Picked 2026-06-06 from `data/office-top40.md` Kapana/center list. Verify monthly rent model (some listings are hourly/coworking promos). All under €800/mo listed price._

| # | Listing | €/mo | m² | Why shortlist |
|---|---------|------|-----|---------------|
| 1 | [Зала под наем за обучения и семинари](https://www.alo.bg/zala-pod-naem-za-provejdane-na-obucheniya-i-seminari-4734755) | 26 | 42 | Explicit training/seminar use; center |
| 2 | [Офис под наем на топ локация в Капана](https://www.alo.bg/ofis-pod-naem-na-top-lokaciya-v-kapana-11108782) | 400 | 50 | Kapana; kitchen mentioned |
| 3 | [Дава се под наем офис в Капана!](https://www.alo.bg/dava-se-pod-naem-ofis-v-kapana-11136732) | 400 | 50 | Kapana; central |
| 4 | [Офис в гр. Пловдив - Капана!](https://www.alo.bg/ofis-v-gr-plovdiv-kapana-10769362) | 450 | 76 | Kapana; kitchen; larger floor plate |
| 5 | [ОФИС под наем в сърцето на Капана](https://www.alo.bg/ofis-pod-naem-v-sarceto-na-kapana-11086332) | 450 | 75 | Kapana; kitchen |

**Denis reply template:** `Update: #1 Office Plovdiv — visit shortlist: 1,2,4` (or paste URLs / edits)

_Last updated: 2026-06-06 (agent shortlist draft added)_
