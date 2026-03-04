# Installing spec-forge for OpenCode

## Prerequisites

- [OpenCode](https://github.com/opencode-ai/opencode) installed and configured
- Git installed

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tercel/spec-forge.git
```

2. Create the skills directory if it doesn't exist:

```bash
mkdir -p ~/.config/opencode/skills
```

3. Symlink to the OpenCode skills directory:

```bash
ln -s "$(pwd)/spec-forge" ~/.config/opencode/skills/spec-forge
```

4. Verify the installation:

```bash
ls ~/.config/opencode/skills/spec-forge/commands/
# Should list: decompose.md  idea.md  prd.md  spec-forge.md  srs.md  tech-design.md  test-plan.md
```

## Usage

Once installed, the following commands are available in OpenCode:

- `/spec-forge:idea <name>` — Interactive brainstorming and demand validation
- `/spec-forge:decompose <name>` — Decompose project into sub-features
- `/spec-forge:tech-design <name>` — Generate Tech Design + Feature Specs
- `/spec-forge <name>` — Run full chain (Idea → Decompose → Tech Design + Feature Specs)
- `/spec-forge:prd <name>` — Generate PRD (on-demand, for stakeholders)
- `/spec-forge:srs <name>` — Generate SRS (on-demand, for compliance)
- `/spec-forge:test-plan <name>` — Generate Test Plan (on-demand, for QA)

## Uninstall

```bash
rm ~/.config/opencode/skills/spec-forge
```
