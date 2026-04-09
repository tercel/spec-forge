### Doc Discipline: Doc-First Over Doc-Patch

These rules apply to **every** spec-forge document generation — PRD, SRS, tech design, test cases, test plan, decompose. They are the upstream defense against documentation bloat: parallel `prd-v2.md` files, `## Update 2026-XX-XX:` addendum blocks, deprecated-but-not-deleted sections, and contradictory statements scattered across files. Documentation is *code for humans*; the same anti-bloat principles that govern code (design-first, no `_v2` files, no patch-soup) govern docs.

**The Iron Law of Document Changes:**

> **Read existing docs first. Edit in place. Never create parallel versions. Git is the version system; the document itself only ever expresses the current state.**

#### The Four Rules

1. **Read first — discover what already exists.**
   Before generating a new document or section, scan the project's existing documentation thoroughly. Use `Glob` to find all `.md` files under `docs/`, `specs/`, `design/`, `architecture/`, `ideas/`, and the project root. Use `Grep` to find existing discussion of the topic, terms, requirements, components, or modules you are about to write about. You must be able to answer "what does the project already say about this?" before adding anything new.

2. **Edit in place, do not branch.**
   When existing documentation already covers the topic, **edit it directly**. Never create:
   - `prd-v2.md`, `prd.new.md`, `prd-2026.md`, `prd-revised.md`, or any versioned parallel
   - `## Update 2026-04-09: New Requirement` addendum blocks at the end of an existing doc
   - `change-request-001.md`, `addendum.md`, `errata.md` style separate files for changes
   - `~~deprecated~~` strikethrough sections that are kept "for historical reference"
   - Duplicate sections in two places "in case the reader misses one"
   The only exception is when the project has publicly released a versioned contract (e.g., `api-v1.md` exposed to external customers under a frozen contract). In that case, the old version is a **release artifact** preserved for compatibility, not a hedge against editing.

3. **Single source of truth per concept.**
   Each requirement, decision, term, metric, or component must have exactly **one** authoritative location. Other documents may reference it, but must not restate its content. If you find the same concept defined in two places with even slightly different wording, you have a bug — pick one location as authoritative and replace the other with a reference. Inconsistency is worse than duplication, but duplication causes inconsistency.

4. **Upstream → downstream propagation is the author's responsibility.**
   Project documents form a chain: Idea → PRD → SRS → Tech Design → Feature Specs → Test Cases → README. When you change an upstream document, you are responsible for either (a) updating every downstream document the change touches, or (b) running `/spec-forge:propagate` to discover and resolve the staleness systematically. Never leave the chain partially updated — partial updates are how docs lose the trust of the team.

#### Pre-Generation Checklist (run before writing any new spec content)

Before generating or modifying spec content, answer all five questions in order:

1. **What documents exist?** List every `.md` file in `docs/`, `specs/`, `design/`, `ideas/`, and adjacent locations. Read the relevant ones at section level. If `spec-forge:analyze` was recently run, use its landscape report instead of re-scanning.
2. **What does the project already say about this topic?** Grep for the topic's keywords, related terms, requirement IDs, component names. List every existing mention with file:line.
3. **Reuse, extend, or new?** For each section/requirement/decision you are about to write, decide:
   - **REUSE** — the existing document already says this correctly. Do not duplicate; reference it.
   - **EXTEND** — the existing document discusses this but needs more detail or revision. Edit the existing file, do not add a parallel section.
   - **NEW** — genuinely no overlap. Create the new content, but link from related existing docs.
4. **What stays stable?** Enumerate which existing requirement IDs, terms, defined names, and section titles must NOT change to preserve traceability with code, tests, and downstream docs.
5. **What downstream docs will need updating?** If this is a change to an existing doc rather than a fresh creation, list every doc that references the changed concepts. The user must know upfront what the propagation cost is.

If you cannot answer all five, you have not read enough — go back to rule 1.

#### Anti-Patterns to Avoid

These are signals that you are doc-patching instead of doc-designing:

- **The `prd-v2.md` file.** Creating a new file because the old one is "scary" or "long". Either edit the old one in place or split it into multiple focused docs (one per topic) — never two parallel versions of the same topic.
- **The trailing `## Update` block.** Appending update logs at the end of the document instead of editing the relevant section in place. Updates belong in `git log`, not in the document body.
- **The `~~strikethrough~~` graveyard.** Marking deprecated content with strikethrough or `(DEPRECATED)` and leaving it in. Either delete it (`git log` remembers) or remove the deprecation by updating the content.
- **The "see also" forest.** Adding `(see also: srs.md§3.2, tech-design.md§4.1)` everywhere instead of consolidating. References are fine when crossing layers (PRD references the feature it describes); they are noise when used within a single document.
- **The synonyms parade.** Using "User Account", "Customer Profile", and "Member Record" interchangeably for the same concept. Pick one term and use it everywhere.
- **The duplicate definition.** Defining the same term, metric, or requirement in two sections "for clarity". Define once, reference elsewhere.
- **The orphaned addendum file.** Creating `addendum.md`, `change-notes.md`, `errata.md`, or `meeting-notes-2026-04.md` next to specs and never folding the content back in.
- **The retroactive PRD.** Writing a PRD after the SRS / tech-design / code already exist, just to "have one for the file". A PRD that does not actually drive decisions is dead documentation.
- **The doc-shaped stream-of-consciousness.** Filing every requirement change as a new bullet at the bottom of a list rather than reorganizing the list to express the current intent.

#### When Doc-Patching IS Acceptable

Doc-first does not mean "every change requires a global refactor". Direct in-place editing — even if small and localized — is still doc-first as long as:

- You read the existing content before editing
- You edit the right section (not append at the end)
- You leave the document expressing the *current* state, not a history of changes
- You note any downstream propagation needs

What's NOT acceptable is creating parallel content to avoid touching existing content. The forbidden pattern is structural ("v2 file", "addendum", "see also forest"), not size-based.

#### How This Interacts With code-forge:plan and code-forge:fix

- `code-forge:plan Step 4.5` (reuse discovery) is the *code-side* mirror of this discipline. When the planner generates tasks based on a feature spec, it already prefers "modify existing X" over "create new Y". For docs to feed cleanly into that, the spec itself must reflect the same discipline — no contradictions, no parallel versions, no duplicate concepts.
- `code-forge:fix` traces bug fixes back to upstream documents (Level 2 task → Level 3 plan → Level 4 feature spec). For that trace-back to work, upstream docs must be the authoritative current state. If you have `prd.md` and `prd-v2.md`, the trace-back is broken before it starts.
- `spec-forge:propagate` is the symmetric tool: when you change an upstream doc, it walks downstream to keep everything consistent. It only works if every layer has a single canonical source.

#### How This Interacts With spec-forge:analyze and spec-forge:audit

These two skills are *detectors* for doc-first violations:

- `spec-forge:analyze` produces a landscape map of all docs and surfaces themes, conflicts, gaps, redundancies, and staleness. Run it periodically to catch drift.
- `spec-forge:audit` checks docs against the actual code and against quality criteria.

If either skill flags duplication, conflict, or `_v2` files on docs you authored, doc-first was skipped — go back and consolidate rather than acknowledging the warning and moving on.
