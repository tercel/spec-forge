# SRS Quality Checklist

Use this checklist to validate the Software Requirements Specification before finalizing. Every item must pass. If any item fails, revise the document and re-check.

## 1. Completeness Check

- [ ] All IEEE 830 sections are present: Introduction, Overall Description, Functional Requirements, Non-Functional Requirements, Data Requirements, External Interface Requirements, Requirements Traceability Matrix, and Appendix
- [ ] All features and user stories from the upstream PRD are covered by at least one functional requirement (no PRD item left unaddressed without justification)
- [ ] Both functional requirements (FR) and non-functional requirements (NFR) are defined -- neither category is missing
- [ ] A data model is included with an entity-relationship diagram and a data dictionary describing all fields, types, and constraints
- [ ] External interface requirements are listed for all relevant categories: user interfaces, hardware interfaces, software interfaces, and communication interfaces
- [ ] The requirements traceability matrix is complete, mapping every PRD item to its corresponding SRS requirement(s) with a coverage status
- [ ] The Definitions, Acronyms, and Abbreviations table is populated with all domain-specific and technical terms used in the document
- [ ] The References table lists all documents cited in the SRS, including the upstream PRD, API specifications, regulatory standards, and design documents

## 2. Quality Check

- [ ] Every requirement is unambiguous -- each requirement has exactly one interpretation and does not use vague terms like "fast," "user-friendly," "efficient," or "robust" without quantitative targets
- [ ] Every functional requirement has testable acceptance criteria written in a verifiable format (e.g., Given/When/Then or explicit pass/fail conditions)
- [ ] Modal verbs are used correctly throughout: "shall" for mandatory requirements, "should" for recommended requirements, "may" for optional requirements
- [ ] Requirements describe WHAT the system must do, not HOW it should be implemented -- no implementation details, specific algorithms, or technology choices appear in requirement descriptions unless they are genuine constraints
- [ ] Boundary conditions are specified for all requirements involving numeric ranges, string lengths, file sizes, date ranges, or collection sizes
- [ ] Error scenarios and alternative flows are documented for each functional requirement, covering invalid input, timeout, unauthorized access, and system failure cases
- [ ] Every non-functional requirement includes a specific, measurable metric with a quantitative target value and a defined measurement method

## 3. Consistency Check

- [ ] All requirement IDs follow the naming convention: FR-MODULE-NNN for functional requirements and NFR-CATEGORY-NNN for non-functional requirements, with zero-padded three-digit numbers
- [ ] Terminology is consistent between the SRS and the upstream PRD -- the same concepts use the same names in both documents, and any differences are explained in the glossary
- [ ] No two requirements conflict with each other -- there are no contradictions between functional requirements, between non-functional requirements, or between functional and non-functional requirements
- [ ] All documents referenced in the body of the SRS are listed in the References table (Section 3.4) with version and date
- [ ] Priority levels (P0, P1, P2) are assigned consistently and align with the priority scheme used in the upstream PRD
- [ ] Requirement IDs referenced in the CRUD matrix, the traceability matrix, and cross-references within the document all correspond to defined requirements

## 4. Format Check

- [ ] All functional requirement IDs follow the FR-XXX-NNN format, where XXX is an uppercase module abbreviation and NNN is a zero-padded three-digit number (e.g., FR-AUTH-001)
- [ ] All non-functional requirement IDs follow the NFR-XXX-NNN format, where XXX is an uppercase category abbreviation (PERF, SEC, REL, AVL, MNT, PRT, USB) and NNN is a zero-padded three-digit number (e.g., NFR-PERF-001)
- [ ] All tables are properly formatted with aligned columns, header rows, and separator rows -- no broken or misaligned table markup
- [ ] Mermaid diagrams (entity-relationship, context, or other) use valid Mermaid syntax and render correctly without errors
- [ ] The requirements traceability matrix includes all four columns (PRD ID, PRD Description, SRS ID(s), Coverage Status) and every row is populated
- [ ] The document follows the section numbering from the template (Sections 1 through 10) with no missing or misnumbered sections
