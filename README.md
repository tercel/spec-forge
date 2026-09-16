# spec-forge

**Professional Software Specification Generator for Claude Code**

Generate industry-standard specifications — from early-stage brainstorming to Technical Design with auto-generated feature specs — each usable standalone or as part of a streamlined auto chain.

## Overview

Software projects need clear specifications. spec-forge covers the journey from idea to implementation-ready documents, with one thing at its centre: **a requirements specification precise enough to hand to an implementation team and settle acceptance against.**

| Command | Description | Standards |
|---------|-------------|-----------|
| `/spec-forge:srs <name>` | **Software Requirements Specification — the delivery contract** | IEEE 830, ISO/IEC/IEEE 29148 |
| `/spec-forge:tech-design <name>` | Technical Design Document + auto-generated feature specs | Google Design Doc, RFC Template |
| `/spec-forge <name>` | **Full chain** — `[Idea] → [Decompose] → [PRD] → SRS → Tech Design → Review` | All of the above |
| `/spec-forge:prd <name>` | Product Requirements Document — the business case (conditional) | Google PRD, Amazon PR/FAQ |
| `/spec-forge:idea <name>` | Interactive brainstorming — explore and refine ideas | — |
| `/spec-forge:decompose <name>` | Decompose project into sub-features | — |
| `/spec-forge:review <name>` | Review generated specs for quality & consistency, auto-fix issues | — |
| `/spec-forge:test-cases <name>` | Test Cases with coverage matrix (on-demand) | Multi-dimensional coverage |
| `/spec-forge:audit [path]` | Audit docs for quality, completeness & code alignment | — |
| `/spec-forge:analyze [path]` | Analyze document collection — map themes, find conflicts & gaps | — |

**Aliases**: `/prd`, `/srs`, `/tech-design`, `/test-cases`, `/idea`, `/decompose`, `/review`, `/audit`, `/analyze` work as shortcuts — they invoke each skill directly, bypassing the `/spec-forge` orchestrator.

## Features

- **Delivery-grade requirements**: The SRS is written to be handed to an implementation team — explicit scope boundaries, field-level input rules, state machines with illegal-transition handling, permission matrix, error catalogue with degradation behavior, and acceptance and change control
- **Idea to Spec**: Brainstorm interactively, then graduate ideas into requirements, architecture docs, and feature specs
- **Full Chain Mode**: One command runs `[Idea] → [Decompose] → [PRD] → SRS → Tech Design → Review`, then hands off to code-forge
- **Standalone or Chained**: Use any command on its own, or run the full chain for traceability
- **Industry Standards**: Templates grounded in Google, Amazon, Stripe, IEEE, and ISTQB best practices
- **Automatic Context Scanning**: Scans your project structure, README, and existing docs before generation
- **Project Decomposition**: Automatically analyzes scope and splits large projects into sub-features
- **Smart Upstream Detection**: Finds upstream documents when available; asks compensating questions when not
- **Quality Checklists**: Built-in 4-tier validation (completeness, quality, consistency, formatting)
- **Mermaid Diagrams**: Architecture, sequence, user journey, and Gantt diagrams
- **Spec Review**: Review generated specs for completeness, consistency, and actionability with auto-fix
- **Documentation Audit**: Cross-reference docs against code for quality, completeness, and consistency
- **Document Landscape Analysis**: Map, cluster, and evaluate document ecosystems

## Commands

### `/spec-forge:idea <name>` — Brainstorming

Interactive, multi-session brainstorming for early-stage ideas:

- **Iterative**: Explore an idea across multiple sessions, days apart
- **Persistent**: Sessions stored in `ideas/` directory (add to `.gitignore` or commit for team use)
- **Graduated**: When an idea is ready, it flows into the spec chain seamlessly

```bash
/spec-forge:idea cool-feature       # Start or resume brainstorming
/spec-forge:idea                    # List all ideas
```

Status flow: `exploring` → `researching` → `refining` → `ready` → `graduated` (or `parked` at any stage)

### `/spec-forge <name>` — Full Chain

Run the streamlined specification chain in one command:

```bash
/spec-forge user-login              # Auto: [Idea] → [Decompose] → [PRD] → SRS → Tech Design → Review
```

- Detects existing documents and resumes from where you left off
- Idea stage is interactive; Tech Design minimizes questions when idea draft exists
- Auto-generates per-component feature specs in `docs/features/` (Step 7 of tech-design)
- If an idea draft exists in `ideas/`, uses it as requirements context

### `/spec-forge:decompose <name>` — Project Decomposition

Analyze project scope and split into sub-features if needed:

```bash
/spec-forge:decompose my-project     # Interview → split analysis → manifest
```

