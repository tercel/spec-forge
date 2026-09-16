---
allowed-tools: Read, Glob, Grep, Write, Edit, AskUserQuestion, Task, Bash
description: "Use when generating software specifications — full chain ([Idea]→[Decompose]→[PRD]→SRS→Tech Design→Review) or individual documents"
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
  Feature        | SRS | Tech Design | PRD | Test Cases
  user-login     |  +  |      +      |  +  |     +
  payment        |  +  |             |     |
  reporting      |     |             |     |          ← no SRS: nothing to implement against

Commands:
  /spec-forge:idea <name>          Start or resume brainstorming
  /spec-forge:decompose <name>     Decompose project into sub-features
  /spec-forge <name>               Run full chain ([Idea] → [Decompose] → [PRD] → SRS → Tech Design → Review)
  /spec-forge:srs <name>           Generate SRS — the delivery contract handed to implementers
  /spec-forge:prd <name>           Generate PRD — business case, for a go/no-go decision
  /spec-forge:tech-design <name>   Generate Tech Design + Feature Specs
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

Run the full specification chain automatically for `feature_name`. The chain has a **mandatory spine** — a delivery-grade requirements spec, then a technical design — with conditional stages around it:

1. **Idea** *(conditional)* — Validate demand and crystallize the concept (interactive). Run when the demand itself is unvalidated; skip when the user already knows what they want built.
2. **Decompose** *(conditional)* — Determine if the project needs splitting into sub-features. Skip for a single coherent feature.
3. **PRD** *(conditional)* — Business case and product definition at `docs/{feature_name}/prd.md`. Run for a new product or anything needing a go/no-go decision, budget approval, or stakeholder alignment. Skip when the decision to build is already made — a PRD written after the decision is ceremony.
4. **SRS** *(mandatory)* — The delivery contract at `docs/{feature_name}/srs.md`: `FR-*`/`NFR-*` requirements, input field rules, state machines, permission matrix, error catalogue, machine-verifiable acceptance criteria, acceptance and change control.
5. **Tech Design** *(mandatory)* — Architecture document, plus one feature spec in `docs/features/` per component in §8.1 and an `overview.md` carrying the dependency graph and execution order.
6. **Review** *(mandatory)* — Audit generated documents for quality and consistency; auto-fix issues if found.
7. **Handoff** — Report the `/code-forge:plan` command; do not run it.

> **Why the SRS is never skipped.** It is the document an implementation team — an external vendor, another team, or code-forge — is held to. Skipping it to reach the tech design faster produces a design built on unstated requirements, and code whose correctness nobody can settle. Earlier versions of this chain let the tech-design capture requirements through ad-hoc questions; that saved a stage and lost the acceptance contract.
>
> **Test Cases are NOT part of the chain.** Tests are derived from the SRS acceptance criteria by `code-forge:tdd`. spec-forge owns requirements and design; code-forge owns implementation and verification. `/spec-forge:test-cases` remains available on-demand for QA planning that is not driven by implementation.

#### D.Pre: Project Context Scan (Once for Entire Chain)

Before launching any stage, scan the project once to build shared context. This avoids each sub-agent re-scanning the same project independently.

Read and execute the Project Context Protocol:
`skills/shared/project-context.md`

Execute PC.1 (Project Discovery), PC.2 (Tech Stack Detection), PC.3 (Project Profile), and PC.4 (Architecture Awareness).

Store the results as `{project_context_summary}` — a concise (~500 words) summary including:
- Project Profile (Web API / CLI / Frontend / etc.)
- Tech Stack (language, framework, database, test framework)
- Architecture pattern (layered, MVC, clean, microservices)
- Module structure (key directories and their roles)

This summary is passed to EVERY sub-agent in the chain via their prompts, so they don't need to re-scan.

---

#### D.0: Check for Existing Idea

Check if `ideas/{feature_name}/` exists:
- If status is `ready` or `graduated`: note the idea is available as context, proceed to D.1
- If status is `exploring` or `refining`: warn user that the idea is still in progress, suggest running `/spec-forge:idea {feature_name}` to finish it first
- If no idea exists: proceed to D.0a (start with idea stage)

#### D.0a: Stage 1 — Idea

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:idea skill for '{feature_name}'. Guide the user through iterative discovery to validate the concept and produce a draft at ideas/{feature_name}/draft.md.\n\n## Project Context (pre-scanned)\n{project_context_summary}"
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
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'. Skip project scanning in Step 1 — use the pre-scanned context below instead.\n\n## Project Context (pre-scanned)\n{project_context_summary}"
- Wait for completion

