---
name: srs-generation
description: >
  Generates professional Software Requirements Specification (SRS) documents based on IEEE 830,
  ISO/IEC/IEEE 29148, and Amazon technical specification standards. This skill activates when the
  user needs a requirements document, requirements specification, SRS, functional requirements,
  non-functional requirements, software requirements, requirements analysis, or requirements
  engineering. It formalizes product needs into structured, testable, and traceable requirements
  with unique IDs, acceptance criteria, use cases, a CRUD matrix, and a full traceability matrix
  linking back to the upstream PRD.
instructions: >
  Generate a complete Software Requirements Specification following IEEE 830, ISO/IEC/IEEE 29148,
  and Amazon technical specification standards. Use the template at references/template.md and
  validate against references/checklist.md before finalizing.
---

# SRS Generation Skill

## What Is a Software Requirements Specification?

A Software Requirements Specification (SRS) is a formal document that describes exactly what a software system must do and the constraints under which it must operate. It serves as the contractual bridge between stakeholders who define the product vision (captured in a PRD) and the engineering team that designs, builds, and tests the system. A well-written SRS eliminates ambiguity, reduces rework, and provides a single source of truth for every requirement the system must satisfy.

The two foundational standards for SRS documents are **IEEE 830** (IEEE Recommended Practice for Software Requirements Specifications) and **ISO/IEC/IEEE 29148** (Systems and Software Engineering -- Life Cycle Processes -- Requirements Engineering). IEEE 830 established the canonical section structure -- introduction, overall description, specific requirements -- and defined the quality attributes every requirement must exhibit: correctness, unambiguity, completeness, consistency, ranking for importance, verifiability, modifiability, and traceability. ISO/IEC/IEEE 29148 modernized this foundation by integrating requirements engineering into the full systems and software lifecycle, emphasizing stakeholder needs analysis, requirements analysis, and requirements validation as continuous activities rather than one-time documentation events. This skill combines the structural rigor of both standards with the pragmatic, metric-driven approach found in Amazon technical specifications, where every requirement must be tied to a measurable outcome.

## Generation Workflow

The SRS generation process follows a six-step workflow designed to produce a complete, high-quality document:

### Step 1: Scan Context

Before writing a single requirement, scan the project to build context:

@../shared/project-context.md

Execute the Project Context Protocol. Prefer its **PC.0 fast path** — resolve `<sf_scripts>` (see `@../shared/scripts.md`) and run `python3 "<sf_scripts>/sf-scan.py" --root "<project_root>"`, which returns the languages, frameworks, DB/auth signals, test command, and the existing-doc inventory (including any upstream `prd.md` with its declared IDs) in one pass. Fall back to the manual PC.1–PC.3 scan only if the script is unavailable. Then apply judgement the script does not: label the project profile (PC.3) and pick which non-functional requirement categories are most relevant (e.g., database-backed projects need data integrity NFRs; CLI tools need usability NFRs).

### Step 1.5: Doc-First Discipline (Mandatory)

Before locating the upstream PRD or writing any requirements, the doc-first discipline applies. Read the existing documentation, identify what already covers the topic, and decide for each requirement whether to **REUSE** (reference existing), **EXTEND** (edit existing in place), or **NEW** (genuinely missing). The default for any requirement that has coverage in an existing SRS is to extend in place — never to create parallel `srs-v2.md` files, never to append `## Update` blocks, never to leave deprecated requirements strikethrough'd. Requirement IDs are contracts: once issued, they should not be silently re-purposed.

The full discipline, the four rules, the pre-generation checklist, and the anti-patterns to avoid:

@../shared/doc-first.md

**You MUST run the pre-generation checklist (the five questions) from doc-first.md before proceeding to Step 2.** If existing docs already cover any of the requirements this SRS will discuss, you must:

