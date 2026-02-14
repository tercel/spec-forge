# SRS Generation Instructions

Follow these steps exactly to generate the SRS document.

## Step 1: Generate Document

Load and follow the SRS template from the skill reference file at:
`skills/srs-generation/references/template.md`

Generate the complete SRS following the template structure. Key requirements:
- Functional requirement IDs: FR-<MODULE>-<NNN> (e.g., FR-AUTH-001)
- Non-functional requirement IDs: NFR-<CATEGORY>-<NNN> (e.g., NFR-PERF-001)
- Each functional requirement must include: description, input/output, acceptance criteria, priority
- Each non-functional requirement must include: description, metric, target value, measurement method
- Include a CRUD matrix for data operations
- Include use case descriptions with actors, preconditions, main flow, alternate flows, postconditions

## Step 2: Traceability Matrix

**Chain mode** (PRD found):
- Create a requirements traceability matrix mapping PRD items → SRS requirements
- Every PRD feature should map to at least one SRS functional requirement
- Flag any PRD items that are not covered by the SRS

**Standalone mode** (no PRD):
- Skip the PRD traceability matrix
- Instead, include a "Requirements Source" section noting that requirements were derived from user clarification (not an upstream PRD)
- Add a note: *"To establish full traceability, consider running `/prd` first, then re-running `/srs`."*

## Step 3: Quality Check

Load the quality checklist from:
`skills/srs-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 4: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/srs-<feature-name>.md`
4. Confirm the file path and provide a brief summary

## Important Guidelines

- Requirements must be unambiguous — each requirement should have exactly one interpretation
- Requirements must be testable — each must have clear acceptance criteria
- Requirements must be traceable — link back to PRD items where applicable
- Use "shall" for mandatory requirements, "should" for recommended, "may" for optional
- Avoid implementation details — describe WHAT, not HOW
- Include boundary conditions and error scenarios for each requirement

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality SRS documents:

1. **Do NOT copy-paste PRD content as requirements.** The PRD describes *what the product should be*; the SRS must specify *what the system shall do* in precise, testable terms. Simply rephrasing PRD bullets is not requirements engineering.
2. **Do NOT skip alternative flows and exception scenarios.** Every use case has error paths, edge cases, and recovery scenarios. Writing only the happy path is incomplete. Each functional requirement must include alternative and exception flows.
3. **Do NOT use vague verbs.** Words like "handle", "manage", "process", or "support" are ambiguous. Replace with specific behaviors: "validate", "reject with error code 422", "persist to the `orders` table", "return within 200ms".
4. **Do NOT omit boundary conditions.** Every input field, parameter, and data entity has limits. If you don't specify min/max lengths, allowed characters, and range constraints, engineers will guess differently.
5. **Do NOT write untestable requirements.** If a requirement cannot be verified by a concrete test case, it is not a valid requirement. Every requirement must have measurable acceptance criteria (Given/When/Then or explicit conditions).
