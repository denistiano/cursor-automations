#!/usr/bin/env python3
"""One-time / idempotent import of legacy markdown into data/hq.db."""

from __future__ import annotations

import re
from pathlib import Path

from hq_db import (
    DB_PATH,
    ROOT,
    connect,
    init_db,
    json_dumps,
    replace_list_items,
    replace_table,
    set_meta,
    upsert_collection,
    upsert_entry,
)


def read_maybe(relative: str) -> str:
    path = ROOT / relative
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def clean_inline(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    value = re.sub(r"_([^_]+)_", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip()


def slugify(value: str) -> str:
    value = clean_inline(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def parse_sections(markdown: str, depth: int = 2) -> list[dict]:
    pattern = re.compile(rf"^{'#' * depth}\s+(.+)$")
    sections: list[dict] = []
    current: dict | None = None
    for line in markdown.split("\n"):
        match = pattern.match(line)
        if match:
            if current:
                current["content"] = "\n".join(current.pop("lines", [])).strip()
            current = {"title": clean_inline(match.group(1)), "slug": slugify(match.group(1)), "lines": []}
            sections.append(current)
            continue
        if current is not None:
            current.setdefault("lines", []).append(line)
    if current:
        current["content"] = "\n".join(current.pop("lines", [])).strip()
    return sections


def parse_list_items(content: str) -> list[str]:
    items = []
    for line in content.split("\n"):
        match = re.match(r"^\s*(?:[-*]|\d+\.)\s+(.*)$", line)
        if match:
            text = clean_inline(re.sub(r"^\[[ xX]\]\s+", "", match.group(1)))
            if text:
                items.append(text)
    return items


def parse_checklist(content: str) -> list[dict]:
    items = []
    for line in content.split("\n"):
        match = re.match(r"^\s*-\s+\[([ xX])\]\s+(.*)$", line)
        if match:
            items.append({"text": clean_inline(match.group(2)), "done": match.group(1).lower() == "x"})
    return items


def split_table_row(line: str) -> list[str]:
    trimmed = line.strip().strip("|")
    cells: list[str] = []
    current = ""
    in_code = False
    for char in trimmed:
        if char == "`":
            in_code = not in_code
        if char == "|" and not in_code:
            cells.append(current.strip())
            current = ""
        else:
            current += char
    cells.append(current.strip())
    return cells


def parse_markdown_table(lines: list[str], start: int = 0) -> tuple[list[dict], list[str]]:
    index = start
    while index < len(lines) and not lines[index].strip().startswith("|"):
        index += 1
    if index + 1 >= len(lines):
        return [], []

    headers = [slugify(clean_inline(h)) or f"col_{i}" for i, h in enumerate(split_table_row(lines[index]))]
    sep = split_table_row(lines[index + 1])
    if not headers or not all(re.match(r"^:?-{2,}:?$", cell.strip()) for cell in sep):
        return [], headers

    rows: list[dict] = []
    index += 2
    while index < len(lines) and lines[index].strip().startswith("|"):
        cells = split_table_row(lines[index])
        row = {headers[i]: clean_inline(cells[i] if i < len(cells) else "") for i in range(len(headers))}
        if any(row.values()):
            rows.append(row)
        index += 1
    return rows, headers


def extract_tables(markdown: str) -> list[tuple[list[str], list[dict]]]:
    lines = markdown.split("\n")
    tables = []
    index = 0
    while index < len(lines):
        if not lines[index].strip().startswith("|"):
            index += 1
            continue
        rows, headers = parse_markdown_table(lines, index)
        if rows:
            tables.append((headers, rows))
        index += 1
    return tables


def extract_code_fence(markdown: str) -> str:
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", markdown)
    return match.group(1).strip() if match else ""


def seed_collections(conn) -> None:
    specs = [
        ("tasks", "Tasks", "Priorities, blockers, and checklists", "check-square", 10),
        ("roadmap", "Roadmap", "Launch tracks and phases", "map", 20),
        ("standups", "Standups", "Daily PM records", "calendar", 30),
        ("business", "Business", "Plan and approved messaging", "briefcase", 40),
        ("office", "Office", "Location search and shortlists", "building", 50),
        ("research", "Research", "Competitors and reports", "search", 60),
        ("jobs", "Jobs", "Role descriptions and publish log", "users", 70),
        ("names", "Course names", "Naming options and decision", "tag", 80),
        ("automations", "Automations", "Cursor automation prompts", "zap", 90),
        ("social", "Social", "Draft posts and approval queue", "share", 100),
    ]
    for slug, label, desc, icon, order in specs:
        upsert_collection(conn, slug, label, desc, icon, order)


def seed_meta_and_readme(conn) -> None:
    readme = read_maybe("README.md")
    lines = readme.split("\n")
    title = clean_inline(next((line[2:] for line in lines if line.startswith("# ")), "Course Business HQ"))
    description = clean_inline(next((line for line in lines if line.strip() and not line.startswith("#")), ""))
    set_meta(conn, "project.title", title)
    set_meta(conn, "project.description", description)

    status_items = parse_checklist(readme)
    status_id = upsert_entry(conn, "tasks", "project-status", "Project status", sort_order=999)
    replace_list_items(conn, status_id, "items", status_items)


def seed_tasks(conn) -> None:
    markdown = read_maybe("planning/TODO.md")
    sections = parse_sections(markdown)
    group_order = 0
    for section in sections:
        slug = section["slug"]
        if slug == "blockers":
            continue
        owner = "denis" if "denis" in slug else "pm" if "pm" in slug or "agent" in slug else None
        group_id = upsert_entry(
            conn,
            "tasks",
            slug,
            section["title"],
            owner=owner,
            sort_order=group_order,
            props={"kind": "group"},
        )
        replace_list_items(conn, group_id, "items", parse_checklist(section.get("content", "")))
        group_order += 1

    blockers_lines = read_maybe("planning/TODO.md").split("\n")
    blockers_start = next((i for i, line in enumerate(blockers_lines) if line.startswith("## Blockers")), None)
    blockers: list[dict] = []
    if blockers_start is not None:
        rows, _ = parse_markdown_table(blockers_lines, blockers_start + 1)
        for row in rows:
            blocker = row.get("blocker") or row.get("col_1") or ""
            owner = row.get("owner") or row.get("col_2") or ""
            if blocker:
                blockers.append({"text": blocker, "meta": {"owner": owner}})
    blockers_id = upsert_entry(conn, "tasks", "blockers", "Blockers", sort_order=900, props={"kind": "blockers"})
    replace_list_items(conn, blockers_id, "items", blockers)


def seed_roadmap(conn) -> None:
    markdown = read_maybe("planning/roadmap.md")
    lines = markdown.split("\n")
    upsert_entry(
        conn,
        "roadmap",
        "overview",
        "Roadmap overview",
        body=markdown.split("## How we work")[0].strip(),
        props={"horizon": "Multi-week path", "updated": "2026-05-26"},
    )

    tracks_start = next((i for i, line in enumerate(lines) if "Tracks" in line), 0)
    track_rows, track_cols = parse_markdown_table(lines, tracks_start)
    tracks_id = upsert_entry(conn, "roadmap", "tracks", "Launch tracks", sort_order=1)
    mapped = []
    for row in track_rows:
        num = row.get("") or row.get("col_1") or row.get("1")
        topic = row.get("topic") or row.get("col_2") or ""
        if not topic or topic.startswith("---"):
            continue
        mapped.append(
            {
                "track_num": num,
                "topic": topic,
                "denis": row.get("denis") or row.get("col_3") or "",
                "pm": row.get("pm-agent") or row.get("pm-agent-") or row.get("col_4") or "",
            }
        )
    replace_table(conn, tracks_id, "tracks", ["track_num", "topic", "denis", "pm"], mapped)

    phases_start = next((i for i, line in enumerate(lines) if "Suggested phase order" in line), 0)
    phase_rows, _ = parse_markdown_table(lines, phases_start + 5)
    phases_id = upsert_entry(conn, "roadmap", "phases", "Phases", sort_order=2)
    replace_table(
        conn,
        phases_id,
        "phases",
        ["phase", "focus", "unlocks"],
        [
            {
                "phase": r.get("phase") or r.get("col_1") or "",
                "focus": r.get("focus") or r.get("col_2") or "",
                "unlocks": r.get("unlocks") or r.get("col_3") or "",
            }
            for r in phase_rows
            if any(r.values())
        ],
    )

    near_start = next((i for i, line in enumerate(lines) if "Near-term queue" in line), 0)
    near_items = parse_list_items("\n".join(lines[near_start:]))
    near_id = upsert_entry(conn, "roadmap", "near-term", "Near-term queue", sort_order=3)
    replace_list_items(conn, near_id, "items", [{"text": t} for t in near_items])


def seed_standups(conn) -> None:
    standup_dir = ROOT / "planning" / "standups"
    if not standup_dir.exists():
        return
    for path in sorted(standup_dir.glob("????-??-??.md"), reverse=True):
        markdown = path.read_text(encoding="utf-8")
        date = path.stem
        sections = {s["slug"]: s for s in parse_sections(markdown)}
        entry_id = upsert_entry(
            conn,
            "standups",
            date,
            f"Standup — {date}",
            props={"date": date},
        )
        mapping = {
            "done": "done",
            "ongoing-denis-agents": "ongoing",
            "ongoing": "ongoing",
            "today-max-3": "today",
            "blockers-decisions-for-denis": "blockers",
            "agent-next-actions": "agent_next",
        }
        for src, dest in mapping.items():
            content = sections.get(src, {}).get("content", "")
            items = parse_list_items(content) if dest != "today" else []
            if dest == "today":
                for line in content.split("\n"):
                    match = re.match(r"^\d+\.\s+(.*)$", line.strip())
                    if match:
                        items.append(clean_inline(match.group(1)))
            replace_list_items(conn, entry_id, dest, [{"text": t} for t in items])


def seed_business(conn) -> None:
    plan_md = read_maybe("business/plan-v1.md")
    status = re.search(r"\*\*Status:\*\*\s*(.+)", plan_md)
    updated = re.search(r"\*\*Last updated:\*\*\s*(.+)", plan_md)
    plan_id = upsert_entry(
        conn,
        "business",
        "plan",
        "Business plan v1",
        status=status.group(1).strip() if status else None,
        body=plan_md,
        props={"last_updated": updated.group(1).strip() if updated else None},
    )
    for index, section in enumerate(parse_sections(plan_md)):
        child_id = upsert_entry(
            conn,
            "business",
            f"plan-{section['slug']}",
            section["title"],
            parent_id=plan_id,
            body=section.get("content", ""),
            sort_order=index,
        )
        tables = extract_tables(section.get("content", ""))
        for t_index, (headers, rows) in enumerate(tables):
            replace_table(conn, child_id, f"table-{t_index}", headers, rows, t_index)

    msg_md = read_maybe("business/approved-messaging.md")
    msg_sections = {s["slug"]: s for s in parse_sections(msg_md)}
    msg_id = upsert_entry(conn, "business", "messaging", "Approved messaging", body=msg_md)
    course_props = {}
    for line in (msg_sections.get("course-fill-in-with-denis", {}).get("content") or "").split("\n"):
        match = re.match(r"^-\s+\*\*([^:]+):\*\*\s*(.*)$", line)
        if match:
            course_props[slugify(match.group(1))] = clean_inline(match.group(2))
    conn.execute("UPDATE entries SET props=? WHERE id=?", (json_dumps({"course": course_props}), msg_id))

    pricing_rows, pricing_cols = parse_markdown_table(
        (msg_sections.get("pricing-launch", {}).get("content") or "").split("\n")
    )
    replace_table(
        conn,
        msg_id,
        "pricing",
        ["item", "approved_text", "status"],
        [
            {
                "item": r.get("item") or "",
                "approved_text": r.get("approved-text") or r.get("approved_text") or "",
                "status": r.get("status") or "",
            }
            for r in pricing_rows
        ],
    )
    replace_list_items(
        conn,
        msg_id,
        "allowed_claims",
        [{"text": t} for t in parse_list_items(msg_sections.get("claims-we-allow", {}).get("content", ""))],
    )
    replace_list_items(
        conn,
        msg_id,
        "disallowed_claims",
        [{"text": t} for t in parse_list_items(msg_sections.get("claims-we-do-not-allow-until-approved", {}).get("content", ""))],
    )


def seed_office(conn) -> None:
    md = read_maybe("planning/office-plovdiv.md")
    status = re.search(r"\*\*Status:\*\*\s*(.+)", md)
    entry_id = upsert_entry(
        conn,
        "office",
        "plovdiv",
        "Office search — Plovdiv",
        status=status.group(1).strip() if status else None,
        body=md,
    )
    criteria_rows, criteria_cols = parse_markdown_table(md.split("\n"), md.split("\n").index("## Criteria (Denis to fill)") + 1 if "## Criteria" in md else 0)
    if criteria_rows:
        replace_table(
            conn,
            entry_id,
            "criteria",
            ["field", "value"],
            [{"field": r.get("field") or "", "value": r.get("value") or ""} for r in criteria_rows],
        )
    shortlist_rows, _ = parse_markdown_table(md.split("\n"), md.split("\n").index("## Shortlist") + 1 if "## Shortlist" in md else 0)
    replace_table(
        conn,
        entry_id,
        "shortlist",
        ["num", "address", "rent", "notes", "visit"],
        [
            {
                "num": r.get("") or r.get("col_1") or "",
                "address": r.get("address-listing") or r.get("address") or "",
                "rent": r.get("rent") or "",
                "notes": r.get("notes") or "",
                "visit": r.get("denis-visit") or r.get("visit") or "",
            }
            for r in shortlist_rows
        ],
    )


def seed_research(conn) -> None:
    md = read_maybe("research/competitors/COMPETITORS.md")
    entry_id = upsert_entry(conn, "research", "competitors", "Competitor watchlist", body=md)
    lines = md.split("\n")
    table_start = next((i for i, line in enumerate(lines) if "Name" in line and "URL" in line), 0)
    rows, cols = parse_markdown_table(lines, table_start)
    replace_table(
        conn,
        entry_id,
        "watchlist",
        ["name", "url", "notes", "priority"],
        [
            {
                "name": r.get("name") or "",
                "url": r.get("url") or "",
                "notes": r.get("notes") or "",
                "priority": r.get("priority") or "",
            }
            for r in rows
            if r.get("name") and not r.get("name").startswith("_")
        ],
    )
    triggers = parse_list_items(
        next((s["content"] for s in parse_sections(md) if s["slug"] == "how-to-trigger-research"), "")
    )
    replace_list_items(conn, entry_id, "triggers", [{"text": t} for t in triggers])

    comp_dir = ROOT / "research" / "competitors"
    if comp_dir.exists():
        for index, path in enumerate(sorted(comp_dir.glob("????-??-??-*.md"))):
            report_md = path.read_text(encoding="utf-8")
            title = clean_inline(next((line[2:] for line in report_md.split("\n") if line.startswith("# ")), path.stem))
            upsert_entry(
                conn,
                "research",
                slugify(path.stem),
                title,
                parent_id=entry_id,
                body=report_md,
                props={"report_date": path.stem[:10]},
                sort_order=index,
            )


def seed_jobs(conn) -> None:
    md = read_maybe("business/jobs/product-owner.md")
    status = re.search(r"\*\*Status:\*\*\s*(.+)", md)
    entry_id = upsert_entry(
        conn,
        "jobs",
        "product-owner",
        "Product Owner",
        status=status.group(1).strip() if status else None,
        body=md,
    )
    replace_list_items(conn, entry_id, "checklist", parse_checklist(md))
    pos = md.split("## Position text")
    position_text = pos[1].split("---")[0].strip() if len(pos) > 1 else ""
    conn.execute(
        "UPDATE entries SET props=? WHERE id=?",
        (json_dumps({"position_text": position_text}), entry_id),
    )
    pub_rows, _ = parse_markdown_table(md.split("\n"), md.split("\n").index("## Publish log") + 1 if "## Publish log" in md else 0)
    replace_table(
        conn,
        entry_id,
        "publish_log",
        ["channel", "date", "link"],
        [
            {
                "channel": r.get("channel") or "",
                "date": r.get("date") or "",
                "link": r.get("link") or "",
            }
            for r in pub_rows
        ],
    )


def seed_names(conn) -> None:
    md = read_maybe("business/course-name-options.md")
    entry_id = upsert_entry(conn, "names", "options", "Course name options", body=md, status="draft")
    sections = parse_sections(md, depth=2)
    shortlist_rows, _ = parse_markdown_table(md.split("\n"), md.find("## Shortlist"))
    more_rows, _ = parse_markdown_table(md.split("\n"), md.find("## More options"))
    names = []
    for row in shortlist_rows:
        name = row.get("name") or ""
        if name and not name.startswith("---"):
            names.append(
                {
                    "name": name,
                    "category": "shortlist",
                    "vibe": row.get("vibe") or "",
                    "notes": row.get("notes") or "",
                }
            )
    for row in more_rows:
        name = row.get("name") or ""
        if name and not name.startswith("---"):
            names.append(
                {
                    "name": name,
                    "category": "more",
                    "tagline": row.get("tagline-idea-draft") or row.get("tagline") or "",
                }
            )
    replace_table(conn, entry_id, "names", ["name", "category", "vibe", "notes", "tagline"], names)
    replace_list_items(conn, entry_id, "criteria", parse_checklist(md))
    decision = {"chosen": "", "rejected": ""}
    for line in md.split("\n"):
        if line.startswith("- **Chosen name:**"):
            decision["chosen"] = clean_inline(line.split(":", 1)[1])
        if line.startswith("- **Rejected:**"):
            decision["rejected"] = clean_inline(line.split(":", 1)[1])
    conn.execute("UPDATE entries SET props=? WHERE id=?", (json_dumps({"decision": decision}), entry_id))


def seed_automations(conn) -> None:
    auto_dir = ROOT / "docs" / "automations"
    if not auto_dir.exists():
        return
    for index, path in enumerate(sorted(auto_dir.glob("*.md"))):
        md = path.read_text(encoding="utf-8")
        title = clean_inline(next((line[2:] for line in md.split("\n") if line.startswith("# ")), path.stem))
        slug = slugify(title)
        settings_rows, _ = parse_markdown_table(
            md.split("\n"),
            next((i for i, line in enumerate(md.split("\n")) if line.strip() == "## Settings"), 0) + 1,
        )
        settings = {}
        for row in settings_rows:
            field = row.get("field") or row.get("col_1") or ""
            value = row.get("value") or row.get("col_2") or ""
            if field:
                settings[slugify(field)] = value
        checklist = parse_checklist(
            next((s["content"] for s in parse_sections(md) if s["slug"] == "denis-checklist"), "")
        )
        upsert_entry(
            conn,
            "automations",
            slug,
            settings.get("name") or title,
            body=extract_code_fence(md),
            props={"settings": settings, "source_file": str(path.relative_to(ROOT))},
            sort_order=index,
        )
        entry = conn.execute("SELECT id FROM entries WHERE collection='automations' AND slug=?", (slug,)).fetchone()
        replace_list_items(conn, int(entry["id"]), "checklist", checklist)


def seed_social(conn) -> None:
    social_dir = ROOT / "content" / "social"
    if not social_dir.exists():
        return
    for index, path in enumerate(sorted(social_dir.glob("**/*.md"))):
        if path.name.startswith("_"):
            continue
        md = path.read_text(encoding="utf-8")
        frontmatter = {}
        if md.startswith("---\n"):
            end = md.find("\n---", 4)
            if end != -1:
                for line in md[4:end].split("\n"):
                    match = re.match(r"^([^:]+):\s*(.*)$", line)
                    if match:
                        frontmatter[match.group(1).strip()] = match.group(2).strip()
        title = clean_inline(next((line[2:] for line in md.split("\n") if line.startswith("# ")), path.stem))
        upsert_entry(
            conn,
            "social",
            slugify(path.stem + "-" + str(index)),
            title,
            body=md,
            props={
                "platform": frontmatter.get("platform", "unknown"),
                "approved": frontmatter.get("approved", "false") == "true",
                "scheduled_at": frontmatter.get("scheduled_at"),
                "post_id": frontmatter.get("post_id"),
                "source_path": str(path.relative_to(ROOT)),
            },
            sort_order=index,
        )


def seed_all(force: bool = False) -> None:
    init_db(force=force)
    with connect() as conn:
        seed_collections(conn)
        seed_meta_and_readme(conn)
        seed_tasks(conn)
        seed_roadmap(conn)
        seed_standups(conn)
        seed_business(conn)
        seed_office(conn)
        seed_research(conn)
        seed_jobs(conn)
        seed_names(conn)
        seed_automations(conn)
        seed_social(conn)
        set_meta(conn, "schema_version", "1")
        set_meta(conn, "data_model", "generic-collections-v1")
        conn.commit()
    print(f"Seeded {DB_PATH}")


if __name__ == "__main__":
    import sys

    force = "--force" in sys.argv
    seed_all(force=force)
