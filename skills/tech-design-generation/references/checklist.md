# Technical Design Document Quality Checklist

Use this checklist to validate the Technical Design Document before finalizing. Every item must pass or be explicitly marked as not applicable with justification.

---

## 1. Completeness Check

- [ ] §3.5 User Scenarios are present with at least 1 concrete persona/goal/steps/success-condition (not generic placeholders), each row includes a Type column (Human or Agent)
- [ ] If upstream PRD marks AI Agent as applicable (§10.1), at least one Agent scenario is present with programmatic steps and machine-verifiable success conditions
- [ ] If no upstream PRD exists, a conscious decision about agent consumers is documented (either an Agent scenario is included, or a note explains why agents are not applicable)
- [ ] §3.6 Acceptance Criteria table has at least 5 testable entries with AC-IDs, criteria, and verification methods
- [ ] §3.7 Success Metrics has at least 2 measurable metrics with baselines, targets, and measurement methods
- [ ] Architecture diagrams are included at the appropriate C4 levels (at minimum Context and Container)
- [ ] At least two alternative solutions are described and compared
- [ ] Technology stack table is complete with language, framework, runtime versions, and rationale for each choice
- [ ] Naming conventions are defined for code (files, classes, functions, variables), API (URLs, params, fields), and database (tables, columns, indexes)
- [ ] Parameter validation rules matrix covers every external input with type, min/max, pattern, default, and error messages
- [ ] Boundary values and system limits are documented with explicit behavior when exceeded
- [ ] Edge cases table covers at minimum: empty input, unicode, duplicate requests, concurrent updates, null vs zero, timezone handling
- [ ] Business logic rules are documented: state machine (if applicable), computation formulas with precision, conditional logic
- [ ] Error handling taxonomy covers all HTTP error categories with retry strategy and user-facing messages
- [ ] Retry and circuit breaker configuration is defined for every external dependency
- [ ] API specifications are complete with endpoints, methods, request/response schemas, and error codes
- [ ] Database schema is defined with table structures, column types, and constraints
- [ ] Security design is addressed covering authentication, authorization, encryption, and audit logging
- [ ] Performance targets are set with specific, measurable values and measurement methods
- [ ] Deployment plan is included with environments, CI/CD pipeline, and rollback strategy
- [ ] Observability is covered with logging, monitoring, and alerting strategies
- [ ] Testing strategy overview is present with coverage at unit, integration, and E2E levels
- [ ] Feature specs are generated in `docs/features/` for every component in §8.1 Component Overview
- [ ] Feature spec overview file (`docs/features/overview.md`) is generated with dependency graph and execution order
- [ ] Each feature spec contains implementation-level detail (method signatures, logic steps, field mappings), not just section headings
- [ ] Each feature spec Acceptance Criteria section has at least 1 testable entry (not a placeholder)
- [ ] Each feature spec File Structure uses real source paths and file extensions, not placeholders
- [ ] Each feature spec Test Module names the exact test file path and lists specific methods to test
- [ ] Feature specs have NO numeric IDs, order prefixes, or sequence numbers in titles or filenames — ordering lives only in `overview.md`'s `#` column

## 2. Quality Check

- [ ] Decision rationale is explicit for the recommended solution, explaining why it was chosen over alternatives
- [ ] Technology choices have clear rationale — not just "popular" but justified by project needs
- [ ] Naming conventions are consistent with the chosen language/framework ecosystem conventions
- [ ] Every validation rule specifies exact min/max values (not "reasonable length" or "appropriate size")
- [ ] Boundary values have concrete numbers (not "configurable" without stating the default)
- [ ] Business logic computation rules include precision, rounding strategy, and worked examples
- [ ] State machine transitions include guard conditions and side effects, not just from→to
- [ ] Error taxonomy distinguishes client-retryable vs non-retryable errors clearly
- [ ] All diagrams are clear, properly labeled, and have descriptive titles
- [ ] API design follows RESTful conventions (or deviation is justified with a stated reason)
- [ ] Performance targets are specific and measurable (not vague terms like "fast" or "scalable")
- [ ] Security design considers OWASP Top 10 risks relevant to the system
- [ ] Backward compatibility is considered for APIs, database schema, and data formats
- [ ] Milestones and task breakdown are realistic with reasonable time estimates

## 3. Consistency Check

- [ ] Design aligns with SRS functional requirements (all FR items are traceable to design components)
- [ ] Design aligns with SRS non-functional requirements (all NFR items are traceable to architecture decisions)
- [ ] Terminology matches upstream documents (PRD and SRS) and uses consistent naming throughout
- [ ] API endpoint naming is consistent (same pluralization, casing, and versioning pattern throughout)
- [ ] Component names match across all diagrams (context, container, component, and sequence diagrams use the same names)
- [ ] Data model in schema design matches the ER diagram and aligns with API request/response schemas

## 4. Format Check

- [ ] All Mermaid diagrams use the correct ` ```mermaid ` fence and render without syntax errors
- [ ] All tables are properly formatted with consistent column alignment and no missing cells
- [ ] JSON examples in API specifications are valid and properly formatted
- [ ] No sections are left empty (every section has meaningful content or is marked as not applicable with justification)
- [ ] Document metadata is complete (version, author, reviewers, date, status, and related document references)
- [ ] Open questions table is populated (at least reviewed, even if no questions remain open)
