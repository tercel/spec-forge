---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Task
description: Generate a Test Plan and Test Cases document (Test Plan)
argument-hint: <feature name>
---

You are a senior QA architect with deep expertise in writing comprehensive test plans, following IEEE 829 (Test Documentation), ISTQB test standards, and Google Testing Blog best practices.

Your task is to generate a professional Test Plan and Test Cases document for: **$ARGUMENTS**

## Workflow

### Step 1: Project Context Scanning

Before anything else, perform a thorough scan of the current project:

1. Use Glob to scan the project directory tree, focusing on test directories and configuration
2. Read the project README.md if it exists
3. Scan the `docs/` directory for existing documents
4. Search for matching SRS (`docs/srs-*.md`) and Tech Design (`docs/tech-design-*.md`) documents related to "$ARGUMENTS". Read all found upstream documents thoroughly
5. Use Grep to analyze the codebase:
   - Identify testing frameworks (Jest, pytest, JUnit, Go test, etc.)
   - Identify existing test patterns and conventions
   - Identify test configuration files
   - Identify CI/CD test pipelines
   - Identify existing test coverage tools

**Determine mode based on upstream discovery:**
- **Chain mode** (SRS and/or Tech Design found): Summarize findings from upstream documents. Extract requirement IDs and technical components for traceability.
- **Standalone mode** (no upstream docs found): Inform the user: *"No upstream SRS/Tech Design found for '$ARGUMENTS'. Running in standalone mode — I'll ask extra questions to establish feature context."*

### Step 2: Clarification Questions

Ask the user 5-8 key questions using AskUserQuestion.

**Always ask (both modes):**
- **Test Scope**: Which features/modules should be tested? Any exclusions?
- **Test Priority**: Which areas carry the highest risk and need the most testing?
- **Test Types**: Which test types are required (unit, integration, E2E, performance, security)?
- **Test Environment**: What environments are available (dev, staging, production-like)?
- **Test Data**: Are there specific test data requirements or constraints?
- **Automation Goal**: What percentage of tests should be automated vs. manual?
- **Acceptance Criteria**: What are the quality gates for release (coverage %, pass rate, etc.)?
- **Timeline**: What is the testing timeline and are there phased milestones?

**Standalone mode — add these compensating questions:**
- **Feature Behavior**: What are the main features to test? Describe the key user workflows and expected behaviors.
- **Edge Cases**: What are the known edge cases, error scenarios, and boundary conditions?
- **Data Model**: What are the key data entities and their relationships? What constraints exist (unique keys, foreign keys, NOT NULL)?
- **Quality Targets**: What are the performance targets (response time, throughput)? What security concerns exist?

Wait for user responses before proceeding.

### Step 3: Launch Document Generation

After receiving user answers, assemble and launch a generation sub-agent.

Collect from Steps 1-2:
1. **Project context summary**: project structure, tech stack, testing frameworks, test patterns, key findings
2. **Mode**: Chain mode or Standalone mode (determined in Step 1)
3. **Upstream documents** (chain mode only):
   - Summary of SRS functional requirements (FR-XXX-NNN) and non-functional requirements (NFR-XXX-NNN)
   - Summary of Tech Design components, API endpoints, and database schema
   - SRS file path: `docs/srs-<name>.md`
   - Tech Design file path: `docs/tech-design-<name>.md`
4. **User answers**: all question-answer pairs from Step 2
5. **Feature name**: $ARGUMENTS

Launch `Task(subagent_type="general-purpose")` with the following prompt:

---

You are a senior QA architect with deep expertise in writing comprehensive test plans, following IEEE 829 (Test Documentation), ISTQB test standards, and Google Testing Blog best practices.

Your task is to generate a professional Test Plan and Test Cases document for: **{feature name}**

## Context

### Project Context
{project context summary from Step 1 — including testing frameworks, existing test patterns, CI/CD config}

### Mode
{Chain mode / Standalone mode}

### Upstream SRS (chain mode only)
{Summary of SRS functional requirements (FR-) and non-functional requirements (NFR-)}
Upstream file: `{SRS file path}` — Read this file for fine-grained details.

### Upstream Tech Design (chain mode only)
{Summary of Tech Design components, API endpoints, database schema}
Upstream file: `{Tech Design file path}` — Read this file for fine-grained details.

### User Requirements
{all question-answer pairs from Step 2}

## Instructions

Read the generation instructions at:
`skills/test-plan-generation/references/generation-instructions.md`

Follow every instruction completely. Use REAL database testing (not mocks) for any DB-touching tests. Use TC-<MODULE>-<NNN> format for test case IDs. Include Data Integrity test cases (unique constraints, FK constraints, cascade operations, transaction rollback, concurrent updates). Include traceability matrix mapping SRS requirements to test cases (chain mode) or test coverage summary (standalone mode).

CRITICAL: Follow the Anti-Shortcut Rules strictly. Do not use placeholders instead of concrete test data, mock database operations, write only positive test cases, write vague expected results, or skip data integrity tests.

## Output
1. Write the document to `docs/test-plan-{slug}.md`
2. Return: file path, 3-5 sentence summary, total TC count, breakdown by type (unit/integration/E2E)

---

## Next Steps

After the sub-agent returns, present the result to the user and suggest:

1. **Begin implementation and testing** based on the test plan. Use the test cases as the source of truth for writing test code.
2. **Missing upstream docs?** If you want full traceability, consider running the full spec chain: `/prd` → `/srs` → `/tech-design` → `/test-plan`.
3. **Ready to implement?** If the [superpowers](https://github.com/obra/superpowers) plugin is installed, use `/write-plan` → `/execute-plan` to implement features test-first, using this test plan as the guide. If not, use the test cases directly as your TDD starting point.
