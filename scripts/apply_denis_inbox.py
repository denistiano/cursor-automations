#!/usr/bin/env python3
"""Apply Denis batched inbox replies (2026-05-28) to data/hq.db."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db, json_dumps, json_loads, replace_list_items, upsert_entry
from hq_db import entry_by_slug, replace_table

ONE_LINER = "Стани част от AI революцията"
SUB_ONE_LINER = "Бъдещето е сега"


def _items(conn, collection: str, slug: str, section: str = "items"):
    entry = entry_by_slug(conn, collection, slug)
    if not entry:
        raise SystemExit(f"Missing entry {collection}/{slug}")
    rows = conn.execute(
        "SELECT text, done, meta, sort_order FROM list_items WHERE entry_id=? AND section=? ORDER BY sort_order",
        (entry["id"], section),
    ).fetchall()
    return entry["id"], [
        {
            "text": r["text"],
            "done": bool(r["done"]),
            "meta": json_loads(r["meta"]),
            "sort_order": r["sort_order"],
        }
        for r in rows
    ]


def _patch_item(items: list[dict], needle: str, **updates) -> None:
    for item in items:
        if needle in item["text"]:
            item["meta"] = {**item.get("meta", {}), **updates.get("meta", {})}
            for key, val in updates.items():
                if key != "meta":
                    item[key] = val
            return
    raise SystemExit(f"No list item matching: {needle}")


def _remove_item(items: list[dict], needle: str) -> None:
    before = len(items)
    items[:] = [i for i in items if needle not in i["text"]]
    if len(items) == before:
        raise SystemExit(f"No list item to remove: {needle}")


def update_messaging(conn) -> None:
    row = entry_by_slug(conn, "business", "messaging")
    if not row:
        return
    props = json_loads(row["props"])
    course = props.get("course", {})
    course["one-liner"] = ONE_LINER
    course["sub-one-liner"] = SUB_ONE_LINER
    course["planned-domain"] = "vibe-coders.academy — registered; landing page TODO (Denis)"
    props["course"] = course
    body = row["body"] or ""
    body = body.replace("**One-liner:** _TBD_", f"**One-liner:** {ONE_LINER}")
    body = body.replace(
        "`vibe-coders.academy` — not active yet",
        "`vibe-coders.academy` — domain purchased; landing page not live yet",
    )
    if "sub-one-liner" not in body.lower():
        body = body.replace(
            f"**One-liner:** {ONE_LINER}",
            f"**One-liner:** {ONE_LINER}\n- **Sub-one-liner:** {SUB_ONE_LINER}",
        )
    conn.execute(
        "UPDATE entries SET props=?, body=?, updated_at=datetime('now') WHERE id=?",
        (json_dumps(props), body, row["id"]),
    )


def update_blockers(conn) -> None:
    entry_id, items = _items(conn, "tasks", "blockers")
    # Resolved / deferred
    _patch_item(
        items,
        "One-liner",
        done=True,
        meta={
            "owner": "Denis",
            "inbox_status": "done",
            "reply": f"{ONE_LINER} | sub: {SUB_ONE_LINER}",
        },
    )
    _remove_item(items, "Early bird")
    _remove_item(items, "Brand direction")
    _patch_item(
        items,
        "PO apply",
        meta={
            "owner": "Denis → in progress",
            "inbox_status": "in_progress",
            "reply": "Denis handling publish channels — keep in progress",
        },
    )
    _patch_item(
        items,
        "vibe-coders.academy",
        done=True,
        meta={
            "owner": "Denis",
            "inbox_status": "done",
            "reply": "Domain purchased; landing page + presentation doc are Denis TODOs",
        },
    )
    _remove_item(items, "vibe-coders.academy")
    _remove_item(items, "SoftUni")
    items.append(
        {
            "text": "Plovdiv IT/AI courses landscape scan (expand beyond SoftUni)",
            "done": False,
            "meta": {"owner": "Research agent → report in research/", "inbox_status": "open"},
            "sort_order": len(items),
        }
    )
    replace_list_items(conn, entry_id, "items", items)


def update_denis_tasks(conn) -> None:
    entry_id, items = _items(conn, "tasks", "denis-decisions-manual")
    _patch_item(
        items,
        "#2 Publish",
        done=False,
        meta={"inbox_status": "in_progress", "reply": "Denis will publish — no duplicate agent task"},
    )
    _patch_item(
        items,
        "#1 Office",
        meta={
            "inbox_status": "in_progress",
            "reply": "Budget <800 EUR; agent researching alo.bg + imot.bg",
        },
    )
    _patch_item(
        items,
        "#4 Create social",
        meta={"inbox_status": "in_progress", "reply": "Current TODO for Denis"},
    )
    _patch_item(
        items,
        "#5 Approve brand",
        meta={"inbox_status": "backlog", "reply": "BACKLOG"},
    )
    _patch_item(
        items,
        "#11 Approve early bird",
        meta={"inbox_status": "backlog", "reply": "BACKLOG"},
    )
    _patch_item(
        items,
        "#12 Record video",
        meta={"inbox_status": "backlog", "reply": "BACKLOG — after script approved"},
    )
    for needle in ("#vibe-inbox", "MCPs: Slack", "Automations 02"):
        _remove_item(items, needle)
    # Denis TODOs called out in Slack
    extras = [
        "Landing page on vibe-coders.academy (Denis TODO)",
        "Presentation document (Denis TODO)",
    ]
    for text in extras:
        if not any(text in i["text"] for i in items):
            items.append(
                {"text": text, "done": False, "meta": {"inbox_status": "open", "owner": "Denis"}, "sort_order": len(items)}
            )
    replace_list_items(conn, entry_id, "items", items)


def add_plovdiv_research(conn) -> None:
    parent = entry_by_slug(conn, "research", "competitors")
    if not parent:
        return
    body = """# Plovdiv IT / AI courses landscape