Check result:
- If `docs/project-{feature_name}.md` exists → multi-split mode, go to D.1a
- Otherwise → single feature, proceed to D.2

#### D.1a: Multi-Split Chain Execution

Read `docs/project-{feature_name}.md` and parse the FEATURE_MANIFEST comment block to extract sub-feature names and their scope descriptions.

Each sub-feature runs the same mandatory spine as a single feature — **SRS, then tech design**. A sub-feature is not a reason to skip the delivery contract; it is a reason to have one per sub-feature, since each will be implemented and accepted separately.

For each sub-feature in execution order, run two sub-agents in sequence:

**1. SRS** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:srs skill for '{sub_feature_name}'. Read docs/project-{feature_name}.md for this sub-feature's scope and dependencies (look for the section describing '{sub_feature_name}'), and ideas/{feature_name}/draft.md for the overall requirements context. Scope this SRS to '{sub_feature_name}' only — the §3.2 out-of-scope table must explicitly list the sibling sub-features and name which one owns each excluded capability, so the boundary between them is written down rather than assumed. This document is the delivery contract: the contractual sections are mandatory wherever they apply (scope boundaries, input field rules, state machines with illegal-transition handling, permission matrix, error catalogue with degradation behavior, acceptance and change control). Skip project scanning — use the pre-scanned context below.\n\n## Project Context (pre-scanned)\n{project_context_summary}"
- Wait for completion → verify `docs/{sub_feature_name}/srs.md` exists

**2. Tech Design** — Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:tech-design skill for '{sub_feature_name}'. SRS-first mode. Read docs/{sub_feature_name}/srs.md as the authoritative requirements source and populate §3.4–§3.7 from it, carrying its out-of-scope table through to §3.4. Every component in §8.1 must name the FR-*/NFR-* requirements it satisfies; report any requirement you cannot place. Also read docs/project-{feature_name}.md for this sub-feature's dependencies on its siblings. Do not re-ask questions the SRS already answers. IMPORTANT: This will also auto-generate feature specs in docs/features/ as part of Step 7. Skip project scanning in Step 1 — use the pre-scanned context below instead.\n\n## Project Context (pre-scanned)\n{project_context_summary}"
- Wait for completion → verify `docs/{sub_feature_name}/tech-design.md` exists and feature specs exist in `docs/features/`

After each sub-feature completes, display progress:

```
spec-forge project: {feature_name} ({N} sub-features)

  {sub-feature-1}:
    [x] SRS + Tech Design + Feature Specs

  {sub-feature-2}:
    [x] SRS + Tech Design + Feature Specs

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
    [x] srs.md           — delivery contract
    [x] tech-design.md
  {sub-feature-2}/
    [x] srs.md           — delivery contract
    [x] tech-design.md

Feature specs (auto-generated with tech-design):
  docs/features/
    [x] overview.md
    [x] {component-1}.md
    [x] {component-2}.md
    ...

Review: {PASS | N issues fixed | N issues remaining}
Project manifest: docs/project-{feature_name}.md

Hand off to implementation:
  /code-forge:plan @docs/features/                        → Plan from the feature specs
  /code-forge:impl {component-name}                       → Execute tasks (TDD from SRS acceptance criteria)

Optional (on-demand):
  /spec-forge:test-cases {sub-feature-name}               → QA coverage matrix, if you need one beyond code-forge's TDD
  /spec-forge:prd {feature_name}                          → Project-level business case, if a go/no-go decision is still needed
```

Each sub-feature now has its own `srs.md` — that is the contract for whoever implements it. Do not offer to "generate the SRS" here; it already exists.

#### D.2: Detect Existing Progress

Scan for existing documents matching `feature_name`:
- `ideas/{feature_name}/` (idea draft)
- `docs/{feature_name}/prd.md` (business case)
- `docs/{feature_name}/srs.md` (delivery contract)
- `docs/{feature_name}/tech-design.md` (tech design)
- `docs/features/overview.md` (feature specs)

Determine which stages are already complete.

If the SRS, tech-design, and feature specs all exist, inform the user and ask:
- Regenerate tech-design and feature specs only (keep the SRS and everything upstream) — **Recommended**, since the requirements contract is usually the part you want to preserve
- Regenerate from the SRS down (re-specify requirements, then redesign)
- Regenerate all (start over from idea)
- Cancel

