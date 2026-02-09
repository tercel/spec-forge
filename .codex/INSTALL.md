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
# Should list: prd.md  srs.md  tech-design.md  test-plan.md
```

## Usage

Once installed, the following commands are available in Codex:

- `/prd <product/feature name>` — Generate a Product Requirements Document
- `/srs <feature name>` — Generate a Software Requirements Specification
- `/tech-design <feature name>` — Generate a Technical Design Document
- `/test-plan <feature name>` — Generate a Test Plan & Test Cases

## Uninstall

```bash
rm ~/.agents/skills/spec-forge
```
