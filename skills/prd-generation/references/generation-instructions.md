# PRD Generation Instructions

Follow these steps exactly to generate the PRD document.

**What this document is — and where it stops.** The PRD is the business case and product definition: why this is worth building, for whom, what is in scope, at what priority, by when, and how success is measured. It is a decision document read by stakeholders *before* commitment, and largely frozen once the decision is made. It is **not** the delivery contract. The precise system behavior an implementer is held to — field-level input rules, state machines, permission matrices, error codes, Given/When/Then acceptance criteria, interface contracts — belongs to the SRS (`docs/{feature}/srs.md`), which keeps evolving through delivery.

Keeping the two separate is what lets a requirement change without touching market sizing, and what keeps internal go/no-go reasoning out of a document handed to an implementation vendor. When you catch yourself writing a testable condition here, it belongs in the SRS.

## Step 1: Generate Document

Load and follow the PRD template from the skill reference file at:
`skills/prd-generation/references/template.md`

Generate the complete PRD following the template structure. Key requirements:
- Use clear, concise language
- **Market Research & Analysis**: Include market sizing (TAM/SAM/SOM), competitive landscape with at least 2 competitors, and competitive differentiation. Cite real data sources where possible.
- **Value Proposition & Validation**: Clearly state the value proposition. Provide concrete evidence that this is a real need (user research, analytics, support data) — NOT a pseudo-requirement. Include "What happens if we don't build this?" to justify urgency.
- **Feasibility Analysis**: Assess technical, business, and resource feasibility with honest GO / CONDITIONAL GO / NO-GO verdict. Do NOT rubber-stamp everything as GO — be honest.
- Include a Mermaid diagram for the user journey. Do **not** draw a solution architecture diagram — components, services, data stores, and their data flows belong to the tech design (§6). A PRD that prescribes architecture pre-commits engineering decisions before the trade-offs have been analysed, and adds a third diagram that must then be kept in sync with the SRS and the tech design.
- Include Mermaid Gantt chart for timeline/milestones. These are the *business-expected* dates; the engineering task breakdown belongs to the tech design.
- **§11 User Stories**: canonical "As a… I want… so that…" format, each with a one-sentence **Success signal** (the observable outcome) and a **Covered by** field listing the FR IDs that implement it (`TBD (SRS pending)` when no SRS exists yet). Do NOT write Given/When/Then acceptance criteria here.
- **§12 Capability Scope**: list **business capabilities**, not system behaviors. If a row needs more than two sentences to describe, it is a system behavior and belongs in the SRS. §12.1 additionally records capabilities considered and deferred, with a reason and a revisit trigger — distinct from §9.2 Non-Goals, which are things the product will never do.
- Prioritize capabilities as P0 (must-have), P1 (should-have), P2 (nice-to-have)
- Define measurable KPIs/OKRs with specific targets
- Include a risk assessment matrix with likelihood and impact ratings

## Step 2: Quality Check

Load the quality checklist from:
`skills/prd-generation/references/checklist.md`

Run through every item in the checklist. For any failed check, revise the document before finalizing.

## Step 3: Write Output

1. Sanitize the feature name to create a filename slug (lowercase, hyphens, no special chars)
2. Create the `docs/` directory if it doesn't exist
3. Write the final document to `docs/<feature-name>/prd.md`
4. Confirm the file path and provide a brief summary of what was generated

## Important Guidelines

- **Anti-pseudo-requirement principle**: Every feature must be backed by evidence of real demand. If no evidence exists, flag it clearly and recommend validation before committing resources.
- Every requirement should be testable and verifiable
- Use specific numbers instead of vague terms ("99.9% uptime" not "high availability")
- Market sizing must cite sources — do not fabricate market data
- Competitive analysis must be balanced — acknowledge competitor strengths honestly
- Feasibility verdict must be honest — a CONDITIONAL GO or NO-GO is a valid and valuable outcome
- **Consumer Analysis**: Before writing personas, explicitly decide whether the feature serves Human Users, AI Agents, or both. If AI Agent is marked "Yes", include at least one Agent Persona (with Agent Type, Integration Pattern, Context Constraints, and Failure Modes) and at least one Agent User Story with machine-verifiable acceptance criteria.
- User stories should follow the format: "As a [user type], I want [action] so that [benefit]"
- PRD IDs should follow the format: PRD-<MODULE>-<NNN> (e.g., PRD-AUTH-001). A `PRD-*-NNN` identifies a **business capability**; the SRS's `FR-*-NNN` identifies a **system behavior**, and the relationship is one-to-many. These are two levels of one traceability chain, not competing schemes. Never renumber an issued PRD ID — the SRS, the tech design, and any downstream plan reference it.
- Include both goals and non-goals to set clear boundaries

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality PRDs:

1. **Do NOT fabricate market data.** TAM/SAM/SOM numbers without a cited source are worthless. If real data is unavailable, state "data not available" and recommend the user research it — never invent numbers.
2. **Do NOT skip or trivialize competitive analysis.** Listing zero or only one competitor is unacceptable. Every market has at least indirect competitors. Analyze a minimum of 2 competitors with honest strengths and weaknesses.
3. **Do NOT rubber-stamp the GO verdict.** A feasibility analysis that always concludes "GO" adds no value. Evaluate technical, business, and resource feasibility honestly — CONDITIONAL GO and NO-GO are valid and valuable outcomes.
4. **Do NOT use vague language instead of specific metrics.** Phrases like "improve user experience", "high performance", or "scalable system" are meaningless without numbers. Every success metric must have a concrete target (e.g., "page load < 2s at p95", "NPS > 40").
5. **Do NOT skip the "What happens if we don't build this?" analysis.** This is a critical anti-pseudo-requirement check. If the answer is "nothing significant changes", the feature may not be worth building.
6. **Do NOT write the SRS inside the PRD.** Field-level input rules, state machines, permission matrices, error codes, and Given/When/Then acceptance criteria belong to `docs/{feature}/srs.md`. Duplicating them here produces two sources of truth that drift on the first requirement change, and forces a reader to guess which one governs. Keep §12 at capability granularity and let the SRS carry the precision.
