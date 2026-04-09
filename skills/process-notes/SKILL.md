---
name: process-notes
description: Maintains comprehensive project history in a process-notes/ folder that documents work process, decisions, dead ends, and progress. Each entry is a separate file named by timestamp + slug. Use when context window fills up (approaching 60% of token budget), when making key decisions or reaching milestones, or when the user explicitly requests /project-docs:process-notes.
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
---

# Process Notes Documentation Skill

## Purpose
Maintain a comprehensive project history in a `process-notes/` folder that documents work process, decisions, dead ends, and progress. Each entry is a separate file so writes stay small and atomic, grep works naturally across the whole history, and reading recent entries is `ls -t process-notes/ | head -3`.

## When to Update

Update process notes when any of these conditions occur:

1. **Context window fills up** - When approaching ~60% of token budget, create an entry before context gets compacted
2. **Key decision or milestone** - When making an important architectural decision, completing a major feature, or reaching a significant milestone
3. **Explicit user request** - When user invokes `/project-docs:process-notes`

## How to Update

### Step 1: Check format

Before writing anything, check which format the project is using:

```bash
ls -la process-notes.md process-notes/ 2>/dev/null
```

- **If `process-notes/` exists**: Use the new folder format. Proceed to step 2.
- **If `process-notes.md` exists but `process-notes/` does not**: The project is using the legacy flat-file format. Stop and tell the user to run `/project-docs:convert-flat-process-notes-to-dir` first. Do not attempt to write anything until the conversion is done.
- **If neither exists**: This is a fresh project. Create the `process-notes/` folder with `mkdir process-notes` and proceed to step 2.

### Step 2: Read recent entries for context

Before writing a new entry, read the most recent 2-3 entries so the new entry fits into the ongoing narrative:

```bash
ls -t process-notes/ | head -3
```

Then `Read` those files. Do not read the entire folder — just the recent ones.

### Step 3: Build the new entry filename

Filename format: `YYYY-MM-DDTHHMM-slug.md`

- Use the current date and time (24-hour, minute precision, no seconds)
- Slug: lowercase, alphanumeric + hyphens, derived from the entry title, no longer than ~60 chars
- Example: `2026-04-08T1432-revise-process-notes-to-folder-model.md`

If a file with the exact same name already exists (rare — only if two entries land in the same minute with the same title), append `-2`, `-3`, etc.

### Step 4: Write the new entry

Create the file with the structured content format below. Each file is self-contained — do NOT read, edit, or touch any other file in `process-notes/`.

## Entry Format

Use this exact structure for each entry file:

```markdown
# [Brief Title]

**Context:** [Brief statement of what was being worked on in this session/segment]

**Progress:**
- Accomplished task 1
  - Created `src/auth/login.ts` - implemented JWT authentication
  - Modified `src/config/database.ts:45-67` - added connection pooling
- Accomplished task 2
  - Details with file references

**Key Decisions:**
- **Decision:** [What was decided]
  - **Rationale:** [Why this approach was chosen]
  - **Alternatives considered:** [What else was looked at]
  - **Trade-offs:** [What was gained/sacrificed]
  - **Files affected:** `path/to/file.ts:lines`

**Dead Ends & Lessons:**
- **Attempted:** [What was tried]
  - **Implementation:** [Specific approach taken]
  - **Files involved:** `path/to/file.ts:lines`
  - **Error/Issue:** [What failed - include error messages if relevant]
  - **Why it failed:** [Root cause analysis]
  - **What was learned:** [Key takeaway]
  - **Solution:** [What was done instead and why it worked]

**Technical Details:**
- New files created: [list with purpose]
- Files modified: [list with what changed]
- Dependencies added/removed: [package changes]
- Configuration changes: [environment, build configs, etc.]

**Next Steps:**
- [ ] Task 1 - [with enough context to understand what/why]
- [ ] Task 2 - [reference to relevant files/functions if helpful]
- **Context for next session:** [Anything the next agent needs to know to pick up smoothly]

**Questions/Blockers:**
- Open questions that need answering
- Blockers encountered that aren't resolved yet
```

Note: the file starts with `# Title`, NOT `## [timestamp] Entry N: Title`. The timestamp lives in the filename, and there is no global entry numbering — each entry file is self-contained.

## Guidelines for Comprehensive Documentation

### Progress Section
- List all significant accomplishments in this segment
- Always include file references with line numbers when relevant
- Describe what was implemented, not just "created file X"
- Example: "Created `src/auth/middleware.ts:1-45` - implemented JWT verification middleware with error handling"