1. List the existing files and requirement IDs that overlap (with `file:line` references)
2. Decide REUSE / EXTEND / NEW for each requirement
3. Bias toward EXTEND — opening the existing SRS and modifying it — over NEW
4. **Preserve existing requirement IDs.** Once a requirement ID has been issued, it must not be silently renumbered. If a requirement is split, the original ID is retained for one of the parts and the new parts get new IDs. If a requirement is removed, its ID is retired (not reused).
5. Surface any downstream documents (tech-design, test-cases, feature specs) this generation will affect, so the user knows the propagation cost

If the project shows signs of doc drift (multiple `srs-*.md` files, obvious duplication, requirement ID collisions), warn the user before proceeding and recommend they run `/spec-forge:analyze` or `/spec-forge:propagate` first.

If a usable existing SRS already covers most of what the user is asking for, the right action is **edit it in place**, not generate a new file.

---

### Step 2: Find the Upstream PRD

The most critical input to any SRS is the Product Requirements Document. The `sf-scan.py` inventory from Step 1 already reports any `docs/<feature-name>/prd.md` (under `document_index.prd`) and the requirement IDs it declares; read that PRD thoroughly. The PRD provides the product vision, user stories, feature definitions, success metrics, and scope boundaries that the SRS must formalize into precise, testable requirements. If no PRD is found, proceed but flag that traceability to product-level requirements will be limited.

### Step 3: Clarify Only What You Cannot Infer

First infer every answer you can from the PRD, the scanned project context, and any existing SRS — and state those inferences as explicit assumptions the user can correct. Then ask the user **only** the questions whose answers materially change the requirements and cannot be inferred: typically specific NFR thresholds (response-time targets, concurrent-user capacity, data-retention policies), regulatory obligations, and integration contracts. Do not march through a fixed questionnaire or re-ask anything the upstream docs already answer; a strong scan often makes most questions unnecessary.

### Step 4: Generate the SRS

Using the template at `references/template.md`, the skill generates the full SRS document. Every section of the IEEE 830 structure is populated: introduction, overall description, functional requirements, non-functional requirements, data requirements, external interface requirements, and the requirements traceability matrix. Requirements are written following the conventions and quality standards described in the sections below.

**This document is the delivery contract.** The SRS is what an implementation team — an external vendor, another team, or code-forge — is held to. The upstream PRD answers "is this worth building and for whom"; the SRS answers "exactly what must be built, and how do we settle whether it was". That distinction drives six sections that a merely descriptive requirements document omits, and that this skill treats as mandatory wherever they apply:

| Section | Why it is contractual |
|---------|----------------------|
| §3.2 Scope Boundaries | The explicit out-of-scope table. Ambiguity about what is *not* included is the most common source of delivery disputes; an unstated exclusion becomes the reader's assumption. |
| Input Field Rules (per FR) | Field-level type/required/constraint/default/boundary rules. "Reasonable length" is negotiable; "max 254 characters, reject with `VAL_TOO_LONG`" is not. |
| §5.4 State Machines | Legal transitions **and** the rejection behavior for every illegal one. Specifying only the legal paths leaves the implementer to invent the rest. |
| §5.5 Permission Matrix | Role × operation × data scope, plus the denial behavior (403 vs 404 is a security decision, not an implementation detail). |
| §5.6 Error Catalogue | Every anticipated failure as a distinct diagnosable code with its user-facing message and degradation path. |
| §10 Acceptance & Change Control | What "accepted" means, in which environment, and the procedure by which the contract may change. |

Omit any of these only when it genuinely does not apply — a requirement that takes no input needs no field-rule table — and say so explicitly in the document rather than deleting the heading silently. A missing section reads as an oversight; a section marked "N/A: this feature has no entity with a lifecycle" reads as a decision.

### Step 5: Traceability

If an upstream PRD was found, build a requirements traceability matrix (RTM) that maps every PRD feature or user story to one or more SRS requirements, with a coverage status (Fully / Partially / Not Covered). Let the script layer do the coverage math: after the SRS is drafted, run

```bash
python3 "<sf_scripts>/sf-trace.py" matrix --upstream "<prd.md>" --downstream "<srs.md>"
```

