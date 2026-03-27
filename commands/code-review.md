---
description: Review uncommitted code changes for consistency, quality, and maintainability
---

Use the `code-reviewer` agent to review all uncommitted changes in the current directory.

The agent will:
- Run `git diff` to see staged and unstaged changes
- Read README.md
- Read ARCHITECTURE.md
- Read test.md

### Check for Consistency
- Are the changes consistent with the project's ARCHITECTURE.md patterns
- Evaluate code quality and maintainabiltiy. 
- Is anything over-engineered?
- For AWS resources that need unique names across an account, is region added to the resource naem (e.g. s3 buckets, roles).

### Error Handling
Do a dedicated pass through all code changes evaluating error handling:
- Are all external calls (APIs, databases, file system) wrapped in error handling?
- What happens when each external call fails? Is there retry logic where appropriate?
- Is all function input verified? Is invalid input handled correctly?
- Are errors logged with enough context to diagnose problems later?
- Are error messages user-friendly where end users will see them?
- Highlight any gaps in error handling coverage.
- If specific errors are not caught, list them and weigh in on if this is appropriate.

### Test Coverage
- Does the project have a test.md document? Are all tests and testing patterns properly documented?
- Are there unit tests for new functions and modules?
- Are the unit tests testing the right things (not just testing that the code runs)?
- Are there integration tests? List all the ways the code might be used and check that there is an integration test for each path.
- If the project has test-deployed-*.sh scripts have they been updated?
- Flag any missing test coverage.

### Security
- **Dependency vulnerabilities** — Are any packages outdated? Are any package names hallucinated (don't actually exist in the registry)?
- **Secrets in code** — Are there any exposed API keys, passwords, tokens, or other credentials? Check .env.example files, config files, and code comments.
- **Least-privilege access** — Are IAM roles, API permissions, and database access scoped to only what's needed?
- **Input validation** — Is user input validated before being processed?
- **Logging hygiene** — Is any sensitive data (PII, tokens, passwords) being logged?
- **CORS configuration** — Is CORS properly restricted to known origins?
- **Package versions** — Verify all required packages exist and version floors are current.

### Documentation
- Does the README reflect the current code base?
- Does the ARCHITECTURE.md reflect the current code base?
- Does the test.md reflectt the current tests and test patterns?
- Is there a process-notes entry for this work? 


Report the agent's findings back to the user.
