#!/usr/bin/env python3
"""Seed and sync the actions collection — unified query/action cards for the HQ UI."""

from __future__ import annotations

import re
import sqlite3

from hq_db import connect, init_db, json_dumps, json_loads, upsert_collection, upsert_entry

ROLE_CHANNELS = {
    "pm": "#vibe-standup",
    "research": "#vibe-research",
    "business": "#vibe-business",
    "social": "#vibe-social",
    "developer": "#vibe-code",
}

ROLE_PROMPTS = {
    "pm": """You are the PM Agent for Vibe Coders Academy. Prefix Slack output with: 🎯 *PM Agent* |

Read data/hq.db (collections: standups, tasks, actions). After Denis replies in Slack with inputs:
1. Update the matching action(s) in actions collection — set props.status=done, store reply in props.reply.
2. Upsert today's standup with Done / Today (max 3) / Blockers / Agent next actions.
3. Sync tasks collection from roadmap priorities.
4. Run: python3 scripts/build_site.py
5. Post ≤15 line summary to #vibe-standup listing what unblocked and next agent steps.

Rules: never invent completed work; ask explicit questions only when still blocked.""",

    "research": """You are the Research Agent for Vibe Coders Academy. Prefix Slack output with: 🔍 *Research Agent* |

Trigger: post `competitor: {name}` or `research: {topic}` in #vibe-research.

1. Read research/competitors watchlist in data/hq.db.
2. Research with web / Exa MCP — cite URLs and dates.
3. Insert child entry under research/competitors with full report body.
4. Run python3 scripts/build_site.py
5. Reply in thread: 3-bullet summary + entry slug.

Rules: no invented pricing; mark unknowns; follow .cursor/rules/competitor-research.mdc.""",

    "business": """You are the Business Agent for Vibe Coders Academy. Prefix Slack output with: 📊 *Business Agent* |

Trigger: post `plan update` or `business update` in #vibe-business.

1. Read business/plan, business/messaging, tasks, research in data/hq.db.
2. Update relevant entries; note assumptions.
3. Run python3 scripts/build_site.py
4. Reply: what changed + open questions for Denis.

Rules: no pricing/launch claims unless in messaging entry; follow brand-voice rule.""",

    "social": """You are the Social Agent for Vibe Coders Academy. Prefix Slack output with: 📣 *Social Agent* |

Trigger: post `draft: {brief}` in #vibe-social.

1. Read business/messaging and business/plan in data/hq.db.
2. Create draft entries in social collection with props.approved=false.
3. Run python3 scripts/build_site.py
4. Reply with previews; Denis approves via `approve: {slug}` in Slack.

Rules: NEVER publish here; follow .cursor/rules/social-guardrails.mdc.""",

    "developer": """You are the Developer Agent for Vibe Coders Academy. Prefix Slack output with: 🛠 *Dev Agent* |

Trigger: @Cursor or post in #vibe-code with a dev task (repo must be attached).

1. Read the request and relevant entries in data/hq.db for context.
2. Implement in the vibe-coding-101 repo — minimal focused diffs.
3. Run python3 scripts/build_site.py if data/UI changed.
4. Reply with: what changed, how to test, any blockers.

Scope: web/, scripts/, data/ — landing page, HQ UI, build pipeline, SQLite helpers.
Rules: match existing conventions; no scope creep; ask before destructive changes.""",
}


def action_props(
    kind: str,
    role: str,
    *,
    priority: int = 2,
    status: str = "open",
    slack_reply: str = "",
    prompt: str = "",
    hint: str = "",
    trigger: str = "",
    input_label: str = "",
    input_example: str = "",
    source: dict | None = None,
) -> dict:
    return {
        "kind": kind,
        "role": role,
        "priority": priority,
        "status": status,
        "slack_channel": ROLE_CHANNELS.get(role, "#vibe-inbox"),
        "slack_reply": slack_reply,
        "slack_trigger": trigger,
        "prompt": prompt,
        "hint": hint,
        "input_label": input_label,
        "input_example": input_example,
        "source": source or {},
    }


