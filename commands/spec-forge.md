---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task, Bash
description: "Use when generating software specifications — full chain (Idea→Decompose→Tech Design + Feature Specs) or individual documents"
argument-hint: "[idea|decompose|prd|srs|tech-design|test-cases|audit|analyze] <name or path>"
---

You are the spec-forge orchestrator. Your job is to route subcommands or run the full specification chain.

The user invoked: `/spec-forge $ARGUMENTS`

## Step 1: Parse Arguments

Parse `$ARGUMENTS` into `subcommand` and `argument`:

| Input Pattern | subcommand | argument |
|---|---|---|
| `idea cool-feature` | `idea` | `cool-feature` |
| `prd cool-feature` | `prd` | `cool-feature` |
| `srs cool-feature` | `srs` | `cool-feature` |
| `tech-design cool-feature` | `tech-design` | `cool-feature` |
| `test-cases cool-feature` | `test-cases` | `cool-feature` |
| `test-cases --formal cool-feature` | `test-cases` | `--formal cool-feature` |
| `decompose cool-feature` | `decompose` | `cool-feature` |
| `review cool-feature` | `review` | `cool-feature` |
| `audit ../../project` | `audit` | `../../project` |
| `analyze ../../docs-repo` | `analyze` | `../../docs-repo` |
| `cool-feature` (no known subcommand) | `chain` | `cool-feature` |
| (empty) | `dashboard` | — |

For routes B-E (idea, prd, srs, tech-design, test-cases, decompose, review, chain), `argument` is a feature name — referred to as `feature_name` in route descriptions below. For routes F-G (audit, analyze), `argument` is a file path.

## Step 2: Route

### Route A: `dashboard` (no arguments)

Display spec-forge dashboard:

1. Scan `docs/` for existing spec documents (`docs/*/prd.md`, `docs/*/srs.md`, `docs/*/tech-design.md`, `docs/*/test-cases.md`)
2. Scan `docs/` for decomposed projects (`docs/project-*.md`)
3. Scan `docs/features/` for lightweight feature specs (`docs/features/*.md`)
4. Scan `ideas/` for active ideas
5. Display:

```
spec-forge — Professional Software Specification Generator

Active Ideas (in ideas/):
  # | Idea            | Status     | Sessions | Last Updated
  1 | cool-feature    | refining   | 3        | 2026-02-10
  2 | another-idea    | exploring  | 1        | 2026-02-14

Projects (in docs/):
  # | Project         | Sub-Features | Manifest
  1 | my-project      | 3            | docs/project-my-project.md

Feature Specs (in docs/features/):
  # | Feature         | Source Tech Design
  1 | core-executor   | docs/my-feature/tech-design.md
  2 | schema-system   | docs/my-feature/tech-design.md

Specifications (in docs/):
  Feature        | PRD | SRS | Tech Design | Test Cases
  user-login     |  +  |  +  |      +      |     +
  payment        |  +  |  +  |             |

Commands:
  /spec-forge:idea <name>          Start or resume brainstorming
  /spec-forge:decompose <name>     Decompose project into sub-features
  /spec-forge <name>               Run full chain (Idea → Decompose → Tech Design + Feature Specs → Review)
  /spec-forge:tech-design <name>   Generate Tech Design + Feature Specs
  /spec-forge:prd <name>           Generate PRD (on-demand, for stakeholders)
  /spec-forge:srs <name>           Generate SRS (on-demand, for compliance)
  /spec-forge:test-cases <name>    Generate test cases with coverage matrix (on-demand)
  /spec-forge:test-cases --formal <name>  Same + management sections (environment, roles, schedule)
  /spec-forge:review <name>        Review generated specs for quality & consistency, auto-fix issues
  /spec-forge:audit [path]         Audit docs for quality, completeness & code alignment
  /spec-forge:analyze [path]       Analyze doc collection — map themes, find conflicts & gaps

Tip: audit = docs + code in one project, analyze = docs-only or cross-repo collections.
     Unsure which to use? Describe your goal and I'll recommend.
```

5. Use `AskUserQuestion` to ask what to do next.

### Route B: `idea`

Invoke the spec-forge:idea skill. Pass `feature_name` as the argument.

### Route C: `prd` / `srs` / `tech-design` / `test-cases` / `review` (single document)

Invoke the corresponding skill:
- `prd` → invoke `spec-forge:prd` skill with `feature_name`
- `srs` → invoke `spec-forge:srs` skill with `feature_name`
- `tech-design` → invoke `spec-forge:tech-design` skill with `feature_name`
- `test-cases` → invoke `spec-forge:test-cases` skill with `feature_name`
- `review` → invoke `spec-forge:review` skill with `feature_name`

### Route D: `chain` (full chain auto mode)

Run the full specification chain automatically for `feature_name`. The chain consists of four stages:

1. **Idea** — Validate requirements and crystallize the concept (interactive)
2. **Decompose** — Determine if the project needs splitting into sub-features
3. **Tech Design** — Generate architecture document + auto-generate feature specs in `docs/features/`
4. **Review** — Audit generated documents for quality and consistency; auto-fix issues if found

