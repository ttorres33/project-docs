---
name: process-notes
description: Maintains comprehensive project history in process-notes.md that documents work process, decisions, dead ends, and progress. Use when context window fills up (approaching 90% of token budget), when making key decisions or reaching milestones, or when user explicitly requests /process-notes command.
allowed-tools: Read, Edit, Write, Glob, Bash, Grep
---

# Process Notes Documentation Skill

## Purpose
Maintain a comprehensive project history in `process-notes.md` that documents our work process, decisions, dead ends, and progress. This creates a complete record that helps remember key decisions and provides full context for what happened and when.

## When to Update

Update `process-notes.md` when any of these conditions occur:

1. **Context window fills up** - When approaching ~90% of token budget, create an entry before context gets compacted
2. **Key decision or milestone** - When we make an important architectural decision, complete a major feature, or reach a significant milestone
3. **Explicit user request** - When user invokes `/process-notes` command

## How to Update

1. **Ensure .gitignore is configured** - Before creating or updating `process-notes.md`, ensure it's excluded from git
   - Check if project is a git repository by looking for `.git` directory
   - If git repo exists, check if `.gitignore` exists
   - If `.gitignore` exists, check if `process-notes.md` is already listed
   - If not listed, append `process-notes.md` to `.gitignore`
   - If `.gitignore` doesn't exist and this is a git repo, create it with `process-notes.md`
   - Rationale: process-notes.md is internal working documentation, not meant for version control
2. **Read existing file** - Always read `process-notes.md` first to understand current state and append new entries
3. **Create comprehensive entry** - Use the structured format below with detailed technical information
4. **Append to file** - Add new entry at the bottom with timestamp
5. **Preserve history** - Never remove or modify previous entries, only append

## Entry Format

Use this exact structure for each entry:

```markdown
## [YYYY-MM-DD HH:MM] Entry N: [Brief Title]

**Context:** [Brief statement of what we were working on in this session/segment]

**Progress:**
- Accomplished task 1
  - Created `src/auth/login.ts` - implemented JWT authentication
  - Modified `src/config/database.ts:45-67` - added connection pooling
- Accomplished task 2
  - Details with file references

**Key Decisions:**
- **Decision:** [What was decided]
  - **Rationale:** [Why we chose this approach]
  - **Alternatives considered:** [What else we looked at]
  - **Trade-offs:** [What we gained/sacrificed]
  - **Files affected:** `path/to/file.ts:lines`

**Dead Ends & Lessons:**
- **Attempted:** [What we tried]
  - **Implementation:** [Specific approach taken]
  - **Files involved:** `path/to/file.ts:lines`
  - **Error/Issue:** [What failed - include error messages if relevant]
  - **Why it failed:** [Root cause analysis]
  - **What we learned:** [Key takeaway]
  - **Solution:** [What we did instead and why it worked]

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

---
```

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
- Describe trade-offs explicitly (what we gained vs. what we sacrificed)
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

- Always create/update `process-notes.md` in the current working directory root
- If file doesn't exist, create it with a title: `# Project Process Notes`
- Always append new entries at the bottom, never modify existing entries

## Gitignore Management

Process-notes.md is internal working documentation and should NOT be committed to version control. Before creating or updating process-notes.md, ensure proper .gitignore configuration:

### Step-by-step .gitignore check:

1. **Check if git repository exists:**
   ```bash
   test -d .git && echo "Git repo" || echo "Not a git repo"
   ```

2. **If git repo exists, check for .gitignore:**
   - Use Glob or Read to check if `.gitignore` exists in current directory

3. **If .gitignore exists, check if process-notes.md is already listed:**
   - Use Grep to search for `process-notes.md` in `.gitignore`
   - Search pattern: `^process-notes\.md$` (exact match on its own line)

4. **If not listed, add it:**
   - Use Edit or Write to append `process-notes.md` to `.gitignore`
   - Add a comment explaining why: `# Internal working documentation - not for version control`

5. **If .gitignore doesn't exist (but git repo does), create it:**
   - Create `.gitignore` with `process-notes.md` entry
   - Add comment explaining the file's purpose

### Example implementation:

