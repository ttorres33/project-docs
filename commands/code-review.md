---
description: Review uncommitted code changes for consistency, quality, and maintainability
---

Use the `code-reviewer` agent to review all uncommitted changes in the current directory.

The agent will:
- Run `git diff` to see staged and unstaged changes
- Check consistency with ARCHITECTURE.md patterns
- Evaluate code quality and maintainability
- Flag any security concerns

Report the agent's findings back to the user.