def slugify(text: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")[:60]


def _inbox_status(meta: dict) -> str:
    return (meta or {}).get("inbox_status", "open")


def build_inbox_batch(actions: list[dict]) -> dict:
    """Single Slack template listing all open inputs (numbered)."""
    inputs = [
        a
        for a in actions
        if a.get("kind") == "input" and a.get("status") in ("open", "in_progress")
    ]
    inputs.sort(key=lambda a: (a.get("priority", 2), a.get("title", "")))
    lines = [
        "standup batch — reply in #vibe-code or #vibe-standup with numbered answers:",
        "",
    ]
    for index, action in enumerate(inputs, start=1):
        lines.append(f"{index}. {action['title']}")
        if action.get("slackReply"):
            lines.append(f"   {action['slackReply'].strip()}")
        lines.append("")
    if len(inputs) == 1:
        lines.append("(Or reply with a single line using the template above.)")
    return {
        "channel": "#vibe-standup",
        "count": len(inputs),
        "slackReply": "\n".join(lines).rstrip(),
    }


def _prune_stale_actions(conn: sqlite3.Connection, active_slugs: set[str]) -> None:
    rows = conn.execute(
        "SELECT slug FROM entries WHERE collection='actions' AND json_extract(props,'$.kind') IN ('input','approve')"
    ).fetchall()
    for row in rows:
        slug = row["slug"]
        if slug.startswith("role-prompt-"):
            continue
        if slug not in active_slugs:
            conn.execute("DELETE FROM entries WHERE collection='actions' AND slug=?", (slug,))


def sync_actions(conn: sqlite3.Connection) -> None:
    active_slugs: set[str] = set()
    upsert_collection(
        conn,
        "actions",
        "Actions",
        "Unified inbox: inputs, approvals, and copy-paste prompts",
        "inbox",
        5,
    )

    # Role prompt kits (kind=prompt, always available)
    for role, prompt in ROLE_PROMPTS.items():
        upsert_entry(
            conn,
            "actions",
            f"role-prompt-{role}",
            f"{role.title()} — role prompt",
            body=prompt,
            props=action_props("prompt", role, priority=0, status="ready", prompt=prompt, trigger=_role_trigger(role)),
            sort_order=0,
        )

    order = 10

    # Blockers → input actions
    blockers = conn.execute(
        """
        SELECT li.id, li.text, li.meta
        FROM list_items li
        JOIN entries e ON e.id = li.entry_id
        WHERE e.collection='tasks' AND e.slug='blockers' AND li.section='items'
        ORDER BY li.sort_order
        """
    ).fetchall()
    for row in blockers:
        meta = json_loads(row["meta"])
        status = _inbox_status(meta)
        if status in ("done", "backlog"):
            continue
        owner_note = meta.get("owner", "")
        hint = owner_note.split("→")[-1].strip() if "→" in owner_note else owner_note
        if status == "in_progress":
            hint = meta.get("reply") or hint or "In progress — Denis owns next step"
        text = row["text"]
        slug = f"input-blocker-{slugify(text)}"
        slack_reply = _blocker_slack_reply(text)
        upsert_entry(
            conn,
            "actions",
            slug,
            text,
            props=action_props(
                "input",
                "pm",
                priority=1,
                status=status if status in ("open", "in_progress") else "open",
                slack_reply=slack_reply,
                hint=hint or "Unblocks agent work after you reply in Slack",
                trigger="standup",
                input_label=_input_label(text),
                input_example=_input_example(text),
                source={"collection": "tasks", "slug": "blockers", "listItemId": row["id"]},
            ),
            sort_order=order,
        )
        active_slugs.add(slug)
        order += 1

    # Denis open tasks → input actions
    denis_tasks = conn.execute(
        """
        SELECT li.id, li.text, li.done, li.meta, e.slug AS group_slug
        FROM list_items li
        JOIN entries e ON e.id = li.entry_id
        WHERE e.collection='tasks' AND e.owner='denis' AND li.section='items' AND li.done=0
        ORDER BY li.sort_order
        """
    ).fetchall()
    for row in denis_tasks:
        meta = json_loads(row["meta"]) if row["meta"] else {}
        status = _inbox_status(meta)
        if status in ("done", "backlog"):
            continue
        text = row["text"]
        slug = f"input-task-{slugify(text)}"
        brand = _brand_sprint_action(text, meta)
        upsert_entry(
            conn,
            "actions",
            slug,
            text,
            props=action_props(
                "input",
                brand.get("role", "pm"),
                priority=brand.get("priority", 2),
                status=status if status in ("open", "in_progress") else "open",
                slack_reply=brand.get("slack_reply")
                or meta.get("slack_reply")
                or (f"Done: {text}" if "publish" in text.lower() else f"Update: {text}"),
                hint=brand.get("hint") or meta.get("reply") or "Denis manual task from launch path",
                trigger=brand.get("trigger", "standup"),
                source={"collection": "tasks", "slug": row["group_slug"], "listItemId": row["id"]},
            ),
            sort_order=order,
        )
        active_slugs.add(slug)
        order += 1

    # Automations → approve actions
    automations = conn.execute(
        "SELECT slug, title, body, props FROM entries WHERE collection='automations' ORDER BY sort_order"
    ).fetchall()
    for row in automations:
        props = json_loads(row["props"])
        settings = props.get("settings", {})
        role = _automation_role(row["slug"])
        trigger = settings.get("trigger", "")
        also = settings.get("also", "")
        upsert_entry(
            conn,
            "actions",
            f"approve-{row['slug']}",
            row["title"],
            body=row["body"],
            props=action_props(
                "approve",
                role,
                priority=3,
                slack_reply=_approve_slack_reply(role, trigger, also),
                prompt=row["body"],
                hint=f"Green-light: {trigger or 'scheduled run'}",
                trigger=also or trigger,
                source={"collection": "automations", "slug": row["slug"]},
            ),
            sort_order=order,
        )
        active_slugs.add(f"approve-{row['slug']}")
        order += 1

    # Social drafts pending approval
    social = conn.execute(
        "SELECT slug, title, props FROM entries WHERE collection='social' AND json_extract(props,'$.approved')=0"
    ).fetchall()
    for row in social:
        props = json_loads(row["props"])
        upsert_entry(
            conn,
            "actions",
            f"approve-social-{row['slug']}",
            f"Approve: {row['title']}",
            props=action_props(
                "approve",
                "social",
                priority=2,
                slack_reply=f"approve: {row['slug']}",
                hint="Approves draft for publish automation",
                trigger="draft",
                source={"collection": "social", "slug": row["slug"]},
            ),
            sort_order=order,
        )
        active_slugs.add(f"approve-social-{row['slug']}")
        order += 1

    # Messaging gaps
    messaging = conn.execute(
        "SELECT props FROM entries WHERE collection='business' AND slug='messaging'"
    ).fetchone()
    if messaging:
        course = json_loads(messaging["props"]).get("course", {})
        one = (course.get("one-liner") or "").strip()
        if not one or one in ("TBD", "_TBD_"):
            upsert_entry(
                conn,
                "actions",
                "input-one-liner",
                "Provide course one-liner",
                props=action_props(
                    "input",
                    "business",
                    priority=1,
                    slack_reply="One-liner: ",
                    hint="Blocks customer-facing copy and social drafts",
                    trigger="plan",
                    input_label="One-liner",
                    input_example="Ship real projects with Cursor and AI agents — practitioner-first.",
                    source={"collection": "business", "slug": "messaging"},
                ),
                sort_order=5,
            )
            active_slugs.add("input-one-liner")

    _prune_stale_actions(conn, active_slugs)


def _brand_sprint_action(text: str, meta: dict) -> dict:
    """Custom inbox cards for the 4-day brand sprint tasks."""
    if not text.lower().startswith("brand sprint day"):
        return {}
    day_match = re.search(r"day\s*(\d)", text, re.I)
    day = int(day_match.group(1)) if day_match else 0
    replies = {
        1: "brand day1: ICP= — NOT for= — secret sauce= — ops=",
        2: "brand day2: visual= — one-liner= — CTA= — tone OK=",
        3: "brand day3: channels= — facebook= — rhythm= — path=",
        4: "brand day4: budget= — early bird= — plan=",
    }
    hints = {
        1: "Day 1 — ICP, anti-audience, secret sauce, PO/consultant model",
        2: "Day 2 — visual A/B/C, one-liner, primary CTA",
        3: "Day 3 — channel rank, Facebook strategy, deck/landing path",
        4: "Day 4 — budget tier + 90-day calendar sign-off",
    }
    if day not in replies:
        return {}
    return {
        "role": "business",
        "priority": 1 if day == 1 else 2,
        "slack_reply": replies[day],
        "hint": hints[day],
        "trigger": "brand sprint",
    }


def _role_trigger(role: str) -> str:
    return {
        "pm": "standup",
        "research": "competitor: {name}",
        "business": "plan update",
        "social": "draft: {brief}",
        "developer": "@Cursor {task} in #vibe-code",
    }[role]


def _automation_role(slug: str) -> str:
    if "standup" in slug:
        return "pm"
    if "competitor" in slug or "research" in slug:
        return "research"
    if "business" in slug or "plan" in slug:
        return "business"
    if "social" in slug:
        return "social"
    return "pm"


def _blocker_slack_reply(text: str) -> str:
    lower = text.lower()
    if "one-liner" in lower:
        return "One-liner: "
    if "po apply" in lower or "publish channel" in lower:
        return "PO apply: email | form URL | LinkedIn Easy Apply — publish first on: "
    if "early bird" in lower:
        return "Early bird: price= | end date= | max seats= | legal line= "
    if "brand" in lower:
        return "Brand direction: colors= | logo style= | DIY or hire designer= "
    if "domain" in lower or "vibe-coders.academy" in lower:
        return "Domain: vibe-coders.academy status= (registrar/DNS notes) "
    if "plovdiv" in lower and "landscape" in lower:
        return "Research: Plovdiv IT/AI landscape — notes= "
    if "softuni" in lower or "positioning" in lower:
        return "Positioning vs SoftUni: "
    return f"Re: {text} — "


def _input_label(text: str) -> str:
    if "one-liner" in text.lower():
        return "Approved one-liner"
    if "early bird" in text.lower():
        return "Early bird terms"
    if "brand" in text.lower():
        return "Brand direction"
    return "Your answer"


def _input_example(text: str) -> str:
    if "one-liner" in text.lower():
        return "Ship real projects with Cursor and AI agents — not theory slides."
    if "early bird" in text.lower():
        return "price=299 BGN | end=2026-07-15 | seats=20 | legal=Terms on site"
    return ""


def _approve_slack_reply(role: str, trigger: str, also: str) -> str:
    channel = ROLE_CHANNELS.get(role, "#vibe-inbox")
    if role == "pm":
        return "standup"
    if role == "research":
        return "competitor: SoftUni AI"
    if role == "business":
        return "plan update positioning"
    if role == "social":
        return "draft: 2 linkedin posts about Cursor automations"
    if "slack" in (also or trigger).lower():
        return also.split("→")[-1].strip() if "→" in also else trigger
    return f"Run {role} agent"


def sync_all() -> None:
    init_db()
    with connect() as conn:
        sync_actions(conn)
        conn.commit()
    print("Synced actions collection")


if __name__ == "__main__":
    sync_all()