and use its `uncovered_upstream` (PRD IDs with no SRS requirement — coverage gaps to close) and `orphan_downstream_refs` (SRS references to PRD IDs that do not exist — dangling links to fix). The script computes the coverage; you decide whether each gap is intentional (out of scope) or a real omission. Fall back to building the matrix by hand if the script is unavailable.

### Step 6: Quality Check

Run the structural gate with the script, then apply judgement with the checklist:

```bash
python3 "<sf_scripts>/sf-verify-doc.py" "<srs.md>" --strict
```

This deterministically confirms the title, recommended IEEE 830 sections, ID format/uniqueness (a heading plus its ID table row count as one definition), and the absence of leftover template placeholders. Fix everything it flags. Then load `references/checklist.md` and evaluate the items the script cannot judge — requirement unambiguity, testability, whether each NFR target has a real threshold rationale. The document is only written to disk once the structural gate passes and the judgement items hold. (If `python3` is unavailable, run every checklist item by hand.)

## Requirement ID Conventions

Every requirement receives a unique identifier that encodes its type and module or category:

- **Functional Requirements**: `FR-<MODULE>-<NNN>` where `<MODULE>` is a short uppercase label for the feature module (e.g., AUTH, CART, SEARCH, NOTIFY) and `<NNN>` is a zero-padded sequential number. Examples: FR-AUTH-001, FR-CART-012, FR-SEARCH-003.
- **Non-Functional Requirements**: `NFR-<CATEGORY>-<NNN>` where `<CATEGORY>` identifies the quality attribute (e.g., PERF, SEC, REL, AVL, MNT, PRT, USB) and `<NNN>` is a zero-padded sequential number. Examples: NFR-PERF-001, NFR-SEC-003, NFR-REL-002.

These IDs are used throughout the document -- in the requirements traceability matrix, in cross-references between related requirements, and in downstream documents such as technical designs and test plans. Consistent ID formatting is essential for automated traceability and search. When extending an existing SRS, allocate the next free number deterministically instead of guessing: `python3 "<sf_scripts>/sf-trace.py" next-id --prefix FR --module AUTH --existing "<srs.md>"` returns the next unused `FR-AUTH-NNN` (respecting existing zero-padding), which avoids collisions and reuse.

## Functional Requirements Writing Standards

Each functional requirement is structured as a complete use case specification with the following elements:

- **Requirement ID and Title**: The unique identifier and a concise descriptive title.
- **Description**: A clear statement of what the system shall do, written from the perspective of the system behavior rather than the implementation approach.
- **Actors**: The user classes or external systems that participate in this requirement. Actors include both human users and AI agent consumers — if a requirement is exercised by an API client, automation tool, or other programmatic consumer, list that actor explicitly with its interaction pattern (REST API, async event, webhook, etc.).
- **Preconditions**: The conditions that must be true before the requirement can be exercised.
- **Main Flow**: A numbered sequence of steps describing the standard successful path through the use case.
- **Alternative Flows**: Branches from the main flow covering variations, error conditions, and edge cases.
- **Postconditions**: The observable state of the system after successful completion of the main flow.
- **Input Field Rules**: For any requirement that accepts input, a table giving every field's type, whether it is required, its exact constraints, its default, and its boundary/rejection behavior referencing a code from the §5.6 Error Catalogue. State exact rules, never categories — "max 254 characters" not "reasonable length", "1 ≤ n ≤ 999" not "a positive number". Unspecified field rules are the single largest source of acceptance disputes, because each side fills the gap with a different assumption. Omit the block only for requirements that take no input, and say so rather than deleting the heading.
- **Acceptance Criteria**: Specific, testable conditions that must be met for the requirement to be considered satisfied, written in Given/When/Then form. Each acceptance criterion should be verifiable through inspection, demonstration, test, or analysis. For agent-facing requirements, acceptance criteria must be machine-verifiable — expressed as exact input/output contracts (e.g., "Given POST /api/v1/users with body {name, email}, then response status is 201 and JSON body contains {id, email, created_at}") rather than human-subjective descriptions. **These criteria are the acceptance contract** (§10.1): a requirement is accepted when every one of its criteria is demonstrably satisfied, so a criterion that cannot be objectively settled is a defect in the specification, not a matter to resolve later.
- **Priority**: The importance level of the requirement (P0 = must-have, P1 = should-have, P2 = nice-to-have), consistent with the prioritization used in the upstream PRD.
- **Source**: A reference back to the PRD item or stakeholder request that originated this requirement.

