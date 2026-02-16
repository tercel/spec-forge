---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task, Bash
description: "Generate professional software specifications — run the full chain or individual documents"
argument-hint: "[idea|decompose|prd|srs|tech-design|test-plan] <feature name>"
---

You are the spec-forge orchestrator. Your job is to route subcommands or run the full specification chain.

The user invoked: `/spec-forge $ARGUMENTS`

## Step 1: Parse Arguments

Parse `$ARGUMENTS` into `subcommand` and `feature_name`:

| Input Pattern | subcommand | feature_name |
|---|---|---|
| `idea cool-feature` | `idea` | `cool-feature` |
| `prd cool-feature` | `prd` | `cool-feature` |
| `srs cool-feature` | `srs` | `cool-feature` |
| `tech-design cool-feature` | `tech-design` | `cool-feature` |
| `test-plan cool-feature` | `test-plan` | `cool-feature` |
| `decompose cool-feature` | `decompose` | `cool-feature` |
| `cool-feature` (no known subcommand) | `chain` | `cool-feature` |
| (empty) | `dashboard` | — |

## Step 2: Route

### Route A: `dashboard` (no arguments)

Display spec-forge dashboard:

1. Scan `docs/` for existing spec documents (`docs/*/prd.md`, `docs/*/srs.md`, `docs/*/tech-design.md`, `docs/*/test-plan.md`)
2. Scan `docs/` for decomposed projects (`docs/project-*.md`)
3. Scan `ideas/` for active ideas
4. Display:

```
spec-forge — Professional Software Specification Generator

Active Ideas (in ideas/):
  # | Idea            | Status     | Sessions | Last Updated
  1 | cool-feature    | refining   | 3        | 2026-02-10
  2 | another-idea    | exploring  | 1        | 2026-02-14

Projects (in docs/):
  # | Project         | Sub-Features | Manifest
  1 | my-project      | 3            | docs/project-my-project.md

Specifications (in docs/):
  Feature        | PRD | SRS | Tech Design | Test Plan
  user-login     |  +  |  +  |      +      |     +
  payment        |  +  |  +  |             |

Commands:
  /spec-forge idea <name>          Start or resume brainstorming
  /spec-forge decompose <name>     Decompose project into sub-features
  /spec-forge <name>               Run full chain (Scope Analysis → PRD → SRS → Tech Design → Test Plan)
  /spec-forge prd <name>           Generate PRD only
  /spec-forge srs <name>           Generate SRS only
  /spec-forge tech-design <name>   Generate Tech Design only
  /spec-forge test-plan <name>     Generate Test Plan only
```

5. Use `AskUserQuestion` to ask what to do next.

### Route B: `idea`

Invoke the spec-forge:idea skill. Pass `feature_name` as the argument.

### Route C: `prd` / `srs` / `tech-design` / `test-plan` (single document)

Invoke the corresponding skill:
- `prd` → invoke `spec-forge:prd` skill with `feature_name`
- `srs` → invoke `spec-forge:srs` skill with `feature_name`
- `tech-design` → invoke `spec-forge:tech-design` skill with `feature_name`
- `test-plan` → invoke `spec-forge:test-plan` skill with `feature_name`

### Route D: `chain` (full chain auto mode)

Run the full specification chain automatically for `feature_name`.

#### D.0: Scope Analysis

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'."
- Wait for completion

Check result:
- If `docs/project-{feature_name}.md` exists → multi-split mode, go to D.0a
- Otherwise → single feature, proceed to D.1

#### D.0a: Multi-Split Chain Execution

Read `docs/project-{feature_name}.md` and parse the FEATURE_MANIFEST comment block to extract sub-feature names.

For each sub-feature in execution order:

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Run the spec-forge specification chain for '{sub_feature_name}'. Generate all 4 documents sequentially:
  1. Invoke the spec-forge:prd skill for '{sub_feature_name}'. Write to docs/{sub_feature_name}/prd.md.
  2. Invoke the spec-forge:srs skill for '{sub_feature_name}'. Chain mode: upstream PRD at docs/{sub_feature_name}/prd.md. Minimize user questions.
  3. Invoke the spec-forge:tech-design skill for '{sub_feature_name}'. Chain mode: upstream PRD at docs/{sub_feature_name}/prd.md, SRS at docs/{sub_feature_name}/srs.md. Minimize user questions.
  4. Invoke the spec-forge:test-plan skill for '{sub_feature_name}'. Chain mode: upstream SRS at docs/{sub_feature_name}/srs.md, Tech Design at docs/{sub_feature_name}/tech-design.md. Minimize user questions."
- Wait for completion → verify all 4 files exist in docs/{sub_feature_name}/

