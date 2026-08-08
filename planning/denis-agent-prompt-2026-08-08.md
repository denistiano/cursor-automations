# Denis → agent prompt pack (2026-08-08)

Copy-paste the block below into a new agent run. Fill `[…]` placeholders only.

---

```
You are helping Denis (founder, Vibe Coders Academy) clear P1 blockers and unblock agent automations. Repo: cursor-automations. Data store: data/hq.db.

## Context

Vibe Coders Academy is a practitioner-first Cursor/AI cohort in Plovdiv — students ship real repos, automations, and landing pages. We are pre-launch: PO hire, office lease, brand plan, and public assets (landing/deck, social) are waiting on Denis decisions. Last Denis HQ Inbox reply: 2026-06-10. PO blocker day 64; office shortlist A′/B′/C re-validated 2026-08-08 (still listed on 2026-08-03 scrape).

## What we need to achieve

1. Publish PO role with official JD + apply link on at least one channel (LinkedIn preferred).
2. Lock 3 office visit targets in Plovdiv (<€800/mo, ~20 seats, training use).
3. Green-light HQ Inbox (4 automations + 3 social drafts) so scheduled agents and profile setup can proceed.
4. (Stretch) Brand sprint day 1 positioning answers to unblock marketing plan merge.

## Denis inputs (fill these)

### PO apply + publish
- Apply method: [Google Form URL | email careers@… | LinkedIn Easy Apply]
- First publish channel: [LinkedIn | jobs.bg | network]
- JD: [approve planning/po-jd-expanded-draft-2026-06-19.md | paste official JD below]
- PO type/compensation: [part-time | full-time | contract] — [comp range or structure]
- Remote %: [0–100%]

### Office visits (A′/B′/C validated 2026-08-08 — still listed)
Pick 3 from data/office-top40.md or paste URLs:
- A′ Kapana €600: https://www.alo.bg/targovsko-pomeshtenie-kv-kapana-top-oferta-10658435
- B′ Center €450: https://www.alo.bg/ofis-v-gr-plovdiv-stochna-gara-10639118
- C Training €26*: https://www.alo.bg/zala-pod-naem-za-provejdane-na-obucheniya-i-seminari-4734755
- My picks: [A′, B′, C | or paste 3 URLs]

### HQ Inbox batch (copy to Slack as-is if approving all)
- approve: linkedin-page-bio
- approve: linkedin-first-post
- approve: x-bio-and-first-post
- standup
- competitor: SoftUni AI
- plan update positioning
- draft: 2 linkedin posts about Cursor automations
- Approving all above: [yes | no — list exceptions]

### Brand sprint day 1 (optional this run)
- ICP: [one sentence primary audience]
- NOT for: [anti-audience]
- Secret sauce: [3 bullets max]
- Ops model 90d: [full-time PO | consultant | hybrid]

### Landing vs deck (optional)
- Path: [deck-first | landing-first | hybrid one-pager + deck]
- Primary CTA: [waitlist | PO apply | info session]

## How to execute (agent)

After Denis fills inputs:
1. Update matching actions in data/hq.db (props.status=done, props.reply=…).
2. If PO JD approved: create business/jobs/product-owner.md, sync jobs/product-owner, scaffold careers in web/.
3. If office picks: update planning/office-plovdiv.md + lease comparison in HQ.
4. Run: python3 scripts/sync_actions.py && python3 scripts/build_site.py
5. Post summary to #vibe-standup.
```