Each functional requirement also carries a **Priority Rationale** field explaining *why* the assigned priority (P0/P1/P2) was chosen. Stating "P0" without justification is not sufficient — the rationale must connect the priority to a concrete consequence: "P0: the product cannot launch without this because it is the sole entry point for all user actions" or "P2: a manual workaround exists in v1 and user research shows it is acceptable for the first six months." Priority assignments that lack rationale are flagged as incomplete during the quality check.

In addition to individual requirement specifications, the SRS includes four cross-cutting sections that individual requirements cannot express on their own:

**CRUD matrix (§5.3).** Maps data entities (rows) against Create, Read, Update, and Delete operations (columns), with each cell indicating which functional requirement governs that operation. This provides a rapid completeness check: if an entity has no "Delete" operation defined, that may be intentional (soft-delete policy) or an oversight that needs resolution.

**State machines (§5.4).** For every entity with a lifecycle, a diagram plus two tables: the legal transitions (with trigger, actor, guard condition, and governing FR) and the **illegal transition handling** (what the system does, which error code, what the actor sees). Specifying only the legal transitions is half a state machine — every transition not listed must have a defined rejection behavior, or the implementer picks one and acceptance testing discovers it. State explicitly whether an illegal transition is idempotent-ignored or hard-rejected, and whether side effects fire on rejection.

**Permission matrix (§5.5).** Role × operation × data scope, with the data scopes defined in terms of concrete predicates ("records where `owner_id` equals the authenticated principal") rather than prose. Specify the denial behavior deliberately: `403 Forbidden` reveals that the record exists, `404 Not Found` conceals it. That is a security decision belonging in the requirements, not a detail to leave to the implementer.

**Error catalogue (§5.6).** Every anticipated failure as a distinct, diagnosable code with its trigger, actor-visible message, recovery path, and originating requirement. `INTERNAL_ERROR` is not an acceptable entry for any anticipated condition — collapsing distinct causes into one code makes the failure untestable. For every external dependency, the catalogue also states the degradation behavior when it is unavailable: fail closed, fail open, serve stale data (and how stale is acceptable), or queue for retry (and for how long).

## Non-Functional Requirements Categories

Non-functional requirements define the quality attributes and constraints of the system. Each NFR must include a specific, measurable metric, a target value, a measurement method, a **Verification** method (one of Test, Demonstration, Inspection, or Analysis, naming the environment and conditions under which the measurement is taken), and a **Threshold Rationale** explaining *why this specific target value was chosen* rather than a higher or lower one. An NFR with a target but no agreed verification method cannot be accepted or disputed on any objective basis — "the system shall handle 10,000 concurrent users" is unsettleable until the document says who measures it, where, and under what load profile. The rationale must cite at least one of: a business contract or SLA obligation, observed production baseline data, competitive benchmark, regulatory standard, or a cost/complexity trade-off analysis. NFR targets written without threshold rationale (e.g., "99.9% uptime" with no explanation) are treated as unsubstantiated guesses and flagged during the quality check. The SRS organizes NFRs into the following categories:

