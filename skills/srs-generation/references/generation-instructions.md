# SRS Generation Instructions

Follow these steps exactly to generate the SRS document.

**What this document is.** The SRS is the delivery contract — what an implementation team, an external vendor, or code-forge is held to, and what acceptance is settled against. A requirements document that merely *describes* the system is not sufficient; this one must be precise enough that two readers cannot reasonably disagree about what was promised.

## Step 1: Generate Document

Load and follow the SRS template from the skill reference file at:
`skills/srs-generation/references/template.md`

Generate the complete SRS following the template structure. Key requirements:
- Functional requirement IDs: FR-<MODULE>-<NNN> (e.g., FR-AUTH-001)
- Non-functional requirement IDs: NFR-<CATEGORY>-<NNN> (e.g., NFR-PERF-001)
- Each functional requirement must include: description, actors, preconditions, **input field rules**, main flow, alternative flows, postconditions, acceptance criteria, priority with rationale, and source
- Each non-functional requirement must include: description, metric, target value, measurement method, **verification method**, and threshold rationale
- Include a CRUD matrix for data operations
- Include use case descriptions with actors, preconditions, main flow, alternate flows, postconditions

### The six contractual sections

These distinguish a delivery contract from a description. Each is mandatory wherever it applies; where one genuinely does not apply, mark it **N/A with a one-line reason** rather than deleting the heading — a missing section reads as an oversight, a section marked "N/A: no entity in this feature has a lifecycle" reads as a decision.

1. **§3.2 Scope Boundaries — the out-of-scope table.** Every row names an exclusion a reader might reasonably assume is included, why it is excluded, and who owns it instead. An empty table fails review. Ambiguity about what is *not* included is the single most common source of delivery disputes, because each side fills the gap with a different assumption and both only discover it at acceptance. Also state the interpretation precedence between this document, the PRD, the tech design, and verbal agreements.

2. **Input Field Rules — per requirement.** For every field an actor can supply: type, required, exact constraints, default, and the boundary/rejection behavior naming a code from the Error Catalogue. State exact values, never categories — "max 254 characters" not "reasonable length", "1 ≤ n ≤ 999" not "a positive number". A category is negotiable at acceptance time; an exact rule is not.

3. **§5.4 State Machines — including illegal transitions.** For every entity with a lifecycle: the diagram, the legal-transition table (trigger, actor, guard, governing FR), and the **illegal-transition handling** table. Specifying only the legal transitions is half a state machine — every transition not listed must have a defined rejection behavior, stating whether it is idempotent-ignored or hard-rejected and whether side effects fire on rejection.

4. **§5.5 Permission Matrix.** Role × operation × data scope, with each data scope defined as a concrete predicate ("records where `owner_id` equals the authenticated principal") rather than prose. State the denial behavior deliberately: `403 Forbidden` reveals that the record exists, `404 Not Found` conceals it. That is a security decision belonging in the requirements.

5. **§5.6 Error Catalogue.** Every anticipated failure as a distinct diagnosable code with its trigger, actor-visible message, recovery path, and originating requirement. `INTERNAL_ERROR` standing in for an anticipated condition fails review. For every external dependency, state the degradation behavior when it is unavailable: fail closed, fail open, serve stale data (with the acceptable staleness), or queue for retry (with the retry window).

6. **§10 Acceptance and Change Control.** What acceptance means per requirement class and how each is verified; the acceptance environment, test data, window, and defect classification; the change-control procedure including impact assessment and propagation; the change request log. Requirement IDs are contract references — never silently renumbered or repurposed.

## Step 2: Traceability Matrix

**Chain mode** (PRD found):
- Create a requirements traceability matrix mapping PRD items → SRS requirements
- Every PRD feature should map to at least one SRS functional requirement
- Flag any PRD items that are not covered by the SRS

**Standalone mode** (no PRD):
- Skip the PRD traceability matrix
- Instead, include a "Requirements Source" section noting that requirements were derived from user clarification (not an upstream PRD)
- Add a note: *"To establish full traceability, consider running `/spec-forge:prd` first, then re-running `/spec-forge:srs`."*

## Step 3: Quality Check

Load the quality checklist from:
`skills/srs-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 4: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/<feature-name>/srs.md`
4. Confirm the file path and provide a brief summary

## Important Guidelines

- Requirements must be unambiguous — each requirement should have exactly one interpretation
- Requirements must be testable — each must have clear acceptance criteria
- Requirements must be traceable — link back to PRD items where applicable
- Use "shall" for mandatory requirements, "should" for recommended, "may" for optional
- Avoid implementation details — describe WHAT, not HOW
- Include boundary conditions and error scenarios for each requirement
- **Consumer-aware requirements**: If the upstream PRD (§10.1) marks AI Agent as an applicable consumer, ensure that: (1) §4.3 User Characteristics includes agent user classes with Consumer Type, Interaction Pattern, and autonomy level; (2) functional requirements where the primary actor is an agent use programmatic flows (API calls, not UI steps); (3) error responses for agent-facing requirements include structured, machine-parseable fields (error_code, message, field, constraint) — not just human-readable text; (4) acceptance criteria for agent-facing requirements include idempotency, deterministic schema, and timeout behavior conditions where relevant

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality SRS documents:

1. **Do NOT copy-paste PRD content as requirements.** The PRD describes *what the product should be*; the SRS must specify *what the system shall do* in precise, testable terms. Simply rephrasing PRD bullets is not requirements engineering.
2. **Do NOT skip alternative flows and exception scenarios.** Every use case has error paths, edge cases, and recovery scenarios. Writing only the happy path is incomplete. Each functional requirement must include alternative and exception flows. **Every operation error must report the real, specific cause** — name exactly what failed (which field, which rule, which entity, which state), never "the operation fails" or "a server error." Enumerate each *anticipated* failure as a distinct, distinguishable flow (invalid input, uniqueness violation, missing reference, invalid state transition, insufficient permission, not-found, and any requirement-specific business-rule violation). This is what lets the downstream tech-design map each cause to a specific error code instead of a generic 500.
3. **Do NOT use vague verbs.** Words like "handle", "manage", "process", or "support" are ambiguous. Replace with specific behaviors: "validate", "reject with error code 422", "persist to the `orders` table", "return within 200ms".
4. **Do NOT omit boundary conditions.** Every input field, parameter, and data entity has limits. If you don't specify min/max lengths, allowed characters, and range constraints, engineers will guess differently.
5. **Do NOT write untestable requirements.** If a requirement cannot be verified by a concrete test case, it is not a valid requirement. Every requirement must have measurable acceptance criteria (Given/When/Then or explicit conditions). A criterion whose pass/fail depends on reviewer judgement is a defect in the specification, not a matter to resolve at acceptance time.
6. **Do NOT leave the out-of-scope table empty.** "Nothing was excluded" is almost never true, and when it is, it needs saying explicitly with a justification. An empty table does not mean nothing is excluded — it means the exclusions are unwritten, and unwritten exclusions get built or get disputed.
7. **Do NOT specify only the happy state transitions.** Every state machine needs its illegal-transition behavior defined. Leaving it unstated means the behavior is whatever the implementation happens to do, discovered at acceptance.
8. **Do NOT leave degradation unspecified.** For each external dependency, state what happens when it is unavailable. Unstated degradation behavior under partial outage is the failure mode that reaches production untested.
9. **Do NOT invent an acceptance environment.** If you do not know where acceptance happens, what test data it uses, or who signs off, record those as open questions in §11.B rather than filling the table with plausible-sounding defaults. A fabricated acceptance environment is worse than an acknowledged gap.
