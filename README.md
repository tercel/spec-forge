# spec-forge

**Professional Software Specification Generator for Claude Code**

Generate industry-standard specifications — from early-stage brainstorming to Technical Design with auto-generated feature specs — each usable standalone or as part of a streamlined auto chain.

## Overview

Software projects need clear specifications. spec-forge covers the full journey from idea to implementation-ready documents:

| Command | Description | Standards |
|---------|-------------|-----------|
| `/spec-forge:idea <name>` | Interactive brainstorming — explore and refine ideas | — |
| `/spec-forge:decompose <name>` | Decompose project into sub-features | — |
| `/spec-forge:tech-design <name>` | Technical Design Document + auto-generated feature specs | Google Design Doc, RFC Template |
| `/spec-forge <name>` | **Full chain** — auto-run Idea → Decompose → Tech Design + Feature Specs | All of the above |
| `/spec-forge:prd <name>` | Product Requirements Document (on-demand) | Google PRD, Amazon PR/FAQ |
| `/spec-forge:srs <name>` | Software Requirements Specification (on-demand) | IEEE 830, ISO/IEC/IEEE 29148 |
| `/spec-forge:test-plan <name>` | Test Plan & Test Cases (on-demand) | IEEE 829, ISTQB |
| `/spec-forge:audit [path]` | Audit docs for quality, completeness & code alignment | — |
| `/spec-forge:analyze [path]` | Analyze document collection — map themes, find conflicts & gaps | — |

**Aliases**: `/prd`, `/srs`, `/tech-design`, `/test-plan`, `/idea`, `/decompose`, `/audit`, `/analyze` work as shortcuts — they invoke each skill directly, bypassing the `/spec-forge` orchestrator.

## Features

- **Idea to Spec**: Brainstorm interactively, then graduate ideas into architecture docs + feature specs
- **Full Chain Mode**: One command runs the streamlined chain (Idea → Decompose → Tech Design + Feature Specs)
- **Standalone or Chained**: Use any command on its own, or run the full chain for traceability
- **Industry Standards**: Templates grounded in Google, Amazon, Stripe, IEEE, and ISTQB best practices
- **Automatic Context Scanning**: Scans your project structure, README, and existing docs before generation
- **Project Decomposition**: Automatically analyzes scope and splits large projects into sub-features
- **Smart Upstream Detection**: Finds upstream documents when available; asks compensating questions when not
- **Quality Checklists**: Built-in 4-tier validation (completeness, quality, consistency, formatting)
- **Mermaid Diagrams**: Architecture, sequence, user journey, and Gantt diagrams
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

Status flow: `exploring` → `refining` → `ready` → `graduated`

### `/spec-forge <name>` — Full Chain

Run the streamlined specification chain in one command:

```bash
/spec-forge user-login              # Auto: Idea → Decompose → Tech Design + Feature Specs
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

### `/spec-forge:prd <name>`

Generates a Product Requirements Document including:
- Problem statement and product vision
- User personas and user stories
- Feature requirements with P0/P1/P2 prioritization
- Success metrics (KPI/OKR)
- User journey maps (Mermaid)
- Timeline and milestones (Mermaid Gantt)
- Risk assessment matrix

**Reference**: Google PRD, Amazon Working Backwards (PR/FAQ), Stripe Product Spec

### `/spec-forge:srs <name>`

Generates a Software Requirements Specification including:
- Functional requirements with structured IDs (FR-XXX-NNN)
- Non-functional requirements (NFR-XXX-NNN)
- Data model and data dictionary
- External interface requirements
- Requirements traceability matrix (PRD → SRS, when PRD exists)

**Standalone**: When no upstream PRD is found, asks additional questions to compensate.

**Reference**: IEEE 830, ISO/IEC/IEEE 29148, Amazon Technical Specifications

### `/spec-forge:tech-design <name>`

Generates a Technical Design Document including:
- C4 architecture diagrams (Context, Container, Component)
- Alternative solution comparison matrix
- API design (RESTful / GraphQL / gRPC)
- Database schema and migration strategy
- Security, performance, and observability design
- Deployment and rollback strategy

**Standalone**: When no upstream PRD/SRS is found, asks additional questions to compensate.

**Reference**: Google Design Doc, RFC Template, Uber/Meta Engineering Standards

### `/spec-forge:test-plan <name>`

Generates a Test Plan & Test Cases document including:
- Test strategy (test pyramid: Unit → Integration → E2E)
- Detailed test case specifications (preconditions, steps, expected results)
- Entry/exit criteria
- Defect management process
- Requirements traceability matrix (SRS → Test Cases, when SRS exists)

**Standalone**: When no upstream SRS/Tech Design is found, asks additional questions to compensate.

**Reference**: IEEE 829, ISTQB Test Standards, Google Testing Blog

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
/spec-forge cool-feature                   # Idea → Decompose → Tech Design + Feature Specs
    ↓
/code-forge:plan @docs/features/cool-feature.md   # Break into tasks and execute
```

**Quick path** (skip idea stage):
```
/spec-forge:tech-design cool-feature       # Tech Design + auto-generated feature specs
/code-forge:plan @docs/features/cool-feature.md   # Generate implementation plan
```

### Document Traceability

**Default auto chain** (idea → decompose → tech-design):
```
Idea Draft ──────────────────────────────→ Tech Design ──→ Feature Specs
(ideas/<name>/draft.md)                   §3.5/§3.6/§3.7    docs/features/
                                           populated from      auto-generated
                                           idea draft          in Step 7
```

**With optional upstream docs** (on-demand PRD/SRS add traceability):
```
PRD (optional) ──→ SRS (optional) ──→ Tech Design ──→ Feature Specs
/spec-forge:prd     /spec-forge:srs     §3.5/§3.6/§3.7    docs/features/
                                         traced to           auto-generated
                                         FR/NFR IDs          in Step 7
```

## Output

Each feature gets its own directory under `docs/`:
- `docs/<feature-name>/tech-design.md` (always generated)

Auto-generated feature specs go to `docs/features/`:
- `docs/features/overview.md` (feature index + dependency graph)
- `docs/features/<component-name>.md` (per-component implementation spec)

On-demand documents (when explicitly requested):
- `docs/<feature-name>/prd.md`
- `docs/<feature-name>/srs.md`
- `docs/<feature-name>/test-plan.md`

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
