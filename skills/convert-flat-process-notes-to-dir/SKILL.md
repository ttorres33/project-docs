---
name: convert-flat-process-notes-to-dir
description: Converts a legacy flat process-notes.md file into the per-entry process-notes/ folder format. Use when the process-notes skill refuses to write because it detects the old format, or when the user explicitly requests /project-docs:convert-flat-process-notes-to-dir.
allowed-tools: Read, Glob, Grep, Bash
user-invocable: true
---

# Convert Flat Process Notes to Folder

## Purpose

Migrate a project from the legacy single-file `process-notes.md` format to the new per-entry `process-notes/` folder format used by the `process-notes` skill. The heavy lifting is done by a Python script — Claude's job is to validate the input, run the script, and verify the output.

## When to Run

- The `process-notes` skill refused to write because it detected a flat `process-notes.md` file
- The user explicitly invoked `/project-docs:convert-flat-process-notes-to-dir`
- A project still has `process-notes.md` at its root and needs to adopt the folder format

## Steps

Run these steps in order. Abort and report to the user if any step fails.

### 1. Verify preconditions

- Confirm `process-notes.md` exists in the current working directory
- Confirm `process-notes/` does NOT already exist. If it does, stop and tell the user the project appears to already be partially converted — they need to decide whether to keep the existing folder or remove it before re-running.
- Confirm `process-notes.md.archive` does NOT already exist. If it does, stop and tell the user a previous conversion is in the way.

### 2. Record baseline measurements

Capture two numbers for later verification:

```bash
grep -c "^## " process-notes.md  # entry heading count
wc -c < process-notes.md          # byte count
```

Remember both values. If the heading count is `0`, stop and tell the user the file has no `## ` entry headings — it is not a recognizable process-notes file and there is nothing to convert.

### 3. Run the conversion script

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/convert-flat-process-notes-to-dir/scripts/convert.py process-notes.md
```

The script:
- Splits the file on every `## ` heading — each heading becomes exactly one entry file
- Tries to extract a date from each heading. Recognized patterns:
  - `[YYYY-MM-DD HH:MM]` or `[YYYY-MM-DD]` bracket prefixes (tolerates extra content inside the brackets like `[2026-02-25 ~afternoon]`)
  - `YYYY-MM-DD:` or `YYYY-MM-DD -` raw date prefixes
  - `Session: YYYY-MM-DD ...` prefixes
  - Fuzzy fallback: any `YYYY-MM-DD` anywhere in the heading
- Writes dated entries as `process-notes/YYYY-MM-DDTHHMM-slug.md` (defaulting time to `0000` if not specified)
- Writes undated entries (phase-based, topic-based, or otherwise date-free) as `process-notes/NNNN-slug.md` with a per-file sequential counter — these sort before dated entries alphabetically, preserving their relative order in the source file
- Renames the original file to `process-notes.md.archive`
- Prints a summary of converted files to stdout

If the script exits non-zero, show the user the error output and stop. Do not attempt to retry or work around the error — surface it so the user can fix the source file.

### 4. Verify the output

Run two checks:

**a. Entry count matches.** Count files in the new folder and compare to the baseline heading count:

```bash
ls process-notes/*.md | wc -l
```

This should equal the baseline `grep -c "^## "` count from step 2. If not, report the discrepancy.

**b. Byte count is reasonable.** Sum the bytes across all new files:

```bash
wc -c process-notes/*.md | tail -1
```

The total should be *close to* the baseline byte count from step 2, but slightly smaller — expect roughly 20-40 bytes lost per entry. The script replaces the longer `## [YYYY-MM-DD ...] Entry N: Title` headers with shorter `# Title` headers, drops the `---` separators between entries, and discards any preamble like `# Project Process Notes` that lived before the first entry.

Flag as a concern if the new total is *more than* the original, or if the loss is more than ~100 bytes per entry on average — either signals something went wrong.

### 5. Report to the user

Provide a concise summary:
- Number of entries converted (dated vs undated)
- Location of the new `process-notes/` folder
- Location of the archived original (`process-notes.md.archive`)
- Confirmation that both verification checks passed
- Note that the archive file can be deleted once the user has confirmed the conversion looks right

## Notes

- The script is deliberately permissive — it treats every `## ` line as an entry boundary and never refuses to convert based on heading format. This is a one-way migration tool, and the guiding principle is "never lose content."
- Undated entries get ordinal filenames (`0001-slug.md`, `0002-slug.md`, ...) and sort before dated entries. This is intentional for files that mix static topic sections with dated entries — the topic sections end up at the top of the folder listing.
- The script reads the whole file into memory. That is fine for any realistic process-notes file.
- Do NOT modify `process-notes.md.archive` after conversion. It is the user's safety net until they are confident the conversion worked.
