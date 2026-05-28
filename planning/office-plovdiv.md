# Office Plovdiv — search brief

**Budget:** under **800 EUR / month** (incl. VAT assumptions TBD per listing)  
**City:** Plovdiv  
**Use:** small team / studio + occasional meetings  

## Sources (automated + manual)

| Source | URL | Notes |
|--------|-----|-------|
| alo.bg search | https://www.alo.bg/searchq/?q=офис%20под%20наем%20пловдив | Scraped (all pages) → `data/office-listings.json` |
| alo.bg category | https://www.alo.bg/obiavi/imoti-naemi/magazini-ofisi/?location_ids=3333&region_id=16 | Scraped (all pages) |
| imot.bg | https://www.imot.bg/obiavi/naemi/grad-plovdiv/ofis | Scraped (all pages) |

## Agent output

- GitHub Action: `.github/workflows/office-listings.yml` (Mondays 06:00 UTC)
- Run locally: `python3 scripts/fetch_office_listings.py`

## Denis next steps

1. Review `data/office-listings.json` after each run.
2. Shortlist 3–5 for visits (Kapana, center, Dondukov garden area).
3. Confirm deposit / VAT / fit-out before signing.

_Last updated: 2026-05-28 (batched inbox)_
