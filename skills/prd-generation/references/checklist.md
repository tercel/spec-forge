# PRD Quality Checklist

Use this checklist to validate every generated PRD before delivering it to the user. Each item must pass or be explicitly marked as intentionally skipped with a justification.

---

## 1. Completeness Check

- [ ] Document Information section is fully filled in (PRD ID, version, author, reviewers, date, status)
- [ ] Revision History table has at least one entry for the initial draft
- [ ] Executive Summary is present and provides a concise overview of the problem, solution, and impact
- [ ] Market Research section includes market sizing (TAM/SAM/SOM) with cited sources
- [ ] Competitive Landscape table lists at least 2 competitors with strengths, weaknesses, and differentiation analysis
- [ ] Value Proposition is clearly stated with evidence of real demand (not a pseudo-requirement)
- [ ] Evidence of Real Demand table includes at least 3 types of validation evidence (user research, surveys, support tickets, analytics, market validation, or revenue estimates)
- [ ] "What Happens If We Don't Build This?" section explicitly states the cost of inaction with specific numbers
- [ ] Feasibility Analysis covers all three dimensions: technical, business, and resource feasibility
- [ ] Feasibility Verdict provides a clear GO / CONDITIONAL GO / NO-GO recommendation
- [ ] User Personas are defined with name, role, demographics, needs, and pain points (minimum two personas)
- [ ] User Stories are written for every persona, each with at least two acceptance criteria
- [ ] Functional Requirements table lists all identified requirements with IDs, descriptions, priorities, and statuses
- [ ] Success Metrics are defined with target values, measurement methods, and current baselines
- [ ] Timeline and Milestones section includes a Gantt chart or equivalent schedule with key dates
- [ ] Risk Assessment Matrix is present with at least two identified risks and their mitigation strategies

## 2. Quality Check

- [ ] Market sizing data cites credible sources and uses realistic assumptions (not inflated vanity numbers)
- [ ] Competitive analysis is honest and balanced (acknowledges competitor strengths, not just weaknesses)
- [ ] Value proposition evidence comes from real data, not assumptions or hypothetical scenarios
- [ ] Feasibility assessment is honest — a NO-GO is acceptable if the evidence doesn't support proceeding
- [ ] Problem Statement clearly articulates the current situation, user pain points, and the opportunity
- [ ] Goals are specific, measurable, achievable, relevant, and time-bound (SMART criteria)
- [ ] Non-Goals explicitly define what is out of scope with rationale for each exclusion
- [ ] Requirements are testable -- each can be verified with a clear pass/fail condition
- [ ] User Stories follow the canonical format: "As a [user type], I want [action] so that [benefit]"
- [ ] Success Metrics have specific numeric targets, not vague qualifiers (no "improve", "increase", or "better" without a number)
- [ ] Mermaid diagrams are included for user journey, feature architecture, and timeline
- [ ] Document does not contain vague or ambiguous language ("good performance", "fast response", "user-friendly", "easy to use", "seamless", "intuitive")

## 3. Consistency Check

- [ ] Terminology is consistent throughout the document (same feature, concept, or component is always referred to by the same name)
- [ ] Requirement IDs follow the PRD-MODULE-NNN naming convention without gaps or duplicates
- [ ] Priority levels (P0/P1/P2) are applied consistently and every P0 item clearly ties to a stated goal
- [ ] Every requirement traces back to at least one goal in the Goals section
- [ ] Personas defined in Section 7 are referenced in the User Stories in Section 8
- [ ] Success Metrics in Section 12 align with and measure the Goals in Section 6

## 4. Format Check

- [ ] All requirement IDs follow the PRD-XXX-NNN format (uppercase module code, zero-padded three-digit number)
- [ ] Mermaid diagram code blocks use the ```mermaid fence and render without syntax errors
- [ ] All tables are properly formatted with aligned columns and no missing cells
- [ ] Document metadata (version, date, status) is complete and uses the correct date format (YYYY-MM-DD)
- [ ] Revision History reflects the current version and all changes made during the drafting process
- [ ] Headings follow the numbered section structure defined in the template (Section 1 through Section 20)
