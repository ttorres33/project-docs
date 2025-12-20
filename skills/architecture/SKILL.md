---
name: architecture
description: Keeps project ARCHITECTURE.md up-to-date with system design, patterns, and conventions. Use when infrastructure changes, new patterns are established, data models change, or when user explicitly requests /architecture command.
allowed-tools: Read, Edit, Write, Glob, Grep
---

# Architecture Documentation Skill

## Purpose
Keep the project `ARCHITECTURE.md` up-to-date with how the system is designed and why. Unlike `README.md` which explains how to use the project, ARCHITECTURE.md explains how the system works internally, the design decisions behind it, and the patterns to follow when adding new code.

**Key distinction:**
- **README.md** = "What is this and how do I use it" (setup, deploy, test)
- **ARCHITECTURE.md** = "How is this designed and why" (design, patterns, conventions)

## When to Update

Update `ARCHITECTURE.md` when any of these occur:

1. **Infrastructure changes** - New AWS resources, changed SAM templates, modified deployment topology
2. **Data model changes** - New DynamoDB tables/entities, changed attributes, new GSIs
3. **API changes** - New endpoints, changed request/response formats, new authentication patterns
4. **Workflow changes** - New Step Functions, modified state machines, changed orchestration
5. **New patterns established** - When you solve a problem in a way that should be replicated
6. **Convention changes** - Updated naming conventions, file organization, code structure patterns
7. **Explicit user request** - When user invokes `/architecture` command

## How to Update

1. **Read existing ARCHITECTURE.md** - Always read current file first to understand existing structure
2. **Assess scope of changes** - Determine appropriate update strategy:
   - **Minor updates**: Changed a few details → Incremental update of specific sections
   - **Moderate changes**: Added new component or pattern → Update relevant sections
   - **Major restructuring**: Significant architecture changes → Complete rewrite
3. **Document the "why"** - Always explain rationale, not just what exists
4. **Include examples** - Show code patterns, not just describe them

## ARCHITECTURE.md Structure

Use this structure, adapting sections as appropriate for the project:

```markdown
# [Project Name] Architecture

[Brief description of the system's purpose and high-level architecture approach]

## System Overview

[High-level diagram or description of how components interact]
[Key architectural decisions and why they were made]

## System Flow

[How data flows through the system]
[Key workflows and their triggers]
[Sequence of operations for main use cases]

## Data Model

### [Entity Name]
- **Table/Collection**: [name]
- **Partition Key**: [key] - [why this key]
- **Sort Key**: [key] - [why this key]
- **Attributes**:
  - `attribute1` (type) - description
  - `attribute2` (type) - description
- **GSIs**:
  - `GSI-Name`: PK=X, SK=Y - [use case this supports]

[Repeat for each entity]

## API Endpoints

### [Endpoint Group]

#### `METHOD /path`
- **Purpose**: What this endpoint does
- **Request**: Key request parameters
- **Response**: Key response fields
- **Notes**: Any special behavior

[Repeat for each endpoint]

## Workflows

### [Workflow Name]
- **Trigger**: What starts this workflow
- **Steps**:
  1. Step description
  2. Step description
- **Error Handling**: How errors are handled
- **Output**: What the workflow produces

[Repeat for each workflow, including Step Functions]

## Infrastructure

### AWS Resources
- **Lambda Functions**: List with brief purpose
- **Step Functions**: List with brief purpose
- **DynamoDB Tables**: List with key structure
- **API Gateway**: Endpoints exposed
- **Other Resources**: S3 buckets, SQS queues, etc.

### Deployment
- How infrastructure is defined (SAM, CDK, Terraform)
- Key deployment considerations

## Patterns & Conventions

### [Category] Patterns

#### [Pattern Name]
**When to use**: Conditions that call for this pattern
**How to implement**:
```[language]
// Example code showing the pattern
```
**Why**: Rationale for this pattern

[Repeat for each pattern category: Lambda patterns, Step Function patterns, DynamoDB patterns, etc.]

### Naming Conventions
- [Convention 1]: Example
- [Convention 2]: Example

### File Organization
```
project/
├── folder1/     # Description
├── folder2/     # Description
└── folder3/     # Description
```
```

## Guidelines

### Focus on the "Why"
- Don't just document what exists - explain why it's designed that way
- Include trade-offs considered
- Reference decisions from process-notes.md if helpful

### Be Specific with Patterns
- Show concrete code examples, not abstract descriptions
- Include both the pattern and when to use it
- Bad: "Use consistent error handling"
- Good: "Wrap Lambda handlers with `withErrorHandling()` which logs errors and returns standardized error responses"

### Keep It Current
- Remove patterns that are no longer used
- Update examples when code changes
- Mark deprecated patterns clearly if they still exist in code

### Appropriate Detail Level
- More detail than README (which is high-level overview)
- Less detail than inline code comments (which are implementation-specific)
- Right level: Someone new could understand the system and add code that fits

## When NOT to Update

Don't update for:
- Bug fixes that don't change architecture
- Minor code refactoring within existing patterns
- Content changes (copy, messages, etc.)
- Test additions that follow existing patterns

DO update for:
- New infrastructure resources
- New patterns that should be replicated
- Changed conventions
- New data entities or relationships
- New API endpoints or changed contracts

## When to Use ARCHITECTURE.md vs README.md vs Process-Notes

| Content Type | ARCHITECTURE.md | README.md | Process-Notes |
|--------------|-----------------|-----------|---------------|
| How to install/deploy | No | Yes | No |
| System flow diagram | Yes | Link to arch | No |
| Data model details | Yes | No | No |
| API endpoint specs | Yes | Brief list | No |
| Code patterns to follow | Yes | No | No |
| Why we chose X over Y | Yes (current) | No | Yes (historical) |
| What's working now | No | Yes | No |
| Dead ends tried | No | No | Yes |
| SSM parameters needed | No | Yes | No |
| Infrastructure resources | Yes (detailed) | Brief list | No |

### Quick Decision Guide

**Put in ARCHITECTURE.md if:**
- Someone adding new code needs to know this to do it right
- It explains how the system works internally
- It's a pattern or convention to follow
- It describes infrastructure or data structures

**Put in README.md if:**
- Someone using/deploying the project needs to know this
- It's about setup, configuration, or running the project
- It's a high-level overview for orientation

**Put in Process-Notes if:**
- It's about the journey, not the destination
- It documents a decision with alternatives considered
- It's a dead end or lesson learned
- It's session context for continuity

## File Location

- Always update `ARCHITECTURE.md` in the project root
- If ARCHITECTURE.md doesn't exist, create it using the standard structure
- Keep detailed pattern docs in `docs/` folder and link from ARCHITECTURE.md if needed
