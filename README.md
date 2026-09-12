# project-docs

A Claude Code plugin for maintaining project documentation:

- **README.md** - What is this and how do I use it (setup, deploy, test)
- **ARCHITECTURE.md** - How is this designed and why (design, patterns, conventions)
- **process-notes/** - Work history documenting decisions, dead ends, and progress. Each entry is a separate file named `YYYY-MM-DDTHHMM-slug.md` so writes stay atomic, grep works naturally, and reading recent entries is `ls -t process-notes/ | head -3`.
- **A/B test docs** - Structured documentation for experiments and tests

## Installation

```bash
claude plugins add teresa-torres-plugins/project-docs
```

## Commands

### `/project-docs:about`

Show this README for help and usage information.

### `/project-docs:process-notes`

Document current session progress as a new file in `process-notes/`. Creates a comprehensive entry capturing:
- What was accomplished with file references
- Key decisions with rationale and alternatives considered
- Dead ends: what didn't work, why, and what was done instead
- Technical details: files created/modified, dependencies, configs
- Next steps with context for the next session

Entries do not record commit, push, or deploy status. A note is written before the commit and the deploy, so those lines go stale within minutes. The one exception is a deployment that is deliberately on hold, which goes under Questions/Blockers with the reason.

Each invocation writes a new file named `YYYY-MM-DDTHHMM-slug.md`. Existing entry files are never modified — every write is a new, self-contained entry. If the project still has a legacy flat `process-notes.md`, this command will refuse to run and tell you to convert first (see below).

### `/project-docs:convert-flat-process-notes-to-dir`

Migrate a project from the legacy single-file `process-notes.md` format to the per-entry `process-notes/` folder format. Run this once per project when you see the new skill refusing to write, or whenever you want to adopt the folder format.

The skill:
- Runs a dry run first and reviews the planned files with their byte sizes, looking for tiny fragments, template-looking titles, or one oversized file, before converting anything
- Splits the flat file on `## ` headings that sit outside fenced code blocks (a `## ` line inside a code block is content, not an entry boundary)
- Promotes `### ` headings to their own entries when they match the file's own `## ` naming convention (`Phase N`, `Session N`, `Entry N`, or `[YYYY-MM-DD]`), rescuing entries that were appended as sub-headings under whatever section came last
- Extracts a date from each heading when possible (handles `[YYYY-MM-DD HH:MM]`, `[YYYY-MM-DD]`, `YYYY-MM-DD:`, `Session: YYYY-MM-DD`, month-name forms like `Nov 17, 2025`, and a fuzzy fallback for unusual formats)
- Drops a heading left with no content of its own, and says so
- Writes each entry as a separate file in `process-notes/`
- Dated entries: `YYYY-MM-DDTHHMM-slug.md`
- Undated entries (phase-based or topic-based): `NNNN-slug.md`, ordinal-prefixed
- Renames the original to `process-notes.md.archive` as a safety net
- Verifies the conversion (file count against the script's own reported count, plus byte count) before reporting success

If an earlier conversion produced bad output and the archive is still present, the skill can regenerate the folder from it. See "Re-converting after a bad conversion" in the skill for the preconditions and reset steps.

### `/project-docs:readme`

Update `README.md` to document what the project is and how to use it:
- Project overview and current status
- Project structure (file tree)
- Installation and dependencies
- Configuration (SSM parameters, environment variables)
- Deployment instructions
- Development workflows

### `/project-docs:architecture`

Update `ARCHITECTURE.md` to document how the system is designed and why:
- System flow diagrams
- Data model (entities, attributes, indexes)
- API endpoint specs
- Workflow details (Step Functions, etc.)
- Infrastructure resources
- Patterns & conventions to follow when adding new code

### `/project-docs:ab-test <test-name> [file-path]`

Document an A/B test interactively. Creates or updates a structured document capturing:
- Test date
- Hypothesis
- Control and treatment variants (name + description)
- Group assignment (how users are segmented into test/control)
- How success will be measured
- When results will be evaluated
- Results and conclusions (filled in when test completes)

Arguments:
- `test-name` (required): Name of the test
- `file-path` (optional): Where to save. Defaults to `./{test-name}.md`

### `/project-docs:all-docs`

Update all project documentation by running these commands sequentially:
1. `/project-docs:process-notes`
2. `/project-docs:readme`
3. `/project-docs:architecture`

### `/project-docs:code-review`

Launch the `code-reviewer` agent to review all uncommitted changes. The agent checks:
- Consistency with ARCHITECTURE.md patterns
- Error handling coverage
- Test coverage (unit and integration)
- Security (secrets, least-privilege, input validation, logging hygiene, CORS, dependencies)
- Documentation (README, ARCHITECTURE.md, test.md, process-notes)

### `/project-docs:plan-review`

Launch the `plan-reviewer` agent to review the most recent plan in `.claude/plans/`. The agent checks:
- Consistency with project architecture and patterns
- Potential duplicates in the codebase
- Unnecessary complexity that could be simplified

## Skills

All commands have corresponding skills that Claude can invoke proactively:

- **process-notes** - Triggers when context window fills up (~60%), at key milestones, or on explicit request. Writes each entry as a new file in `process-notes/`.
- **convert-flat-process-notes-to-dir** - Migrates a legacy single-file `process-notes.md` to the `process-notes/` folder format. Triggered when the process-notes skill refuses to write or on explicit request.
- **readme** - Triggers when setup/deploy/config changes occur, or on explicit request
- **architecture** - Triggers when infrastructure/data model/patterns change, or on explicit request
- **ab-test** - Triggers when user mentions running an A/B test, comparing variants, or wanting to measure something systematically

**Note:** Claude doesn't consistently invoke skills automatically. Rely on the slash commands to ensure documentation gets updated.

## Migrating Existing Projects

If a project still has a legacy flat `process-notes.md`, the `process-notes` skill will refuse to write and ask you to migrate first. Run:

```
/project-docs:convert-flat-process-notes-to-dir
```

This splits the flat file into per-entry files under `process-notes/` and renames the original to `process-notes.md.archive` as a safety net. Review the dry-run listing it shows before confirming. Once you've confirmed the conversion looks right, you can delete the archive. Keep it until then: it is what a re-conversion rebuilds from.

## Agents

- **code-reviewer** - Reviews uncommitted code changes for consistency with project architecture, code quality, error handling, test coverage, security, and documentation. Use after writing code and before committing.
- **plan-reviewer** - Reviews implementation plans for consistency with ARCHITECTURE.md, checks for duplicate code, and flags unnecessary complexity. Use after creating a plan and before implementation.

## When to Use Each

| Scenario | README | ARCHITECTURE | process-notes/ |
|----------|--------|--------------|---------------|
| Added new feature | Yes (usage) | Maybe (if new pattern) | Yes (how/why) |
| Changed deployment | Yes | No | Yes |
| New infrastructure | Brief mention | Yes (details) | Yes |
| New data model | No | Yes | Yes |
| New pattern established | No | Yes | Yes |
| Changed API structure | No | Yes | Yes |
| Debugged tricky issue | No | No | Yes |
| Context window filling up | No | No | Yes |

## License

MIT