- **Performance (NFR-PERF)**: Response times, throughput, latency percentiles (p50, p95, p99), concurrent user capacity, and resource utilization limits.
- **Security (NFR-SEC)**: Authentication mechanisms, authorization models, encryption standards, data protection measures, vulnerability scanning requirements, and compliance with security frameworks.
- **Reliability (NFR-REL)**: Mean time between failures (MTBF), mean time to recovery (MTTR), error rates, data integrity guarantees, and fault tolerance mechanisms.
- **Availability (NFR-AVL)**: Uptime SLAs (e.g., 99.9%), planned maintenance windows, disaster recovery objectives (RPO/RTO), and geographic redundancy requirements.
- **Maintainability (NFR-MNT)**: Code quality standards, documentation requirements, deployment frequency targets, and technical debt constraints.
- **Portability (NFR-PRT)**: Supported platforms, browsers, operating systems, container runtimes, and cloud provider compatibility.
- **Usability (NFR-USB)**: Accessibility standards (WCAG compliance level), internationalization requirements, maximum task-completion times, and user satisfaction targets.

## Requirements Traceability Matrix

The requirements traceability matrix (RTM) is a table that establishes bidirectional links between PRD items and SRS requirements. Each row maps a PRD identifier to one or more SRS functional or non-functional requirement IDs, along with a coverage status (Fully Covered, Partially Covered, or Not Covered). The RTM serves three purposes: it confirms that every product need has been addressed, it enables impact analysis when requirements change, and it provides the foundation for downstream traceability into technical design and test planning.

## Requirement Language Conventions

The SRS uses precise modal verbs to convey obligation levels, following IEEE 830 and RFC 2119 conventions:

- **"shall"**: Indicates a mandatory requirement. The system must satisfy this requirement to be considered compliant. Example: "The system shall authenticate users via OAuth 2.0 before granting access to protected resources."
- **"should"**: Indicates a recommended requirement. The system is expected to satisfy this requirement under normal circumstances, but justified exceptions are acceptable. Example: "The system should cache frequently accessed queries to reduce database load."
- **"may"**: Indicates an optional requirement. The system is permitted but not required to implement this behavior. Example: "The system may provide a dark-mode theme for the user interface."

Avoiding ambiguous language is critical. Terms like "fast," "user-friendly," "efficient," or "robust" are never used in isolation. Every qualitative claim must be paired with a quantitative target (e.g., "The system shall return search results within 200ms at the 95th percentile" rather than "The system shall be fast").

## Requirement Quality Attributes

Every requirement in the SRS -- functional or non-functional -- must satisfy four quality attributes:

1. **Unambiguous**: The requirement has exactly one interpretation. There is no room for disagreement about what the requirement means. Techniques for achieving unambiguity include using precise terminology defined in the glossary, avoiding pronouns with unclear antecedents, and stating explicit boundary conditions.
2. **Testable**: The requirement includes acceptance criteria or measurable targets that can be verified through testing, inspection, demonstration, or analysis. If a requirement cannot be tested, it must be rewritten until it can.
3. **Traceable**: The requirement can be traced both backward (to its source in the PRD or stakeholder request) and forward (to the design components and test cases that address it). Traceability is maintained through the requirement ID system and the RTM.
4. **Complete**: The requirement contains all information necessary for implementation. It specifies inputs, outputs, preconditions, postconditions, error handling, and boundary conditions without requiring the reader to make assumptions.

## Reference Files

The SRS generation skill relies on two reference files:

- **`references/template.md`**: The complete SRS document template following IEEE 830 structure. This template defines every section, provides placeholder guidance, and establishes the formatting conventions for requirements, tables, and diagrams.
- **`references/checklist.md`**: The quality checklist used during the final validation step. It contains items organized into four categories -- completeness, quality, consistency, and format -- that the generated document must satisfy before it is written to disk.

## Output Convention

The final SRS document is written to `docs/<feature-name>/srs.md` in the project root, where `<feature-name>` is a sanitized, lowercase, hyphen-separated slug derived from the user's input. The `docs/<feature-name>/` directory is created if it does not already exist. If a file with the same name already exists, confirm with the user before overwriting. This naming convention places all documents for a feature in a single `docs/<feature-name>/` directory (`prd.md`, `srs.md`, `tech-design.md`, `test-cases.md`) and enables automatic upstream document discovery by downstream skills.
