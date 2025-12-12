---
name: readme
description: Keeps project README.md up-to-date with current state of the project. Use when structural changes occur, behavior changes, setup/config changes, feature additions/removals, or when user explicitly requests /readme command.
allowed-tools: Read, Edit, Write, Glob, Grep
---

# README Documentation Skill

## Purpose
Keep the project `README.md` up-to-date with the current state of the project. Unlike `process-notes.md` which maintains historical context, the README should reflect how the project works RIGHT NOW - its current structure, features, and usage.

## When to Update

Update `README.md` when any of these meaningful changes occur:

1. **Structural changes** - New files/modules added, architecture changes, component additions/removals
2. **Behavior changes** - Changed how something works, modified APIs/interfaces, updated workflows
3. **Setup/config changes** - New dependencies, environment variables, build process changes, installation steps
4. **Feature additions/removals** - New capabilities added or features removed
5. **Explicit user request** - When user invokes `/readme` command

## How to Update

1. **Read existing README** - Always read current `README.md` first to understand existing structure and content
2. **Assess scope of changes** - Determine appropriate update strategy:
   - **Minor updates**: Changed a few details → Incremental update of specific sections
   - **Moderate changes**: Added features or modules → Update relevant sections, preserve rest
   - **Major restructuring**: Significant architecture changes → Complete rewrite
3. **Preserve user content** - Keep manually-added content when possible (acknowledgments, custom sections, etc.)
4. **Use best judgment** - Choose the approach that makes sense for the magnitude of changes

## README Structure

Use this general structure, adapting sections as appropriate for the project:

```markdown
# [Project Name]

[Brief description - 1-2 sentences explaining what this project does]

## Quick Start

[Minimal steps to get up and running - installation and basic usage]

## Features

[High-level list of what the project can do]

## Installation

[Detailed installation steps, prerequisites, dependencies]

## Usage

[Basic usage examples showing common tasks]
[Link to detailed usage docs if they exist: See [docs/usage.md](docs/usage.md) for more examples]

## Architecture

[High-level overview of how the system is structured]
[Key components and how they interact]
[Important design decisions]
[Link to detailed architecture docs: See [docs/architecture.md](docs/architecture.md) for detailed design]

## Configuration

[Overview of configuration options - environment variables, config files]
[Link to detailed config docs: See [docs/configuration.md](docs/configuration.md) for all options]

## Development

[How to set up development environment]
[How to run tests]
[Link to contributing guide if exists: See [CONTRIBUTING.md](CONTRIBUTING.md)]

## Documentation

- [Architecture Details](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Additional docs as needed]

## License

[License information if applicable]
```

## Guidelines for High-Level Overview

### Keep It Brief
- README is the entry point - provide overview, not exhaustive detail
- Each section should be scannable and concise
- Use bullet points for lists
- Link to detailed docs in `docs/` folder for deep dives

### Architecture Section
- Describe the high-level structure (e.g., "Three-tier architecture: API layer, business logic, data access")
- List major components and their responsibilities
- Explain key design decisions briefly (e.g., "Uses event-driven architecture for scalability")
- Always link to `docs/architecture.md` for detailed design documentation
- Example:
  ```markdown
  ## Architecture

  The system uses a modular architecture with three main components:

  - **API Layer** (`src/api/`) - REST endpoints for client interaction
  - **Service Layer** (`src/services/`) - Business logic and orchestration
  - **Data Layer** (`src/data/`) - Database access and caching

  Key design decisions:
  - Event-driven communication between services for loose coupling
  - Repository pattern for data access to support multiple storage backends

  See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.
  ```

### Configuration Section
- List environment variables with brief descriptions
- Mention config file locations
- Provide one or two simple examples
- Link to `docs/configuration.md` for comprehensive configuration guide
- Example:
  ```markdown
  ## Configuration

  Configure via environment variables:

  - `DATABASE_URL` - PostgreSQL connection string
  - `API_PORT` - Port for API server (default: 3000)
  - `LOG_LEVEL` - Logging verbosity (debug, info, warn, error)

  See [docs/configuration.md](docs/configuration.md) for all configuration options.
  ```

