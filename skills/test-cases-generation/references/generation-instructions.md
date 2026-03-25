# Test Cases Generation Instructions

These instructions are for the **generation sub-agent**. The orchestrator (commands/test-cases.md) handles Steps 1-4 of the SKILL.md workflow (input mode, extraction, dimensions, user confirmation). This sub-agent handles Steps 5-7 (generation, coverage matrix, quality check), expanded into 6 detailed steps below.

Follow these steps exactly to generate the test cases document.

## Step 1: Analyze Context and Verify Project Profile

Review the context provided by the orchestrator:

1. **Project profile** — the orchestrator has already determined the project type (Web API, CLI Tool, etc.), database/auth/external-API flags
2. **Input mode** — Spec Mode, Code Mode, or Scan Mode
3. **Functional inventory** — list of testable units with coverage status
4. **Dimensions** — confirmed dimension set (built-in + auto-detected)
5. **Scope** — which units to generate cases for
6. **User context** — business rules, edge cases, domain knowledge from user answers
7. **Formal mode** — whether `--formal` flag was set

**Verify the project profile** against the functional inventory. The orchestrator already determined the profile; confirm it matches the signals below:

| Signal | Profile | Sections to Include | Example Pattern |
|--------|---------|--------------------|-----------------|
| Routes/endpoints in inventory, HTTP framework detected | **Web API** | All sections; Data Integrity if DB; Security if auth | HTTP status codes, request/response bodies, DB state |
| Exported functions, no routes, no DB | **Function Library** | 4.1-4.3 only; skip 4.4; Security only if handles user input | Input args → return value / thrown error |
| Commands/subcommands in inventory, CLI framework detected | **CLI Tool** | 4.1-4.3; 4.4 only if persistent state; Security if handles untrusted input | Command + flags → exit code + stdout/stderr + file changes |
| Components/props in inventory, frontend framework detected | **Frontend App** | 4.1-4.3; skip 4.4; Security if renders user content | Props + interaction → rendered output + emitted events |
| Tool definitions, trigger conditions in inventory | **AI Agent / Tool System** | 4.1-4.3; skip 4.4 unless tool persists data; add combo section 5 | User message → tool(s) triggered + parameters + response |
| Pipeline stages, transforms in inventory | **Data Pipeline** | 4.1-4.3; 4.4 if writes to DB/store; Performance section | Input dataset → output dataset + transformation correctness |
| Client/SDK methods, connection management | **SDK / Client Library** | 4.1-4.3; skip 4.4; add connection state dimension | Method call → return value + error handling + retry behavior |

**Key rule: follow the project profile.** The orchestrator has already determined whether this project has a database, auth, etc. Use these flags to decide which sections to include:

- **Has Database = No** → skip Section 4.4 (Data Integrity), use "N/A" for Test Infra on pure unit tests
- **Has Auth = No** → skip auth-related Security test cases (4.5), keep injection tests if project handles user input
- **Profile = CLI Tool** → use exit codes and stdout/stderr, not HTTP status codes
- **Profile = Function Library** → use return values and thrown errors, not HTTP status codes
- **Profile = Frontend App** → use rendered output and emitted events, not HTTP status codes

If upstream documents were referenced (SRS, Tech Design), read them to extract requirement IDs for traceability.

## Step 2: Generate Test Cases

Load and follow the template from:
`skills/test-cases-generation/references/template.md`

Generate the test cases document, adapting to the project profile determined in Step 1.

### Coverage Depth Rules

For EVERY testable unit in scope, generate at minimum:

| Depth | Minimum Cases | What to Cover |
|-------|--------------|---------------|
| L1 — Happy Path | 1 | Basic correct behavior with valid inputs |
| L2 — Boundary | 1 | Min/max values, empty input, type boundaries |
| L2 — Error | 1 | Invalid input, missing required fields, malformed data |
| L3 — Negative | 1 | Scenario where behavior should NOT be triggered |

Total minimum: 4 cases per testable unit. High-risk units should have more.

