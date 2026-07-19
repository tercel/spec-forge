### Project Context Protocol

**Purpose:** Ground specification documents in the actual project — its tech stack, architecture, existing code, and conventions. This protocol is referenced by generation skills (prd, srs, tech-design, test-cases, decompose) to ensure outputs match reality.

**When NOT needed:** idea (discovery phase, project may not exist yet), analyze (doc-only, no code).

---

#### PC.0 Fast Path (preferred): run the scan script

The mechanical half of this protocol — globbing the tree, reading build files,
matching framework signatures, finding the test command, enumerating existing
docs, and pulling requirement IDs out of them — is done in one pass by the
script layer (`skills/shared/scripts.md`). Resolve `<sf_scripts>` and run:

```bash
python3 "<sf_scripts>/sf-scan.py" --root "<project_root>"
```

Parse the JSON and use it directly:
- `primary_language`, `languages`, `frameworks`, `signals` (database/auth/
  external_api), `test.framework`, `test.command`, `source_tree` → PC.2 / PC.5.
- `documents` + `document_index` (existing prd/srs/tech-design/feature/idea
  docs, with idea `status` and each doc's `declared_ids`) → PC.1 upstream
  detection and the doc-first enumeration.

Then apply **judgement** the script deliberately does not: label the project
**profile** (PC.3) and recognise the **architecture pattern** (PC.4) from the
facts. The script is a facts collector, not an analyst — verify anything you
rely on.

**Fallback:** if `python3` is unavailable or the script is not found, perform
the equivalent scan by hand using PC.1–PC.5 below. Switch silently.

---

#### PC.1 Project Discovery

Scan the project to build basic awareness:

1. **Glob the project tree** (top 3 levels) to discover structure
2. **Read README.md** to understand purpose, architecture, and usage
3. **Scan `docs/`** for existing specifications, ADRs, architecture docs
4. **Detect upstream documents**: `docs/*/prd.md`, `docs/*/srs.md`, `docs/*/tech-design.md`, `ideas/*/draft.md`

#### PC.2 Tech Stack Detection

Identify the actual technology used:

```
Scan: package.json, pyproject.toml, Cargo.toml, go.mod, build.gradle, pom.xml,
      requirements.txt, composer.json, Gemfile, mix.exs
```

Extract (the framework/tool names below are **illustrative, not an exhaustive
list** — `sf-scan.py` emits the raw dependency names; identify the framework
from those dependencies and the code's idioms even when it is unlisted or newer
than this file):
- **Primary language** and version
- **Project framework** (Express, FastAPI, Spring Boot, Gin, Actix-web, React, Vue, Click, Cobra, etc.)
- **Database** (PostgreSQL, MySQL, MongoDB, SQLite, Redis, etc.) — from ORM/driver dependencies
- **Test framework** (Jest, pytest, Go test, cargo test, JUnit, etc.)
- **CI/CD** (GitHub Actions, GitLab CI, CircleCI, etc.) — from config files

#### PC.3 Project Profile

Determine the project type from the framework and file patterns detected in PC.2:

| Signal | Profile |
|--------|---------|
| HTTP framework + route files | **Web API** |
| CLI framework + command files | **CLI Tool** |
| Frontend framework + component files | **Frontend App** |
| LLM/AI framework + tool definitions | **AI Agent** |
| Pipeline/ETL framework | **Data Pipeline** |
| Exported functions only, published package | **Function Library** |
| Client methods + connection management | **SDK / Client Library** |

Also flag:
- **Has database**: Yes / No
- **Has auth**: Yes / No
- **Has external APIs**: Yes / No

#### PC.4 Architecture Awareness

For generation skills that produce architecture-sensitive output (tech-design, test-cases):

1. **Identify module/package boundaries** from directory structure
2. **Detect architectural pattern** (MVC, layered, clean architecture, microservices, monorepo)
3. **Map import/dependency direction** between major modules
4. **Identify key abstractions** (interfaces, traits, abstract classes) that define contracts

This is lighter than code-forge's PA.3 deep scan — spec-forge needs to understand the architecture at a structural level, not parse every function signature.

#### PC.5 Existing Test Infrastructure

For test-related skills (test-cases):

1. **Find test directories and files**
2. **Identify test framework and runner command**
3. **Assess rough coverage** (which modules have tests, which don't)

#### PC.6 Output: Project Context Summary

```
## Project Context

**Profile**: {type} ({language} + {framework})
**Database**: {yes/no — which one}
**Auth**: {yes/no — which method}
**Architecture**: {pattern} ({description})
**Test Framework**: {name} — Command: {command}

### Existing Documents
  docs/{feature}/prd.md — found
  docs/{feature}/tech-design.md — not found
  ideas/{feature}/draft.md — found (status: ready)

### Module Structure
  src/routes/     — API endpoints
  src/services/   — business logic
  src/models/     — data models
```

This summary is passed to the generation sub-agent as context, ensuring the generated spec matches the real project.
