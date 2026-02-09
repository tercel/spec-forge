---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
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

### Step 3: Document Generation

Load and follow the SRS template from the skill reference file at:
`skills/srs-generation/references/template.md`

Generate the complete SRS following the template structure. Key requirements:
- Functional requirement IDs: FR-<MODULE>-<NNN> (e.g., FR-AUTH-001)
- Non-functional requirement IDs: NFR-<CATEGORY>-<NNN> (e.g., NFR-PERF-001)
- Each functional requirement must include: description, input/output, acceptance criteria, priority
- Each non-functional requirement must include: description, metric, target value, measurement method
- Include a CRUD matrix for data operations
- Include use case descriptions with actors, preconditions, main flow, alternate flows, postconditions

### Step 4: Traceability Matrix

**Chain mode** (PRD found):
- Create a requirements traceability matrix mapping PRD items → SRS requirements
- Every PRD feature should map to at least one SRS functional requirement
- Flag any PRD items that are not covered by the SRS

**Standalone mode** (no PRD):
- Skip the PRD traceability matrix
- Instead, include a "Requirements Source" section noting that requirements were derived from user clarification (not an upstream PRD)
- Add a note: *"To establish full traceability, consider running `/prd` first, then re-running `/srs`."*

### Step 5: Quality Check

Load the quality checklist from:
`skills/srs-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

### Step 6: Write Output

1. Sanitize the feature name from $ARGUMENTS to create a filename slug
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/srs-<feature-name>.md`
4. Confirm the file path to the user and provide a brief summary

## Important Guidelines

- Requirements must be unambiguous — each requirement should have exactly one interpretation
- Requirements must be testable — each must have clear acceptance criteria
- Requirements must be traceable — link back to PRD items where applicable
- Use "shall" for mandatory requirements, "should" for recommended, "may" for optional
- Avoid implementation details — describe WHAT, not HOW
- Include boundary conditions and error scenarios for each requirement

### Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality SRS documents:

1. **Do NOT copy-paste PRD content as requirements.** The PRD describes *what the product should be*; the SRS must specify *what the system shall do* in precise, testable terms. Simply rephrasing PRD bullets is not requirements engineering.
2. **Do NOT skip alternative flows and exception scenarios.** Every use case has error paths, edge cases, and recovery scenarios. Writing only the happy path is incomplete. Each functional requirement must include alternative and exception flows.
3. **Do NOT use vague verbs.** Words like "handle", "manage", "process", or "support" are ambiguous. Replace with specific behaviors: "validate", "reject with error code 422", "persist to the `orders` table", "return within 200ms".
4. **Do NOT omit boundary conditions.** Every input field, parameter, and data entity has limits. If you don't specify min/max lengths, allowed characters, and range constraints, engineers will guess differently.
5. **Do NOT write untestable requirements.** If a requirement cannot be verified by a concrete test case, it is not a valid requirement. Every requirement must have measurable acceptance criteria (Given/When/Then or explicit conditions).

## Next Steps

After the SRS is complete, suggest the following to the user:

1. **Continue the spec chain**: Run `/tech-design` to design the technical architecture based on these requirements.
2. **Jump to testing**: Run `/test-plan` to go directly to test planning (standalone mode will compensate for the missing tech design).
3. **Ready to implement?** If the [superpowers](https://github.com/obra/superpowers) plugin is installed, use `/write-plan` to convert SRS requirements into implementation tasks. If not, consider breaking the requirements into development tasks manually.
