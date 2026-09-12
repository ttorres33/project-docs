#!/usr/bin/env python3
"""Convert a flat process-notes.md file to the per-entry folder format.

Usage: python3 convert.py [--dry-run] <path-to-process-notes.md>

Splits the file on `## ` headings that sit outside fenced code blocks — each
heading becomes one entry file inside a new `process-notes/` directory next to
the input. Two refinements over a naive split:

- A line starting with `## ` inside a ``` or ~~~ fence is content (a quoted
  markdown template, a sample file) and never splits.
- If at least half of the `## ` headings follow an entry-naming convention
  (`Phase N`, `Session N` / `Session:`, `Entry N`, or a leading `[YYYY-MM-DD]`),
  then `### ` headings that start the same way are misplaced entries and get
  their own files. This rescues entries that were appended as sub-headings
  under whatever section happened to come last.

Tries to extract a date from each heading — `YYYY-MM-DD` forms, or month-name
forms like `Nov 17, 2025` — and names files `YYYY-MM-DDTHHMM-slug.md`. Entries
with no recognizable date get an ordinal-prefixed filename `NNNN-slug.md` and
sort before dated entries alphabetically, preserving their original order.

`--dry-run` prints the planned files with byte sizes and writes nothing. Run it
first and look for tiny entries, template-looking titles, or one file far
larger than the rest before converting for real.

The original file is renamed to `process-notes.md.archive`. Content before the
first entry heading (typically a `# Project Process Notes` title) is discarded.

Exits non-zero on any error so the calling skill can surface failures.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

HEADING = re.compile(r"^(##|###) (.+?)\s*$")
# Markdown allows up to three spaces of indentation before a fence.
FENCE = re.compile(r"^\s{0,3}(```|~~~)")

# Entries smaller than this are flagged in the listing — usually a sign that a
# template or sample was split by mistake.
SMALL_ENTRY_BYTES = 200

# Entry-naming conventions. If at least half of the `## ` headings match one
# class, `### ` headings matching that same class are promoted to entries.
CONVENTIONS: Dict[str, "re.Pattern[str]"] = {
    "Phase N": re.compile(r"^Phase\s*\d+", re.I),
    "Session N / Session:": re.compile(r"^Session\s*(\d+\b|:)", re.I),
    "Entry N": re.compile(r"^Entry\s*\d+", re.I),
    "[YYYY-MM-DD]": re.compile(r"^\[\d{4}-\d{2}-\d{2}"),
}

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

# Month-name fallback: `October 26, 2025`, `Oct 27, 2025`, `Nov 17 2025`.
_MONTH_DATE = re.compile(
    r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?"
    r"\s+(\d{1,2}),?\s+(\d{4})\b",
    re.I,
)
_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

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
    """Extract (date, time, title) from the text after `## ` or `### `.

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

    # Month-name fallback: `Phase 24: ... (Nov 17, 2025)`
    m = _MONTH_DATE.search(heading)
    if m and 1 <= int(m.group(2)) <= 31:
        month = _MONTHS[m.group(1)[:3].lower()]
        date = f"{m.group(3)}-{month:02d}-{int(m.group(2)):02d}"
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


def find_headings(lines: List[str]) -> Tuple[List[Tuple[int, int, str]], int]:
    """Return ([(line_index, level, text)], fenced_h2_skipped).

    Only headings outside fenced code blocks are returned. A fence opened with
    ``` closes only with ```, and one opened with ~~~ only with ~~~.
    """
    headings: List[Tuple[int, int, str]] = []
    fenced_h2_skipped = 0
    open_fence: Optional[str] = None
    for i, line in enumerate(lines):
        fm = FENCE.match(line)
        if fm:
            marker = fm.group(1)
            if open_fence is None:
                open_fence = marker
            elif marker == open_fence:
                open_fence = None
            continue
        hm = HEADING.match(line)
        if not hm:
            continue
        if open_fence is not None:
            if hm.group(1) == "##":
                fenced_h2_skipped += 1
            continue
        headings.append((i, len(hm.group(1)), hm.group(2).strip()))
    return headings, fenced_h2_skipped


def detect_convention(headings: List[Tuple[int, int, str]]) -> Optional[str]:
    """Return the convention name that at least half the `## ` headings follow, else None."""
    top = [text for _, level, text in headings if level == 2]
    if not top:
        return None
    counts: Dict[str, int] = {}
    for text in top:
        for name, pattern in CONVENTIONS.items():
            if pattern.match(text):
                counts[name] = counts.get(name, 0) + 1
                break
    if not counts:
        return None
    best = max(counts, key=lambda k: counts[k])
    return best if counts[best] * 2 >= len(top) else None