### Adapting Test Cases to Project Type

**Preconditions** — describe the exact state before the test, using terms natural to the project:

| Project Type | Preconditions describe... |
|-------------|--------------------------|
| Web API | DB records with field values, auth token, feature flags |
| Function Library | Input data, module configuration, mock setup for external deps |
| CLI Tool | File system state, environment variables, config files |
| Frontend App | Component props, store/context state, DOM state |
| AI Agent | Conversation history, available tools, user context |
| Data Pipeline | Input dataset characteristics, pipeline configuration |

**Expected Result** — describe what the test verifies, using terms natural to the project:

| Project Type | Expected Result describes... |
|-------------|------------------------------|
| Web API | HTTP status + response body + DB state after |
| Function Library | Return value / thrown error / mutated state |
| CLI Tool | Exit code + stdout content + stderr content + file changes |
| Frontend App | Rendered output + emitted events + store changes |
| AI Agent | Tool(s) called + parameters passed + final response content |
| Data Pipeline | Output dataset + transformation correctness + side effects |

**Test Infra** — what infrastructure the test needs:

| Project Type | Typical Test Infra |
|-------------|-------------------|
| Web API with DB | Real DB (TestContainers), Mock for external APIs |
| Function Library | N/A (pure unit tests), or Mock for injected dependencies |
| CLI Tool | Temp directory for file operations, Mock for network calls |
| Frontend App | Test renderer (Testing Library / Enzyme), Mock for API calls |
| AI Agent | Mock for LLM responses (if testing orchestration), Real for tool execution |
| Data Pipeline | Test datasets, Temp storage, Mock for external data sources |

### Dimension Cross-Product Rules

For auto-detected dimensions, do NOT blindly generate all combinations. Instead:

1. Identify which dimension values are HIGH RISK for each unit
2. Generate L1 cases for each high-risk dimension value
3. Generate L2/L3 cases only for the most critical dimension combinations
4. Use pairwise coverage for large dimension spaces (not full Cartesian product)

### Combination Test Rules

For units that interact with each other:

1. Identify interaction pairs from the functional inventory (dependency analysis)
2. For each pair, generate at least:
   - 1 × L1: Both units working correctly together
   - 1 × L2: First unit succeeds, second fails (error propagation)
   - 1 × L3: Scenario where combination should NOT occur
3. Prioritize by coupling strength — tightly coupled pairs need more cases

### External Dependency Policy

**Principle: test your own dependencies for real; only mock what you don't control.**

- **Own database** → Real DB (TestContainers, test instance, SQLite in-memory). Mocking hides SQL errors, constraint violations, transaction bugs.
- **Own file system** → Real temp directory. Mocking hides path, permission, encoding issues.
- **Own cache/queue** → Real (TestContainers, embedded). Mocking hides serialization, TTL issues.
- **External third-party APIs** → Mock/stub acceptable. External services may be unavailable.
- **Non-deterministic inputs** → Inject controlled values (time, random, UUIDs).

**If the project has no database or external I/O**: skip Data Integrity section (4.4), simplify Test Infra column to "N/A" for pure unit tests.

**If the project has a database**, include Data Integrity test cases:
- Unique constraint enforcement
- Foreign key constraint enforcement
- Cascade operations (delete parent → verify children)
- Transaction rollback on partial failure
- Concurrent update handling (optimistic locking)
- NOT NULL constraint enforcement

### Test Case Writing Standards

- Test case IDs: `TC-<MODULE>-<NNN>` (e.g., TC-AUTH-001, TC-PARSE-001, TC-CLI-001, TC-TOOL-001)
- Title pattern: `[action] [condition] [expected outcome]`
- Preconditions: exact state (adapted to project type — see table above)
- Steps: concrete test data (`name: "John Doe"`, `count: 42`, `--env staging`), NOT placeholders
- Expected results: exact output (adapted to project type — see table above) AND state verification where applicable
- Not Expected: what should NOT happen (mandatory for L3, recommended for all)
- Priority: P0 (critical path), P1 (important), P2 (nice-to-have)

