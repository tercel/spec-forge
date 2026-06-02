---
name: spec-forge
description: >
  Professional specification system for Codex. Use when the user asks to create,
  improve, review, audit, analyze, or propagate product/software documentation,
  including ideas, PRDs, SRS documents, technical designs, architecture/RFC docs,
  feature specs, test cases, documentation audits, document landscape analysis,
  and full idea-to-spec chains. Supports complex multi-skill orchestration:
  idea -> decompose -> tech-design + feature specs -> review, with optional PRD,
  SRS, test-cases, audit, analyze, and propagate workflows.
version: 1.0
subcommands:
  - idea
  - decompose
  - tech-design
  - prd
  - srs
  - test-cases
  - review
  - audit
  - analyze
  - propagate
---

# Spec-Forge Orchestrator

Spec-forge is a documentation and specification workflow suite. This root skill is
the Codex-facing orchestrator: decide which child skill to load, keep the document
chain coherent, and avoid loading large generation references until they are needed.

## Trigger Patterns

Use this skill when the user asks for any of the following:

- Start or refine an idea before specs: use `skills/idea/SKILL.md`
- Split a large project into sub-features: use `skills/decompose/SKILL.md`
- Write a PRD or product requirements document: use `skills/prd-generation/SKILL.md`
- Write an SRS, requirements spec, or functional/non-functional requirements: use `skills/srs-generation/SKILL.md`
- Write a technical design, architecture doc, design doc, or RFC: use `skills/tech-design-generation/SKILL.md`
- Generate test cases, QA coverage, or a test case matrix: use `skills/test-cases-generation/SKILL.md`
- Review spec-forge documents for quality and consistency: use `skills/review/SKILL.md`
- Audit project docs against code: use `skills/audit/SKILL.md`
- Analyze a document ecosystem for themes, conflicts, gaps, redundancy, or staleness: use `skills/analyze/SKILL.md`
- Propagate an upstream doc change downstream: use `skills/propagate/SKILL.md`
- Run the full chain for a feature: orchestrate `idea -> decompose -> tech-design -> review`

Also treat slash-like requests as aliases:

| User request | Route |
|---|---|
| `/spec-forge <name>` | Full chain |
| `/spec-forge:idea <name>` or `/idea <name>` | Idea |
| `/spec-forge:decompose <name>` or `/decompose <name>` | Decompose |
| `/spec-forge:tech-design <name>` or `/tech-design <name>` | Tech Design |
| `/spec-forge:prd <name>` or `/prd <name>` | PRD |
| `/spec-forge:srs <name>` or `/srs <name>` | SRS |
| `/spec-forge:test-cases <target>` or `/test-cases <target>` | Test Cases |
| `/spec-forge:review <name>` or `/review <name>` | Review |
| `/spec-forge:audit [path]` or `/audit [path]` | Audit |
| `/spec-forge:analyze [path]` or `/analyze [path]` | Analyze |
| `/spec-forge:propagate ...` or `/propagate ...` | Propagate |

The `commands/*.md` files are compatibility command definitions from the original
Claude-oriented implementation. In Codex, prefer reading the child `skills/*/SKILL.md`
files directly. Use `commands/spec-forge.md` only as an additional orchestration
reference if you need more detail about the full chain.

## Progressive Loading

Keep context small.

1. Read this root file first.
2. Read only the child `SKILL.md` matching the user's request.
3. When a child skill references `skills/shared/project-context.md`, read it if the workflow needs code/project awareness.
4. When a child skill references `skills/shared/doc-first.md`, apply it before generating or editing docs.
5. Read generation references, templates, or checklists only when that child skill explicitly needs them.

Do not bulk-load every child skill. Do not read every reference folder just because
the suite is complex.

## Global Rules

- Preserve the user's requested language. If the user writes in Chinese, respond and write user-facing explanations in Chinese unless the target document convention requires English.
- Treat docs as current truth, not history. Before generating a new spec, scan for existing related docs and decide whether to reuse, edit, or create.
- Do not create parallel versions such as `prd-v2.md`, `new-tech-design.md`, or addendum files. Edit the canonical file in place unless no canonical document exists.
- Keep traceability stable: preserve existing requirement IDs, feature names, component names, and section titles unless the user explicitly asks to rename them.
- When changing upstream docs, identify downstream impact. Either update affected downstream docs or recommend/run the propagate workflow.
- Every finding in review, audit, analyze, or propagate output must cite concrete files/sections. Do not invent issues.
- Prefer project-local conventions and existing docs over generic templates.
- Ask only necessary questions. If existing docs or code provide the answer, use them and state the assumption.

## Shared Project Context

For generation workflows that need grounding in the actual codebase, use:

`skills/shared/project-context.md`

Apply it before PRD, SRS, tech-design, decompose, and test-cases work when the
project exists. It produces a concise summary of:

- Project profile
- Language, framework, database, auth, testing, and CI signals
- Existing documents and upstream specs
- Architecture and module boundaries
- Existing test infrastructure when relevant

