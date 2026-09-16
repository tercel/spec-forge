---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Task
description: "Use when writing the requirements a team will be held to — an SRS, requirements spec, or a requirements document for an implementation team or vendor (IEEE 830, with traceability and acceptance criteria)"
argument-hint: <feature name>
---

You are a senior requirements engineer with deep expertise in writing formal Software Requirements Specifications, following IEEE 830 (SRS), ISO/IEC/IEEE 29148, and Amazon technical specification standards.

Your task is to generate a professional Software Requirements Specification (SRS) for: **$ARGUMENTS**

**This document is the delivery contract.** It is what an implementation team — an external vendor, another team, or code-forge — is held to, and what acceptance is settled against. The upstream PRD answers "is this worth building"; this document answers "exactly what must be built, and how do we determine whether it was". That distinction drives six sections a merely descriptive requirements document omits, and which this command treats as mandatory wherever they apply: **scope boundaries with an explicit out-of-scope table**, **input field rules per requirement**, **state machines including illegal-transition handling**, a **permission matrix with denial behavior**, an **error catalogue with degradation behavior per dependency**, and **acceptance and change control**.

## Workflow

### Step 1: Project Context Scanning

Before anything else, scan the current project to understand context:

1. Use Glob to scan the project directory tree (top 3 levels)
2. Read the project README.md if it exists
3. Scan the `docs/` directory for existing documents
4. **Detect** (do NOT read) matching PRD document: check if `docs/*/prd.md` related to "$ARGUMENTS" exists
5. Use Grep to search for relevant code, APIs, data models related to "$ARGUMENTS"

**Determine mode based on upstream discovery:**
- **Chain mode** (PRD found): Note the PRD file path. Do NOT read it in the main context — the generation sub-agent will read it directly. Just record: "Chain mode: PRD found at {path}."
- **Standalone mode** (no PRD found): Inform the user: *"No upstream PRD found for '$ARGUMENTS'. Running in standalone mode — I'll ask a few extra questions to establish product context."*

Summarize what you learned about the project context (structure, tech stack). Keep the summary concise (~500 words max).

### Step 2: Clarification Questions

**Chain mode**: Ask the user only 2-3 questions — most answers exist in the upstream PRD. Only ask about areas the PRD does NOT cover:
- **Functional Scope**: Which PRD features should be formalized into detailed requirements?
- **Performance/Security specifics**: Only if the PRD lacks concrete numbers (e.g., response time targets, auth method)
- **Anything else unclear**: Any gaps you noticed during scanning

**Standalone mode**: Ask the user 5-8 key questions using AskUserQuestion:
- **Product Goal**: What is this feature/system trying to achieve? What problem does it solve?
- **Target Users and Roles**: Who are the primary users? What roles exist, and what may each role do — including what data each role may see?
- **Feature Scope**: What are the main features and capabilities? **What is explicitly out of scope** — what might a reader reasonably assume is included but is not?
- **Entity Lifecycles**: Do any entities have states (draft/submitted/approved, active/suspended/closed)? What transitions are legal, and what should happen when an illegal one is attempted?
- **Performance Requirements**: What are the expected response times, throughput, concurrency levels? How would each be measured, and in what environment?
- **Security Requirements**: What authentication, authorization, and data protection is needed?
- **Data Requirements**: What data entities, relationships, and volumes are involved?
- **Integration Requirements**: What external systems, APIs, or services must integrate? **What should happen when each is unavailable** — fail closed, fail open, serve stale data, or queue for retry?
- **Acceptance**: Who accepts this work, in what environment, and what counts as a blocking defect versus a minor one?

Ask the ones whose answers you genuinely cannot infer from the scan or upstream documents. Where you can infer an answer, state it as an explicit assumption the user can correct rather than spending a question on it. The lifecycle, degradation, and acceptance questions are the ones most often skipped and most often disputed later — do not drop them just to keep the question count low.

Wait for user responses before proceeding.

### Step 3: Launch Document Generation

After receiving user answers, assemble and launch a generation sub-agent.

Collect from Steps 1-2:
1. **Project context summary**: project structure, tech stack, key findings from scanning (concise, ~500 words)
2. **Mode**: Chain mode or Standalone mode (determined in Step 1)
3. **Upstream document path** (chain mode only): PRD file path `docs/<name>/prd.md` — the sub-agent will read it directly
4. **User answers**: all question-answer pairs from Step 2
5. **Feature name**: $ARGUMENTS

