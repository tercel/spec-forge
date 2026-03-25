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

3. Symlink to the Codex skills directory:

```bash
ln -s "$(pwd)/spec-forge" ~/.agents/skills/spec-forge
```

4. Verify the installation:

```bash
ls ~/.agents/skills/spec-forge/commands/
# Should list: decompose.md  idea.md  prd.md  spec-forge.md  srs.md  tech-design.md  test-cases.md
```

## Usage

Once installed, the following commands are available in Codex:

- `/spec-forge:idea <name>` — Interactive brainstorming and demand validation
- `/spec-forge:decompose <name>` — Decompose project into sub-features
- `/spec-forge:tech-design <name>` — Generate Tech Design + Feature Specs
- `/spec-forge <name>` — Run full chain (Idea → Decompose → Tech Design + Feature Specs)
- `/spec-forge:prd <name>` — Generate PRD (on-demand, for stakeholders)
- `/spec-forge:srs <name>` — Generate SRS (on-demand, for compliance)
- `/spec-forge:test-cases <name>` — Generate Test Plan (on-demand, for QA)

## Uninstall

```bash
rm ~/.agents/skills/spec-forge
```