- Lightweight 3-5 round interview focused on scope boundaries
- Generates `docs/project-{name}.md` manifest for multi-split projects
- Automatically invoked as Stage 2 when running `/spec-forge <name>` full chain (after Idea, before Tech Design)

### `/spec-forge:srs <name>` — the delivery contract

**This is the document you hand to whoever builds it.** It is the mandatory spine of the chain, and what acceptance is settled against.

- Functional requirements with structured IDs (FR-XXX-NNN) — main flow, alternative flows, preconditions, postconditions
- **Scope boundaries** with an explicit out-of-scope table — ambiguity about what is *not* included is the most common source of delivery disputes
- **Input field rules** per requirement — type, required, exact constraints, default, boundary/rejection behavior. "Max 254 characters", never "reasonable length"
- **State machines** including illegal-transition handling — specifying only the legal transitions leaves the implementer to invent the rest
- **Permission matrix** — role × operation × data scope, with the 403-vs-404 denial behavior stated as a deliberate security decision
- **Error catalogue** — every anticipated failure as a distinct diagnosable code, plus the degradation behavior for each dependency
- Non-functional requirements (NFR-XXX-NNN) with target, measurement method, **verification method**, and threshold rationale
- Machine-verifiable acceptance criteria in Given/When/Then form
- Data model, data dictionary, and external interface requirements
- **Acceptance and change control** — what acceptance means, in which environment, and how the contract may change
- Requirements traceability matrix (PRD → SRS, when a PRD exists)

**Standalone**: When no upstream PRD is found, asks additional questions to compensate.

**Reference**: IEEE 830, ISO/IEC/IEEE 29148, Amazon Technical Specifications

### `/spec-forge:prd <name>` — the business case

Answers *is this worth building*, for whom, at what priority. A decision document read before commitment — **conditional**, not every project needs one.

- Problem statement and product vision
- Market research, competitive landscape, and demand validation (anti-pseudo-requirement)
- Feasibility analysis with an honest GO / CONDITIONAL GO / NO-GO verdict
- User personas and user stories
- Capability scope with P0/P1/P2 prioritization and priority rationale
- Success metrics (KPI/OKR)
- User journey maps (Mermaid)
- Timeline and milestones (Mermaid Gantt)
- Risk assessment matrix

**Run it** for a new product, or when a go/no-go decision, budget approval, or stakeholder alignment is still outstanding. **Skip it** when the decision to build is already made — go straight to the SRS. A PRD written after the decision is ceremony.

**Deliberately not in the PRD**: field-level rules, state machines, error codes, Given/When/Then acceptance criteria, solution architecture. Those belong to the SRS and tech design — duplicating them creates two sources of truth that drift on the first requirement change.

**Reference**: Google PRD, Amazon Working Backwards (PR/FAQ), Stripe Product Spec

### `/spec-forge:tech-design <name>`

Generates a Technical Design Document including:
- C4 architecture diagrams (Context, Container, Component)
- Alternative solution comparison matrix
- API design (RESTful / GraphQL / gRPC)
- Database schema and migration strategy
- Security, performance, and observability design
- Deployment and rollback strategy

**SRS-first**: Reads `docs/<name>/srs.md` as the authoritative requirements source. Every component names the FR/NFR requirements it satisfies, and every requirement is satisfied by at least one component — unplaced requirements are reported rather than silently dropped. Falls back to asking compensating questions when no upstream SRS exists.

**Reference**: Google Design Doc, RFC Template, Uber/Meta Engineering Standards

### `/spec-forge:test-cases <name>`

Generates structured test cases with multi-dimensional coverage:
- Auto-scans project to extract testable units (APIs, functions, components, CLI commands, tools)
- Detects project profile (Web API, CLI, Frontend, AI Agent, etc.) and adapts output
- Multi-dimensional coverage: L1 (Happy Path) + L2 (Boundary/Error) + L3 (Negative)
- Coverage matrix with gap analysis
- Test strategy and methodology (default); `--formal` adds management sections (environment, roles, schedule)
- Downstream integration: output consumed by `/code-forge:tdd @test-cases.md`

### `/spec-forge:review <name>` — Spec Review

Review generated specifications for quality, completeness, and internal consistency:

```bash
/spec-forge:review user-login          # Review all specs for user-login
```

- Checks completeness, internal consistency, specificity, traceability, and actionability
- Compares feature specs against tech-design for API signature and component boundary alignment
- Auto-fixes Critical and Major issues (up to 2 review-fix iterations)
- Leaves `<!-- REVIEW: ... -->` comments when domain knowledge is needed for a fix
- Automatically runs as Stage 4 in the full chain (`/spec-forge <name>`)

**Best for**: After generating specs, before starting implementation.

### `/spec-forge:audit [path]` — Documentation Audit

Audit existing project documentation for quality, completeness, and code alignment:

