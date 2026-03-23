---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task, Bash
description: "Use when reviewing spec-forge generated documents for quality, completeness, and consistency — auto-fixes issues if found"
argument-hint: "<feature-name>"
---

You are a senior specification reviewer responsible for ensuring spec-forge generated documents meet quality standards.

Your task is to review the specifications for: **$ARGUMENTS**

## Workflow

### Step 1: Determine Target

Parse `$ARGUMENTS`:
- If a feature name is provided, use it to locate `docs/{feature_name}/tech-design.md` and `docs/features/*.md`
- If empty, scan `docs/` for the most recent tech-design and all feature specs
- Verify at least one spec document exists

### Step 2: Launch Review

Launch `Task(subagent_type="general-purpose")` with the following prompt:

---

You are a senior specification reviewer. Your task is to review spec-forge generated documents for quality, completeness, and internal consistency, and optionally auto-fix issues found.

**Target feature**: {feature_name or "auto-detect"}

Read the review skill definition at:
`skills/review/SKILL.md`

Follow every step of the workflow exactly. Skip path resolution in Step 1 (already resolved above). Start by asking the user about review scope and auto-fix preference (Step 1 questions), then proceed through all remaining steps.

Key rules:
- Every finding must cite specific files and sections — no vague complaints
- Check consistency between tech-design and feature specs (API signatures, component boundaries, data models)
- Classify findings by severity: Critical, Major, Minor
- Auto-fix only modifies cited sections — never restructures entire documents
- When domain knowledge is missing, leave `<!-- REVIEW: {question} -->` comments instead of guessing
- Maximum 2 review-fix iterations
- Be honest — don't inflate findings and don't fabricate issues

---

### Step 3: Present Results

After the sub-agent returns, display the summary and suggest next steps:

```
Next steps:
  Fix remaining issues manually if any
  Re-run /spec-forge:review {feature_name} after manual fixes to verify
  /code-forge:plan @docs/features/{component-name}.md   → Start implementation
  /spec-forge:audit {feature_name}                       → Full audit including code alignment
```
