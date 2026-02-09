# spec-forge

**Professional Software Specification Generator for Claude Code**

Generate industry-standard specifications — PRD, SRS, Technical Design, and Test Plan — each usable standalone or as part of a full traceability chain.

## Overview

Software projects need clear specifications. spec-forge generates four types of professional documents, each based on proven industry standards:

| Command | Document Type | Use Standalone | Standards |
|---------|--------------|:-:|-----------|
| `/prd` | Product Requirements Document | Yes | Google PRD, Amazon PR/FAQ |
| `/srs` | Software Requirements Specification | Yes | IEEE 830, ISO/IEC/IEEE 29148 |
| `/tech-design` | Technical Design Document | Yes | Google Design Doc, RFC Template |
| `/test-plan` | Test Plan & Test Cases | Yes | IEEE 829, ISTQB |

**Each command works independently.** Use just `/prd` for a product review, or just `/tech-design` for an architecture discussion. When upstream documents exist (e.g., a PRD before writing an SRS), spec-forge automatically detects and traces requirements across documents.

## Features

- **Standalone or Chained**: Use any command on its own, or run the full chain for bidirectional traceability
- **Industry Standards**: Templates grounded in Google, Amazon, Stripe, IEEE, and ISTQB best practices
- **Automatic Context Scanning**: Scans your project structure, README, and existing docs before generation
- **Smart Upstream Detection**: Finds upstream documents when available; asks compensating questions when not
- **Quality Checklists**: Built-in 4-tier validation (completeness, quality, consistency, formatting)
- **Mermaid Diagrams**: Architecture, sequence, user journey, and Gantt diagrams

## Commands

### `/prd <product/feature name>`

Generates a Product Requirements Document including:
- Problem statement and product vision
- User personas and user stories
- Feature requirements with P0/P1/P2 prioritization
- Success metrics (KPI/OKR)
- User journey maps (Mermaid)
- Timeline and milestones (Mermaid Gantt)
- Risk assessment matrix

**Reference**: Google PRD, Amazon Working Backwards (PR/FAQ), Stripe Product Spec

### `/srs <feature name>`

Generates a Software Requirements Specification including:
- Functional requirements with structured IDs (FR-XXX-NNN)
- Non-functional requirements (NFR-XXX-NNN)
- Data model and data dictionary
- External interface requirements
- Requirements traceability matrix (PRD → SRS, when PRD exists)

**Standalone**: When no upstream PRD is found, asks additional questions about product goals, target users, and success criteria to compensate.

**Reference**: IEEE 830, ISO/IEC/IEEE 29148, Amazon Technical Specifications

### `/tech-design <feature name>`

Generates a Technical Design Document including:
- C4 architecture diagrams (Context, Container, Component)
- Alternative solution comparison matrix
- API design (RESTful / GraphQL / gRPC)
- Database schema and migration strategy
- Security, performance, and observability design
- Deployment and rollback strategy

**Standalone**: When no upstream PRD/SRS is found, asks additional questions about requirements scope, constraints, and acceptance criteria to compensate.

**Reference**: Google Design Doc, RFC Template, Uber/Meta Engineering Standards

### `/test-plan <feature name>`

Generates a Test Plan & Test Cases document including:
- Test strategy (test pyramid: Unit → Integration → E2E)
- Detailed test case specifications (preconditions, steps, expected results)
- Entry/exit criteria
- Defect management process
- Requirements traceability matrix (SRS → Test Cases, when SRS exists)

**Standalone**: When no upstream SRS/Tech Design is found, asks additional questions about feature behavior, edge cases, and quality targets to compensate.

**Reference**: IEEE 829, ISTQB Test Standards, Google Testing Blog

## Document Traceability (Chain Mode)

When you run commands in sequence, spec-forge builds a full traceability chain:

```
PRD ──traceability──→ SRS ──design input──→ Tech Design ──test input──→ Test Plan
 │                     │                      │                         │
 │  PRD-ID             │  FR/NFR-ID           │  Component/API          │  TC-ID
 │                     │                      │                         │
 └─────────────────────┴──────────────────────┴─────────────────────────┘
                        Traceability matrix spans all documents
```

The recommended full-chain workflow:

1. `/prd user-login` — Define the product vision and requirements
2. `/srs user-login` — Formalize functional and non-functional requirements
3. `/tech-design user-login` — Design the technical architecture
4. `/test-plan user-login` — Plan testing strategy and write test cases

Each subsequent command automatically reads upstream documents to maintain consistency.

## Output

All documents are written to the `docs/` directory:
- `docs/prd-<feature-name>.md`
- `docs/srs-<feature-name>.md`
- `docs/tech-design-<feature-name>.md`
- `docs/test-plan-<feature-name>.md`

## Works Great With

**[superpowers](https://github.com/obra/superpowers)** — spec-forge handles upstream specification (what to build and why), superpowers handles downstream execution (how to build it and ship it).

Combined workflow:

1. `/prd` → Define product vision (spec-forge)
2. `/srs` → Formalize requirements (spec-forge)
3. `/tech-design` → Design architecture (spec-forge)
4. `/test-plan` → Plan testing strategy (spec-forge)
5. `/write-plan` → Break into implementation tasks (superpowers)
6. `/execute-plan` → Code with TDD + review (superpowers)

**spec-forge works perfectly standalone — superpowers is optional.**

If superpowers is not installed, each command's "Next Steps" section provides general guidance for moving forward with implementation.

## Installation

### Claude Code (via Plugin Marketplace)

```bash
/plugin marketplace add tercelyi/spec-forge-marketplace
/plugin install spec-forge@spec-forge-marketplace
```

### Codex

See [.codex/INSTALL.md](.codex/INSTALL.md)

### OpenCode

See [.opencode/INSTALL.md](.opencode/INSTALL.md)

## License

MIT License
