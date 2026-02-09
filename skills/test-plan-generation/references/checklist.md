# Test Plan Quality Checklist

Use this checklist to validate the completed Test Plan before delivering it to stakeholders. Every item must be checked. If an item is intentionally skipped, add a justification note next to it.

---

## 1. Completeness Check

- [ ] All IEEE 829 sections are present in the document (Introduction, Test Strategy, Test Scope, Test Environment, Entry/Exit Criteria, Test Cases, Defect Management, Risk Assessment, Traceability Matrix, Schedule, Roles)
- [ ] Test strategy covers all applicable test levels: unit (pure logic), unit (DB-touching), integration, system, and acceptance
- [ ] **Database testing policy section is present** — explicitly defines when to use Real DB vs. Mock
- [ ] **Every test case that involves database operations specifies "Real DB"** as the DB approach — no DB mocking for internal data layer
- [ ] **Data integrity test cases are included** — unique constraints, FK constraints, cascade operations, transaction rollback, concurrent updates
- [ ] Both positive test cases (valid inputs, happy paths) and negative test cases (invalid inputs, error handling) are included for every in-scope feature
- [ ] Boundary value test cases are included for all inputs with defined ranges or limits — including min, max, below-min, above-max, zero, negative
- [ ] **Test cases include DB verification steps** — for write operations, expected results specify what to query and verify in the database, not just API response
- [ ] Entry criteria and exit criteria are explicitly defined with measurable thresholds
- [ ] Defect management process is defined including severity classification, lifecycle, and reporting template
- [ ] Requirements Traceability Matrix is complete with every in-scope SRS requirement mapped to at least one test case
- [ ] Test environment is fully specified including hardware, software, network configuration, and test data requirements
- [ ] **Test data management strategy is defined** — how test data is seeded, isolated between tests, and cleaned up

## 2. Quality Check

- [ ] Test cases are independent -- no test case depends on the execution or outcome of another test case
- [ ] Test steps are specific and reproducible -- use concrete values (e.g., `email: "test@example.com"`), not placeholders (e.g., `email: [valid email]`)
- [ ] Expected results are concrete and verifiable -- no vague language such as "works correctly" or "behaves as expected"
- [ ] **Expected results include DB state verification** — for every write operation, the expected result states what database query to run and what values to assert
- [ ] Preconditions clearly state the **exact database state** required (which records exist, their field values), not just "user is logged in"
- [ ] **No database method is tested with mocks** — every test touching repository/data layer/ORM uses a real database (TestContainers, test DB, or equivalent)
- [ ] **Mocks are used ONLY for external third-party services** — payment gateways, email/SMS providers, external APIs not under your control
- [ ] Performance benchmarks have measurable targets with specific numeric thresholds (response time, throughput, error rate)
- [ ] **Performance tests use production-like data volumes** — not empty databases
- [ ] Risk-based prioritization is applied -- high-risk areas have deeper coverage with more test cases and more edge case scenarios
- [ ] Critical user paths have comprehensive coverage including positive flows, negative flows, boundary values, and edge cases
- [ ] Security test cases address OWASP Top 10 categories relevant to the application

## 3. Consistency Check

- [ ] All test case IDs follow the TC-MODULE-NNN naming convention (e.g., TC-AUTH-001)
- [ ] Terminology and naming conventions are consistent with the upstream SRS and Technical Design documents
- [ ] Every in-scope SRS requirement (both FR and NFR) has at least one mapped test case in the traceability matrix
- [ ] Priority levels assigned to test cases are consistent with the risk assessment -- higher-risk areas have more P0/P1 test cases
- [ ] Test types listed in the test strategy section are reflected in the actual test case specifications
- [ ] Module names used in test case IDs match the module names defined in the SRS and Technical Design

## 4. Format Check

- [ ] Mermaid diagrams (defect lifecycle state diagram, Gantt chart) render correctly with valid syntax
- [ ] All test case specification tables are properly formatted with complete column headers and no missing cells
- [ ] Every section contains substantive content -- no section is left empty or contains only placeholder text
- [ ] Document metadata is complete: version, author, reviewers, date, status, and related document references are all filled in
- [ ] Traceability matrix links are valid -- all referenced SRS requirement IDs and test case IDs exist in their respective sections
- [ ] Tables use consistent formatting with aligned columns and uniform notation throughout the document
