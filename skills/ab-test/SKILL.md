---
name: ab-test
description: Documents A/B tests with variants, hypothesis, measurement plan, and conclusions. Use when the user mentions running an A/B test, comparing two variants, or wanting to measure/test something systematically.
allowed-tools: Read, Edit, Write, Glob, AskUserQuestion
---

# A/B Test Documentation Skill

## Purpose
Create and maintain structured documentation for A/B tests, capturing the hypothesis, variants, measurement approach, timeline, results, and conclusions. This ensures tests are properly documented and learnings are preserved.

## When to Use

Invoke this skill when any of these conditions occur:

1. **User mentions running an A/B test** - "I'm running an A/B test on...", "We're testing two versions..."
2. **User is comparing variants** - "Should we try A or B?", "I want to compare these two approaches..."
3. **User wants to measure something** - "How do we know which is better?", "I want to test if this works..."
4. **Explicit user request** - When user invokes `/project-docs:ab-test` command

## How to Document an A/B Test

### Arguments
- `test-name` (required): Name of the A/B test (used as document title and default filename)
- `file-path` (optional): Where to save the document. Defaults to `./{test-name}.md` in current working directory

### Workflow

1. **Determine file path:**
   - If file path provided, use it
   - Otherwise, create `./{test-name}.md` in current working directory
   - Sanitize test name for filename (lowercase, replace spaces with hyphens)

2. **Check if file exists:**
   - If file exists, read current content and present to user
   - Walk through updating each section
   - If new file, start fresh with all sections

3. **Walk through each section interactively:**

   Ask questions one at a time, waiting for the user's response before moving to the next question.

   **For new tests:**
   - "When does/did this test start?" (Test Date)
   - "What's your hypothesis? What do you expect to happen and why?" (Hypothesis)
   - "What's the name of your control variant (the existing/baseline)?"
   - "Describe the control variant:"
   - "What's the name of your treatment variant (the new/experimental)?"
   - "Describe the treatment variant:"
   - "How are users assigned to test vs control groups?" (Group Assignment - audience segmentation, randomization method, percentage split, etc.)
   - "How will you measure success? What metrics matter?" (Measurement)
   - "When will you evaluate the results?" (Results Timeline)

   **For existing tests (updating):**
   - Show current content for each section
   - Ask "Do you want to update this section?" for each
   - Focus especially on Results and Conclusions sections:
     - "What were the actual results?"
     - "What conclusions did you draw? What's the decision?"

4. **Write the document** using the format below

## Document Format

```markdown
# A/B Test: {test-name}

## Test Date
{when the test started/starts}

## Hypothesis
{what we expect to happen and why}

## Variants

### Control: {control-name}
{control description}

### Treatment: {treatment-name}
{treatment description}

## Group Assignment
{how users are assigned to control vs treatment - randomization, segmentation, percentage split}

## Measurement
{how success will be measured, what metrics}

## Results Timeline
{when results will be evaluated}

## Results
{actual results - may be empty initially}

## Conclusions
{what we learned, decision made - may be empty initially}
```

## Guidelines

### Test Date
- Be specific: "2025-01-15" or "Week of January 15, 2025"
- Can include end date if known: "January 15-29, 2025"

### Hypothesis
- State clearly what you expect to happen
- Include the "why" - the reasoning behind the expectation
- Example: "We expect the larger CTA button to increase click-through rate by 10-15% because it will be more visually prominent and easier to tap on mobile."

### Variants
- **Control**: The existing behavior or baseline
- **Treatment**: The new approach being tested
- Describe each variant clearly enough that someone could recreate it
- Include relevant details: copy, design, behavior, etc.

### Group Assignment
- How are users randomly assigned?
- What's the percentage split? (e.g., 50/50, 90/10)
- Any audience segmentation or targeting criteria?
- How is consistency maintained (same user always sees same variant)?
- Example: "50/50 random split using Optimizely. Users assigned by cookie on first visit. Only including users from US and Canada."

### Measurement
- Specify the primary metric
- List any secondary metrics
- Define how you'll collect the data
- Note sample size requirements if relevant
- Example: "Primary: Click-through rate on CTA. Secondary: Time on page, bounce rate. Measured via Google Analytics events."

### Results Timeline
- When will you have enough data to decide?
- What's the minimum sample size needed?
- Include planned review date
- Example: "Review after 2 weeks or 1,000 visitors per variant, whichever comes first. Planned review: January 29, 2025."

### Results
- Record actual data observed
- Include confidence intervals if relevant
- Note any unexpected observations
- Can be updated multiple times as data comes in

### Conclusions
- What did you learn?
- What decision was made?
- What will you do next?
- Any follow-up tests needed?

## Example Document

```markdown
# A/B Test: Homepage CTA Button Size

## Test Date
January 15, 2025

## Hypothesis
We expect the larger CTA button (treatment) to increase click-through rate by 10-15% because it will be more visually prominent and easier to tap on mobile devices, where 60% of our traffic comes from.

## Variants

### Control: Standard Button
- Size: 120x40px
- Text: "Get Started"
- Color: Blue (#0066CC)
- Current conversion rate: 3.2%

### Treatment: Large Button
- Size: 160x56px
- Text: "Get Started Free"
- Color: Blue (#0066CC) with subtle gradient
- Added micro-copy below: "No credit card required"

## Group Assignment
- 50/50 random split
- Assignment via Optimizely, cookie-based on first homepage visit
- All traffic included (no geographic or device filtering)
- Users see consistent variant across sessions

## Measurement
Primary metric: Click-through rate on homepage CTA
Secondary metrics:
- Signup completion rate
- Time to first click
- Mobile vs desktop CTR difference

Data collection: Google Analytics events + Mixpanel funnel

## Results Timeline
Review after 2 weeks or 5,000 visitors per variant.
Planned review date: January 29, 2025
Statistical significance threshold: 95%

## Results
After 2 weeks (5,200 visitors per variant):
- Control CTR: 3.2%
- Treatment CTR: 4.1%
- Lift: 28% (p < 0.01)
- Mobile lift was higher (35%) than desktop (18%)

## Conclusions
The larger button significantly outperformed the control. The "No credit card required" micro-copy likely contributed to the lift beyond just size.

Decision: Roll out the larger button to 100% of traffic.

Follow-up test: Test the micro-copy separately to isolate its effect.
```

## Important Notes

- **Ask questions one at a time** - Don't overwhelm the user with all questions at once
- **For updates, show current content** - Let users see what's there before deciding to change
- **Results and Conclusions can be empty initially** - Tests are often documented before they complete
- **Preserve the structure** - Keep all sections even if some are empty (use "TBD" or "Pending")
- **Be specific** - Vague tests lead to vague conclusions
