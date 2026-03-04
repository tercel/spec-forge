---
name: feature
description: >
  DEPRECATED: Feature spec generation has been merged into spec-forge:tech-design (Step 7).
  Use /spec-forge:tech-design instead — it generates both the architecture document and
  per-component feature specs in docs/features/ in a single pass.
instructions: >
  This skill has been merged into tech-design. Redirect the user:
  "Feature spec generation is now built into /spec-forge:tech-design (Step 7).
  Run /spec-forge:tech-design <name> to generate both the tech design and feature specs."
---

# Feature Spec — MERGED INTO TECH-DESIGN

This skill has been merged into `/spec-forge:tech-design` as **Step 7: Feature Spec Generation**.

Running `/spec-forge:tech-design <name>` now automatically:
1. Generates the architecture document at `docs/<name>/tech-design.md`
2. Generates per-component feature specs at `docs/features/{component}.md`
3. Generates the feature overview at `docs/features/overview.md`

There is no longer a need to run `/spec-forge:feature` separately.

If the user invokes this skill, inform them of the merge and suggest running `/spec-forge:tech-design` instead.
