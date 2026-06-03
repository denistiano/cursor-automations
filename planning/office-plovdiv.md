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

_Last updated: 2026-06-03 (Denis: central Plovdiv, ~20 students, top-10 lists)_
