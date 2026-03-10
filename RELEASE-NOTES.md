# Release Notes

## v0.12.2 — Skill Review & Consistency Fixes

**Release Date**: 2026-03-10

### Fixes

- **plugin.json keywords**: Added missing keywords for newer capabilities (idea, analyze, audit, feature specs, knowledge mapping, document analysis).
- **README.md**: Fixed idea status flow to include all 6 statuses (`exploring → researching → refining → ready → graduated`, plus `parked`). Fixed code-forge example paths to use component names instead of feature names.
- **generation-instructions.md**: Fixed `overview.md` generation instruction to "Create or update" (merge) instead of "Create" (overwrite), preventing data loss in multi-split projects.
- **tech-design SKILL.md**: Removed residual `/spec-forge:feature` references (command was deleted in v0.12.0).
- **Orchestrator**: Unified variable naming — `feature_name` → `argument` across all routes for consistency with the routing table.

---

## v0.12.0 — Feature Spec Ordering & No-Prefix Rule

**Release Date**: 2026-03-09

### Changes

- **Feature spec ordering enforced via `overview.md`**: The `#` column in `docs/features/overview.md` is now the single source of truth for execution order. Individual feature spec titles and filenames must NOT contain numeric IDs, order prefixes, or sequence numbers.
- **Anti-prefix rules**: Added explicit anti-shortcut rules prohibiting `01-`, `F-01`, or any numeric prefix in feature spec filenames and headings.

---

## v0.11.0 — Audit & Analyze Skills

**Release Date**: 2026-03-08

### New Features

- **`/spec-forge:audit [path]`**: Audit existing project documentation for quality, completeness, consistency, and code alignment. Cross-references docs against the actual codebase. Generates a severity-classified findings report (Critical/Major/Minor/Info) with actionable fix recommendations. Optionally applies fixes.
- **`/spec-forge:analyze [path]`**: Analyze a collection of documents as a body of knowledge. Builds a document map with type classification and theme clustering, detects conflicts and contradictions, identifies coverage gaps and redundancies, assesses staleness, and proposes reorganization. Designed for docs-only repos, cross-repo ecosystems, and research collections.
- **Dashboard updated**: `/spec-forge` (no arguments) now shows audit and analyze commands with usage tips.

---

## v0.10.0 — Rationale Requirements

**Release Date**: 2026-03-07

### Changes

- **Priority Rationale** (PRD, SRS): Every P0/P1/P2 assignment must include a rationale explaining why that tier was chosen. Bare priority labels without justification are flagged during quality check.
- **Threshold Rationale** (SRS): Every NFR target value must cite at least one concrete source (SLA, baseline data, benchmark, regulatory standard, or cost/complexity trade-off).
- **Pyramid Distribution Rationale** (Test Plan): Test pyramid split must reference project-specific factors, not just use a generic distribution.
- **Risk Reasoning** (Test Plan): Risk scores must include one-sentence justification for both likelihood and impact ratings.

---

## v0.9.0 — Streamlined Auto Chain & Feature Spec Generation

**Release Date**: 2026-02-28

### Breaking Changes

- **Auto chain simplified**: Default chain is now `Idea → Decompose → Tech Design + Feature Specs`. PRD, SRS, and Test Plan are on-demand documents, not part of the auto chain.
- **Command syntax**: All commands now use colon syntax (`/spec-forge:prd`, `/spec-forge:srs`, etc.).
- **Feature spec auto-generation**: Tech Design Step 7 automatically generates per-component feature specs in `docs/features/` and an `overview.md` with dependency graph and execution order.

### New Features

- **Idea-first mode for tech-design**: When an idea draft exists but no PRD/SRS, tech-design populates §3.5 User Scenarios, §3.6 Acceptance Criteria, and §3.7 Success Metrics from the idea draft, minimizing user questions.
- **Three operating modes**: Tech Design now supports Upstream mode (PRD/SRS found), Idea-first mode (idea draft found), and Standalone mode (no upstream docs).
- **Sub-agent architecture**: Generation steps are delegated to sub-agents with isolated context, keeping the main orchestrator lightweight.

---

## v0.8.0 — Ideas Directory Convention

**Release Date**: 2026-02-25

### Changes

- **`ideas/` at project root**: Ideas directory is now enforced at the project root (same level as `docs/`), never nested inside `docs/`.
- **`.gitignore` guidance**: First-run prompt asks whether to add `ideas/` to `.gitignore` (recommended for personal notes) or commit for team collaboration.

---

## v0.7.0 — Feature Specs & Overview

**Release Date**: 2026-02-22

### New Features

- **Per-component feature specs**: Tech Design now generates individual `docs/features/{component-name}.md` files with implementation-level detail (method signatures, logic steps, field mappings, state machines, error handling).
- **Feature overview**: `docs/features/overview.md` provides a feature index with dependency graph and execution order.
- **code-forge integration**: Feature specs are designed as direct input for `/code-forge:plan`.

---

## v0.6.0 — Project Decomposition

**Release Date**: 2026-02-18

### New Features

