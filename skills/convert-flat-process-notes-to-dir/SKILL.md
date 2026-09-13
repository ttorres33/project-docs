---
name: convert-flat-process-notes-to-dir
description: Converts a legacy flat process-notes.md file into the per-entry process-notes/ folder format. Use when the process-notes skill refuses to write because it detects the old format, or when the user explicitly requests /project-docs:convert-flat-process-notes-to-dir.
allowed-tools: Read, Glob, Grep, Bash
user-invocable: true
---

# Convert Flat Process Notes to Folder

## Purpose

Migrate a project from the legacy single-file `process-notes.md` format to the new per-entry `process-notes/` folder format used by the `process-notes` skill. The heavy lifting is done by a Python script — Claude's job is to validate the input, review the dry run, run the script, and verify the output.

## When to Run

- The `process-notes` skill refused to write because it detected a flat `process-notes.md` file
- The user explicitly invoked `/project-docs:convert-flat-process-notes-to-dir`
- A project still has `process-notes.md` at its root and needs to adopt the folder format
- A previous conversion produced bad output and needs to be redone (see "Re-converting after a bad conversion" below)

## Steps

Run these steps in order. Abort and report to the user if any step fails.

### 1. Verify preconditions

- Confirm `process-notes.md` exists in the current working directory
- Confirm `process-notes/` does NOT already exist. If it does, stop and tell the user the project appears to already be partially converted — they need to decide whether to keep the existing folder or remove it before re-running.
- Confirm `process-notes.md.archive` does NOT already exist. If it does, stop and tell the user a previous conversion is in the way.

### 2. Record the baseline byte count

```bash
wc -c < process-notes.md
```

Remember this value for step 5. (Do not use a `grep -c "^## "` heading count as the baseline — headings inside code fences are skipped and misplaced `### ` headings may be promoted, so the raw count is not what the script splits on. The script reports its own entry count instead.)

### 3. Dry run and review

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/convert-flat-process-notes-to-dir/scripts/convert.py --dry-run process-notes.md
```

The dry run writes nothing. It prints a summary and the planned file list with byte sizes. Read the whole list and check for:

- **Entries marked `SMALL`** (under 200 bytes). A short entry can be legitimate (a "(Planned)" stub), but a cluster of them usually means a template or sample file was split by mistake.
- **Titles that read like a template, not a session** — "Definition 1", "Section Headers", "Term Title", a bare "Glossary". These are almost always quoted markdown that should have stayed inside an entry.
- **One file far larger than the rest.** A section that swallowed later entries appended as `### ` sub-headings. Check whether the script promoted them (the summary says how many `### ` headings were promoted and under which convention); if it did not, the file may need a manual fix in the source before converting.
- **Promoted `### ` headings that are actually sub-sections.** Promotion only fires when at least half of the `## ` headings share a naming convention (`Phase N`, `Session N`, `Entry N`, or `[YYYY-MM-DD]`) and the `### ` heading starts the same way. Confirm each promoted title is a real entry, not a sub-section such as a plan's own "Phase 2a".
- **Dropped container headings.** A `## ` heading with no content of its own (usually because all of its `### ` children were promoted) is dropped and named in the summary. Confirm nothing meaningful lived under it.

If the script exits non-zero, show the user the error output and stop. If anything in the list looks wrong, show the user the relevant lines and stop — do not convert until they have decided how to handle it. A bad conversion that gets committed is much more work to undo than a paused one.

### 4. Run the conversion

Once the dry run looks right:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/convert-flat-process-notes-to-dir/scripts/convert.py process-notes.md
```

The script:
- Splits the file on every `## ` heading that sits outside a fenced code block (```` ``` ```` or `~~~`). A `## ` line inside a fence is content and never splits.
- Promotes `### ` headings to entries when they match the file's own `## ` naming convention (see step 3). This rescues entries that were appended as sub-headings under whatever section came last.
- Drops any heading left with an empty body.
- Tries to extract a date from each heading. Recognized patterns:
  - `[YYYY-MM-DD HH:MM]` or `[YYYY-MM-DD]` bracket prefixes (tolerates extra content inside the brackets like `[2026-02-25 ~afternoon]`)
  - `YYYY-MM-DD:` or `YYYY-MM-DD -` raw date prefixes
  - `Session: YYYY-MM-DD ...` prefixes
  - Fuzzy fallback: any `YYYY-MM-DD` anywhere in the heading
  - Month-name fallback: `October 26, 2025`, `Nov 17, 2025`, usually in trailing parentheses
