### Script Layer: Deterministic Helpers

spec-forge ships a small layer of Python 3 (standard-library-only) scripts that
own the **mechanical bookkeeping** — project + document scanning, structure
validation, ID/traceability math — so the model can spend its judgement on the
parts that need it (requirement quality, architecture trade-offs, conflict
resolution). Full contract: `skills/shared/scripts/README.md`.

**The division of labour:** run the script, use its output as the starting
inventory, then apply reasoning. The scripts never label a project profile,
judge requirement quality, or decide whether a gap is acceptable — those stay
with you.

#### Locating the scripts (`<sf_scripts>`) — resolve once per session

A skill runs from the **user's** project directory, not from the spec-forge
install, so a project-cwd search will not find these scripts. Resolve the path
from the install:

1. **Preferred:** `<sf_scripts>` is `../shared/scripts/` relative to the
   directory of the SKILL.md you are running (a sibling of the `shared/*.md`
   files this skill references). Same install ⇒ script version matches skill
   version — do not pull scripts from a different cached install.
2. **Fallback discovery** (follows symlinks; bash- and zsh-safe):

   ```bash
   find -L ~/.agents/skills ~/.claude/skills ~/.claude/plugins/cache \
     -maxdepth 7 -type f -name sf_common.py -path '*spec-forge*/skills/shared/scripts/*' \
     2>/dev/null | head -1     # use the parent directory
   ```
3. **Verify** `sf_common.py` exists at `<sf_scripts>` before invoking. If it
   cannot be found, or `python3` is unavailable, use the skill's manual
   fallback — **never guess a path, never stop, never ask the user.**

Always quote the script path and any project file arguments (paths may contain
spaces): `python3 "<sf_scripts>/sf-scan.py" --root "<project_root>"`.

#### The four scripts

| Script | Use it for | Replaces manual |
|---|---|---|
| `sf-config.py` | Resolve project root + doc/ideas/features directories (+ optional `.spec-forge.json`). | Root detection, directory guessing |
| `sf-scan.py` | One-pass project + document facts: languages, frameworks, DB/auth signals, test command, **and** the existing-doc inventory with declared requirement IDs. | Project Context Protocol PC.1–PC.6; per-skill upstream-doc discovery |
| `sf-verify-doc.py` | Structure gate for a generated doc: title, sections, ID format/uniqueness, no leftover placeholders. `--strict` for a hard gate. | Hand-running checklist structural items |
| `sf-trace.py` | ID extraction, requirement→downstream coverage matrix, next-free-ID allocation, tech-design↔feature↔overview membership. | Hand-built RTM / coverage counts / ID numbering |

#### Usage pattern in a skill step

> **Fast path (preferred):** resolve `<sf_scripts>`, run
> `python3 "<sf_scripts>/sf-scan.py" --root "<project_root>"`, parse its JSON,
> and use the `documents`, `document_index`, `frameworks`, `signals`, and
> `test` fields directly. **Fallback:** if `python3` is unavailable or the
> script is not found, perform the equivalent scan by hand as described below.

Graceful degradation is mandatory: switch to the manual fallback silently.