### Key Decisions Section
- Document architectural choices, library selections, pattern decisions
- Always explain rationale - the "why" is crucial
- List alternatives that were considered and why they weren't chosen
- Describe trade-offs explicitly (what was gained vs. what was sacrificed)
- Include file references for where the decision is implemented

### Dead Ends & Lessons Section
- This is critical for avoiding repeated mistakes
- Describe what was attempted with enough detail to understand the approach
- Include actual error messages when relevant
- Explain root cause, not just symptoms
- Document the lesson learned
- Describe the solution that worked and why

### Technical Details Section
- List all new files with their purpose
- List all modified files with summary of changes
- Track dependency additions/removals
- Note configuration changes (env vars, build configs, etc.)
- Include database migrations, API changes, breaking changes

### Next Steps Section
- Use checkbox format for actionable tasks
- Provide enough context that next agent can pick up without full conversation history
- Reference relevant files/functions when helpful
- Add "Context for next session" with any important state or decisions that affect next work

### Questions/Blockers Section
- Document open questions that need user input
- Note blockers that aren't resolved yet
- This helps track what needs to be addressed before proceeding

## File Location

- Always write new entries to `process-notes/` in the current working directory root
- Each entry is its own file — never append to an existing entry file, never read the whole folder
- Never modify existing entry files, only create new ones

## Reading Recent Entries

When starting a new session and needing context from past work:

```bash
ls -t process-notes/ | head -3
```

Then `Read` those files. For grep-style searches across all entries:

```bash
grep -r "pattern" process-notes/
```

Do not `Read` the whole folder — it grows unbounded over time and will waste context. If you need to search for something specific, use `Grep` with a pattern.

## Tone and Style

- Use structured bullet points for scanability
- Be comprehensive but clear
- Include technical specifics (file paths, line numbers, function names)
- Write for future you/agents who need full context
- Don't assume knowledge - explain decisions and reasoning
- Use markdown formatting for code references: `file.ts:lines`

## Example Entry

```markdown
# Initial Authentication System

**Context:** Setting up user authentication for the web application. Need JWT-based auth with refresh tokens.

**Progress:**
- Implemented core authentication system
  - Created `src/auth/jwt.ts:1-120` - JWT token generation and validation utilities
  - Created `src/auth/middleware.ts:1-67` - Express middleware for protecting routes
  - Modified `src/server.ts:23-28` - integrated auth middleware into Express app
  - Created `src/routes/auth.ts:1-89` - login/logout/refresh endpoints

**Key Decisions:**
- **Decision:** Use JWT with short-lived access tokens (15min) + long-lived refresh tokens (7 days)
  - **Rationale:** Balances security (short access token expiry) with UX (don't force frequent re-login)
  - **Alternatives considered:** Session-based auth (rejected - doesn't scale horizontally), long-lived JWTs only (rejected - security risk)
  - **Trade-offs:** Added complexity of refresh token flow, but gained better security posture
  - **Files affected:** `src/auth/jwt.ts:45-89`, `src/routes/auth.ts:34-67`

**Dead Ends & Lessons:**
- **Attempted:** Store refresh tokens in localStorage
  - **Implementation:** Added refresh token to JWT payload, stored in localStorage on client
  - **Files involved:** `src/auth/jwt.ts:23-34`
  - **Error/Issue:** Realized this is vulnerable to XSS attacks - localStorage accessible to any script
  - **Why it failed:** Security best practice is httpOnly cookies for refresh tokens to prevent XSS access
  - **What was learned:** Never store sensitive tokens in localStorage, use httpOnly cookies instead
  - **Solution:** Implemented refresh token in httpOnly cookie in `src/routes/auth.ts:56-62`, removed from JWT payload

**Technical Details:**
- New files created:
  - `src/auth/jwt.ts` - JWT utilities (sign, verify, decode)
  - `src/auth/middleware.ts` - Express auth middleware
  - `src/routes/auth.ts` - Auth endpoints
  - `src/types/auth.ts` - TypeScript types for auth
- Files modified:
  - `src/server.ts:23-28` - integrated auth routes
- Dependencies added:
  - `jsonwebtoken@9.0.2` - JWT signing/verification
  - `@types/jsonwebtoken@9.0.3` - TypeScript types
  - `cookie-parser@1.4.6` - Parse cookies for refresh token
- Configuration changes:
  - Added `JWT_SECRET` and `JWT_REFRESH_SECRET` to `.env`
  - Added `JWT_EXPIRY=15m` and `REFRESH_EXPIRY=7d` to config

**Next Steps:**
- [ ] Add password hashing with bcrypt in user registration flow - needs `src/routes/users.ts` implementation
- [ ] Implement token refresh endpoint - partially done in `src/routes/auth.ts:78-89`, needs testing
- [ ] Add rate limiting to login endpoint to prevent brute force attacks
- **Context for next session:** Auth system works for login/logout. Need to add user registration with password hashing, and test the refresh token flow end-to-end.

**Questions/Blockers:**
- Should we implement 2FA now or in a later iteration?
- Need to confirm password requirements (min length, complexity rules)
```

