# Test Cases Quality Checklist

Use this checklist to validate the completed test cases document before delivery. Every item must be checked. Items marked **(conditional)** should be skipped with justification if the condition doesn't apply to this project.

---

## 1. Project Profile Check

- [ ] Project type is identified in Section 1.1 (REST API / Function Library / CLI / Frontend / AI Agent / etc.)
- [ ] Test case format (Preconditions, Steps, Expected Result) matches the project type — not forced into HTTP patterns for non-HTTP projects
- [ ] Only relevant sections are included — irrelevant sections are omitted, not filled with placeholder content

## 2. Functional Inventory Check

- [ ] All testable units in scope are listed in the Functional Inventory (Section 1.2)
- [ ] Each unit has correct type, file path, and coverage status
- [ ] Interaction map identifies units with dependencies or data flow relationships
- [ ] Coverage summary accurately reflects existing test coverage

## 3. Coverage Depth Check

- [ ] Every testable unit has at least 1 × L1 (Happy Path) test case
- [ ] Every testable unit has at least 2 × L2 (Boundary/Error) test cases — at least one boundary and one error
- [ ] Every testable unit has at least 1 × L3 (Negative) test case — a "should NOT happen" scenario
- [ ] High-risk units (P0 priority areas) have additional cases beyond the minimum
- [ ] L3 cases clearly describe what should NOT be triggered, not just what should happen

## 4. Dimension Check

- [ ] Built-in dimension (Coverage Depth L1/L2/L3) is applied to all units
- [ ] Auto-detected dimensions are listed with rationale for inclusion
- [ ] Dimension-specific test cases exist for each detected dimension value
- [ ] Dimension combinations use risk-based prioritization, not blind Cartesian product

## 5. Combination Check

- [ ] Interaction pairs from the Interaction Map (Section 1.4) have corresponding combination test cases
- [ ] Each high-risk interaction pair has at least: 1 × L1 (both succeed), 1 × L2 (one fails), 1 × L3 (should not combine)
- [ ] Combination cases test the interaction behavior, not just individual unit behavior repeated

## 6. Test Case Quality Check

- [ ] All test case IDs follow TC-MODULE-NNN format (e.g., TC-AUTH-001, TC-PARSE-001, TC-CLI-001)
- [ ] All titles follow pattern: [action] [condition] [expected outcome]
- [ ] Preconditions specify exact state — adapted to project type (DB records / file state / env vars / props / context)
- [ ] Steps use concrete test data (`name: "John Doe"`, `--env staging`, `count: 42`), not placeholders
- [ ] Expected results specify exact output — adapted to project type (HTTP status / return value / exit code / rendered output)
- [ ] Expected results include state verification where applicable (DB query / file check / store assertion / context change)
- [ ] "Not Expected" field is filled for L3 cases (mandatory) and recommended for L2 cases
- [ ] Each test case is independent — no case depends on another case's execution

## 7. External Dependency Check

- [ ] **(conditional: project has database)** Every test case touching the database specifies "Real DB" — no DB mocking for internal data layer
- [ ] **(conditional: project has database)** Data Integrity cases are present: unique constraints, FK constraints, cascade operations, transaction rollback, concurrent updates
- [ ] **(conditional: project has file I/O)** File operations use real temp directories, not mocked file systems
- [ ] Own dependencies (DB, file system, cache, queue) are tested for real — mocks used ONLY for external third-party services
- [ ] Test case preconditions indicate how test state should be set up (seed records, create temp files, configure mocks)

## 8. Coverage Matrix Check

- [ ] Unit × Depth matrix (Section 7.1) has no empty cells for in-scope units
- [ ] Dimension coverage matrix (Section 7.2) shows coverage for all dimension values
- [ ] Combination coverage (Section 7.3) lists all high-risk interaction pairs
- [ ] Category distribution only includes categories relevant to this project — no forced categories
- [ ] Priority distribution is reasonable (not >50% P2, P0 should cover critical paths)
- [ ] Gap Analysis (Section 7.6) identifies all coverage gaps with recommendations

## 9. Strategy Check

- [ ] Test pyramid distribution has project-specific rationale (not generic percentages)
- [ ] External dependency policy clearly states what to test for real vs. mock — adapted to project type
- [ ] Risk-based prioritization includes concrete reasoning for each risk area
- [ ] Test methods (black-box, white-box, gray-box) are identified

## 10. Traceability Check

- [ ] If upstream SRS/Tech Design exists: Requirements Traceability Matrix maps every requirement to test cases
- [ ] If no upstream docs: Test Coverage Summary maps cases to functional inventory
- [ ] Any coverage gaps are flagged with explanation and remediation plan

## 11. Format Check

- [ ] All tables are properly formatted with complete headers and no missing cells
- [ ] Statistics section accurately reflects the actual test case counts
- [ ] No section contains only placeholder text — all content is substantive
- [ ] Document is structured for downstream consumption by code-forge:tdd

## 12. Formal Mode Check (only when --formal flag is set)

- [ ] Document information is complete (version, author, date, status)
- [ ] Test environment specifications are filled in
- [ ] Entry and exit criteria have measurable thresholds
- [ ] Test data management strategy covers setup, isolation, and cleanup approaches
- [ ] Defect management process includes severity classification and lifecycle
- [ ] Risk assessment includes reasoning for likelihood and impact ratings
- [ ] Test schedule has realistic dates and milestones
- [ ] Roles and responsibilities are assigned