### Conditional Sections

| Template Section | Include When |
|-----------------|-------------|
| 4.1-4.3 (Functional by depth) | Always |
| 4.4 (Data Integrity) | Project has database or persistent store |
| 4.5 (Security) | Project handles auth, credentials, or untrusted user input |
| 4.6 (Performance) | Project has latency/throughput/resource requirements |
| 5 (Combination) | Functional inventory has interacting units |
| 6 (Dimension-Specific) | Auto-detected dimensions exist |

**Omit sections that don't apply** rather than generating empty or forced content.

### Formal Mode Sections

If `--formal` flag is set, also generate:
- Document information and revision history
- Test environment specifications
- Entry and exit criteria
- Test data management strategy
- Defect management process
- Risk assessment with reasoning
- Test schedule with Gantt chart
- Roles and responsibilities

If `--formal` is NOT set, skip these sections entirely.

## Step 3: Build Coverage Matrix

After generating all test cases:

1. **Unit Coverage Matrix**: rows = testable units, columns = coverage depth (L1/L2/L3), cells = TC IDs
2. **Dimension Coverage Matrix**: rows = dimension values, columns = coverage depth, cells = count
3. **Combination Coverage**: list of tested interaction pairs with TC IDs
4. **Gap Analysis**: flag any unit × depth cell with zero coverage
5. **Statistics**:
   - Total test cases
   - By priority: P0 / P1 / P2
   - By category: only categories that were included (Functional / Data Integrity / Security / Performance)
   - By depth: L1 / L2 / L3
   - By dimension (for each detected dimension)

## Step 4: Build Traceability (if applicable)

**If upstream SRS/Tech Design exists:**
- Create Requirements Traceability Matrix (RTM)
- Map every FR/NFR requirement ID to test case IDs
- Flag requirements without test coverage

**If no upstream docs:**
- Include a Test Coverage Summary mapping test cases to the functional inventory
- Add note: *"For full traceability, consider running `/spec-forge:srs` first."*

## Step 5: Quality Check

Load the quality checklist from:
`skills/test-cases-generation/references/checklist.md`

Run through every item. Skip items marked as conditional if the condition doesn't apply (e.g., skip DB checks for projects without a database). For any failed check, revise the document before finalizing.

## Step 6: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/<feature-name>/test-cases.md`
4. Confirm file path and provide summary:
   - Project profile detected
   - Total test cases generated
   - Coverage statistics
   - Sections included / omitted (with reason)
   - Gap analysis highlights
   - Downstream command: `/code-forge:tdd @docs/<feature-name>/test-cases.md`

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited**:

1. **Do NOT use placeholders instead of concrete test data.** Steps must use real values (`name: "John Doe"`, `email: "test@example.com"`, `count: 42`, `--env staging`), not placeholders (`name: [valid name]`).
2. **Do NOT mock your own dependencies.** Test your own DB/file system/cache/queue for real. Only mock external third-party services you don't control.
3. **Do NOT write only happy-path test cases.** Every unit needs L1 + L2 + L3 coverage. A set with only L1 cases is fundamentally incomplete.
4. **Do NOT write vague expected results.** "Should succeed" is not an expected result. Specify exact output (return value / status code / exit code / rendered content) AND state changes.
5. **Do NOT skip L3 (negative) cases.** Every testable unit needs at least one "this should NOT happen" case.
6. **Do NOT force irrelevant sections.** If the project has no database, do not generate Data Integrity cases. If the project has no auth, do not generate auth test cases. Adapt to the actual project.
7. **Do NOT generate blind Cartesian products.** Use risk-based prioritization for dimension combinations. Pairwise coverage for large spaces.
8. **Do NOT omit the coverage matrix.** The matrix is a required output — it proves completeness.
9. **Do NOT use HTTP-specific language for non-HTTP projects.** Use exit codes for CLI, return values for libraries, rendered output for frontend. Match the project's interface.