def select_entries(
    headings: List[Tuple[int, int, str]], convention: Optional[str]
) -> List[Tuple[int, str, bool]]:
    """Return [(line_index, heading_text, promoted)] — every `## ` plus promoted `### `."""
    entries: List[Tuple[int, str, bool]] = []
    pattern = CONVENTIONS[convention] if convention else None
    for line_index, level, text in headings:
        if level == 2:
            entries.append((line_index, text, False))
        elif pattern is not None and pattern.match(text):
            entries.append((line_index, text, True))
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a flat process-notes.md into a process-notes/ folder."
    )
    parser.add_argument("path", help="path to process-notes.md")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the planned files and write nothing",
    )
    args = parser.parse_args()

    src = Path(args.path).resolve()
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
    lines = content.split("\n")
    headings, fenced_h2_skipped = find_headings(lines)
    convention = detect_convention(headings)
    boundaries = select_entries(headings, convention)

    if not boundaries:
        print(
            "ERROR: no `## ` entry headings found outside code fences. Nothing to convert.",
            file=sys.stderr,
        )
        return 1

    # Extract each entry: heading parse + body (everything until the next boundary)
    entries = []
    for i, (line_index, heading_text, promoted) in enumerate(boundaries):
        body_start = line_index + 1
        body_end = boundaries[i + 1][0] if i + 1 < len(boundaries) else len(lines)
        body = "\n".join(lines[body_start:body_end]).strip()
        # Strip trailing `---` separator if present
        body = re.sub(r"\n*---\s*$", "", body).rstrip()

        date, time, title = parse_heading(heading_text)
        entries.append(
            {
                "date": date,
                "time": time,
                "title": title,
                "body": body,
                "promoted": promoted,
            }
        )

    # A heading with no content of its own is a container, not an entry —
    # typically a `## ` section whose `### ` children were all promoted.
    dropped_empty = [e for e in entries if not e["body"]]
    entries = [e for e in entries if e["body"]]
    if not entries:
        print("ERROR: every entry heading has an empty body. Nothing to convert.", file=sys.stderr)
        return 1

    # Plan filenames. Dated entries use YYYY-MM-DDTHHMM-slug.md. Undated entries
    # use NNNN-slug.md with a per-file sequential counter — they sort before
    # dated entries alphabetically, preserving their relative order.
    used_filenames: set = set()
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
        entry["filename"] = filename
        entry["content"] = f"# {entry['title']}\n\n{entry['body']}\n"
        entry["bytes"] = len(entry["content"].encode("utf-8"))

    # Summary — printed for both dry runs and real runs so the calling skill
    # can verify against the script's own numbers.
    dated = sum(1 for e in entries if e["date"])
    promoted_count = sum(1 for e in entries if e["promoted"])
    small = [e for e in entries if e["bytes"] < SMALL_ENTRY_BYTES]
    print(f"{'Plan' if args.dry_run else 'Converted'}: {len(entries)} entries -> {out_dir}/")
    print(f"  {len(entries) - promoted_count} from `## ` headings")
    if convention:
        print(
            f"  {promoted_count} promoted from `### ` headings matching the file's "
            f"\"{convention}\" convention"
        )
    else:
        print("  0 promoted (no `## ` naming convention detected)")
    print(f"  {fenced_h2_skipped} `## ` lines skipped inside code fences")
    print(f"  {dated} dated, {len(entries) - dated} undated")
    print(f"  {len(small)} entries under {SMALL_ENTRY_BYTES} bytes (marked SMALL below)")
    if dropped_empty:
        titles = ", ".join(f'"{e["title"]}"' for e in dropped_empty)
        print(f"  {len(dropped_empty)} empty container heading(s) dropped: {titles}")
    print()
    for e in entries:
        flags = []
        if e["bytes"] < SMALL_ENTRY_BYTES:
            flags.append("SMALL")
        if e["promoted"]:
            flags.append("promoted from ###")
        flag_text = f"  <-- {', '.join(flags)}" if flags else ""
        print(f"  - {e['filename']}  ({e['bytes']:,} bytes){flag_text}")

    if args.dry_run:
        print()
        print("Dry run: nothing written.")
        return 0

    out_dir.mkdir()
    for e in entries:
        (out_dir / e["filename"]).write_text(e["content"], encoding="utf-8")

    # Rename original to archive
    src.rename(archive_path)
    print()
    print(f"Archived original as {archive_path.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
