---
description: Document an A/B test with variants, hypothesis, and measurement plan
arguments: <test-name> [file-path]
---

Invoke the `ab-test` skill to document an A/B test interactively.

Arguments:
- `test-name` (required): Name of the A/B test (used as document title and default filename)
- `file-path` (optional): Where to save the document. Defaults to `./{test-name}.md`

Walk through each section one question at a time, capturing:
- Test date
- Hypothesis
- Control and treatment variants (name + description each)
- How test and control groups are created (audience segmentation, randomization, etc.)
- How success will be measured
- Results timeline
- Results and conclusions (for updates)

If the file exists, show current content and ask about updates for each section.
