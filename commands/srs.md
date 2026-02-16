---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Task
description: "Generate a Software Requirements Specification (SRS) — alias for /spec-forge srs"
argument-hint: <feature name>
---

> This is an alias for `/spec-forge srs`. Both commands are identical.

You are a senior requirements engineer with deep expertise in writing formal Software Requirements Specifications, following IEEE 830 (SRS), ISO/IEC/IEEE 29148, and Amazon technical specification standards.

Your task is to generate a professional Software Requirements Specification (SRS) for: **$ARGUMENTS**

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
- **Target Users**: Who are the primary users? What are their key workflows?
- **Feature Scope**: What are the main features and capabilities? What is explicitly out of scope?
- **Performance Requirements**: What are the expected response times, throughput, concurrency levels?
- **Security Requirements**: What authentication, authorization, and data protection is needed?
- **Data Requirements**: What data entities, relationships, and volumes are involved?
- **Integration Requirements**: What external systems, APIs, or services must integrate?
- **Success Criteria**: How will you measure whether this feature is successful?

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

## Output
1. Write the document to `docs/{slug}/srs.md`
2. Return: file path, 3-5 sentence summary, FR count, NFR count

---

## Next Steps

After the sub-agent returns, present the result to the user and suggest:

1. **Continue the spec chain**: Run `/tech-design` to design the technical architecture based on these requirements.
2. **Jump to testing**: Run `/test-plan` to go directly to test planning (standalone mode will compensate for the missing tech design).
3. **Ready to implement?** If the [code-forge](https://github.com/tercel/code-forge) plugin is installed, use `/code-forge:plan @docs/{slug}/srs.md` to convert SRS requirements into implementation tasks and execute them. If not, consider breaking the requirements into development tasks manually.
