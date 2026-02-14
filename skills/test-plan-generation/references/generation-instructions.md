# Test Plan Generation Instructions

Follow these steps exactly to generate the Test Plan document.

## Step 1: Generate Document

Load and follow the test plan template from the skill reference file at:
`skills/test-plan-generation/references/template.md`

Generate the complete test plan document. The PRIMARY PURPOSE is to guide engineers in writing implementation-ready test cases. Key requirements:

**Database Testing Policy (CRITICAL):**
- **Any method that touches the database must be tested against a REAL database, NOT a mock**
- Use TestContainers, test database instances, or equivalent — never mock your own DB, cache, or message queue
- Mocks are acceptable ONLY for external third-party APIs you don't control (payment gateways, email services, etc.)
- Every test case must specify its DB approach: "Real DB" or "Mock external" (with justification)
- Include a dedicated "Data Integrity Test Cases" section covering: unique constraints, FK constraints, cascade operations, transaction rollback, concurrent update handling

**Test Case Writing Standards:**
- Test case IDs: TC-<MODULE>-<NNN> (e.g., TC-AUTH-001)
- Test strategy should follow the test pyramid (Unit → Integration → E2E), with unit tests split into "pure logic" and "DB-touching"
- Each test case must include: ID, title, module, preconditions (including exact DB state), detailed steps (with concrete values not placeholders), expected results (including DB state verification), priority, type, DB approach
- For every write operation, expected results must specify: what to query in the database and what values to assert — not just the API response
- Preconditions must state exact database records that must exist, not vague descriptions
- Steps must use concrete test data (e.g., `name: "John Doe"`, `email: "test@example.com"`), not placeholders
- Include positive, negative, boundary value, data integrity, and performance test cases
- Define clear entry and exit criteria
- Include defect severity classification (Critical, Major, Minor, Trivial)

## Step 2: Traceability Matrix

**Chain mode** (upstream docs found):
- Create a requirements-to-test-cases traceability matrix
- Every SRS functional requirement should map to at least one test case
- Every SRS non-functional requirement should have a corresponding test approach
- Flag any requirements that lack test coverage

**Standalone mode** (no upstream docs):
- Skip the SRS traceability matrix
- Instead, include a "Test Coverage Summary" section mapping test cases to the features described by the user in clarification
- Add a note: *"To establish full traceability, consider running `/srs` → `/tech-design` first, then re-running `/test-plan`."*

## Step 3: Quality Check

Load the quality checklist from:
`skills/test-plan-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 4: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/test-plan-<feature-name>.md`
4. Confirm the file path and provide a brief summary

## Important Guidelines

- **Real DB, not mocks**: Any test involving database operations MUST use a real database. Mocks give false confidence — they hide SQL errors, constraint violations, transaction bugs, and index performance issues. Only mock external third-party services you don't control.
- **Test cases = implementation guide**: Each test case must be detailed enough that an engineer can translate it directly into test code without asking questions
- **Verify DB state, not just API response**: For every write operation, the test must query the database and assert the record was correctly created/updated/deleted
- **Use concrete values**: Steps must use real test data (`name: "John"`, `age: 25`), not placeholders (`name: [valid name]`)
- **Preconditions = exact DB state**: State which records exist in which tables, not just "user is logged in"
- Test cases should be independent — each can run without depending on other test results
- Include setup/teardown instructions for test data (seed, isolate, cleanup)
- Prioritize test cases using risk-based testing (high risk = high priority)
- Group test cases by category: happy path, error path, boundary values, data integrity, performance
- Include data integrity tests: unique constraints, FK violations, cascade deletes, transaction rollbacks, concurrent updates
- Performance tests must use production-like data volumes, not empty databases

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality test plans:

1. **Do NOT use placeholders instead of concrete test data.** Steps must use real values (`name: "John Doe"`, `email: "test@example.com"`, `age: 25`), not placeholders (`name: [valid name]`, `email: [valid email]`). Placeholders are not test cases.
2. **Do NOT mock database operations.** Any test that touches the database MUST use a real database (TestContainers, SQLite in-memory, or dedicated test instance). Mocking your own DB hides SQL errors, constraint violations, and transaction bugs.
3. **Do NOT write only positive test cases.** A test plan with only happy-path tests is fundamentally incomplete. Include negative tests (~40%), boundary value tests, error handling tests, and data integrity tests.
4. **Do NOT write vague expected results.** "Should succeed" or "should return an error" is not an expected result. Specify the exact HTTP status code, response body structure, error code, AND the database state after the operation.
5. **Do NOT skip data integrity tests.** Every test plan must include test cases for: unique constraint violations, foreign key constraint enforcement, cascade operations, transaction rollback behavior, concurrent update handling, and NOT NULL constraint enforcement.
