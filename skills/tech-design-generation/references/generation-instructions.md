# Tech Design Generation Instructions

Follow these steps exactly to generate the Technical Design Document.

> **Step correspondence**: These 5 steps map to the SKILL.md 7-step workflow as follows:
> - Step 1 (Generate Document) → SKILL.md Step 4
> - Step 2 (Traceability) → SKILL.md Step 5
> - Step 3 (Quality Check) → SKILL.md Step 6
> - Step 4 (Write Output) → SKILL.md Step 4 (write phase)
> - Step 5 (Generate Feature Specs) → SKILL.md Step 7
>
> Steps 1-3 of SKILL.md (codebase scan, upstream search, clarification questions) are performed by the
> orchestrator in `commands/tech-design.md` before this sub-agent is launched.

## Step 1: Generate Document

Load and follow the tech design template from the skill reference file at:
`skills/tech-design-generation/references/template.md`

Generate the complete technical design document. Key requirements:
- **§3.5 User Scenarios**: Write 1-3 concrete end-to-end narratives. Each scenario must name a specific persona, a Type (Human or Agent), a specific goal, numbered steps, and a measurable success condition. Do NOT write generic scenarios like "User uses the feature successfully" — they must be specific enough that a QA engineer can derive a test case. If the upstream PRD marks AI Agent as an applicable consumer (§10.1), include at least one Agent scenario with programmatic steps (API calls, not UI clicks) and machine-verifiable success conditions (deterministic schema, idempotent behavior, structured error codes). If no upstream PRD exists, explicitly consider whether agents are realistic consumers before omitting agent scenarios.
- **§3.6 Acceptance Criteria**: Write 5-15 testable AC entries mapping to the user scenarios. Each AC must be verifiable — specify the exact API call, test type, and assertion. ACs drive the Acceptance Criteria section in each feature spec. If an idea draft exists (idea-first mode), extract the MVP requirements and success criteria from it as inputs for the AC table.
- **§3.7 Success Metrics**: Define 2-5 measurable metrics with baselines and targets. Metrics must be observable (tied to specific events or data sources), not aspirational. If standalone mode (no PRD), derive metrics from the idea draft's "Demand Validation" section if available.
- Include at least 2 alternative solutions with a comparison matrix
- **Technology Stack**: Specify exact language, framework, runtime, ORM, database, cache, and all dependencies with version numbers and rationale
- **Naming Conventions**: Define complete naming rules for code (files, classes, functions, variables, constants), API (URLs, params, fields, error codes), and database (tables, columns, indexes, constraints)
- **Parameter Validation**: For EVERY API parameter, define: type, required/optional, min/max, regex pattern, default value, sanitization rules, and specific error messages. No parameter left unspecified.
- **Boundary Values**: Define explicit system limits (request size, field lengths, array sizes, rate limits, pagination caps) with exact behavior when exceeded
- **Edge Cases**: Document handling for: empty input, unicode, duplicate requests, concurrent updates, null vs zero, timezone, numeric overflow
- **Business Logic**: Document all state machines (with guard conditions and side effects per transition), computation rules (with precision and examples), and conditional logic (with explicit true/false branches)
- **Error Handling**: Define error taxonomy with HTTP status, error codes, retry strategy, circuit breaker config, and fallback behavior for every external dependency
- Use Mermaid for all diagrams:
  - C4 Context Diagram (system context)
  - C4 Container Diagram (high-level architecture)
  - Component Diagram (detailed module design)
  - Sequence Diagram (core workflows)
  - State Machine Diagram (if applicable)
- API design must include: endpoints, methods, request/response schemas, error codes
- Database design must include: schema definitions, ER diagram (Mermaid), index strategy, migration plan
- Security section must cover: authentication, authorization, data encryption, audit logging
- Performance section must include: target metrics, caching strategy, optimization techniques

## Step 2: Traceability

**Upstream mode** (PRD/SRS found):
- Map SRS functional requirements to technical components
- Map SRS non-functional requirements to architecture decisions
- Ensure all FR/NFR items are addressed in the design

**Idea-first or Standalone mode** (no PRD/SRS):
- Skip the SRS traceability matrix
- Instead, include a "Design Inputs" section summarizing the requirements derived from the idea draft (idea-first mode) or user clarification (standalone mode)

## Step 3: Quality Check

Load the quality checklist from:
`skills/tech-design-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 4: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/<feature-name>/tech-design.md`
4. Confirm the file path and provide a brief summary

## Step 5: Generate Feature Specs

