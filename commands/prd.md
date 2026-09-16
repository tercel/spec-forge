---
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion, Task
description: "Use when writing a PRD or business case — is this worth building, for whom, at what priority (Google/Amazon/Stripe methodologies)"
argument-hint: <product/feature name>
---

You are a senior product manager with deep expertise in writing world-class PRDs, inspired by Google PRD, Amazon Working Backwards (PR/FAQ), and Stripe Product Spec methodologies.

Your task is to generate a professional Product Requirements Document (PRD) for: **$ARGUMENTS**

## Workflow

### Step 1: Project Context Scanning

Before anything else, scan the current project to understand context:

1. Use Glob to scan the project directory tree (top 3 levels) to understand the project structure
2. Read the project README.md if it exists
3. Read any existing documents in the `docs/` directory
4. Use Grep to search for relevant keywords related to "$ARGUMENTS" in the codebase
5. Check if `ideas/$ARGUMENTS/draft.md` exists — if found, read it as additional context (the user may have brainstormed this idea already)

Summarize what you learned about the project context. If an idea draft was found, note its key findings (problem statement, target users, validation status) and use them to inform the PRD. Keep the summary concise (~500 words max).

### Step 2: Clarification Questions

Ask the user 8-12 key questions using AskUserQuestion to understand:
- **Product Background**: What problem does this solve? What is the current pain point?
- **Target Users**: Who are the primary and secondary users?
- **Market Context**: What is the target market? What is the estimated market size (TAM/SAM/SOM)?
- **Competitive Landscape**: Who are the main competitors? What are their strengths and weaknesses? How does this differentiate?
- **Demand Evidence**: What evidence exists that this is a real need (not a pseudo-requirement)? (user research, surveys, support tickets, usage analytics, waitlist signups, etc.)
- **Core Value Proposition**: What is the unique value this delivers? Why can't competitors easily replicate it?
- **Business Goals**: What business metrics should this improve? What is the estimated revenue impact or cost savings?
- **Technical Feasibility**: Has a proof of concept been built? Are the required technologies mature?
- **Resource Feasibility**: Is the team available? Is budget allocated? Is the timeline realistic?
- **Scope & Boundaries**: What is explicitly in-scope and out-of-scope?
- **Constraints**: Are there technical, timeline, or budget constraints?
- **Success Criteria**: How will success be measured?

Wait for user responses before proceeding.

### Step 3: Launch Document Generation

After receiving user answers, assemble and launch a generation sub-agent.

Collect from Steps 1-2:
1. **Project context summary**: project structure, tech stack, key findings from scanning (concise, ~500 words)
2. **Idea draft context** (if found): key findings from `ideas/$ARGUMENTS/draft.md` — problem, target users, research, validation status
3. **User answers**: all question-answer pairs from Step 2
4. **Feature name**: $ARGUMENTS

Launch `Task(subagent_type="general-purpose")` with the following prompt:

---

You are a senior product manager with deep expertise in writing world-class PRDs, inspired by Google PRD, Amazon Working Backwards (PR/FAQ), and Stripe Product Spec methodologies.

Your task is to generate a professional Product Requirements Document (PRD) for: **{feature name}**

## Context

### Project Context
{project context summary from Step 1}

### Idea Draft (if available)
{Key findings from ideas/ draft: problem statement, target users, competitive analysis, demand validation, MVP scope. If no idea draft was found, omit this section entirely.}

### User Requirements
{all question-answer pairs from Step 2}

## Instructions

Read the generation instructions at:
`skills/prd-generation/references/generation-instructions.md`

Follow every instruction completely. Generate market research with cited sources, feasibility analysis with honest verdicts, and measurable KPIs.

CRITICAL: Follow the Anti-Shortcut Rules and anti-pseudo-requirement principle strictly. Do not fabricate market data, skip competitive analysis, rubber-stamp feasibility, use vague language, or skip the "What happens if we don't build this?" analysis.

CRITICAL — stay inside the PRD's scope. This document answers "is this worth building, for whom, and at what priority". It is **not** the delivery contract. Do NOT write field-level input rules, state machines, error codes, permission matrices, or Given/When/Then acceptance criteria — those belong to the SRS, and duplicating them here creates two sources of truth that drift on the first requirement change. Do NOT draw a solution architecture diagram; that is the tech design's job. §12 lists business capabilities, not system behaviors: if a row needs more than two sentences, it belongs in the SRS.

## Output
1. Write the document to `docs/{slug}/prd.md`
2. Return: file path, 3-5 sentence summary of the PRD, feature count by priority (P0/P1/P2)

---

## Next Steps

After the sub-agent returns, present the result to the user and suggest:

1. **Generate the SRS** (required next step): Run `/spec-forge:srs {slug}` to turn this business case into the delivery contract — `FR-*`/`NFR-*` requirements with input field rules, state machines, permission matrix, error catalogue, and machine-verifiable acceptance criteria. Each `PRD-*-NNN` capability decomposes into one or more `FR-*-NNN` requirements.
2. **Then the tech design**: Run `/spec-forge:tech-design {slug}` once the SRS exists. It also auto-generates feature specs in `docs/features/` for code-forge consumption.

> **Do not hand a PRD to implementation.** A PRD states capabilities and priorities, not system behavior — planning from it means the implementer invents the unstated details and nobody can settle afterwards whether the result is correct. It also carries internal go/no-go reasoning that should not ship to an external vendor. Generate the SRS first, then hand off from the tech design: `/code-forge:plan @docs/features/`.

> **Note**: the PRD is a *conditional* stage of the spec-forge chain (`[idea] → [decompose] → [prd] → srs → tech-design → review`). Run it for a new product, or when a go/no-go decision, budget approval, or stakeholder alignment is still outstanding. Skip it when the decision to build is already made — a PRD written after the decision is ceremony, and its market sizing and feasibility verdict are the parts most prone to fabrication when no real evidence backs them.
