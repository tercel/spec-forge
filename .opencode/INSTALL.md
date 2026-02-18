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
# Should list: decompose.md  feature.md  idea.md  prd.md  spec-forge.md  srs.md  tech-design.md  test-plan.md
```

## Usage

Once installed, the following commands are available in OpenCode:

- `/spec-forge:idea <name>` — Interactive brainstorming and demand validation
- `/spec-forge:feature <name>` — Generate lightweight feature specification
- `/spec-forge:decompose <name>` — Decompose project into sub-features
- `/spec-forge <name>` — Run full chain (PRD → SRS → Tech Design → Test Plan)
- `/prd <product/feature name>` — Generate a Product Requirements Document
- `/srs <feature name>` — Generate a Software Requirements Specification
- `/tech-design <feature name>` — Generate a Technical Design Document
- `/test-plan <feature name>` — Generate a Test Plan & Test Cases

## Uninstall

```bash
rm ~/.config/opencode/skills/spec-forge
```
