# PRD Generation Instructions

Follow these steps exactly to generate the PRD document.

## Step 1: Generate Document

Load and follow the PRD template from the skill reference file at:
`skills/prd-generation/references/template.md`

Generate the complete PRD following the template structure. Key requirements:
- Use clear, concise language
- **Market Research & Analysis**: Include market sizing (TAM/SAM/SOM), competitive landscape with at least 2 competitors, and competitive differentiation. Cite real data sources where possible.
- **Value Proposition & Validation**: Clearly state the value proposition. Provide concrete evidence that this is a real need (user research, analytics, support data) — NOT a pseudo-requirement. Include "What happens if we don't build this?" to justify urgency.
- **Feasibility Analysis**: Assess technical, business, and resource feasibility with honest GO / CONDITIONAL GO / NO-GO verdict. Do NOT rubber-stamp everything as GO — be honest.
- Include Mermaid diagrams for user journeys and feature architecture
- Include Mermaid Gantt chart for timeline/milestones
- Prioritize features as P0 (must-have), P1 (should-have), P2 (nice-to-have)
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
- User stories should follow the format: "As a [user type], I want [action] so that [benefit]"
- PRD IDs should follow the format: PRD-<MODULE>-<NNN> (e.g., PRD-AUTH-001)
- Include both goals and non-goals to set clear boundaries

## Anti-Shortcut Rules

The following shortcuts are **strictly prohibited** — they are common AI failure modes that produce low-quality PRDs:

1. **Do NOT fabricate market data.** TAM/SAM/SOM numbers without a cited source are worthless. If real data is unavailable, state "data not available" and recommend the user research it — never invent numbers.
2. **Do NOT skip or trivialize competitive analysis.** Listing zero or only one competitor is unacceptable. Every market has at least indirect competitors. Analyze a minimum of 2 competitors with honest strengths and weaknesses.
3. **Do NOT rubber-stamp the GO verdict.** A feasibility analysis that always concludes "GO" adds no value. Evaluate technical, business, and resource feasibility honestly — CONDITIONAL GO and NO-GO are valid and valuable outcomes.
4. **Do NOT use vague language instead of specific metrics.** Phrases like "improve user experience", "high performance", or "scalable system" are meaningless without numbers. Every success metric must have a concrete target (e.g., "page load < 2s at p95", "NPS > 40").
5. **Do NOT skip the "What happens if we don't build this?" analysis.** This is a critical anti-pseudo-requirement check. If the answer is "nothing significant changes", the feature may not be worth building.
