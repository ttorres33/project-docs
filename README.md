# project-docs

A Claude Code plugin for maintaining project documentation:

- **README.md** - What is this and how do I use it (setup, deploy, test)
- **ARCHITECTURE.md** - How is this designed and why (design, patterns, conventions)
- **process-notes.md** - Work history documenting decisions, dead ends, and progress
- **A/B test docs** - Structured documentation for experiments and tests

## Installation

```bash
claude plugins add cc-plugins/project-docs
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

## Skills

All commands have corresponding skills that Claude can invoke proactively:

- **process-notes** - Triggers when context window fills up (~90%), at key milestones, or on explicit request
- **readme** - Triggers when setup/deploy/config changes occur, or on explicit request
- **architecture** - Triggers when infrastructure/data model/patterns change, or on explicit request
- **ab-test** - Triggers when user mentions running an A/B test, comparing variants, or wanting to measure something systematically

**Note:** Claude doesn't consistently invoke skills automatically. Rely on the slash commands to ensure documentation gets updated.

## Agents

- **plan-reviewer** - Reviews implementation plans for consistency with ARCHITECTURE.md, checks for duplicate code, and flags unnecessary complexity. Use after creating a plan and before implementation.

## When to Use Each

| Scenario | README | ARCHITECTURE | process-notes |
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
