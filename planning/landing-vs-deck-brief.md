# Landing page vs presentation deck — decision brief

**Date:** 2026-06-09  
**Blocker:** `input-task-landing-page-on-vibe-coders-academy-denis-todo` + `input-task-presentation-document-denis-todo`  
**Context:** Presentation outline exists (`content/presentation/outline.md`, 12 slides). Landing scaffold in `web/` not started.

---

## What each path unlocks

| Path | Unblocks now | Waiting on Denis |
|------|--------------|------------------|
| **Landing first** | Waitlist CTA, vibe-coders.academy credibility, social bios URL, PO careers page host | Early bird price/date/seats (#11 backlog); brand colors optional for v0 |
| **Deck first** | Live talks, network outreach, screen recording for task #12 | Early bird on slides 10–11; brand visuals; PO/careers CTA on slide 11 |

---

## Recommendation (agent view — Denis decides)

**Landing-first** if goal is **waitlist + PO hiring this month**: one URL fixes LinkedIn bio placeholder, presentation slide 11 CTA, and careers section host.

**Deck-first** if goal is **live pitch to network before public URL**: outline is ready; export to Google Slides / Keynote is Denis manual step.

**Hybrid (minimal):** Agent scaffolds a **single-page waitlist** in `web/` (hero + syllabus bullets + waitlist form embed) while Denis builds deck from existing outline — lowest coupling.

---

## Denis reply template

```
Update: Landing page on vibe-coders.academy (Denis TODO)
Path: [landing-first | deck-first | hybrid waitlist-only]
Update: Presentation document (Denis TODO)
Format: [Google Slides | Keynote | PDF export from outline — agent can't choose for Denis]
```

---

## Agent next step after reply

- **landing-first / hybrid:** scaffold `web/` public page + waitlist section (copy draft-only).
- **deck-first:** export speaker notes to `content/presentation/speaker-notes.md`; defer landing to post-deck.
