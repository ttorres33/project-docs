#!/usr/bin/env python3
"""Convert a flat process-notes.md file to the per-entry folder format.

Usage: python3 convert.py <path-to-process-notes.md>

Splits the file on every `## ` heading — each heading becomes one entry file
inside a new `process-notes/` directory next to the input. Tries to extract a
date from each heading and names files `YYYY-MM-DDTHHMM-slug.md`. Entries with
no recognizable date get an ordinal-prefixed filename `NNNN-slug.md` and sort
before dated entries alphabetically, preserving their original order in the
file.

The original file is renamed to `process-notes.md.archive`. Content before the
first `## ` heading (typically a `# Project Process Notes` title) is discarded.

Exits non-zero on any error so the calling skill can surface failures.
"""

import re
import sys
from pathlib import Path
from typing import Optional, Tuple

# Every line starting with `## ` is an entry boundary. No format assumptions.
ENTRY_HEADING = re.compile(r"^## (.+?)\s*$", re.MULTILINE)

# Heading parsers: each returns (date, time, title) or None. Tried in order;
# first match wins. Time can be None if the heading only carried a date.
#
# Bracket prefix: captures everything inside `[...]` as bracket_content so we
# can pull the date out separately — this tolerates weird contents like
# `[2026-02-25 ~afternoon]` or `[2026-02-24 afternoon]`. The `Entry N:` marker
# is optional and consumed if present.
_BRACKET_PREFIX = re.compile(
    r"^\[([^\]]*)\]\s*(?:Entry\s*\d*\s*:)?\s*(.*)$"
)
_RAW_DATE = re.compile(
    r"^(\d{4}-\d{2}-\d{2})(?: (\d{2}):(\d{2}))?\s*[:\-]\s*(.*)$"
)
_SESSION_DATE = re.compile(
    r"^Session:\s*(\d{4}-\d{2}-\d{2})"
    r"(?:\s+\(([^)]*)\))?"
    r"(?:\s*-\s*(.*))?\s*$"
)

# Fuzzy fallback: any YYYY-MM-DD anywhere in the heading. Used when none of
# the structured patterns match — e.g., `Session 25 - 2025-01-07 (Title)` or
# `Session: Reset Canvas Submission Script (2026-03-08)`.
_FUZZY_DATE = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")

# Matches a HH:MM time. Used inside bracket contents to find a time next to
# a date when present.
_TIME = re.compile(r"\b(\d{1,2}):(\d{2})\b")