If some stages are complete, show progress and ask:
- Continue from next missing stage (Recommended)
- Regenerate all
- Cancel

> **Regenerating an existing SRS is a contract change, not a refresh.** If `docs/{feature_name}/srs.md` already exists and the user chooses to regenerate it, warn them first: issued `FR-*`/`NFR-*` IDs are referenced by the tech design, the feature specs, and any code-forge plan already generated — and possibly by an agreement with whoever is implementing it. The regeneration must preserve existing IDs (split → original ID stays with one part; removal → the ID is retired, never reused) and log the change in §10.4. Silently renumbering severs every downstream reference at once.

#### D.2a: Stage 3 — PRD (conditional)

Decide whether this chain needs a business case before specifying requirements. Run the PRD stage when **any** of these hold:

- The work is a new product or a new product line rather than a feature of an existing one.
- A go/no-go decision, budget approval, or stakeholder alignment is still outstanding.
- The user explicitly asked for a PRD, a business case, or market/competitive analysis.

Skip it — and say so in the progress display — when the decision to build is already settled and the work is a well-understood feature. A PRD written after the decision has been made is ceremony, and its market sizing and feasibility verdict are the parts most prone to fabrication when there is no real evidence behind them.

If running, launch `Task(subagent_type="general-purpose")` with: "Invoke the spec-forge:prd skill for '{feature_name}'. Produce the business case and product definition at docs/{feature_name}/prd.md: market context, demand evidence, feasibility verdict, personas, user stories, capability scope, success metrics, milestones, risks. Do NOT write field-level rules, state machines, error codes, or Given/When/Then acceptance criteria — those belong to the SRS generated in the next stage. Do NOT draw a solution architecture diagram. If an idea draft exists at ideas/{feature_name}/draft.md, use it for problem definition, demand validation, and competitive research rather than re-deriving them. Skip project scanning — use the pre-scanned context below.\n\n## Project Context (pre-scanned)\n{project_context_summary}"

Wait for completion → verify `docs/{feature_name}/prd.md` exists. Proceed to D.2b.

#### D.2b: Stage 4 — SRS (mandatory)

**This stage is never skipped.** It produces the delivery contract — the document an implementation team, an external vendor, or code-forge is held to. A chain that reaches the tech design without it is incomplete, not merely abbreviated: the design would rest on unstated requirements, and nobody could settle afterwards whether the delivered code is correct.

Build the sub-agent prompt according to what upstream context exists:

- **PRD exists**: "Invoke the spec-forge:srs skill for '{feature_name}'. Upstream PRD at docs/{feature_name}/prd.md — read it and trace every PRD-*-NNN capability into one or more FR-*-NNN requirements, then build the traceability matrix in §9."
- **Only an idea draft exists**: "Invoke the spec-forge:srs skill for '{feature_name}'. No PRD; upstream idea draft at ideas/{feature_name}/draft.md — derive scope, requirements, and acceptance criteria from its problem statement and MVP scope. Flag in §9 that product-level traceability is limited."
- **Neither exists**: "Invoke the spec-forge:srs skill for '{feature_name}'. No upstream documents — work from the user's request, asking only the questions whose answers materially change the requirements, and record every inference as an explicit stated assumption the user can correct."

Append to every variant: "This document is the delivery contract, so the contractual sections are mandatory wherever they apply: §3.2 Scope Boundaries with a populated out-of-scope table, Input Field Rules for every requirement that accepts input, §5.4 State Machines including illegal-transition handling, §5.5 Permission Matrix with denial behavior, §5.6 Error Catalogue with degradation behavior per dependency, and §10 Acceptance and Change Control. Where one genuinely does not apply, mark it N/A with a one-line reason rather than omitting the heading. Skip project scanning — use the pre-scanned context below.\n\n## Project Context (pre-scanned)\n{project_context_summary}"

Launch `Task(subagent_type="general-purpose")`. Wait for completion → verify `docs/{feature_name}/srs.md` exists and passed its structural gate. Proceed to D.3.

#### D.3: Stage 5 — Tech Design

**CRITICAL**: Do NOT invoke skills directly in the main context. Each stage MUST be a `Task(subagent_type="general-purpose")` call. The sub-agent handles scanning, user questions, and document generation independently. After it completes, its context is discarded and only a brief summary returns to the main context.

The SRS from D.2b is the design's input. The tech design answers *how* the specified requirements will be met — it does not re-elicit *what* they are.

