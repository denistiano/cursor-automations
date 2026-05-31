#!/usr/bin/env python3
"""PM standup 2026-05-31 — upsert standup + Denis input prompts in hq.db."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, entry_by_slug, init_db, json_dumps, json_loads, replace_list_items, upsert_entry

STANDUP_DATE = "2026-05-31"

DENIS_BATCH_PROMPT = """You are helping Denis (founder, Vibe Coders Academy) unblock launch work. Context: practitioner-first AI/Cursor course in Bulgaria; one-liner approved ("Стани част от AI революцията"); domain vibe-coders.academy registered; PO job draft in repo; 689 Plovdiv office listings in HQ (<800 EUR/mo filter). Denis owes updates — fill in [BRACKETS] from his replies, then write each answer to the matching hq.db action (props.status=done, props.reply=...) and unblock agent tasks.

1. PO hiring — apply method = [email | form URL | LinkedIn Easy Apply]; publish first on = [LinkedIn | job board | network]
2. Office Plovdiv — shortlist/visits = [listing URLs or "none yet"]; area preference = [Kapana | center | other]; budget = [<800 EUR/mo confirmed?]
3. Landing vs deck — priority = [landing first | presentation first | both]; status = [not started | in progress | blocked on X]
4. Social accounts — platforms = [LinkedIn | FB | IG | ...]; ready to create = [yes/no — waiting on bios draft?]
5. PO published — [Done: link] or [Update: blocker]

Missing input only: Denis's bracketed answers above. After capture, run python3 scripts/sync_actions.py && python3 scripts/build_site.py and post a ≤15-line summary to #vibe-standup."""

INPUT_PROMPTS = {
    "input-blocker-po-apply-method-publish-channels": (
        "Denis must choose how PO candidates apply and where to publish first. "
        "Reply template: PO apply: [email | form URL | LinkedIn Easy Apply] — publish first on: [channel]. "
        "Unblocks: careers page copy, LinkedIn PO announcement, publish checklist in pm-agent-drafts-build."
    ),
    "input-task-1-office-plovdiv-budget-area-constraints-visit-shortlist": (
        "Denis reviews 689 Plovdiv office listings in HQ (budget <800 EUR/mo). "
        "Reply template: Update: #1 Office Plovdiv — [shortlist URLs or areas visited; Kapana/center preference; budget confirm]. "
        "Agent keeps planning/office-plovdiv.md aligned."
    ),
    "input-task-landing-page-on-vibe-coders-academy-denis-todo": (
        "Denis picks landing vs deck-first strategy. "
        "Reply template: Update: Landing page — [not started | in progress | blocked]; priority vs presentation = [landing | deck | both]. "
        "Unblocks: web/ public landing scaffold when landing-first."
    ),
    "input-task-presentation-document-denis-todo": (
        "Denis status on presentation document. "
        "Reply template: Update: Presentation document — [not started | in progress | blocked]; deck-first? [yes/no]. "
        "Agent delivers content/presentation/ outline (Today item)."
    ),
    "input-task-4-create-social-accounts-after-name-bios-approved": (
        "Denis creates social accounts after bios approved. "
        "Reply template: Update: #4 Create social accounts — platforms=[...]; bios approved=[yes/no]; blocker=[if any]. "
        "Depends on agent social bios draft (Today item)."
    ),
    "input-task-2-publish-share-po-position-linkedin-boards-network": (
        "Denis publishes PO job after apply method confirmed. "
        "Reply template: Done: #2 Publish & share PO position — [LinkedIn/board link] OR Update: [blocker]. "
        "Blocked until PO apply method + channel decided."
    ),
}


def upsert_standup(conn) -> None:
    entry_id = upsert_entry(
        conn,
        "standups",
        STANDUP_DATE,
        f"Standup — {STANDUP_DATE}",
        props={"date": STANDUP_DATE},
    )
    sections = {
        "done": [
            "_(none since 2026-05-29 — no repo commits; agent Today deliverables not yet in tree)_",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel — in progress",
            "Denis: #1 Office Plovdiv — budget/area constraints; visit shortlist (689 listings in HQ)",
            "Denis: Landing page on vibe-coders.academy OR presentation document — in progress",
            "Denis: #4 Create social accounts (after name + bios approved) — in progress",
        ],
        "today": [
            "Agent: Presentation outline + slide copy (content/presentation/) — one-liner approved; still open since 2026-05-29",
            "Denis: HQ Inbox — approve automations (standup prep, competitor research, business plan, social drafts)",
            "Agent: Social page bios + first-post pack (draft) — supports Denis social setup",
        ],
        "blockers": [
            "PO apply: How candidates apply + where to publish first → HQ Inbox input-blocker-po-apply-method-publish-channels",
        ],
        "agent_next": [
            "Ship presentation outline + social bios (Today items carried forward)",
            "After PO channels → careers page copy + LinkedIn announcement draft",
            "Office: listings last refreshed 2026-05-28; next GitHub Action run Monday 06:00 UTC",
            "Public landing scaffold in web/ when Denis picks landing vs deck-first",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def patch_action_prompts(conn) -> None:
    for slug, prompt in INPUT_PROMPTS.items():
        row = entry_by_slug(conn, "actions", slug)
        if not row:
            continue
        props = json_loads(row["props"])
        props["prompt"] = prompt
        props["batch_prompt"] = DENIS_BATCH_PROMPT
        conn.execute(
            "UPDATE entries SET props=?, updated_at=datetime('now') WHERE id=?",
            (json_dumps(props), row["id"]),
        )


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        patch_action_prompts(conn)
        conn.commit()
    print(f"Standup {STANDUP_DATE} + input prompts applied")


if __name__ == "__main__":
    main()