**Date:** 2026-05-28  
**Analyst:** Developer agent (batched inbox)  
**Confidence:** medium  
**Scope:** IT, programming, and AI-related education reachable from Plovdiv (on-site, hybrid, or national online with local presence).

## Summary

Plovdiv has university and high-school AI/informatics tracks, a local IT STEP campus for multi-year software development (including Python AI modules), and access to national brands (SoftUni, NobleProg, Telerik) that sell into the city online or via Sofia/Plovdiv classrooms. There is no obvious independent “Cursor-first academy” headquartered in Plovdiv; the competitive set is a mix of degree programs, teen coding schools, and national bootcamp brands.

## Offer & positioning

| Provider | Locality | Offer & positioning | Audience | Notes |
|----------|----------|---------------------|----------|-------|
| Plovdiv University — AI (bachelor) | Plovdiv on-site | Degree in AI, ML, intelligent systems | Students 18+ | Academic path, not practitioner bootcamp |
| Plovdiv University — Informatics / ICE | Plovdiv on-site | CS / ICE engineering degrees | Students 18+ | Adjacent pipeline, long cycle |
| PU AIU short courses | Plovdiv | Applied AI basics for researchers | Academic staff / PhD | Not commercial dev training |
| GIKN “Academik Senov” gymnasium | Plovdiv | High-school “Programming for AI” specialty | Teens | Feeds university, not pro upskill |
| IT STEP Plovdiv | Plovdiv on-site + online | 2-year software dev diploma; Python AI module | 15–55 career switchers | Broad stack; not Cursor/agent-first |
| SoftUni / SoftUni AI | National online + exams | AI-first programming, vibe coding, Cursor/Copilot courses | Beginners → seniors | Primary direct competitor nationally |
| NobleProg Bulgaria | Online + Plovdiv classroom listings | Copilot, Cursor, agent workflow corporate training | Teams / pros | B2B pricing anchor |
| Telerik Academy | National online | GenAI for Developers sprint | Working developers | Certificate, self-paced |
| Logiscool / teen brands | Plovdiv franchises possible | Kids coding + intro AI | Children | Adjacent, different ICP |

## Pricing