- Writes dated entries as `process-notes/YYYY-MM-DDTHHMM-slug.md` (defaulting time to `0000` if not specified)
- Writes undated entries (phase-based, topic-based, or otherwise date-free) as `process-notes/NNNN-slug.md` with a per-file sequential counter — these sort before dated entries alphabetically, preserving their relative order in the source file
- Renames the original file to `process-notes.md.archive`
- Prints the same summary and file list as the dry run

If the script exits non-zero, show the user the error output and stop. Do not attempt to retry or work around the error — surface it so the user can fix the source file.

### 5. Verify the output

Run two checks:

**a. File count matches the script's count.** Compare the number of files in the folder to the `Converted: N entries` line the script printed:

```bash
ls process-notes/*.md | wc -l
```

If they differ, report the discrepancy.

**b. Byte count is reasonable.** Sum the bytes across all new files:

```bash
wc -c process-notes/*.md | tail -1
```

The total should be *close to* the baseline byte count from step 2, but slightly smaller — expect roughly 10-40 bytes lost per entry. The script replaces the longer `## [YYYY-MM-DD ...] Entry N: Title` headers with shorter `# Title` headers, drops the `---` separators between entries, and discards any preamble like `# Project Process Notes` that lived before the first entry.

Flag as a concern if the new total is *more than* the original, or if the loss is more than ~100 bytes per entry on average — either signals something went wrong.

### 6. Report to the user

Provide a concise summary:
- Number of entries converted (dated vs undated, and how many were promoted from `### `)
- Number of `## ` lines skipped inside code fences, if any
- Location of the new `process-notes/` folder
- Location of the archived original (`process-notes.md.archive`)
- Confirmation that both verification checks passed
- Note that the archive file can be deleted once the user has confirmed the conversion looks right

## Re-converting after a bad conversion

Use this when an earlier conversion produced fragments, buried entries, or other bad output, and the archive is still present.

**Preconditions — check all three before touching anything:**

1. `process-notes.md.archive` exists and is intact (its byte count should be roughly the sum of the current folder plus the per-entry header loss).
2. No new entries have been written to `process-notes/` since the conversion. Every file should carry the conversion's timestamp, and `git log -- process-notes/` should show no commits after the conversion commit. If new entries exist, set them aside first (copy them out of the folder) and put them back after re-converting.
3. The user has agreed to regenerate the folder. The old files stay in git history, but this is still a delete.

**Reset sequence:**

```bash
git rm -r -q process-notes/          # or rm -rf process-notes/ if the folder is untracked
mv process-notes.md.archive process-notes.md
```

Then run steps 2 through 6 above from the top, including the dry run. Restore any set-aside entries afterward.

## Notes

- The script is deliberately permissive about heading formats — it never refuses to convert based on how an entry is titled. Its two structural rules (skip fenced `## ` lines, promote convention-matching `### ` lines) exist because real files quote markdown inside code blocks and append late entries under the wrong heading level. The guiding principle is still "never lose content": nothing is dropped except headings with no body.
- Undated entries get ordinal filenames (`0001-slug.md`, `0002-slug.md`, ...) and sort before dated entries. This is intentional for files that mix static topic sections with dated entries — the topic sections end up at the top of the folder listing.
- The converted folder is flat. The next `/project-docs:process-notes` run files the dated entries into `YYYY-MM/` folders and the ordinal ones into `no-date/`.
- The script reads the whole file into memory. That is fine for any realistic process-notes file.
- Do NOT modify `process-notes.md.archive` after conversion. It is the user's safety net until they are confident the conversion worked.