- **`/spec-forge:decompose <name>`**: Lightweight project decomposition skill. Analyzes scope through 3-5 rounds of interview questions and determines whether to treat the project as a single feature or split into multiple sub-features.
- **Project manifest**: For multi-split projects, generates `docs/project-{name}.md` with a machine-parseable `FEATURE_MANIFEST` block listing sub-features, dependencies, and execution order.
- **Split rationale**: Every verdict includes a formal rationale block citing which heuristics fired with project-specific evidence.
- **Multi-split chain execution**: `/spec-forge <name>` now handles multi-split projects by generating tech-design + feature specs for each sub-feature in dependency order.
- **Output path convention**: Migrated from `docs/{type}-{name}.md` to `docs/{name}/{type}.md` for better per-feature organization.

---

## v0.5.1 — Idea Validation Skill

**Release Date**: 2026-02-14

### New Features

- **`/spec-forge:idea <name>`**: Interactive, multi-session brainstorming and demand validation skill. Explores ideas through iterative sessions (Explore, Research, Validate, Refine), stores progress in `ideas/` directory, and graduates validated ideas into the spec chain.
- **Anti-pseudo-requirement principle**: Every idea must answer "What happens if we don't build this?" before graduating. Demand validation checklist requires evidence of real need.
- **Session persistence**: Each session saved as a separate file with chronological tracking in `sessions/overview.md`.
- **Competitive research**: Research sessions use WebSearch to analyze competitors, market demand, and user evidence.
- **Status lifecycle**: `exploring → researching → refining → ready → graduated` (plus `parked`).

---

## v0.5.0 — Rename to spec-forge + Standalone Mode

**Release Date**: 2025-02-09

### Breaking Changes

- **Renamed from `doc-lifecycle` to `spec-forge`**. Update your plugin installation accordingly.

### New Features

- **Standalone mode**: Each command now works independently without upstream documents. When no upstream PRD/SRS/Tech Design is found, the command asks additional clarification questions to compensate. No need to run the full chain.
- **Updated description**: Clearer positioning as a specification forging tool, not a document lifecycle manager.

### Upgrade Guide

```bash
/plugin uninstall doc-lifecycle
/plugin install tercel/spec-forge
```

---

## v0.1.0 — Initial Release

**Release Date**: 2025-01-01

### Overview

spec-forge (originally doc-lifecycle) is a Claude Code plugin that generates professional-grade software specifications at every stage of the development lifecycle, based on industry best practices from Google, Amazon, Stripe, IEEE, and ISTQB standards.

### Core Features

#### `/spec-forge:prd` — Product Requirements Document Generation
- 5-step workflow: context scanning → clarification → generation → quality check → output
- Market research & analysis (TAM/SAM/SOM) with source citations
- Anti-pseudo-requirement principle: every feature backed by evidence of real demand
- Competitive analysis (2+ competitors), user personas, user stories
- Feasibility analysis with honest GO / CONDITIONAL GO / NO-GO verdict
- Mermaid diagrams: user journeys, feature architecture, Gantt timeline
- Risk assessment matrix with likelihood/impact ratings
- Quality checklist validation

#### `/spec-forge:srs` — Software Requirements Specification Generation
- IEEE 830 / ISO/IEC/IEEE 29148 compliant structure
- Functional requirements (FR-MODULE-NNN) with actors, flows, acceptance criteria
- Non-functional requirements (NFR-CATEGORY-NNN) with metrics and targets
- CRUD matrix for data operations
- Upstream PRD auto-detection and traceability matrix
- Modal verb discipline: "shall" / "should" / "may"
- Quality checklist validation

#### `/spec-forge:tech-design` — Technical Design Document Generation
- C4 architecture diagrams (Context, Container, Component, Code)
- At least 2 alternative solutions with comparison matrix
- Complete parameter validation matrix for every API input
- Boundary value and edge case documentation
- Business logic specification: state machines, computation rules, conditional logic
- Error handling taxonomy with retry/circuit breaker configuration
- Database schema with ER diagram, index strategy, migration plan
- Security, performance, observability, and deployment design
- Quality checklist validation

#### `/spec-forge:test-plan` — Test Plan & Test Cases Generation
- IEEE 829 compliant test documentation
- Real database testing policy: NO mocks for DB operations
- Test case format (TC-MODULE-NNN) with exact DB state preconditions
- Modified test pyramid: pure unit → DB-touching unit → integration → system → acceptance
- Data integrity test cases: unique constraints, FK constraints, cascades, transactions
- Concrete test data (no placeholders), DB state verification in expected results
- Entry/exit criteria, defect severity classification
- Quality checklist validation

### Document Traceability

Full bidirectional traceability across all document types:
```
PRD (PRD-ID) → SRS (FR/NFR-ID) → Tech Design (Component/API) → Test Plan (TC-ID) → Feature Spec (code-forge input)
```

### Standards Referenced
- Google PRD, Amazon Working Backwards (PR/FAQ), Stripe Product Spec
- IEEE 830 (SRS), IEEE 829 (Test Plans)
- ISO/IEC/IEEE 29148
- ISTQB Test Standards
- Google Testing Blog
- Google Design Doc, RFC Template, Uber/Meta Engineering Standards
