#!/usr/bin/env python3
"""Upsert a single standup markdown file into hq.db (used by PM cron)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hq_db import connect, init_db
from seed_from_md import seed_standups


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("date", help="Standup date YYYY-MM-DD (must exist in planning/standups/)")
    args = parser.parse_args()
    path = Path(__file__).resolve().parent.parent / "planning" / "standups" / f"{args.date}.md"
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    init_db()
    with connect() as conn:
        seed_standups(conn)
        conn.commit()
    print(f"Upserted standup {args.date} → hq.db")


if __name__ == "__main__":
    main()