| Provider | Price signal | Source URL | Checked |
|----------|--------------|------------|---------|
| IT STEP Plovdiv software dev | Unknown — needs manual check (contact academy) | https://plovdiv.itstep.org/razrabotka-na-softuer | 2026-05-28 |
| GIKN high school | 4000 BGN / year (2025/26 admission page) | https://gikn.eu/priem/ | 2026-05-28 |
| SoftUni AI-Assisted Development | 112.48 EUR / 5 weeks | https://ai.softuni.bg/trainings/189/ai-assisted-development-january-2026 | 2026-05-27 |
| NobleProg Cursor (Plovdiv classroom listed) | 540–2240 EUR depending on format | https://www.nobleprog.bg/cc/cursor1 | 2026-05-27 |

## Format

- **Universities / schools:** semesters, degrees, teen tracks.
- **IT STEP:** 2×/week, 4 semesters, certificate/diploma path.
- **National bootcamps:** live online + exams/projects; SoftUni adds lifetime resource access.
- **NobleProg:** instructor-led, corporate-friendly onsite/online.

## Strengths vs Vibe Coders Academy

- Established local brands (PU, IT STEP) for students already in Plovdiv.
- SoftUni/Telerik own search terms for “AI programming Bulgaria”.
- NobleProg can win corporate training budgets with onsite Plovdiv sessions.

## Gaps we can exploit

- **Practitioner Cursor + automations** for developers already working — not teen/degree/general AI literacy.
- **Ship-a-business-project** narrative (landing, agents, Slack ops) vs broad diplomas.
- **Small cohort + founder access** vs mass-market modules.

## Sources

- https://uni-plovdiv.bg/pages/index/2987/
- https://plovdiv.itstep.org/razrabotka-na-softuer
- https://gikn.eu/priem/
- https://aiu.uni-plovdiv.bg/
- Prior scan: `research/competitors/2026-05-27-bulgaria-ai-coding-market.md`

## Strategic recommendations

- Position Vibe Coders Academy as **national online with Plovdiv founder story**, not “local classroom” — compete on depth, not campus footprint.
- Use this watchlist for outreach/partnerships (IT STEP alumni, PU career events) rather than head-to-head teen marketing.
- Refresh quarterly; add any new Plovdiv meetups/bootcamps when discovered manually.
"""
    upsert_entry(
        conn,
        "research",
        "2026-05-28-plovdiv-it-ai-landscape",
        "Plovdiv IT / AI courses landscape",
        parent_id=parent["id"],
        body=body,
        props={"report_date": "2026-05-28", "scope": "plovdiv", "confidence": "medium"},
        sort_order=2,
    )
    # Extend watchlist with Plovdiv-local rows
    tables = conn.execute(
        "SELECT id, columns FROM tables WHERE entry_id=? AND name='watchlist'",
        (parent["id"],),
    ).fetchone()
    if tables:
        cols = json_loads(tables["columns"])
        existing = conn.execute(
            "SELECT cells FROM table_rows WHERE table_id=? ORDER BY sort_order",
            (tables["id"],),
        ).fetchall()
        rows = [json_loads(r["cells"]) for r in existing]
        new_rows = [
            {
                "name": "IT STEP Plovdiv — Software development",
                "url": "https://plovdiv.itstep.org/razrabotka-na-softuer",
                "notes": "Plovdiv campus; 2-year diploma incl. Python AI; offline/online.",
                "priority": "high",
            },
            {
                "name": "Plovdiv University — AI (bachelor)",
                "url": "https://uni-plovdiv.bg/pages/index/2987/",
                "notes": "Degree program; academic AI/ML — adjacent, long cycle.",
                "priority": "medium",
            },
            {
                "name": "GIKN Plovdiv — Programming for AI (high school)",
                "url": "https://gikn.eu/priem/",
                "notes": "Teen pipeline in Plovdiv; not pro developer upskill.",
                "priority": "low",
            },
        ]
        names = {r.get("name") for r in rows}
        for row in new_rows:
            if row["name"] not in names:
                rows.append(row)
        replace_table(conn, parent["id"], "watchlist", cols, rows)


def main() -> None:
    init_db()
    with connect() as conn:
        update_messaging(conn)
        update_blockers(conn)
        update_denis_tasks(conn)
        add_plovdiv_research(conn)
        conn.commit()
    print("Applied Denis inbox batch to hq.db")


if __name__ == "__main__":
    main()
