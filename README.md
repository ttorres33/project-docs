# project-docs

A Claude Code plugin for maintaining project documentation:

- **process-notes.md** - Work history documenting decisions, dead ends, and progress
- **README.md** - Current state documentation for users and contributors
- **A/B test docs** - Structured documentation for experiments and tests

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

### `/project-docs:ab-test <test-name> [file-path]`

Document an A/B test interactively. Creates or updates a structured document capturing:
- Test date
- Hypothesis
- Control and treatment variants (name + description)
- How success will be measured
- When results will be evaluated
- Results and conclusions (filled in when test completes)

Arguments:
- `test-name` (required): Name of the test
- `file-path` (optional): Where to save. Defaults to `./{test-name}.md`

## Skills

All commands have corresponding skills that Claude can invoke proactively:

- **process-notes** - Triggers when context window fills up (~90%), at key milestones, or on explicit request
- **readme** - Triggers when structural/behavior/config changes occur, features are added/removed, or on explicit request
- **ab-test** - Triggers when user mentions running an A/B test, comparing variants, or wanting to measure something systematically

**Note:** Claude doesn't consistently invoke skills automatically. Rely on the slash commands to ensure documentation gets updated.

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
