#!/usr/bin/env python3
"""Brand sprint 2026-06-19 — tasks, actions, business plan, standup, research."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import (
    ROOT,
    connect,
    entry_by_slug,
    init_db,
    json_dumps,
    json_loads,
    replace_list_items,
    replace_table,
    upsert_collection,
    upsert_entry,
)

STANDUP_DATE = "2026-06-19"
SPRINT_START = "2026-06-19"
SPRINT_END = "2026-06-22"


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def upsert_brand_sprint_roadmap(conn) -> int:
    upsert_collection(
        conn,
        "roadmap",
        "Roadmap",
        "Launch tracks, phases, and brand sprint",
        "map",
        20,
    )
    body = _read("planning/brand-sprint-2026-06-19.md")
    entry_id = upsert_entry(
        conn,
        "roadmap",
        "brand-sprint",
        "Brand sprint — 4 days",
        body=body,
        props={
            "sprint_start": SPRINT_START,
            "sprint_end": SPRINT_END,
            "current_day": 1,
            "plan_doc": "planning/brand-marketing-plan-draft-2026-06-19.md",
        },
        sort_order=4,
    )
    days = [
        ("day1", [
            "Read research/2026-06-19-brand-positioning-secret-sauce",
            "Pick primary ICP (one sentence)",
            "Confirm anti-audience + 3-bullet secret sauce",
            "Choose ops model: full-time PO | consultant | hybrid",
            "Slack: brand day1: ICP=… — NOT for=… — secret sauce=… — ops=…",
        ]),
        ("day2", [
            "Read content/brand/creative-brief.md — pick visual A/B/C",
            "Confirm one-liner + sub-line",
            "Pick primary CTA: waitlist | LinkedIn | info session",
            "Approve tone (practitioner / no hype)",
            "Slack: brand day2: visual=… — one-liner=… — CTA=… — tone OK=…",
        ]),
        ("day3", [
            "Rank channels for 90 days (LinkedIn, FB, X, YouTube, meetups, paid)",
            "Facebook page purpose: hub | events | repost | skip",
            "Pick content rhythm (2×/week LI, etc.)",
            "Path: deck-first | landing-first | hybrid",
            "Slack: brand day3: channels=… — facebook=… — rhythm=… — path=…",
        ]),
        ("day4", [
            "Pick budget tier: lean | medium | aggressive",
            "Early bird: defer OR price/seats/month",
            "Review 90-day calendar in brand-marketing-plan-draft",
            "Slack: brand day4: budget=… — early bird=… — plan=approved|edits",
        ]),
    ]
    for section, lines in days:
        replace_list_items(
            conn,
            entry_id,
            section,
            [{"text": t, "meta": {"owner": "Denis"}} for t in lines],
        )

    replace_table(
        conn,
        entry_id,
        "budget_scenarios",
        ["tier", "monthly_eur", "best_for", "includes"],
        [
            {
                "tier": "Lean",
                "monthly_eur": "€50–200",
                "best_for": "Pre-waitlist; founder-led LI only",
                "includes": "Tools only; no paid ads; DIY brand",
            },
            {
                "tier": "Medium",
                "monthly_eur": "€1–2.5k",
                "best_for": "Landing live + part-time ops",
                "includes": "Modest ads; design; PO/consultant partial",
            },
            {
                "tier": "Aggressive",
                "monthly_eur": "€4–8k",
                "best_for": "Fast cohort fill",
                "includes": "Always-on paid; video; events; FT ops",
            },
        ],
    )

    replace_list_items(
        conn,
        entry_id,
        "resources",
        [
            {"text": "SoftUni Vibe Coding — https://ai.softuni.bg/application-vibe-coding", "meta": {"tag": "competitor"}},
            {"text": "Telerik marketing budgets sprint — https://www.telerikacademy.com/sprint/marketing-budgets-that-drive-growth", "meta": {"tag": "budget"}},
            {"text": "BG Google Ads CPA case study — https://www.adwaycreative.bg/arlet-k-professional-training-center-case-study-google-ads-strategy/", "meta": {"tag": "paid"}},
            {"text": "Internal: planning/brand-marketing-plan-draft-2026-06-19.md", "meta": {"tag": "plan"}},
            {"text": "Internal: content/brand/creative-brief.md", "meta": {"tag": "brand"}},
            {"text": "Internal: planning/landing-vs-deck-decision-brief.md", "meta": {"tag": "decision"}},
        ],
    )
    return entry_id


def upsert_research(conn) -> None:
    body = _read("planning/research-brand-positioning-2026-06-19.md")
    upsert_entry(
        conn,
        "research",
        "2026-06-19-brand-positioning-secret-sauce",
        "Brand positioning & secret sauce",
        body=body,
        props={"report_date": "2026-06-19", "scope": "brand", "confidence": "high"},
        sort_order=10,
    )


def _section(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    chunk = text.split(start, 1)[1]
    if end in chunk:
        chunk = chunk.split(end, 1)[0]
    return start + chunk.strip()


def upsert_business_plan(conn) -> None:
    plan_body = _read("planning/brand-marketing-plan-draft-2026-06-19.md")
    upsert_entry(
        conn,
        "business",
        "plan",
        "Business plan v1",
        body=plan_body,
        props={"last_updated": "2026-06-19", "status": "draft", "sprint": "brand-2026-06-19"},
    )
    sections = {
        "plan-1-executive-summary": _section(plan_body, "## 1. Executive summary", "## 2."),
        "plan-2-problem-icp": _section(plan_body, "## 2. Positioning", "## 3."),
        "plan-6-go-to-market": _section(plan_body, "## 4. Channel strategy", "## 5."),
        "plan-7-revenue-model": _section(plan_body, "## 6. Budget scenarios", "## 7."),
        "plan-8-90-day-roadmap": _section(plan_body, "## 7. 90-day rollout", "## 8."),
    }
    for slug, body in sections.items():
        title = slug.replace("plan-", "").replace("-", " ").title()
        upsert_entry(conn, "business", slug, title, body=body)


def upsert_brand_actions(conn) -> None:
    """Brand sprint inbox cards are synced from denis-decisions-manual tasks."""
    pass


def patch_tasks(conn) -> None:
    entry = entry_by_slug(conn, "tasks", "denis-decisions-manual")
    if not entry:
        return
    rows = conn.execute(
        "SELECT text, done, meta, sort_order FROM list_items WHERE entry_id=? AND section='items' ORDER BY sort_order",
        (entry["id"],),
    ).fetchall()
    items = [
        {"text": r["text"], "done": bool(r["done"]), "meta": json_loads(r["meta"]), "sort_order": r["sort_order"]}
        for r in rows
    ]
    sprint_tasks = [
        "Brand sprint day 1 — positioning & secret sauce (HQ → Brand sprint)",
        "Brand sprint day 2 — visual identity + CTA",
        "Brand sprint day 3 — channels + Facebook strategy + deck/landing path",
        "Brand sprint day 4 — budget tier + 90-day calendar sign-off",
    ]
    existing_texts = {i["text"] for i in items}
    sort_base = max((i.get("sort_order", 0) for i in items), default=0) + 1
    for offset, task in enumerate(sprint_tasks):
        if task not in existing_texts:
            items.append(
                {
                    "text": task,
                    "done": False,
                    "meta": {"owner": "Denis", "inbox_status": "in_progress", "sprint": "brand-2026-06-19"},
                    "sort_order": sort_base + offset,
                }
            )
    replace_list_items(conn, entry["id"], "items", items)

    pm = entry_by_slug(conn, "tasks", "pm-agent-drafts-build")
    if pm:
        pm_rows = conn.execute(
            "SELECT text, done, meta, sort_order FROM list_items WHERE entry_id=? AND section='items' ORDER BY sort_order",
            (pm["id"],),
        ).fetchall()
        pm_items = [
            {"text": r["text"], "done": bool(r["done"]), "meta": json_loads(r["meta"]), "sort_order": r["sort_order"]}
            for r in pm_rows
        ]
        agent_task = "Brand sprint HQ tab + marketing plan draft (2026-06-19)"
        if not any(agent_task in i["text"] for i in pm_items):
            pm_items.append({"text": agent_task, "done": True, "meta": {"owner": "agent"}, "sort_order": 999})
        replace_list_items(conn, pm["id"], "items", pm_items)


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
            "Agent: Brand sprint plan + marketing draft → planning/brand-marketing-plan-draft-2026-06-19.md",
            "Agent: Brand positioning research → research/2026-06-19-brand-positioning-secret-sauce",
            "Agent: Creative brief draft → content/brand/creative-brief.md",
            "Agent: HQ Brand sprint tab + 4 daily inbox actions",
        ],
        "ongoing": [
            "Denis: Brand sprint days 1–4 (19–22 Jun) — complete marketing plan",
            "Denis: PO interviews + ops model (consultant vs FT vs hybrid)",
            "Denis: Facebook page (empty) — strategy in brand sprint day 3",
            "Denis: Office Plovdiv — pick 3 visits",
            "Denis: HQ Inbox — automations + social drafts still open",
        ],
        "today": [
            "Denis: Brand sprint day 1 — ICP + secret sauce + ops model (HQ → Brand sprint)",
            "Denis: PO apply + channels (if not done)",
            "Denis: HQ Inbox — approve LinkedIn bio + first post when ready",
        ],
        "blockers": [
            "Brand plan incomplete until sprint days 1–4 answered",
            "Early bird pricing deferred until Denis legal line",
        ],
        "agent_next": [
            "After brand day1 → refine positioning in business/plan",
            "After brand day3 → FB page copy + channel-specific drafts",
            "After brand day4 → merge approved plan; unlock landing/social CTA",
        ],
    }
    for section, lines in sections.items():
        replace_list_items(conn, entry_id, section, [{"text": t} for t in lines])


def main() -> None:
    init_db()
    with connect() as conn:
        upsert_brand_sprint_roadmap(conn)
        upsert_research(conn)
        upsert_business_plan(conn)
        upsert_brand_actions(conn)
        patch_tasks(conn)
        upsert_standup(conn)
        conn.commit()
    print("Applied brand sprint 2026-06-19")


if __name__ == "__main__":
    main()
