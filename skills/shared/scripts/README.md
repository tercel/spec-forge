# spec-forge script layer

Deterministic helpers that absorb the mechanical, token-heavy bookkeeping the
skills used to do by hand: config resolution, project + document scanning,
document-structure validation, and traceability/coverage math. The model keeps
the *reasoning* (requirement quality, architecture trade-offs, conflict
judgement); these scripts keep the *record-keeping*.

## Runtime contract

- **Python 3 standard library only.** No third-party packages, no `pip install`,
  no network. Runs anywhere `python3` exists.
- Each CLI is a single file with `--help`. `sf_common.py` is the shared library
  the four CLIs import (they live in the same directory, so the import resolves
  even when a script is invoked by absolute path).
- These scripts are the **single source of truth** for the logic they encode.
  The skill prose says "run the script, use its output" rather than restating
  the algorithm, so the two cannot drift.
- **Graceful degradation:** every skill that calls a script keeps a manual
  fallback for when `python3` is unavailable. Switch to it silently — never
  stop or ask the user.
- **Facts/structure only, never an analyst.** `sf-scan.py` collects signals but
  does not label the project profile or infer the architecture; `sf-verify-doc.py`
  checks structure but does not judge requirement quality; `sf-trace.py` computes
  coverage but does not decide whether a gap is acceptable. Those are model calls.

## Locating the scripts at runtime

A skill runs from the *user's* project directory, not from the spec-forge
install — so a project-cwd glob will not find these scripts. Resolve the path
from the **install** instead, once per session, and reuse it:

1. **Preferred:** `<sf_scripts>` is `../shared/scripts/` relative to the skill
   you are running — the *same* installation, so the script version matches the
   skill version. Do not borrow scripts from a different (possibly stale) cached
   install.
2. **Fallback discovery** (follows symlinks, bash- and zsh-safe):

   ```bash
   find -L ~/.agents/skills ~/.claude/skills ~/.claude/plugins/cache \
     -maxdepth 7 -type f -name sf_common.py -path '*spec-forge*/skills/shared/scripts/*' \
     2>/dev/null | head -1     # use the parent dir
   ```
3. Verify `sf_common.py` exists before use; otherwise fall back to the manual
   path in the skill.

Invoke as `python3 "<sf_scripts>/<script>.py" ...`, quoting both the script path
and any project file arguments (project paths may contain spaces).

## Scripts

### `sf-config.py` — configuration resolver (read-only)
Project-root detection, the three-layer merge (system defaults →
`~/.spec-forge.json` → `<root>/.spec-forge.json`), validation, and directory
resolution. Prints one JSON object: `project_root, config, base_dir, docs_dir,
ideas_dir, features_dir, sources, errors`. On a validation error it reports the
error and falls back to system defaults. Never writes files.

```bash
python3 sf-config.py [--root PATH]
```

### `sf-scan.py` — project + document facts collector (read-only)
One-pass enumeration for the Project Context Protocol (PC.1–PC.6) **plus**
document discovery: language mix, build files, dependency names, detected
frameworks, database/auth/external-api signals, test framework + command,
source-tree top level, **and** a document inventory (existing prd/srs/
tech-design/feature specs/idea drafts with status) with the requirement IDs
declared in each. A FACTS COLLECTOR — profile labelling (PC.3) and architecture
pattern (PC.4) stay with the model.

```bash
python3 sf-scan.py [--root PATH] [--max-tree N] [--docs-only]
```

### `sf-verify-doc.py` — document-structure validator
The deterministic half of the review/audit quality gate for a single document:
non-empty + has a title, recommended sections for its type present, IDs
well-formed and unique (a heading + its ID table row count as one definition),
no leftover template placeholders. Structural problems are errors (non-zero
exit); cosmetic problems are warnings. `--strict` promotes warnings to errors
(use it for a hard gate). Type auto-detects from the filename; `--type unknown`
runs the type-agnostic rules only (for arbitrary external docs).

```bash
python3 sf-verify-doc.py <file> [--type TYPE] [--strict] [--json]
```

### `sf-trace.py` — traceability + coverage bookkeeping
Extract IDs, compute the requirement→downstream coverage matrix, allocate the
next free ID, and cross-check tech-design ↔ feature-spec ↔ overview membership.
Judgement (is a gap acceptable, is a mismatch Critical) stays with the model.

```bash
python3 sf-trace.py ids <file...>
python3 sf-trace.py matrix --upstream U.md --downstream D.md
python3 sf-trace.py next-id --prefix FR --module AUTH --existing srs.md
python3 sf-trace.py chain --tech-design T.md --features-dir docs/features [--overview overview.md]
```

`ids`, `matrix`, and `next-id` always emit JSON; add `--json` to `verify-doc`.

## Tests

`python3 skills/shared/scripts/test_scripts.py` — standard-library `unittest`
covering `sf_common` plus every CLI end-to-end.