### Usage Section
- Show the most common use cases (1-3 examples)
- Keep examples simple and self-contained
- Link to detailed usage documentation for advanced scenarios
- Example:
  ```markdown
  ## Usage

  Basic example:

  \`\`\`javascript
  const client = new APIClient({ apiKey: process.env.API_KEY });
  const result = await client.fetchData({ id: 123 });
  \`\`\`

  See [docs/usage.md](docs/usage.md) for more examples and advanced usage.
  ```

## Update Strategies

### Incremental Update (Minor Changes)
Use when:
- Adding a new feature to existing section
- Updating dependency versions
- Tweaking configuration options
- Small behavior changes

Process:
- Read existing README
- Identify specific sections to update
- Make surgical edits to those sections
- Preserve everything else

### Section Update (Moderate Changes)
Use when:
- Adding new major component
- Changing architecture of one part
- Adding new configuration requirements
- Restructuring one area

Process:
- Read existing README
- Rewrite affected sections completely
- Update related links/references
- Preserve unaffected sections

### Complete Rewrite (Major Changes)
Use when:
- Major architectural overhaul
- Project pivot or significant restructuring
- README is severely outdated
- Starting new project

Process:
- Analyze current codebase structure
- Generate fresh README based on current state
- Preserve any custom sections user added (acknowledgments, etc.)
- Ensure all sections reflect current reality

## Linking to Detailed Documentation

When the README references detailed docs:
- Use relative links: `[Architecture Details](docs/architecture.md)`
- Create placeholder if doc doesn't exist yet, or mention it should be created
- Ensure links are accurate to actual file locations
- Prefer `docs/` folder for all detailed documentation

Example linking pattern:
```markdown
## Architecture

[High-level overview here - 2-3 paragraphs]

For detailed architecture documentation including:
- Component interaction diagrams
- Data flow details
- Design patterns used
- Scalability considerations

See [docs/architecture.md](docs/architecture.md)
```

## When NOT to Update README

Don't update for:
- Code refactoring that doesn't change external behavior
- Internal implementation details that don't affect usage
- Bug fixes that restore intended behavior (unless fixing undocumented behavior)
- Whitespace or formatting changes in code
- Comment updates in code

DO update for:
- New features or capabilities
- Changed APIs or interfaces
- New configuration options
- Installation/setup changes
- Architecture changes
- Breaking changes

## Tone and Style

- **Clear and welcoming** - Assume reader is new to the project
- **Action-oriented** - Use active voice ("Run `npm install`" not "Dependencies can be installed")
- **Concise** - Every word should add value
- **Well-structured** - Use headings, bullets, code blocks for scannability
- **Current** - Always reflect the actual current state, not planned features or historical context

## Example README

