# Release Notes

## v1.1.0 — Rename to spec-forge + Standalone Mode

**Release Date**: 2025-02-09

### Breaking Changes

- **Renamed from `doc-lifecycle` to `spec-forge`**. Update your plugin installation accordingly.

### New Features

- **Standalone mode**: Each command now works independently without upstream documents. When no upstream PRD/SRS/Tech Design is found, the command asks additional clarification questions to compensate. No need to run the full chain.
- **Updated description**: Clearer positioning as a specification forging tool, not a document lifecycle manager.

### Upgrade Guide

```bash
/plugin uninstall doc-lifecycle
/plugin install spec-forge@superpowers-marketplace
```

---

## v1.0.0 — Initial Release

**Release Date**: 2025-01-01

### Overview

spec-forge (originally doc-lifecycle) is a Claude Code plugin that generates professional-grade software specifications at every stage of the development lifecycle, based on industry best practices from Google, Amazon, Stripe, IEEE, and ISTQB standards.

### Core Features

#### `/prd` — Product Requirements Document Generation
- 5-step workflow: context scanning → clarification → generation → quality check → output
- Market research & analysis (TAM/SAM/SOM) with source citations
- Anti-pseudo-requirement principle: every feature backed by evidence of real demand
- Competitive analysis (2+ competitors), user personas, user stories
- Feasibility analysis with honest GO / CONDITIONAL GO / NO-GO verdict
- Mermaid diagrams: user journeys, feature architecture, Gantt timeline
- Risk assessment matrix with likelihood/impact ratings
- Quality checklist validation

#### `/srs` — Software Requirements Specification Generation
- IEEE 830 / ISO/IEC/IEEE 29148 compliant structure
- Functional requirements (FR-MODULE-NNN) with actors, flows, acceptance criteria
- Non-functional requirements (NFR-CATEGORY-NNN) with metrics and targets
- CRUD matrix for data operations
- Upstream PRD auto-detection and traceability matrix
- Modal verb discipline: "shall" / "should" / "may"
- Quality checklist validation

#### `/tech-design` — Technical Design Document Generation
- C4 architecture diagrams (Context, Container, Component, Code)
- At least 2 alternative solutions with comparison matrix
- Complete parameter validation matrix for every API input
- Boundary value and edge case documentation
- Business logic specification: state machines, computation rules, conditional logic
- Error handling taxonomy with retry/circuit breaker configuration
- Database schema with ER diagram, index strategy, migration plan
- Security, performance, observability, and deployment design
- Quality checklist validation

#### `/test-plan` — Test Plan & Test Cases Generation
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
PRD (PRD-ID) → SRS (FR/NFR-ID) → Tech Design (Component/API) → Test Plan (TC-ID)
```

### Standards Referenced
- Google PRD, Amazon Working Backwards (PR/FAQ), Stripe Product Spec
- IEEE 830 (SRS), IEEE 829 (Test Plans)
- ISO/IEC/IEEE 29148
- ISTQB Test Standards
- Google Testing Blog
- Google Design Doc, RFC Template, Uber/Meta Engineering Standards
