# spec-forge

**Professional Software Specification Generator for Claude Code**

Generate industry-standard specifications — from early-stage brainstorming to PRD, SRS, Technical Design, and Test Plan — each usable standalone or as part of a full traceability chain.

## Overview

Software projects need clear specifications. spec-forge covers the full journey from idea to implementation-ready documents:

| Command | Description | Standards |
|---------|-------------|-----------|
| `/spec-forge:idea <name>` | Interactive brainstorming — explore and refine ideas | — |
| `/spec-forge:feature <name>` | Lightweight feature spec — bridge to code-forge | — |
| `/spec-forge:prd <name>` | Product Requirements Document | Google PRD, Amazon PR/FAQ |
| `/spec-forge:srs <name>` | Software Requirements Specification | IEEE 830, ISO/IEC/IEEE 29148 |
| `/spec-forge:tech-design <name>` | Technical Design Document | Google Design Doc, RFC Template |
| `/spec-forge:test-plan <name>` | Test Plan & Test Cases | IEEE 829, ISTQB |
| `/spec-forge:decompose <name>` | Decompose project into sub-features | — |
| `/spec-forge <name>` | **Full chain** — auto-run PRD → SRS → Tech Design → Test Plan | All of the above |

**Aliases**: `/prd`, `/srs`, `/tech-design`, `/test-plan`, `/idea`, `/feature`, `/decompose` work as shortcuts.

## Features

- **Idea to Spec**: Brainstorm interactively, then graduate ideas into formal documents
- **Full Chain Mode**: One command runs the entire specification chain automatically
- **Standalone or Chained**: Use any command on its own, or run the full chain for bidirectional traceability
- **Industry Standards**: Templates grounded in Google, Amazon, Stripe, IEEE, and ISTQB best practices
- **Automatic Context Scanning**: Scans your project structure, README, and existing docs before generation
- **Project Decomposition**: Automatically analyzes scope and splits large projects into sub-features
- **Smart Upstream Detection**: Finds upstream documents when available; asks compensating questions when not
- **Quality Checklists**: Built-in 4-tier validation (completeness, quality, consistency, formatting)
- **Mermaid Diagrams**: Architecture, sequence, user journey, and Gantt diagrams

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

### `/spec-forge:feature <name>` — Lightweight Feature Spec

Generate a concise, implementation-ready feature specification:

```bash
/spec-forge:feature core-executor     # Standalone: 2-3 round Q&A → docs/features/core-executor.md
/spec-forge:feature user-auth         # Extract: if tech-design exists, auto-extracts from it
```

- **Two modes**: standalone Q&A or extract from existing tech-design
- **Language-agnostic**: describes what to build, not how (no Pydantic, no TypeBox)
- **code-forge ready**: output at `docs/features/` is the default input for `/code-forge:plan`
- **Concise**: 1-3 pages, focused on module purpose, interfaces, data flow, and constraints

### `/spec-forge <name>` — Full Chain

Run the complete specification chain in one command:

```bash
/spec-forge user-login              # Auto: PRD → SRS → Tech Design → Test Plan
```

- Detects existing documents and resumes from where you left off
- PRD stage requires user interaction; subsequent stages run with minimal input (chain mode)
- If an idea draft exists in `ideas/`, uses it as additional context

### `/spec-forge:decompose <name>` — Project Decomposition

Analyze project scope and split into sub-features if needed:

```bash
/spec-forge:decompose my-project     # Interview → split analysis → manifest
```

- Lightweight 3-5 round interview focused on scope boundaries
- Generates `docs/project-{name}.md` manifest for multi-split projects
- Automatically invoked as Step 0 when running `/spec-forge <name>` full chain

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

## Complete Workflow

```
/spec-forge:idea cool-feature              # Brainstorm (iterative, multi-session)
    ↓ (graduated)
/spec-forge cool-feature                   # Scope analysis → PRD → SRS → Tech Design → Test Plan
    ↓
/spec-forge:feature cool-feature           # Extract lightweight feature spec from tech-design
    ↓
/code-forge:plan @docs/features/cool-feature.md   # Break into tasks and execute
```

**Quick path** (skip formal chain):
```
/spec-forge:feature cool-feature           # 2-3 round Q&A → docs/features/cool-feature.md
/code-forge:plan @docs/features/cool-feature.md   # Generate implementation plan
```

### Document Traceability (Chain Mode)

When you run the full chain, spec-forge builds bidirectional traceability:

```
PRD ──traceability──→ SRS ──design input──→ Tech Design ──test input──→ Test Plan
 │                     │                      │                         │
 │  PRD-ID             │  FR/NFR-ID           │  Component/API          │  TC-ID
 │                     │                      │                         │
 └─────────────────────┴──────────────────────┴─────────────────────────┘
                        Traceability matrix spans all documents
```

## Output

Each feature gets its own directory under `docs/`:
- `docs/<feature-name>/prd.md`
- `docs/<feature-name>/srs.md`
- `docs/<feature-name>/tech-design.md`
- `docs/<feature-name>/test-plan.md`

Lightweight feature specs go to `docs/features/`:
- `docs/features/<feature-name>.md`

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
/plugin marketplace add tercel/claude-code-skills
/plugin install spec-forge@claude-code-skills
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md)

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md)

## License

MIT License
