---
description: Review the current plan for consistency, duplicates, and complexity
---

Use the `plan-reviewer` agent to review the current plan document.

The plan document is located at `.claude/plans/` in the project directory. Find the most recent plan file and pass it to the plan-reviewer agent for review.

The agent will check:
- Consistency with project architecture and patterns
- Potential duplicates in the codebase
- Unnecessary complexity that could be simplified

Report the agent's findings back to the user.
