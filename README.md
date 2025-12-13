# project-docs

A Claude Code plugin for maintaining project documentation with two complementary files:

- **process-notes.md** - Work history documenting decisions, dead ends, and progress
- **README.md** - Current state documentation for users and contributors

## Installation

```bash
claude plugins add ttorres33/project-docs
```

## Commands

### `/project-docs:about`

Show this README for help and usage information.

### `/project-docs:process-notes`

Document current session progress to `process-notes.md`. Creates a comprehensive entry capturing:
- What was accomplished with file references
- Key decisions with rationale and alternatives considered
- Dead ends: what didn't work, why, and what was done instead
- Technical details: files created/modified, dependencies, configs
- Next steps with context for the next session

### `/project-docs:readme`

Update `README.md` to reflect the current project state:
- High-level overview
- Quick start and installation
- Current features and usage
- Architecture overview
- Configuration options
- Development setup

## Skills

Both commands have corresponding skills that Claude can invoke proactively:

- **process-notes** - Triggers when context window fills up (~90%), at key milestones, or on explicit request
- **readme** - Triggers when structural/behavior/config changes occur, features are added/removed, or on explicit request

**Note:** Claude doesn't consistently invoke skills automatically. Rely on the slash commands (`/project-docs:process-notes` and `/project-docs:readme`) to ensure documentation gets updated.

## When to Use Each

| Scenario | process-notes | README |
|----------|---------------|--------|
| Added new feature | Yes (how/why) | Yes (what it does) |
| Debugged tricky issue | Yes | No |
| Changed API structure | Yes (reasoning) | Yes (new API) |
| Context window filling up | Yes | No |
| Refactored internals | Yes | No |

## License

MIT
