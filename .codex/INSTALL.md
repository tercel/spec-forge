# Installing spec-forge for Codex

## Prerequisites

- [Codex](https://github.com/openai/codex) installed and configured
- Git installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tercel/spec-forge.git
```

2. Create the skills directory if it doesn't exist:

```bash
mkdir -p ~/.agents/skills
```

3. Symlink this repository to the Codex skills directory:

```bash
ln -s "$(pwd)" ~/.agents/skills/spec-forge
```

If you are running this from the parent directory instead of the repository root,
use:

```bash
ln -s "$(pwd)/spec-forge" ~/.agents/skills/spec-forge
```

4. Verify the installation:

```bash
test -f ~/.agents/skills/spec-forge/SKILL.md
ls ~/.agents/skills/spec-forge/commands/
ls ~/.agents/skills/spec-forge/skills/
# commands/ should include: analyze.md  audit.md  decompose.md  idea.md  prd.md
#                           propagate.md  review.md  spec-forge.md  srs.md
#                           tech-design.md  test-cases.md
# skills/ should include the child skill directories.
```

## Usage

Once installed, the following commands are available in Codex:

- `/spec-forge:idea <name>` — Interactive brainstorming and demand validation
- `/spec-forge:decompose <name>` — Decompose project into sub-features
- `/spec-forge:tech-design <name>` — Generate Tech Design + Feature Specs
- `/spec-forge <name>` — Run full chain (Idea → Decompose → Tech Design + Feature Specs → Review)
- `/spec-forge:prd <name>` — Generate PRD (on-demand, for stakeholders)
- `/spec-forge:srs <name>` — Generate SRS (on-demand, for compliance)
- `/spec-forge:test-cases <name>` — Generate test cases with coverage matrix (on-demand, for QA)
- `/spec-forge:review <name>` — Review generated specs for quality and consistency
- `/spec-forge:audit [path]` — Audit project docs against code
- `/spec-forge:analyze [path]` — Analyze a document collection
- `/spec-forge:propagate ...` — Propagate upstream doc changes downstream

## Notes

This repository is installed as a Codex skill tree via `~/.agents/skills`. It is
not currently packaged as a Codex plugin with `.codex-plugin/plugin.json` because
the repository contains `skills/shared/` as a shared reference directory rather
than an invokable skill. Packaging as a Codex plugin would require either moving
shared references out of `skills/` or otherwise adapting the layout to the plugin
validator.

## Uninstall

```bash
rm ~/.agents/skills/spec-forge
```