After writing the main tech-design document, generate individual feature spec files from the Component Overview table in §8.

1. **Extract components**: For each row in §8.1 Component Overview, create a feature spec at `docs/features/{component-name}.md`
2. **Populate implementation detail**: Each feature spec contains the implementation-level content — method signatures, logic steps, field mapping tables, state machines, default values, error handling specifics. This is the depth that would traditionally live in §8 but now lives in per-component files for code-forge consumption.
3. **Assign metadata**: Use the component slug (filename without `.md`) as the stable identifier for all cross-references in `Depends On` / `Blocks` fields. Do NOT assign numeric IDs (F-01, F-02, ...), do NOT prefix filenames with numbers (01-, 02-...), and do NOT include order numbers in feature spec titles or headings. Execution order is defined exclusively in the `#` column of the Features table in `overview.md`. Map SRS requirement IDs from the Traceability Matrix. Derive priority from requirement priorities.
4. **Generate overview**: Create or update `docs/features/overview.md` with the feature table, dependency graph, and execution order. If the file already exists (e.g., from a prior sub-feature in a multi-split project), merge the new components into the existing table rather than overwriting.
5. **Cross-reference**: Ensure each feature spec's SRS Refs field matches the Traceability Matrix in the main tech-design document. Ensure Depends On / Blocks fields use component slugs and form a consistent dependency graph. Verify all referenced slugs correspond to actual files in `docs/features/`.

Read `skills/tech-design-generation/SKILL.md` and locate Step 7 (Feature Spec Generation) — it contains the Feature Spec Template you must use for each component file.

**Anti-Shortcut Rules for Feature Specs:**
- Do NOT generate empty-shell feature specs with just section headings and no content
- Do NOT write "see tech-design for details" — the feature spec must be self-contained for implementation
- Do NOT skip the metadata header (Component slug, SRS Refs, Dependencies) — code-forge:plan relies on it
- Do NOT duplicate system-level content (API specs, DB schema, security design) — only component internals
- Do NOT leave Acceptance Criteria empty or write "TBD" — map relevant ACs from §3.6, add component-specific ones
- Do NOT add numeric prefixes, order numbers, or IDs to feature spec titles or filenames — ordering lives exclusively in `overview.md`
- Do NOT write placeholder File Structure or Test Module — derive actual paths from the project structure
- File Structure must use real source root, real file extension, and real module path derived from the architecture
- Test Module must name the exact test file path and list specific functions/methods to unit test

## Important Guidelines

- **Implementation-ready detail**: The document should be detailed enough that an engineer can implement without asking clarifying questions. Vague specs like "validate input appropriately" or "handle errors gracefully" are NOT acceptable — specify exact rules.
- **Every parameter defined**: No API parameter should lack a type, range, format, or error message. If you don't define the boundary, engineers will guess differently.
- **Every edge case addressed**: If the system can receive empty input, nulls, duplicates, or concurrent writes, the design must say what happens. Silence is ambiguity.
- **Business logic is unambiguous**: State transitions need guard conditions. Formulas need precision and rounding rules. Conditions need both the true AND false branch.
- Always present the recommended solution first, then alternatives
- Decision rationale must be explicit — explain WHY, not just WHAT
- Diagrams should be self-explanatory with proper labels and legends
- API designs should follow RESTful conventions unless there's a specific reason not to
- Consider backward compatibility and migration paths
- Address failure modes and error handling for every component
- Include rollback strategy for deployments
- Keep security as a first-class concern, not an afterthought

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality tech designs:

1. **Do NOT present only one solution disguised as a comparison.** The plan requires at least 2 genuine alternatives with honest trade-off analysis. Adding a straw-man "do nothing" option does not count.
2. **Do NOT use "handle appropriately" or "validate as needed".** Every error condition must specify the exact HTTP status code, error code, retry behavior, and user-facing message. Every validation rule must specify the exact type, range, pattern, and error response.
3. **Do NOT omit parameter validation details.** Every API parameter must have: type, required/optional, min/max, regex pattern, default value, sanitization rule, and specific error message. No parameter may be left unspecified.
4. **Do NOT draw empty-shell Mermaid diagrams.** Every node must have a label. Every arrow must have a description. Diagrams without annotations are decoration, not documentation. If a diagram doesn't add information beyond the text, remove it.
5. **Do NOT write "details to follow" or "TBD" without a concrete follow-up plan.** If a section is incomplete, state what is unknown, what is needed to resolve it, and who is responsible. Open questions must be logged in the document's Open Questions section.
