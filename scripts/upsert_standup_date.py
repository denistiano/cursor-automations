#!/usr/bin/env python3
"""Seed a single standup markdown file into data/hq.db (standups collection)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db
from seed_from_md import seed_standups


def main() -> None:
    date = sys.argv[1] if len(sys.argv) > 1 else None
    init_db()
    with connect() as conn:
        if date:
            path = Path(__file__).resolve().parent.parent / "planning" / "standups" / f"{date}.md"
            if not path.exists():
                raise SystemExit(f"Missing {path}")
        seed_standups(conn)
        conn.commit()
    print("Seeded standups → hq.db")


if __name__ == "__main__":
    main()