```bash
/spec-forge:audit                          # Audit current project's docs
/spec-forge:audit ../../other-project      # Audit another project
```

- Cross-references docs against the actual codebase (API surfaces, features, architecture)
- Checks internal consistency between documents (terminology, facts, versions)
- Evaluates quality dimensions (completeness, accuracy, clarity, currency)
- Generates a findings report with severity levels (Critical/Major/Minor/Info)
- Optionally applies fixes to resolved findings

**Best for**: Single projects with both documentation and source code.

### `/spec-forge:analyze [path]` — Document Landscape Analysis

Analyze a collection of documents to understand the knowledge landscape:

```bash
/spec-forge:analyze ../../aipartnerup-docs  # Analyze a docs-only repo
/spec-forge:analyze                         # Analyze current project's docs/
```

- Builds a document map with type classification and theme clustering
- Detects conflicts and contradictions between documents
- Identifies coverage gaps and missing documentation
- Finds redundancies and near-duplicate content
- Assesses document staleness from content signals
- Proposes reorganization when structure can be improved

**Best for**: Document ecosystems, cross-repo docs, research collections, mixed-format doc repos.

## Complete Workflow

```
/spec-forge:idea cool-feature              # Brainstorm (iterative, multi-session)
    ↓ (graduated)
/spec-forge cool-feature                   # [Idea] → [Decompose] → [PRD] → SRS → Tech Design → Review
    ↓
/code-forge:plan @docs/features/           # Break into tasks and execute
```

**Quick path** (decision already made, skip idea and PRD):
```
/spec-forge:srs cool-feature               # The delivery contract
/spec-forge:tech-design cool-feature       # Tech Design + auto-generated feature specs
/spec-forge:review cool-feature            # Review before implementation
/code-forge:plan @docs/features/           # Generate implementation plan
```

**Handing work to an implementation team or vendor**: give them `docs/<name>/srs.md`. It carries the scope boundaries, the field rules, the acceptance criteria, and the change procedure. Keep `prd.md` internal — it contains go/no-go reasoning and market analysis that is not theirs to act on.

### Document Traceability

The chain is two levels of one traceability chain, not competing numbering schemes. `PRD-*-NNN` identifies a **business capability** (a scope-and-priority decision); `FR-*-NNN` identifies a **system behavior** (the delivery contract). The relationship is one-to-many.

```
[Idea Draft]  ──→  [PRD]      ──→   SRS        ──→  Tech Design  ──→  Feature Specs
ideas/<name>/      docs/<name>/     docs/<name>/    docs/<name>/      docs/features/
  draft.md           prd.md           srs.md         tech-design.md     *.md
                   PRD-MOD-NNN      FR-MOD-NNN       components         auto-generated
demand             capabilities     system behavior  trace to           in Step 7
validation         + priority       + acceptance     FR/NFR IDs
                                                          ↓
                                          /code-forge:plan @docs/features/
```

Brackets mark conditional stages. The SRS and tech design are not optional: skipping the SRS to reach the design faster produces a design resting on unstated requirements, and code whose correctness nobody can settle.

**Coverage is checked, not assumed**: `sf-trace.py matrix --upstream prd.md --downstream srs.md` reports PRD capabilities with no requirement covering them and SRS references to PRD IDs that do not exist. The same check runs from SRS to tech design.

## Output

Each feature gets its own directory under `docs/`:
- `docs/<feature-name>/srs.md` — **the delivery contract** (always generated by the chain)
- `docs/<feature-name>/tech-design.md` — architecture and design (always generated by the chain)
- `docs/<feature-name>/prd.md` — business case (conditional; generated when a go/no-go decision is still open)

Auto-generated feature specs go to `docs/features/`:
- `docs/features/overview.md` (feature index + dependency graph)
- `docs/features/<component-name>.md` (per-component implementation spec)

On-demand documents (when explicitly requested):
- `docs/<feature-name>/test-cases.md` — a standalone QA coverage matrix. Not part of the chain: tests are derived from the SRS acceptance criteria by `code-forge:tdd`. spec-forge owns requirements and design; code-forge owns implementation and verification.

For decomposed projects, a manifest is also generated:
- `docs/project-<project-name>.md`

Brainstorming ideas are stored in the project's `ideas/` directory. Add `ideas/` to `.gitignore` to keep them private, or commit for team collaboration.

## Works Great With

**[code-forge](https://github.com/tercel/code-forge)** — spec-forge handles upstream specification (what to build and why), code-forge handles downstream execution (how to build it and ship it).

**spec-forge works perfectly standalone — code-forge is optional.**

If code-forge is not installed, each command's "Next Steps" section provides general guidance for moving forward with implementation.

## Installation

### Claude Code (via Plugin Marketplace)

```bash
/plugin install tercel/spec-forge
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md)

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md)

## License

MIT License