```markdown
# Task Management CLI

A command-line tool for managing tasks and projects using markdown files and Obsidian.

## Quick Start

\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Import Trello cards
python scripts/import-trello.py export.json list-id

# Generate daily task files
python scripts/generate-daily-files.py
\`\`\`

## Features

- Import tasks from Trello boards
- Organize tasks by due date (today, this week, next week)
- Track recurring tasks with automatic date updates
- Markdown-based for use with Obsidian or any text editor
- Archive completed tasks automatically

## Architecture

The system uses a file-based architecture:

- **Task files** (`tasks/*.md`) - Individual task definitions with YAML frontmatter
- **View files** (`today.md`, `this-week.md`, etc.) - Generated aggregations of tasks by due date
- **Scripts** (`scripts/*.py`) - Automation for imports, date calculations, file generation
- **Templates** (`templates/*.md`) - Reusable task templates

Key design decisions:
- Markdown + YAML frontmatter for human readability and git-friendliness
- File-based storage (no database) for simplicity and portability
- Python scripts for automation while keeping data in plain text

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Configuration

Tasks use YAML frontmatter:

\`\`\`yaml
---
type: task | idea | template | memory
due: YYYY-MM-DD
recurrence: monthly | weekly | quarterly
tags: [tag1, tag2]
---
\`\`\`

See [CLAUDE.md](CLAUDE.md) for complete configuration guide.

## Development

\`\`\`bash
# Run tests
python -m pytest

# Check for new Trello cards
python scripts/trello_mcp_server.py
\`\`\`

## Documentation

- [Architecture Details](docs/architecture.md)
- [Task Management Guide](CLAUDE.md)
- [Script Documentation](scripts/README.md)

## License

Personal project - not licensed for public use
```

## File Location

- Always update `README.md` in the current working directory root
- If README doesn't exist, create it using the standard structure
- Never create README in subdirectories unless explicitly requested

## When to Use README vs Process-Notes

### Use README For:
- **The destination** - What the project is RIGHT NOW
- **Current state** - How it works today, not how it used to work
- **External-facing** - Documentation for users/contributors
- **Getting started** - How to install, configure, use the project
- **Current architecture** - How the system is structured now
- **No history** - Only what's true today, no "we used to..." or "we tried..."

### Use Process-Notes For:
- **The journey** - How we got here, what we tried, why we made decisions
- **Historical context** - What happened when, in chronological order
- **Learning from failures** - Dead ends, errors, what didn't work and why
- **Decision rationale** - Why we chose X over Y, alternatives considered
- **Session continuity** - Context for next agent to pick up where we left off
- **Work-in-progress** - Documenting as we go, even incomplete work

### Common Scenarios

| Scenario | README | Process-Notes | Both? |
|----------|--------|---------------|-------|
| **Just added OAuth authentication** | Yes - Update to show OAuth is now available, how to configure it | Yes - Document why we chose OAuth, what we tried first, implementation decisions | Both |
| **Debugged tricky issue for 2 hours** | No - Unless it changes how the project works or needs documentation | Yes - Document the debugging journey, what we learned, the solution | Process-Notes only |
| **Refactored file structure but behavior unchanged** | Maybe - If file paths in docs need updating | Maybe - If significant decisions were made about structure | Use judgment |
| **Added new feature (e.g., export to CSV)** | Yes - Update features list, add usage example | Yes - How we built it, libraries chosen, design decisions | Both |
| **Changed API endpoint structure** | Yes - Update API docs to reflect new structure | Yes - Why we changed it, migration path, breaking change reasoning | Both |
| **Fixed bug that restores documented behavior** | No - Behavior already documented correctly | Maybe - Only if debugging revealed important insights | Usually Process-Notes only |
| **Added environment variable** | Yes - Update configuration section | Yes - Why we needed it, what we considered | Both |
| **Spent time researching library options** | No - Unless we actually added the library | Yes - What we evaluated, pros/cons, final choice | Process-Notes only (until implementation) |
| **Reorganized code but kept same public API** | No - Internal structure doesn't affect users | Maybe - If architectural decisions were made | Usually Process-Notes only |
| **Context window approaching 90%** | No - Unless meaningful changes to document | Yes - Checkpoint current progress | Process-Notes only (checkpoint) |
| **Completed major milestone** | Maybe - If milestone adds/changes features | Yes - Document what we accomplished, decisions made | Process-Notes always, README if user-facing changes |

### Quick Decision Guide

**Update README if:**
- External behavior changed (how users interact with it)
- Features added or removed
- Installation/setup steps changed
- Configuration options changed
- Architecture changed in a way that affects understanding

**Update Process-Notes if:**
- We made a decision (any decision worth remembering)
- We hit a dead end or learned something
- Context window is getting full
- We completed work on something (even if not fully done)
- Future us needs to understand why we did something

**Update both if:**
- We added a new feature (README: what it does, process-notes: how/why)
- We made breaking changes (README: new API, process-notes: migration reasoning)
- We changed project structure in user-visible ways

**Update neither if:**
- Pure code cleanup with no behavioral change
- Minor bug fixes that restore documented behavior
- Internal refactoring invisible to users
- Just reading/researching (not implementing yet)

## Important Notes

- **Reflect current state only** - No historical context, no future plans
- **Link to detailed docs** - Keep README high-level, use `docs/` for depth
- **Use best judgment** - Choose update strategy appropriate to the change magnitude
- **Preserve user additions** - Keep custom sections, acknowledgments, badges, etc.
- **Stay synchronized** - README should always accurately reflect the actual codebase
- **README is external** - Written for users/contributors, not just internal team
- **README is current-state only** - Update/replace content as project evolves, don't keep old info
