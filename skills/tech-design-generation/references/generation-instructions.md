# Tech Design Generation Instructions

Follow these steps exactly to generate the Technical Design Document.

## Step 1: Generate Document

Load and follow the tech design template from the skill reference file at:
`skills/tech-design-generation/references/template.md`

Generate the complete technical design document. Key requirements:
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

**Chain mode** (upstream docs found):
- Map SRS functional requirements to technical components
- Map SRS non-functional requirements to architecture decisions
- Ensure all FR/NFR items are addressed in the design

**Standalone mode** (no upstream docs):
- Skip the SRS traceability matrix
- Instead, include a "Design Inputs" section summarizing the requirements derived from user clarification
- Add a note: *"To establish full traceability, consider running `/prd` → `/srs` first, then re-running `/tech-design`."*

## Step 3: Quality Check

Load the quality checklist from:
`skills/tech-design-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 4: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/tech-design-<feature-name>.md`
4. Confirm the file path and provide a brief summary

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