After each sub-feature completes, display progress:

```
spec-forge project: {feature_name} ({N} sub-features)

  {sub-feature-1}:
    [x] PRD    [x] SRS    [x] Tech Design    [x] Test Plan

  {sub-feature-2}:
    [x] PRD    [ ] SRS    [ ] Tech Design     [ ] Test Plan

  {sub-feature-3}:
    [ ] PRD    [ ] SRS    [ ] Tech Design     [ ] Test Plan
```

After all sub-features complete, display multi-split completion:

```
spec-forge project complete: {feature_name}

Generated documents:
  {sub-feature-1}/
    [x] prd.md  [x] srs.md  [x] tech-design.md  [x] test-plan.md
  {sub-feature-2}/
    [x] prd.md  [x] srs.md  [x] tech-design.md  [x] test-plan.md

Project manifest: docs/project-{feature_name}.md

Next steps:
  /forge @docs/{sub-feature-1}/tech-design.md  → Implement sub-feature-1
  /forge @docs/{sub-feature-2}/tech-design.md  → Implement sub-feature-2
```

#### D.1: Detect Existing Progress

Scan `docs/` for existing documents matching `feature_name`:
- `docs/{feature_name}/prd.md`
- `docs/{feature_name}/srs.md`
- `docs/{feature_name}/tech-design.md`
- `docs/{feature_name}/test-plan.md`

Determine which stages are already complete.

If all 4 documents exist, inform the user and ask:
- Regenerate all (start over)
- Regenerate from a specific stage
- Cancel

If some documents exist, show progress and ask:
- Continue from next missing stage (Recommended)
- Regenerate all
- Cancel

#### D.2: Check for Idea Draft

Check if `ideas/{feature_name}/` exists with status `ready` or `graduated`:
- If `ready`: read `draft.md` as additional context for PRD generation
- If `graduated`: note that idea has already been processed
- If `exploring` or `refining`: warn user that the idea is still in progress, suggest running `/spec-forge idea {feature_name}` first
- If no idea exists: proceed normally (ideas are optional)

#### D.3: Execute Chain

Run each stage sequentially. **Each stage is dispatched as a complete `Task` sub-agent** to prevent context accumulation across stages. The main context only handles coordination: checking progress, dispatching the next stage, and displaying status.

**CRITICAL**: Do NOT invoke skills directly in the main context. Each stage MUST be a `Task(subagent_type="general-purpose")` call. The sub-agent handles scanning, user questions, and document generation independently. After it completes, its context is discarded and only a brief summary returns to the main context.

**Stage 1: PRD** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:prd skill for '{feature_name}'. {If idea draft exists: 'Also read ideas/{feature_name}/draft.md for additional context.'}"
- This is the only stage that requires significant user interaction
- Wait for completion → verify `docs/{feature_name}/prd.md` exists

**Stage 2: SRS** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:srs skill for '{feature_name}'. Chain mode: upstream PRD exists at docs/{feature_name}/prd.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/{feature_name}/srs.md` exists

**Stage 3: Tech Design** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:tech-design skill for '{feature_name}'. Chain mode: upstream PRD at docs/{feature_name}/prd.md, SRS at docs/{feature_name}/srs.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/{feature_name}/tech-design.md` exists

**Stage 4: Test Plan** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:test-plan skill for '{feature_name}'. Chain mode: upstream SRS at docs/{feature_name}/srs.md, Tech Design at docs/{feature_name}/tech-design.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/{feature_name}/test-plan.md` exists

After each stage completes, display brief progress in the main context:
```
spec-forge chain: {feature_name}
  [x] PRD          docs/{feature_name}/prd.md
  [x] SRS          docs/{feature_name}/srs.md
  [ ] Tech Design  (next)
  [ ] Test Plan
```

#### D.4: Chain Completion

After all 4 stages complete:

```
spec-forge chain complete: {feature_name}

Generated documents:
  [x] docs/{feature_name}/prd.md
  [x] docs/{feature_name}/srs.md
  [x] docs/{feature_name}/tech-design.md
  [x] docs/{feature_name}/test-plan.md

Next steps:
  /forge @docs/{feature_name}/tech-design.md  → Break into tasks and execute (code-forge)
```

If an idea draft was used, update its status to `graduated`:
```json
{ "status": "graduated", "graduated_to": "docs/{feature_name}/prd.md" }
```

### Route E: `decompose`

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'."
- Wait for completion

After the sub-agent returns:
- If `docs/project-{feature_name}.md` exists: display the manifest and suggest running `/spec-forge {feature_name}` to execute the full chain for all sub-features
- If no manifest (single verdict): inform user and suggest running `/spec-forge {feature_name}` to start the spec chain