```bash
# Check if git repo
if [ -d .git ]; then
  # Check if .gitignore exists
  if [ -f .gitignore ]; then
    # Check if process-notes.md is already in .gitignore
    if ! grep -q "^process-notes\.md$" .gitignore; then
      # Add it with a comment
      echo "" >> .gitignore
      echo "# Internal working documentation - not for version control" >> .gitignore
      echo "process-notes.md" >> .gitignore
    fi
  else
    # Create .gitignore with process-notes.md
    cat > .gitignore << 'EOF'
# Internal working documentation - not for version control
process-notes.md
EOF
  fi
fi
```

### Why this matters:

- **process-notes.md is for internal use** - Contains work-in-progress thoughts, dead ends, and implementation details
- **Not meant for external consumption** - Unlike README which is public-facing
- **Privacy** - May contain internal reasoning or sensitive context
- **Reduces noise** - Prevents cluttering repository with internal working documents
- **Per-developer artifact** - Each developer/agent may have their own process notes

## Tone and Style

- Use structured bullet points for scanability
- Be comprehensive but clear
- Include technical specifics (file paths, line numbers, function names)
- Write for future you/agents who need full context
- Don't assume knowledge - explain decisions and reasoning
- Use markdown formatting for code references: `file.ts:lines`

## Example Entry

```markdown
## [2025-11-17 14:32] Entry 1: Initial Authentication System

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
  - **What we learned:** Never store sensitive tokens in localStorage, use httpOnly cookies instead
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

---
```

## When to Use Process-Notes vs README

### Use Process-Notes For:
- **The journey** - How we got here, what we tried, why we made decisions
- **Historical context** - What happened when, in chronological order
- **Learning from failures** - Dead ends, errors, what didn't work and why
- **Decision rationale** - Why we chose X over Y, alternatives considered
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
| **Just added OAuth authentication** | Yes - Document why we chose OAuth, what we tried first, implementation decisions | Yes - Update to show OAuth is now available, how to configure it | Both |
| **Debugged tricky issue for 2 hours** | Yes - Document the debugging journey, what we learned, the solution | No - Unless it changes how the project works or needs documentation | Process-Notes only |
| **Refactored file structure but behavior unchanged** | Maybe - If significant decisions were made about structure | Maybe - If file paths in docs need updating | Use judgment |
| **Added new feature (e.g., export to CSV)** | Yes - How we built it, libraries chosen, design decisions | Yes - Update features list, add usage example | Both |
| **Changed API endpoint structure** | Yes - Why we changed it, migration path, breaking change reasoning | Yes - Update API docs to reflect new structure | Both |
| **Fixed bug that restores documented behavior** | Maybe - Only if debugging revealed important insights | No - Behavior already documented correctly | Usually Process-Notes only |
| **Added environment variable** | Yes - Why we needed it, what we considered | Yes - Update configuration section | Both |
| **Spent time researching library options** | Yes - What we evaluated, pros/cons, final choice | No - Unless we actually added the library | Process-Notes only (until implementation) |
| **Reorganized code but kept same public API** | Maybe - If architectural decisions were made | No - Internal structure doesn't affect users | Usually Process-Notes only |
| **Context window approaching 90%** | Yes - Checkpoint current progress | No - Unless meaningful changes to document | Process-Notes only (checkpoint) |
| **Completed major milestone** | Yes - Document what we accomplished, decisions made | Maybe - If milestone adds/changes features | Process-Notes always, README if user-facing changes |

### Quick Decision Guide

**Update Process-Notes if:**
- We made a decision (any decision worth remembering)
- We hit a dead end or learned something
- Context window is getting full
- We completed work on something (even if not fully done)
- Future us needs to understand why we did something

**Update README if:**
- External behavior changed (how users interact with it)
- Features added or removed
- Installation/setup steps changed
- Configuration options changed
- Architecture changed in a way that affects understanding

**Update both if:**
- We added a new feature (process-notes: how/why, README: what it does)
- We made breaking changes (process-notes: migration reasoning, README: new API)
- We changed project structure in user-visible ways

**Update neither if:**
- Pure code cleanup with no behavioral change
- Minor bug fixes that restore documented behavior
- Internal refactoring invisible to users
- Just reading/researching (not implementing yet)

## Important Notes

- **Be comprehensive** - This is our project memory, capture everything important
- **Always include technical details** - File paths, line numbers, function names, error messages
- **Document the why** - Decisions and reasoning are more valuable than just what was done
- **Learn from failures** - Dead ends section is crucial for avoiding repeated mistakes
- **Provide context for next session** - Future agents need to pick up smoothly
- **Process-Notes is internal** - Written for us, not external users
- **Process-Notes is append-only** - Never delete history, always add to it
