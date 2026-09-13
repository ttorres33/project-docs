#!/usr/bin/env python3
"""Tidy a process-notes/ folder before a new entry is written.

Usage: tidy.py [--dry-run] [DIR]

Only the top level of DIR (default: process-notes) is examined. Every
`YYYY-MM-DDTHHMM-slug.md` entry dated before the current month moves into
`DIR/YYYY-MM/`. Every other `.md` file at the top level (for example the
`NNNN-slug.md` entries the converter writes for undated sections) moves into
`DIR/no-date/`. The current month's entries stay where they are.

Files are renamed, never rewritten or overwritten. If the destination already
exists, or an entry is dated after the current month, the file stays put and is
named in the output. The month comes from the filename, never from mtime.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
import re

DATED = re.compile(r"^(?P<year>\d{4})-(?P<month>\d{2})-\d{2}T\d{4}-.+\.md$")
NO_DATE = "no-date"


def classify(name: str, current: str):
    """Return (folder, reason) for a top-level .md file.

    folder is the subfolder the file belongs in, or None if it stays at the top
    level. reason is set only when the file is left in place for a reason worth
    reporting (a future date).
    """
    m = DATED.match(name)
    if m and 1 <= int(m.group("month")) <= 12:
        ym = f"{m.group('year')}-{m.group('month')}"
        if ym < current:
            return ym, None
        if ym == current:
            return None, None
        return None, "dated after the current month"
    return NO_DATE, None


def plural(n: int, singular: str, plural_form: str) -> str:
    return f"{n} {singular if n == 1 else plural_form}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="File older process-notes entries into YYYY-MM/ folders "
        "and undated entries into no-date/."
    )
    parser.add_argument("dir", nargs="?", default="process-notes",
                        help="the process-notes folder (default: process-notes)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print what would move without moving anything")
    args = parser.parse_args(argv)

    root = Path(args.dir)
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 1

    current = datetime.now().strftime("%Y-%m")
    moves: dict[str, list[Path]] = {}
    left: list[tuple[str, str]] = []

    for path in sorted(root.iterdir()):
        name = path.name
        if not path.is_file() or name.startswith(".") or not name.endswith(".md"):
            continue
        folder, reason = classify(name, current)
        if reason:
            left.append((name, reason))
            continue
        if folder is None:
            continue
        if (root / folder / name).exists():
            left.append((name, f"{folder}/{name} already exists"))
            continue
        moves.setdefault(folder, []).append(path)

    verb = "Would move" if args.dry_run else "Moved"
    for folder in sorted(moves):
        paths = moves[folder]
        if not args.dry_run:
            (root / folder).mkdir(exist_ok=True)
            for path in paths:
                path.rename(root / folder / path.name)
        what = (plural(len(paths), "undated file", "undated files")
                if folder == NO_DATE else plural(len(paths), "entry", "entries"))
        print(f"{verb} {what} into {folder}/")
    for name, reason in left:
        print(f"Left in place: {name} ({reason})")
    if not moves and not left:
        print("Nothing to move.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