> **Note**: PRD, SRS, and Test Cases are NOT part of the auto chain. They can be generated on-demand via `/spec-forge:prd`, `/spec-forge:srs`, or `/spec-forge:test-cases` when needed (e.g., for stakeholder alignment, compliance, or test coverage). The tech-design in standalone mode captures requirements directly through targeted questions, eliminating the need for intermediate PRD/SRS documents.

#### D.0: Check for Existing Idea

Check if `ideas/{feature_name}/` exists:
- If status is `ready` or `graduated`: note the idea is available as context, proceed to D.1
- If status is `exploring` or `refining`: warn user that the idea is still in progress, suggest running `/spec-forge:idea {feature_name}` to finish it first
- If no idea exists: proceed to D.0a (start with idea stage)

#### D.0a: Stage 1 — Idea

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:idea skill for '{feature_name}'. Guide the user through iterative discovery to validate the concept and produce a draft at ideas/{feature_name}/draft.md."
- This is the most interactive stage — the user shapes the core requirements here
- Wait for completion

After sub-agent returns, check `ideas/{feature_name}/state.json`:
- If `status` is `ready` or `graduated`: proceed to D.1
- If `status` is `parked`: inform user — *"The idea was parked. Run `/spec-forge:idea {feature_name}` to resume when ready."* — stop chain
- If `status` is `exploring`, `researching`, or `refining`: ask user via `AskUserQuestion`:
  - **Continue anyway** — proceed to D.1 using partial draft as context. Warn the user: *"This design will be based on an unvalidated idea. The requirements may not be solid — consider running `/spec-forge:idea {feature_name}` to completion before finalizing."* Pass this warning context to the tech-design sub-agent so it appears in the generated document's Scope section.
  - **Finish idea first** — stop chain, user resumes with `/spec-forge:idea {feature_name}`
- If `ideas/{feature_name}/` still doesn't exist: warn and stop

#### D.1: Stage 2 — Decompose

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'."
- Wait for completion

Check result:
- If `docs/project-{feature_name}.md` exists → multi-split mode, go to D.1a
- Otherwise → single feature, proceed to D.2

#### D.1a: Multi-Split Chain Execution

Read `docs/project-{feature_name}.md` and parse the FEATURE_MANIFEST comment block to extract sub-feature names and their scope descriptions.

For each sub-feature in execution order:

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:tech-design skill for '{sub_feature_name}'. Idea-first mode. Read ideas/{feature_name}/draft.md for overall requirements context and use it to populate §3.5 User Scenarios, §3.6 Acceptance Criteria, and §3.7 Success Metrics. Also read docs/project-{feature_name}.md for this sub-feature's specific scope and dependencies (look for the section describing '{sub_feature_name}') and use it to define §3.4 Scope and §3.2 Goals. Minimize user questions — extract answers from these documents where possible. IMPORTANT: This will also auto-generate feature specs in docs/features/ as part of Step 7."
- Wait for completion → verify `docs/{sub_feature_name}/tech-design.md` exists and feature specs exist in `docs/features/`

After each sub-feature completes, display progress:

```
spec-forge project: {feature_name} ({N} sub-features)

  {sub-feature-1}:
    [x] Tech Design + Feature Specs

  {sub-feature-2}:
    [x] Tech Design + Feature Specs

  {sub-feature-3}:
    [ ] In progress...
```

After all sub-features complete, display multi-split progress:

```
spec-forge project: {feature_name} — all sub-features generated, starting review...
```

Then proceed to **D.4 (Review)** — the review covers ALL generated documents across all sub-features.

After review completes, display multi-split chain completion:

```
spec-forge project complete: {feature_name}

Generated documents:
  {sub-feature-1}/
    [x] tech-design.md
  {sub-feature-2}/
    [x] tech-design.md

Feature specs (auto-generated with tech-design):
  docs/features/
    [x] overview.md
    [x] {component-1}.md
    [x] {component-2}.md
    ...

Review: {PASS | N issues fixed | N issues remaining}
Project manifest: docs/project-{feature_name}.md

Next steps:
  /code-forge:plan @docs/features/{component-name}.md   → Generate implementation plan for a component
  /code-forge:status                                     → Track progress across features

Optional (on-demand):
  /spec-forge:prd {feature_name}                         → Generate PRD (for stakeholders)
  /spec-forge:srs {feature_name}                         → Generate SRS (for compliance/audit)
  /spec-forge:test-cases {feature_name}                   → Generate test cases with coverage matrix
```

#### D.2: Detect Existing Progress

Scan for existing documents matching `feature_name`:
- `ideas/{feature_name}/` (idea draft)
- `docs/{feature_name}/tech-design.md` (tech design)
- `docs/features/overview.md` (feature specs)

Determine which stages are already complete.

If tech-design and feature specs both exist, inform the user and ask:
- Regenerate all (start over from idea)
- Regenerate tech-design only (keep idea)
- Cancel

If some stages are complete, show progress and ask:
- Continue from next missing stage (Recommended)
- Regenerate all
- Cancel

#### D.3: Stage 3 — Tech Design