def _clean_title(title: str) -> str:
    """Tidy up a title after date extraction.

    Removes empty `()` and `[]` left behind when the matched date was wrapped
    in them, collapses whitespace, and strips dangling connective punctuation
    (`-`, `:`, `,`, `~`) from either end. Balanced parens/brackets with content
    inside are preserved — they may be legitimate parts of the title.
    """
    title = re.sub(r"\s+", " ", title).strip()
    # Remove empty parens/brackets left behind by date removal
    title = re.sub(r"\s*\(\s*\)\s*", " ", title)
    title = re.sub(r"\s*\[\s*\]\s*", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    # Strip dangling connective punctuation from ends — NOT parens/brackets.
    title = title.strip(" -:,~")
    return title.strip()


def parse_heading(heading: str) -> Tuple[Optional[str], Optional[str], str]:
    """Extract (date, time, title) from the text after `## `.

    Date is `YYYY-MM-DD` or None. Time is `HH:MM` or None. Title is always a
    non-empty string — falls back to the original heading text if no other
    title component can be found.
    """
    # Bracket prefix like `[2026-02-25 ~afternoon] Entry 12: Title`
    m = _BRACKET_PREFIX.match(heading)
    if m:
        bracket_content = m.group(1)
        title = m.group(2).strip()
        dm = _FUZZY_DATE.search(bracket_content)
        if dm:
            date = dm.group(1)
            # Look for HH:MM after the date inside the brackets
            tm = _TIME.search(bracket_content[dm.end():])
            time = f"{int(tm.group(1)):02d}:{tm.group(2)}" if tm else None
            return date, time, _clean_title(title) or heading.strip()

    m = _RAW_DATE.match(heading)
    if m:
        date = m.group(1)
        time = f"{m.group(2)}:{m.group(3)}" if m.group(2) else None
        title = _clean_title(m.group(4)) or heading.strip()
        return date, time, title

    m = _SESSION_DATE.match(heading)
    if m:
        date = m.group(1)
        # Title priority: explicit trailing title > parenthetical note > "Session"
        title = _clean_title(m.group(3) or m.group(2) or "Session")
        return date, None, title or "Session"

    # Fuzzy fallback: find any date in the heading and strip it from the title.
    m = _FUZZY_DATE.search(heading)
    if m:
        date = m.group(1)
        stripped = heading[: m.start()] + heading[m.end() :]
        title = _clean_title(stripped) or heading.strip()
        return date, None, title

    # No date found — preserve the full heading as the title.
    return None, None, heading.strip()


def slugify(title: str, max_len: int = 60) -> str:
    """Generate a filesystem-safe slug from an entry title."""
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("-")
    return slug or "untitled"


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python3 convert.py <path-to-process-notes.md>", file=sys.stderr)
        return 2

    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        print(f"ERROR: {src} does not exist", file=sys.stderr)
        return 1
    if not src.is_file():
        print(f"ERROR: {src} is not a file", file=sys.stderr)
        return 1

    out_dir = src.parent / "process-notes"
    if out_dir.exists():
        print(
            f"ERROR: {out_dir} already exists - refusing to overwrite",
            file=sys.stderr,
        )
        return 1

    archive_path = src.with_suffix(src.suffix + ".archive")
    if archive_path.exists():
        print(
            f"ERROR: {archive_path} already exists - refusing to overwrite",
            file=sys.stderr,
        )
        return 1

    content = src.read_text(encoding="utf-8")
    matches = list(ENTRY_HEADING.finditer(content))

    if not matches:
        print(
            "ERROR: no `## ` entry headings found in file. Nothing to convert.",
            file=sys.stderr,
        )
        return 1

    # Extract each entry: heading parse + body (everything until the next heading)
    entries = []
    for i, match in enumerate(matches):
        heading_text = match.group(1).strip()
        body_start = match.end()
        body_end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[body_start:body_end].strip()
        # Strip trailing `---` separator if present
        body = re.sub(r"\n*---\s*$", "", body).rstrip()

        date, time, title = parse_heading(heading_text)
        entries.append(
            {
                "date": date,
                "time": time,
                "title": title,
                "body": body,
            }
        )

    # Write files. Dated entries use YYYY-MM-DDTHHMM-slug.md. Undated entries
    # use NNNN-slug.md with a per-file sequential counter — they sort before
    # dated entries alphabetically, preserving their relative order.
    out_dir.mkdir()
    used_filenames: set = set()
    written_files = []
    undated_counter = 0

    for entry in entries:
        if entry["date"]:
            if entry["time"]:
                hh, mm = entry["time"].split(":")
            else:
                hh, mm = "00", "00"
            base_name = f"{entry['date']}T{hh}{mm}-{slugify(entry['title'])}"
        else:
            undated_counter += 1
            base_name = f"{undated_counter:04d}-{slugify(entry['title'])}"

        filename = f"{base_name}.md"
        suffix = 2
        while filename in used_filenames:
            filename = f"{base_name}-{suffix}.md"
            suffix += 1
        used_filenames.add(filename)

        file_content = f"# {entry['title']}\n\n{entry['body']}\n"
        (out_dir / filename).write_text(file_content, encoding="utf-8")
        written_files.append(filename)

    # Rename original to archive
    src.rename(archive_path)

    # Summary
    dated = sum(1 for e in entries if e["date"])
    undated = len(entries) - dated
    print(f"Converted {len(entries)} entries to {out_dir}/")
    print(f"  {dated} dated, {undated} undated")
    print(f"Archived original as {archive_path.name}")
    for f in written_files:
        print(f"  - {f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
