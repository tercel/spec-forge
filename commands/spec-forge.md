---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task, Bash
description: "Generate professional software specifications — run the full chain or individual documents"
argument-hint: "[idea|prd|srs|tech-design|test-plan] <feature name>"
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
| `cool-feature` (no known subcommand) | `chain` | `cool-feature` |
| (empty) | `dashboard` | — |

## Step 2: Route

### Route A: `dashboard` (no arguments)

Display spec-forge dashboard:

1. Scan `docs/` for existing spec documents (`prd-*.md`, `srs-*.md`, `tech-design-*.md`, `test-plan-*.md`)
2. Scan `ideas/` for active ideas
3. Display:

```
spec-forge — Professional Software Specification Generator

Active Ideas (in ideas/):
  # | Idea            | Status     | Sessions | Last Updated
  1 | cool-feature    | refining   | 3        | 2026-02-10
  2 | another-idea    | exploring  | 1        | 2026-02-14

Specifications (in docs/):
  Feature        | PRD | SRS | Tech Design | Test Plan
  user-login     |  +  |  +  |      +      |     +
  payment        |  +  |  +  |             |

Commands:
  /spec-forge idea <name>          Start or resume brainstorming
  /spec-forge <name>               Run full chain (PRD -> SRS -> Tech Design -> Test Plan)
  /spec-forge prd <name>           Generate PRD only
  /spec-forge srs <name>           Generate SRS only
  /spec-forge tech-design <name>   Generate Tech Design only
  /spec-forge test-plan <name>     Generate Test Plan only
```

4. Use `AskUserQuestion` to ask what to do next.

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

#### D.1: Detect Existing Progress

Scan `docs/` for existing documents matching `feature_name`:
- `docs/prd-{feature_name}.md`
- `docs/srs-{feature_name}.md`
- `docs/tech-design-{feature_name}.md`
- `docs/test-plan-{feature_name}.md`

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
- Wait for completion → verify `docs/prd-{feature_name}.md` exists

**Stage 2: SRS** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:srs skill for '{feature_name}'. Chain mode: upstream PRD exists at docs/prd-{feature_name}.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/srs-{feature_name}.md` exists

**Stage 3: Tech Design** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:tech-design skill for '{feature_name}'. Chain mode: upstream PRD at docs/prd-{feature_name}.md, SRS at docs/srs-{feature_name}.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/tech-design-{feature_name}.md` exists

**Stage 4: Test Plan** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:test-plan skill for '{feature_name}'. Chain mode: upstream SRS at docs/srs-{feature_name}.md, Tech Design at docs/tech-design-{feature_name}.md. Minimize user questions — extract answers from upstream docs where possible."
- Wait for completion → verify `docs/test-plan-{feature_name}.md` exists

After each stage completes, display brief progress in the main context:
```
spec-forge chain: {feature_name}
  [x] PRD          docs/prd-{feature_name}.md
  [x] SRS          docs/srs-{feature_name}.md
  [ ] Tech Design  (next)
  [ ] Test Plan
```

#### D.4: Chain Completion

After all 4 stages complete:

```
spec-forge chain complete: {feature_name}

Generated documents:
  [x] docs/prd-{feature_name}.md
  [x] docs/srs-{feature_name}.md
  [x] docs/tech-design-{feature_name}.md
  [x] docs/test-plan-{feature_name}.md

Next steps:
  /forge @docs/tech-design-{feature_name}.md  → Break into tasks and execute (code-forge)
```

If an idea draft was used, update its status to `graduated`:
```json
{ "status": "graduated", "graduated_to": "docs/prd-{feature_name}.md" }
```