## When to Use Process-Notes vs README

### Use Process-Notes For:
- **The journey** - How we got here, what was tried, why decisions were made
- **Historical context** - What happened when, in chronological order
- **Learning from failures** - Dead ends, errors, what didn't work and why
- **Decision rationale** - Why X was chosen over Y, alternatives considered
- **Session continuity** - Context for next agent to pick up where we left off
- **Work-in-progress** - Documenting as we go, even incomplete work

### Use README For:
- **The destination** - What the project is RIGHT NOW
- **Current state** - How it works today, not how it used to work
- **External-facing** - Documentation for users/contributors
- **Getting started** - How to install, configure, use the project
- **Current architecture** - How the system is structured now
- **No history** - Only what's true today, no "we used to..." or "we tried..."

### Common Scenarios

| Scenario | Process-Notes | README | Both? |
|----------|--------------|--------|-------|
| **Just added OAuth authentication** | Yes - Document why OAuth was chosen, what was tried first, implementation decisions | Yes - Update to show OAuth is now available, how to configure it | Both |
| **Debugged tricky issue for 2 hours** | Yes - Document the debugging journey, what was learned, the solution | No - Unless it changes how the project works or needs documentation | Process-Notes only |
| **Refactored file structure but behavior unchanged** | Maybe - If significant decisions were made about structure | Maybe - If file paths in docs need updating | Use judgment |
| **Added new feature (e.g., export to CSV)** | Yes - How it was built, libraries chosen, design decisions | Yes - Update features list, add usage example | Both |
| **Changed API endpoint structure** | Yes - Why it changed, migration path, breaking change reasoning | Yes - Update API docs to reflect new structure | Both |
| **Fixed bug that restores documented behavior** | Maybe - Only if debugging revealed important insights | No - Behavior already documented correctly | Usually Process-Notes only |
| **Added environment variable** | Yes - Why it was needed, what was considered | Yes - Update configuration section | Both |
| **Spent time researching library options** | Yes - What was evaluated, pros/cons, final choice | No - Unless the library was actually added | Process-Notes only (until implementation) |
| **Reorganized code but kept same public API** | Maybe - If architectural decisions were made | No - Internal structure doesn't affect users | Usually Process-Notes only |
| **Context window approaching 60%** | Yes - Checkpoint current progress | No - Unless meaningful changes to document | Process-Notes only (checkpoint) |
| **Completed major milestone** | Yes - Document what was accomplished, decisions made | Maybe - If milestone adds/changes features | Process-Notes always, README if user-facing changes |

### Quick Decision Guide

**Update Process-Notes if:**
- A decision was made (any decision worth remembering)
- A dead end was hit or something was learned
- Context window is getting full
- Work was completed on something (even if not fully done)
- Future agents need to understand why something was done

**Update README if:**
- External behavior changed (how users interact with it)
- Features added or removed
- Installation/setup steps changed
- Configuration options changed
- Architecture changed in a way that affects understanding

**Update both if:**
- A new feature was added (process-notes: how/why, README: what it does)
- Breaking changes were made (process-notes: migration reasoning, README: new API)
- Project structure changed in user-visible ways

**Update neither if:**
- Pure code cleanup with no behavioral change
- Minor bug fixes that restore documented behavior
- Internal refactoring invisible to users
- Just reading/researching (not implementing yet)

## Important Notes

- **Be comprehensive** - This is the project's memory, capture everything important
- **Always include technical details** - File paths, line numbers, function names, error messages
- **Document the why** - Decisions and reasoning are more valuable than just what was done
- **Learn from failures** - Dead ends section is crucial for avoiding repeated mistakes
- **Provide context for next session** - Future agents need to pick up smoothly
- **Process-Notes is internal** - Written for the team, not external users
- **Each entry file is immutable** - Never edit an existing entry, always create a new file
