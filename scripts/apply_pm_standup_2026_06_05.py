#!/usr/bin/env python3
"""PM standup 2026-06-05 — upsert standup sections + social draft entries."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, json_dumps, upsert_collection, upsert_entry

STANDUP_DATE = "2026-06-05"

SOCIAL_DRAFTS = [
    {
        "slug": "linkedin-page-bio",
        "title": "LinkedIn — page bio (draft)",
        "platform": "linkedin",
        "body": """Vibe Coders Academy — практически курс за разработчици, които искат да пускат реални проекти с AI агенти в Cursor.

Стани част от AI революцията. Бъдещето е сега.

→ Waitlist / early bird: _URL TBD (vibe-coders.academy)_
→ Не публикуваме цени или дати без одобрение от основателя.""",
    },
    {
        "slug": "linkedin-first-post",
        "title": "LinkedIn — first post (draft)",
        "platform": "linkedin",
        "body": """Стартираме Vibe Coders Academy — за dev-ове, които вече кодят и искат система: Cursor rules, skills, MCP и automations, не само chat.

Какво ще изградиш до края на кохортата:
• реален repo с агентен workflow
• automations (PM, research, content)
• launch / waitlist чернова

Ако искаш да си в първата вълна — коментар „waitlist“ или DM. (_Early bird детайли — скоро._)

#Cursor #AI #Bulgaria""",
    },
    {
        "slug": "x-bio-and-first-post",
        "title": "X — bio + first post (draft)",
        "platform": "x",
        "body": """**Bio (160 chars max — trim before publish):**
Vibe Coders Academy · Ship real projects with Cursor + agents · Стани част от AI революцията · BG/dev-first

**First post:**
Building in public: teaching devs to ship with Cursor agents + automations — not theory-only courses.

First cohort waitlist opening soon. Follow for build logs.""",
    },
]


def upsert_standup(conn) -> None:
    entry_id = upsert_entry(
        conn,
        "standups",
        STANDUP_DATE,
        f"Standup — {STANDUP_DATE}",
        props={"date": STANDUP_DATE},
    )
    from hq_db import replace_list_items

    sections = {
        "done": [
            "Office: PR #24 — top-40 rankings, kitchen/leisure scoring, data/office-top40.md",
            "Agent: Presentation outline → content/presentation/outline.md",
            "Agent: Social bios + first-post pack → social collection (3 drafts, approved=false)",
        ],
        "ongoing": [
            "Denis: PO apply method + first publish channel",
            "Denis: Office Plovdiv — review top-40; shortlist 3–5 visits",
            "Denis: Landing page OR presentation deck (outline ready)",
            "Denis: Create social accounts after approving bios",
        ],
        "today": [
            "Denis: HQ Inbox — approve automations (standup, research, business plan, social drafts)",
            "Denis: PO apply method + publish channels",
            "Denis: Office — pick 3–5 visit targets from Kapana/center top-10",
        ],
        "blockers": [
            "PO apply method + publish channels → input-blocker-po-apply-method-publish-channels",
        ],
        "agent_next": [
            "After PO channels → PO job text in repo + careers page + LinkedIn announcement draft",
            "After social copy approved → Denis creates profiles; agent can repurpose deck → posts",
            "Landing scaffold in web/ when Denis picks landing-first vs deck-first",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def seed_presentation_entry(conn) -> None:
    outline = (Path(__file__).resolve().parent.parent / "content" / "presentation" / "outline.md")
    if not outline.exists():
        return
    upsert_entry(
        conn,
        "content",
        "presentation-outline",
        "Presentation outline + slide copy",
        body=outline.read_text(encoding="utf-8"),
        props={"status": "draft", "path": "content/presentation/outline.md"},
        sort_order=30,
    )


def seed_social_drafts(conn) -> None:
    upsert_collection(
        conn,
        "social",
        "Social",
        "Draft posts — Denis approves before publish",
        "share-2",
        40,
    )
    for i, draft in enumerate(SOCIAL_DRAFTS):
        upsert_entry(
            conn,
            "social",
            draft["slug"],
            draft["title"],
            body=draft["body"],
            props={
                "platform": draft["platform"],
                "approved": False,
                "scheduled_at": None,
                "post_id": None,
            },
            sort_order=i,
        )


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_standup(conn)
        seed_presentation_entry(conn)
        seed_social_drafts(conn)
        conn.commit()
    print(f"Applied PM standup → {STANDUP_DATE}")


if __name__ == "__main__":
    main()