**CRITICAL**: Do NOT invoke skills directly in the main context. Each stage MUST be a `Task(subagent_type="general-purpose")` call. The sub-agent handles scanning, user questions, and document generation independently. After it completes, its context is discarded and only a brief summary returns to the main context.

Before launching, check whether `ideas/{feature_name}/draft.md` exists and build the sub-agent prompt accordingly:

- **If idea draft exists**: prompt = "Invoke the spec-forge:tech-design skill for '{feature_name}'. Idea-first mode. Read ideas/{feature_name}/draft.md for requirements context — extract User Scenarios from the draft to populate §3.5, extract validated requirements and MVP criteria to populate §3.6 Acceptance Criteria, extract success criteria and demand validation metrics to populate §3.7 Success Metrics, and extract MVP scope/boundaries to populate §3.4 Scope and §3.2 Goals. Minimize user questions where the idea draft already provides answers. IMPORTANT: After writing the tech-design, also auto-generate feature specs in docs/features/ as part of Step 7."
- **If no idea draft**: prompt = "Invoke the spec-forge:tech-design skill for '{feature_name}'. Standalone mode — no upstream idea draft found. Ask the user the full set of standalone clarification questions (including user scenarios, acceptance criteria, and success metrics). IMPORTANT: After writing the tech-design, also auto-generate feature specs in docs/features/ as part of Step 7."

Launch `Task(subagent_type="general-purpose")` with the appropriate prompt above.
Wait for completion → verify `docs/{feature_name}/tech-design.md` exists and feature specs exist in `docs/features/`.

After completion, scan `docs/features/` to count generated specs, then display:
```
spec-forge chain: {feature_name}
  [x] Idea           ideas/{feature_name}/
  [x] Decompose      single feature
  [x] Tech Design    docs/{feature_name}/tech-design.md
  [x] Feature Specs  docs/features/overview.md + {actual count from scan} component specs
  [ ] Review         pending...
```

Proceed to D.4 (Review).

#### D.4: Stage 4 — Review

After all documents are generated (tech-design + feature specs), review them for quality and consistency. This stage catches issues like incomplete sections, internal contradictions, missing traceability, and vague specifications before the chain completes.

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt:

```
You are a senior specification reviewer. Review and auto-fix spec-forge generated documents for '{feature_name}'.

Read the review skill definition at:
skills/review/SKILL.md

Follow every step of the workflow exactly. In this chain context:
- Skip Step 1 user questions — review scope is "All", auto-fix is "Yes — fix Critical+Major automatically"
- Review targets: docs/{feature_name}/tech-design.md and all docs/features/*.md
- Upstream reference (read for context, NOT reviewed): ideas/{feature_name}/draft.md (if exists)
- Maximum 2 review-fix iterations
- Be honest — don't inflate findings and don't fabricate issues
```

Wait for completion. Parse the sub-agent's result to determine:
- **PASS**: All documents passed quality check
- **N issues fixed**: Issues were found and auto-fixed
- **N issues remaining**: Some issues could not be auto-fixed

Display review status:
```
spec-forge review: {PASS | N issues fixed | N issues remaining}
```

If issues remain after review, display the remaining findings for user awareness, then proceed to D.5.

#### D.5: Chain Completion

```
spec-forge chain complete: {feature_name}

Generated:
  [x] ideas/{feature_name}/              — validated requirements
  [x] docs/{feature_name}/tech-design.md — architecture & design
  [x] docs/features/overview.md          — feature index
  [x] docs/features/{component-1}.md     — implementation spec
  [x] docs/features/{component-2}.md     — implementation spec
  ...
  [x] Review                             — {PASS | N issues fixed | N issues remaining}

Next steps:
  /code-forge:plan @docs/features/{component-name}.md   → Generate implementation plan for a component
  /code-forge:status                                     → Track progress across features

Optional (on-demand):
  /spec-forge:prd {feature_name}                         → Generate PRD (for stakeholders)
  /spec-forge:srs {feature_name}                         → Generate SRS (for compliance/audit)
  /spec-forge:test-cases {feature_name}                   → Generate test cases with coverage matrix
```

If an idea draft was used, update its status to `graduated`:
```json
{ "status": "graduated", "graduated_to": "docs/{feature_name}/tech-design.md" }
```

### Route E: `decompose`

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'."
- Wait for completion

After the sub-agent returns:
- If `docs/project-{feature_name}.md` exists: display the manifest and suggest running `/spec-forge {feature_name}` to execute the full chain for all sub-features
- If no manifest (single verdict): inform user and suggest running `/spec-forge {feature_name}` to start the spec chain

> **Note**: Running `/spec-forge {feature_name}` starts from the **Idea** stage if `ideas/{feature_name}/` does not exist yet. If you only want the Tech Design (skipping idea and decompose), run `/spec-forge:tech-design {feature_name}` directly.

### Route F: `audit`

Invoke the spec-forge:audit skill. Pass `argument` as the path to the project to audit (may be a relative path to another project).

### Route G: `analyze`

Invoke the spec-forge:analyze skill. Pass `argument` as the path to the document collection to analyze (may be a relative path to a docs repo).