For the full chain, scan project context once and reuse the summary across stages
instead of repeatedly rescanning the same repository.

## Document Discipline

For any document creation or edit, apply:

`skills/shared/doc-first.md`

Minimum pre-write checklist:

1. List relevant existing docs under `docs/`, `specs/`, `design/`, `architecture/`, `ideas/`, and the project root.
2. Grep for the feature name, domain terms, requirement IDs, component names, and aliases.
3. Decide for each topic: reuse existing content, extend existing content, or create new content.
4. Preserve stable IDs and terminology.
5. Note downstream docs that will need updates.

## Full Chain

When the user asks for `/spec-forge <name>` or "run the full spec-forge chain",
execute this sequence:

1. **Idea**: Use `skills/idea/SKILL.md`.
   - Goal: validate demand and produce `ideas/{name}/draft.md`.
   - If a ready or graduated idea already exists, reuse it.
   - If the idea is still exploring/refining, warn the user before continuing.

2. **Decompose**: Use `skills/decompose/SKILL.md`.
   - Goal: decide single feature vs multi-split project.
   - Multi-split output: `docs/project-{name}.md` with a first-line `FEATURE_MANIFEST` block.

3. **Tech Design + Feature Specs**: Use `skills/tech-design-generation/SKILL.md`.
   - Single feature output: `docs/{name}/tech-design.md`.
   - Multi-split output: one tech design per sub-feature.
   - The tech-design workflow also generates implementation-facing feature specs under `docs/features/`.
   - If `ideas/{name}/draft.md` exists, use it for user scenarios, acceptance criteria, success metrics, scope, and goals.

4. **Review**: Use `skills/review/SKILL.md`.
   - Review generated tech designs and `docs/features/*.md`.
   - Auto-fix only where the review skill permits it.
   - Leave review comments where domain knowledge is missing.

PRD, SRS, and test cases are optional on-demand outputs, not required stages in
the default full chain.

## Single-Skill Routes

### Idea

Read `skills/idea/SKILL.md`.

Use for early exploration, demand validation, competitive research, and
anti-pseudo-requirement checks. Output lives in top-level `ideas/{idea-name}/`,
not under `docs/`.

### Decompose

Read `skills/decompose/SKILL.md`.

Use for deciding whether a project is one feature or several independently
specifiable sub-features. If multi-split, generate `docs/project-{name}.md`.

### PRD

Read `skills/prd-generation/SKILL.md`.

Use for product requirements, stakeholder alignment, product strategy, market
context, personas, user stories, priorities, success metrics, and timelines.

### SRS

Read `skills/srs-generation/SKILL.md`.

Use for formal functional/non-functional requirements, requirement IDs,
interfaces, data requirements, acceptance criteria, and traceability matrices.

### Tech Design

Read `skills/tech-design-generation/SKILL.md`.

Use for architecture/design docs, RFCs, API design, data model design,
deployment, observability, security, performance, alternatives, and generated
feature specs.

### Test Cases

Read `skills/test-cases-generation/SKILL.md`.

Use for test case generation, coverage matrices, test strategy, testable unit
extraction, and code/spec-driven QA planning. Honor `--formal` when requested.

### Review

Read `skills/review/SKILL.md`.

Use after spec generation to check completeness, specificity, internal
consistency, traceability, and actionability. Findings first; fixes only where
allowed.

### Audit

Read `skills/audit/SKILL.md`.

Use when auditing one project that has docs and code. It checks documentation
quality, completeness, consistency, staleness, and alignment with the codebase.

### Analyze

Read `skills/analyze/SKILL.md`.

Use for docs-only or cross-repo document landscapes. It maps themes, conflicts,
gaps, redundancies, and stale areas without assuming a single codebase.

### Propagate

Read `skills/propagate/SKILL.md`.

Use after upstream document changes. It finds downstream docs affected by changed
concepts and updates them surgically or reports unresolved stale references.

## Output Locations

Default locations:

- Ideas: `ideas/{name}/`
- PRD: `docs/{name}/prd.md`
- SRS: `docs/{name}/srs.md`
- Tech design: `docs/{name}/tech-design.md`
- Feature specs: `docs/features/*.md`
- Test cases: `docs/{name}/test-cases.md` or the path specified by the child skill
- Project manifest: `docs/project-{name}.md`
- Audit report: `{target-docs-path}/audit-report.md`
- Analysis report: `{target-root}/analysis-report.md`

If existing project conventions differ, follow the existing convention and state
the location you used.

## Completion Criteria

Before finishing a spec-forge task:

- Confirm the requested document or report exists, or explain why it could not be written.
- Mention the exact files changed or generated.
- For generation tasks, note whether project context and existing docs were scanned.
- For review/audit/analyze tasks, summarize findings by severity and cite the report path.
- For chain tasks, summarize which stages completed and which optional stages remain.
