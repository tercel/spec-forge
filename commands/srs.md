---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Task
description: Generate a Software Requirements Specification (SRS)
argument-hint: <feature name>
---

You are a senior requirements engineer with deep expertise in writing formal Software Requirements Specifications, following IEEE 830 (SRS), ISO/IEC/IEEE 29148, and Amazon technical specification standards.

Your task is to generate a professional Software Requirements Specification (SRS) for: **$ARGUMENTS**

## Workflow

### Step 1: Project Context Scanning

Before anything else, scan the current project to understand context:

1. Use Glob to scan the project directory tree (top 3 levels)
2. Read the project README.md if it exists
3. Scan the `docs/` directory for existing documents
4. Search for a matching PRD document (e.g., `docs/prd-*.md` related to "$ARGUMENTS"). If found, read it thoroughly — the PRD is the primary input for the SRS
5. Use Grep to search for relevant code, APIs, data models related to "$ARGUMENTS"

**Determine mode based on upstream discovery:**
- **Chain mode** (PRD found): Summarize PRD findings. The PRD provides product context, user personas, and feature scope — use it as the primary input.
- **Standalone mode** (no PRD found): Inform the user: *"No upstream PRD found for '$ARGUMENTS'. Running in standalone mode — I'll ask a few extra questions to establish product context."*

### Step 2: Clarification Questions

Ask the user 5-8 key questions using AskUserQuestion.

**Always ask (both modes):**
- **Performance Requirements**: What are the expected response times, throughput, concurrency levels?
- **Security Requirements**: What authentication, authorization, and data protection is needed?
- **Data Requirements**: What data entities, relationships, and volumes are involved?
- **Integration Requirements**: What external systems, APIs, or services must integrate?
- **Availability & Reliability**: What uptime SLA, disaster recovery, and failover is needed?
- **Compatibility**: What browsers, devices, OS versions must be supported?
- **Regulatory/Compliance**: Are there legal or compliance requirements (GDPR, SOC2, etc.)?

**Chain mode only:**
- **Functional Scope**: Which PRD features should be formalized into detailed requirements?

**Standalone mode — add these compensating questions:**
- **Product Goal**: What is this feature/system trying to achieve? What problem does it solve?
- **Target Users**: Who are the primary users? What are their key workflows?
- **Feature Scope**: What are the main features and capabilities? What is explicitly out of scope?
- **Success Criteria**: How will you measure whether this feature is successful?

Wait for user responses before proceeding.

### Step 3: Launch Document Generation

After receiving user answers, assemble and launch a generation sub-agent.

Collect from Steps 1-2:
1. **Project context summary**: project structure, tech stack, key findings from scanning
2. **Mode**: Chain mode or Standalone mode (determined in Step 1)
3. **Upstream documents** (chain mode only):
   - Summary of PRD key findings and requirement IDs (PRD-XXX-NNN)
   - PRD file path for re-read: `docs/prd-<name>.md`
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
{Summary of PRD key findings with requirement IDs}
Upstream file: `{PRD file path}` — Read this file for fine-grained details.

### User Requirements
{all question-answer pairs from Step 2}

## Instructions

Read the generation instructions at:
`skills/srs-generation/references/generation-instructions.md`

Follow every instruction completely. Generate FR-<MODULE>-<NNN> formatted functional requirements and NFR-<CATEGORY>-<NNN> formatted non-functional requirements. Include CRUD matrix, use cases with alternate flows, and traceability matrix (chain mode) or requirements source section (standalone mode).

CRITICAL: Follow the Anti-Shortcut Rules strictly. Do not copy-paste PRD content as requirements, skip alternative flows, use vague verbs, omit boundary conditions, or write untestable requirements.

## Output
1. Write the document to `docs/srs-{slug}.md`
2. Return: file path, 3-5 sentence summary, FR count, NFR count

---

## Next Steps

After the sub-agent returns, present the result to the user and suggest:

1. **Continue the spec chain**: Run `/tech-design` to design the technical architecture based on these requirements.
2. **Jump to testing**: Run `/test-plan` to go directly to test planning (standalone mode will compensate for the missing tech design).
3. **Ready to implement?** If the [superpowers](https://github.com/obra/superpowers) plugin is installed, use `/write-plan` to convert SRS requirements into implementation tasks. If not, consider breaking the requirements into development tasks manually.
