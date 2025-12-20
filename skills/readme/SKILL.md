---
name: readme
description: Keeps project README.md up-to-date with current state of the project. Use when structural changes occur, behavior changes, setup/config changes, feature additions/removals, or when user explicitly requests /readme command.
allowed-tools: Read, Edit, Write, Glob, Grep
---

# README Documentation Skill

## Purpose
Keep the project `README.md` up-to-date with what the project is and how to use it. The README is the entry point for users and contributors - it answers "What is this and how do I use it?"

**Key distinction:**
- **README.md** = "What is this and how do I use it" (setup, deploy, test)
- **ARCHITECTURE.md** = "How is this designed and why" (design, patterns, conventions)

README should reflect how the project works RIGHT NOW - its current status, structure, and usage. Link to ARCHITECTURE.md for design details.

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

## Current Status

[What's working, what's ready, what's in progress]

## Quick Start

[Minimal steps to get up and running - installation and basic usage]

## Project Structure

[File tree showing key directories and their purpose]

## Installation

[Detailed installation steps, prerequisites, dependencies]

## Dependencies

[External dependencies, imported stacks, required services]

## Configuration

[SSM parameters required, environment variables, config files]
[Link to detailed config docs: See [docs/configuration.md](docs/configuration.md) for all options]

## Deployment

[How to deploy - deploy.sh, sync-prompts.sh, etc.]
[Key deployment steps and scripts]

## Development

[How to set up development environment]
[How to run tests - unit tests, integration tests]
[Development workflows - prompt testing, local testing, etc.]
[Link to contributing guide if exists: See [CONTRIBUTING.md](CONTRIBUTING.md)]

## Documentation

- [Architecture & Design](ARCHITECTURE.md) - How the system is designed and why
- [Additional docs as needed]

## License

[License information if applicable]
```

## Guidelines

### Keep It Brief
- README is the entry point - provide overview, not exhaustive detail
- Each section should be scannable and concise
- Use bullet points for lists
- Link to ARCHITECTURE.md for design details
- Link to docs/ folder for deep dives on specific topics

### Project Structure Section
- Show the file tree with key directories
- Brief description of what each directory contains
- Example:
  ```markdown
  ## Project Structure

  ```
  project/
  ├── lambdas/           # Lambda function handlers
  ├── step-functions/    # Step Function definitions
  ├── prompts/           # LLM prompt templates
  ├── tests/             # Unit and integration tests
  └── template.yaml      # SAM template
  ```
  ```

### Configuration Section
- List SSM parameters required
- List environment variables with brief descriptions
- Mention config file locations
- Example:
  ```markdown
  ## Configuration

  ### SSM Parameters
  - `/app/openai-api-key` - OpenAI API key
  - `/app/airtable-token` - Airtable API token

  ### Environment Variables
  - `STAGE` - Deployment stage (dev, prod)
  - `LOG_LEVEL` - Logging verbosity (debug, info, warn, error)
  ```

### Deployment Section
- List deployment scripts and what they do
- Show the basic deployment command
- Example:
  ```markdown
  ## Deployment

  ```bash
  # Deploy all infrastructure
  ./deploy.sh

  # Sync prompts to S3
  ./sync-prompts.sh

  # Deploy dashboard only
  ./deploy-dashboard.sh
  ```
  ```

### Development Section
- How to run tests
- Key development workflows
- Example:
  ```markdown
  ## Development

  ```bash
  # Run unit tests
  npm test

  # Test prompts locally
  ./test-prompt.sh prompt-name

  # Run integration tests
  npm run test:integration
  ```
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
# Canvas Coach API

Serverless API for coaching users through the Business Fundamentals Canvas.

## Current Status

- Canvas extraction: Working
- Coaching flow: Working
- Dashboard: In development

## Quick Start

\`\`\`bash
# Deploy to AWS
./deploy.sh

# Sync prompts
./sync-prompts.sh
\`\`\`

## Project Structure

\`\`\`
project/
├── lambdas/           # Lambda function handlers
├── step-functions/    # Step Function state machines
├── prompts/           # LLM prompt templates
├── dashboard/         # React dashboard
├── tests/             # Unit and integration tests
└── template.yaml      # SAM infrastructure
\`\`\`

## Dependencies

- Imports `shared-infrastructure` stack for VPC and common resources
- Requires OpenAI API access
- Requires Airtable for data storage

## Configuration

### SSM Parameters
- `/canvas-coach/openai-api-key` - OpenAI API key
- `/canvas-coach/airtable-token` - Airtable API token

### Environment Variables
- `STAGE` - Deployment stage (dev, prod)

## Deployment

\`\`\`bash
# Full deployment
./deploy.sh

# Sync prompts only
./sync-prompts.sh

# Deploy dashboard
./deploy-dashboard.sh
\`\`\`

## Development

\`\`\`bash
# Run unit tests
npm test

# Test a prompt locally
./test-prompt.sh coaching-prompt

# Run canvas extraction test
./test-extraction.sh sample.pdf
\`\`\`

## Documentation

- [Architecture & Design](ARCHITECTURE.md) - System design, data model, patterns
- [Prompt Guide](docs/prompts.md) - How to write and test prompts

## License

Proprietary
```

## File Location

- Always update `README.md` in the current working directory root
- If README doesn't exist, create it using the standard structure
- Never create README in subdirectories unless explicitly requested

## When to Use README vs ARCHITECTURE.md vs Process-Notes

### Use README For:
- **What and how to use** - What the project is and how to use it
- **Current status** - What's working, what's ready
- **Getting started** - How to install, deploy, configure
- **Project structure** - File tree overview
- **Development workflows** - How to test, how to develop
- **No design details** - Link to ARCHITECTURE.md for that

### Use ARCHITECTURE.md For:
- **How it's designed** - System flow, data model, infrastructure
- **Why it's designed that way** - Design decisions, trade-offs
- **Patterns to follow** - Conventions for adding new code
- **Technical specs** - API contracts, data schemas, workflows

### Use Process-Notes For:
- **The journey** - How we got here, what we tried
- **Historical context** - What happened when, in chronological order
- **Dead ends** - What didn't work and why
- **Decision rationale** - Why we chose X over Y, alternatives considered
- **Session continuity** - Context for next session

### Quick Decision Guide

**Update README if:**
- Deployment or setup steps changed
- Project structure changed
- New configuration options
- Development workflow changed
- Status of features changed

**Update ARCHITECTURE.md if:**
- New infrastructure resources
- Data model changes
- New patterns established
- API contracts changed
- Design decisions made

**Update Process-Notes if:**
- Made a decision worth remembering
- Hit a dead end or learned something
- Context window is getting full
- Completed work on something

## Important Notes

- **Reflect current state only** - No historical context, no future plans
- **Link to detailed docs** - Keep README high-level, use `docs/` for depth
- **Use best judgment** - Choose update strategy appropriate to the change magnitude
- **Preserve user additions** - Keep custom sections, acknowledgments, badges, etc.
- **Stay synchronized** - README should always accurately reflect the actual codebase
- **README is external** - Written for users/contributors, not just internal team
- **README is current-state only** - Update/replace content as project evolves, don't keep old info