prompt = "Invoke the spec-forge:tech-design skill for '{feature_name}'. SRS-first mode. Read docs/{feature_name}/srs.md as the authoritative requirements source: populate §3.5 User Scenarios from its functional requirement flows, §3.6 Acceptance Criteria from its FR acceptance criteria, §3.4 Scope from its §3.2 Scope Boundaries (carrying the out-of-scope table through), and derive §3.7 Success Metrics from its NFR targets. Every component in §8.1 must name the FR-*/NFR-* requirements it satisfies, and every FR must be satisfied by at least one component — report any requirement you cannot place rather than silently dropping it. Do NOT re-ask the user questions the SRS already answers; ask only about implementation trade-offs the requirements deliberately leave open. If docs/{feature_name}/prd.md exists, read it for product intent behind the requirements. IMPORTANT: After writing the tech-design, also auto-generate feature specs in docs/features/ as part of Step 7. Skip project scanning in Step 1 — use the pre-scanned context below instead.\n\n## Project Context (pre-scanned)\n{project_context_summary}"

Launch `Task(subagent_type="general-purpose")` with the appropriate prompt above.
Wait for completion → verify `docs/{feature_name}/tech-design.md` exists and feature specs exist in `docs/features/`.

After completion, scan `docs/features/` to count generated specs, then display:
```
spec-forge chain: {feature_name}
  [x] Idea           ideas/{feature_name}/
  [x] Decompose      single feature
  [-] PRD            skipped — {reason, e.g. "decision to build already made"}
  [x] SRS            docs/{feature_name}/srs.md
  [x] Tech Design    docs/{feature_name}/tech-design.md
  [x] Feature Specs  docs/features/overview.md + {actual count from scan} component specs
  [ ] Review         pending...
```

Proceed to D.4 (Review).

#### D.4: Stage 6 — Review

After all documents are generated (SRS + tech-design + feature specs), review them for quality and consistency. This stage catches issues like incomplete sections, internal contradictions, missing traceability, and vague specifications before the chain completes.

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
  [x] ideas/{feature_name}/              — validated demand
  [-] docs/{feature_name}/prd.md         — skipped: {reason}   (or [x] business case)
  [x] docs/{feature_name}/srs.md         — delivery contract: {N} FR, {M} NFR
  [x] docs/{feature_name}/tech-design.md — architecture & design
  [x] docs/features/overview.md          — feature index
  [x] docs/features/{component-1}.md     — implementation spec
  [x] docs/features/{component-2}.md     — implementation spec
  ...
  [x] Review                             — {PASS | N issues fixed | N issues remaining}

Hand off to implementation:
  /code-forge:plan @docs/features/                        → Plan from the feature specs
  /code-forge:plan @docs/{feature_name}/tech-design.md    → Single-component alternative
  /code-forge:impl {component-name}                       → Execute tasks (TDD from SRS acceptance criteria)
  /code-forge:review {component-name}                     → Review code quality

Optional (on-demand):
  /spec-forge:test-cases {feature_name}                   → QA coverage matrix, if you need one beyond code-forge's TDD
  /spec-forge:prd {feature_name}                          → Business case, if a go/no-go decision is still needed
```

**Report the handoff command; do not run it.** Implementation is code-forge's decision to start, not this chain's.

If an idea draft was used, update its status to `graduated`:
```json
{ "status": "graduated", "graduated_to": "docs/{feature_name}/srs.md" }
```

### Route E: `decompose`

Launch `Task(subagent_type="general-purpose")`:
- Sub-agent prompt: "Invoke the spec-forge:decompose skill for '{feature_name}'."
- Wait for completion

After the sub-agent returns:
- If `docs/project-{feature_name}.md` exists: display the manifest and suggest running `/spec-forge {feature_name}` to execute the full chain for all sub-features
- If no manifest (single verdict): inform user and suggest running `/spec-forge {feature_name}` to start the spec chain

> **Note**: Running `/spec-forge {feature_name}` starts from the **Idea** stage if `ideas/{feature_name}/` does not exist yet and the demand is unvalidated. If you only want the requirements contract, run `/spec-forge:srs {feature_name}` directly; if you already have an SRS and only want the design, run `/spec-forge:tech-design {feature_name}`.

### Route F: `audit`

Invoke the spec-forge:audit skill. Pass `argument` as the path to the project to audit (may be a relative path to another project).

### Route G: `analyze`

Invoke the spec-forge:analyze skill. Pass `argument` as the path to the document collection to analyze (may be a relative path to a docs repo).