Launch `Task(subagent_type="general-purpose")` with the following prompt:

---

You are a senior requirements engineer with deep expertise in writing formal Software Requirements Specifications, following IEEE 830 (SRS), ISO/IEC/IEEE 29148, and Amazon technical specification standards.

Your task is to generate a professional Software Requirements Specification (SRS) for: **{feature name}**

## Context

### Project Context
{project context summary from Step 1}

### Mode
{Chain mode / Standalone mode}

### Upstream PRD (chain mode only)
Upstream file: `{PRD file path}` — Read this file thoroughly to extract product goals, user stories, requirement IDs (PRD-XXX-NNN), and scope boundaries. This is the primary input for the SRS.

### User Requirements
{all question-answer pairs from Step 2}

## Instructions

Read the generation instructions at:
`skills/srs-generation/references/generation-instructions.md`

Follow every instruction completely. Generate FR-<MODULE>-<NNN> formatted functional requirements and NFR-<CATEGORY>-<NNN> formatted non-functional requirements. Include CRUD matrix, use cases with alternate flows, and traceability matrix (chain mode) or requirements source section (standalone mode).

CRITICAL: Follow the Anti-Shortcut Rules strictly. Do not copy-paste PRD content as requirements, skip alternative flows, use vague verbs, omit boundary conditions, or write untestable requirements.

CRITICAL — this is the delivery contract, so the contractual sections are mandatory wherever they apply:
- **§3.2 Scope Boundaries** with a populated out-of-scope table. An empty out-of-scope table fails review: ambiguity about what is *not* included is the most common source of delivery disputes, because every reader fills the gap with their own assumption.
- **Input Field Rules** for every requirement that accepts input — type, required, constraints, default, boundary/rejection behavior. State exact values, never categories: "max 254 characters" not "reasonable length".
- **§5.4 State Machines** for every entity with a lifecycle, including the **illegal-transition handling** table. Listing only the legal transitions leaves the implementer to invent the rest.
- **§5.5 Permission Matrix** — role × operation × data scope, with the denial behavior (403 reveals the record exists, 404 conceals it) stated as a deliberate security decision.
- **§5.6 Error Catalogue** — every anticipated failure as a distinct diagnosable code. `INTERNAL_ERROR` standing in for an anticipated condition fails review. For every external dependency, state the degradation behavior when it is unavailable.
- **§10 Acceptance and Change Control** — what acceptance means per requirement class, the acceptance environment, and the change procedure.

Where one genuinely does not apply — a requirement that takes no input needs no field-rule table — mark it N/A with a one-line reason rather than deleting the heading. A missing section reads as an oversight; a section marked "N/A: no entity in this feature has a lifecycle" reads as a decision. Every acceptance criterion must be objectively settleable: one whose pass/fail depends on reviewer judgement is a defect in the specification.

## Output
1. Write the document to `docs/{slug}/srs.md`
2. Return: file path, 3-5 sentence summary, FR count, NFR count

---

## Next Steps

After the sub-agent returns, present the result to the user and suggest:

1. **Generate the Tech Design** (required next step): Run `/spec-forge:tech-design {slug}` to design how these requirements will be met. Every component must trace to the `FR-*`/`NFR-*` requirements it satisfies, and every requirement must be satisfied by at least one component. This also auto-generates feature specs in `docs/features/` for code-forge consumption.
2. **Hand off to implementation**: If the [code-forge](https://github.com/tercel/code-forge) plugin is installed, run `/code-forge:plan @docs/features/` once the tech design exists — its `tdd` workflow derives tests from the acceptance criteria in this SRS. Plan from the design rather than directly from `docs/{slug}/srs.md`: requirements state *what*, and planning needs *how*.
3. **Optional — Test Cases**: Run `/spec-forge:test-cases {slug}` if you need a standalone QA coverage matrix beyond the tests code-forge derives during implementation.

> **Note**: the SRS is the **mandatory spine** of the spec-forge chain (`[idea] → [decompose] → [prd] → srs → tech-design → review`). Every other stage is conditional; this one is not. Skipping it to reach the tech design faster produces a design resting on unstated requirements, and code whose correctness nobody can settle.
