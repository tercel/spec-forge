#!/usr/bin/env python3
"""Collect project + document facts for the spec-forge Project Context Protocol.

Replaces the by-hand PC.1-PC.6 scan (project-context.md) and the per-skill
upstream-document discovery: language mix, build files, dependency names,
detected frameworks, database/auth/external-api signals, test framework +
command, source-tree top level, PLUS a document inventory (existing prd/srs/
tech-design/feature specs/idea drafts with status) and the requirement IDs
declared in each upstream doc.

It is deliberately a FACTS COLLECTOR, not an analyst. Architecture pattern
recognition, project-profile labelling, and risk assessment stay with the
model (PC.3/PC.4) — use this JSON as the starting inventory and verify it.

Usage:
  sf-scan.py [--root PATH] [--max-tree N] [--docs-only]
Output: JSON on stdout.
"""

import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_common as sf

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    tomllib = None

EXT_LANG = {
    ".py": "Python", ".ts": "TypeScript", ".tsx": "TypeScript",
    ".js": "JavaScript", ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".go": "Go", ".rs": "Rust", ".java": "Java", ".rb": "Ruby", ".php": "PHP",
    ".cs": "C#", ".kt": "Kotlin", ".swift": "Swift", ".scala": "Scala",
    ".c": "C", ".h": "C", ".cpp": "C++", ".cc": "C++", ".hpp": "C++", ".ex": "Elixir",
}

BUILD_FILES = [
    "package.json", "pyproject.toml", "requirements.txt", "setup.py", "setup.cfg",
    "Cargo.toml", "go.mod", "build.gradle", "build.gradle.kts", "pom.xml",
    "composer.json", "Gemfile", "Makefile", "mix.exs",
]

# Substring (lowercased) -> framework label, matched against dependency names.
# Illustrative, NOT exhaustive — the model classifies the profile from the raw
# dependency list this script also emits, so an unlisted/newer framework is
# still recognisable.
FRAMEWORKS = {
    "fastapi": "FastAPI", "flask": "Flask", "django": "Django", "starlette": "Starlette",
    "express": "Express", "@nestjs/core": "NestJS", "koa": "Koa", "hono": "Hono",
    "fastify": "Fastify", "next": "Next.js", "react": "React", "vue": "Vue",
    "svelte": "Svelte", "@angular/core": "Angular", "click": "Click", "typer": "Typer",
    "spf13/cobra": "Cobra", "gin-gonic/gin": "Gin", "labstack/echo": "Echo",
    "clap": "clap", "actix-web": "Actix-web", "axum": "Axum", "spring-boot": "Spring Boot",
    "langchain": "LangChain", "crewai": "CrewAI", "autogen": "AutoGen",
}

SIGNAL_DEPS = {
    "database": ["prisma", "sqlalchemy", "sequelize", "gorm", "diesel", "knex",
                 "mongoose", "typeorm", "alembic", "pg", "psycopg", "mysql", "sqlite"],
    "auth": ["jsonwebtoken", "pyjwt", "passport", "oauth", "authlib", "bcrypt",
             "argon2", "jose"],
    "external_api": ["axios", "requests", "httpx", "reqwest", "node-fetch", "got"],
}

TEST_GLOBS = [".test.", ".spec.", "_test.go", "_test.rs"]
SOURCE_DIR_NAMES = ["src", "app", "lib", "cmd", "internal", "pkg"]

# Upstream document filename patterns -> logical type.
DOC_TYPES = [
    ("prd", re.compile(r"(^|/)prd\.md$", re.I)),
    ("srs", re.compile(r"(^|/)srs\.md$", re.I)),
    ("tech-design", re.compile(r"(^|/)tech-design\.md$", re.I)),
    ("test-cases", re.compile(r"(^|/)test-cases\.md$", re.I)),
    ("test-plan", re.compile(r"(^|/)test-plan\.md$", re.I)),
    ("idea-draft", re.compile(r"(^|/)ideas/[^/]+/draft\.md$", re.I)),
    ("project-manifest", re.compile(r"(^|/)project-[^/]+\.md$", re.I)),
]
_IDEA_STATUS = re.compile(r"(?im)^\s*(?:>\s*)?(?:[-*]\s*)?\**\s*status\**\s*[:：]\s*([A-Za-z_-]+)")


def _idea_status(doc_path, text):
    """Return an idea's status. The authoritative source is the sibling
    state.json; fall back to a `Status:` line in draft.md."""
    state_path = os.path.join(os.path.dirname(doc_path), "state.json")
    if os.path.isfile(state_path):
        try:
            status = sf.read_json(state_path).get("status")
            if status:
                return str(status).lower()
        except (OSError, ValueError):
            pass
    m = _IDEA_STATUS.search(text)
    return m.group(1).lower() if m else None


def _read_lines(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read().splitlines()
    except OSError:
        return []


def _strip_pkg(name):
    name = name.strip().strip('"').strip("'")
    name = re.split(r"[<>=!~;\[\(\s]", name, maxsplit=1)[0]
    return name.strip()


def _toml_keys(path, *table_path):
    if tomllib is None:
        return []
    try:
        with open(path, "rb") as fh:
            data = tomllib.load(fh)
        for key in table_path:
            data = data.get(key, {})
        return list(data.keys()) if isinstance(data, dict) else []
    except (OSError, ValueError):
        return []


def extract_dependencies(root):
    deps = set()
    raw = {}

    pkg = os.path.join(root, "package.json")
    if os.path.isfile(pkg):
        try:
            with open(pkg, encoding="utf-8") as fh:
                data = json.load(fh)
            names = list(data.get("dependencies", {})) + list(data.get("devDependencies", {}))
            deps.update(names)
            raw["package.json"] = {"deps": names, "scripts": data.get("scripts", {})}
        except (OSError, ValueError):
            pass

    pyproject = os.path.join(root, "pyproject.toml")
    if os.path.isfile(pyproject) and tomllib is not None:
        names = []
        try:
            with open(pyproject, "rb") as fh:
                data = tomllib.load(fh)
            for d in data.get("project", {}).get("dependencies", []):
                names.append(_strip_pkg(d))
            names += [_strip_pkg(k) for k in _toml_keys(pyproject, "tool", "poetry", "dependencies")]
        except (OSError, ValueError):
            pass
        deps.update(n for n in names if n and n.lower() != "python")
        raw["pyproject.toml"] = [n for n in names if n]

    req = os.path.join(root, "requirements.txt")
    if os.path.isfile(req):
        names = [_strip_pkg(l) for l in _read_lines(req)
                 if l.strip() and not l.strip().startswith(("#", "-"))]
        deps.update(names)
        raw["requirements.txt"] = names

    cargo = os.path.join(root, "Cargo.toml")
    if os.path.isfile(cargo):
        names = _toml_keys(cargo, "dependencies")
        deps.update(names)
        raw["Cargo.toml"] = names

    gomod = os.path.join(root, "go.mod")
    if os.path.isfile(gomod):
        names = re.findall(r"^\s*([\w\.\-/]+)\s+v[\d]", "\n".join(_read_lines(gomod)), re.M)
        deps.update(names)
        raw["go.mod"] = names

    gemfile = os.path.join(root, "Gemfile")
    if os.path.isfile(gemfile):
        names = re.findall(r"""gem\s+['"]([^'"]+)['"]""", "\n".join(_read_lines(gemfile)))
        deps.update(names)
        raw["Gemfile"] = names

    composer = os.path.join(root, "composer.json")
    if os.path.isfile(composer):
        try:
            with open(composer, encoding="utf-8") as fh:
                data = json.load(fh)
            names = list(data.get("require", {})) + list(data.get("require-dev", {}))
            deps.update(names)
            raw["composer.json"] = names
        except (OSError, ValueError):
            pass

    for gradle in ("build.gradle", "build.gradle.kts", "pom.xml"):
        path = os.path.join(root, gradle)
        if os.path.isfile(path):
            text = "\n".join(_read_lines(path))
            names = re.findall(r"['\"]([\w\.\-]+:[\w\.\-]+)(?::[\w\.\-]+)?['\"]", text)
            if gradle == "pom.xml":
                names += re.findall(r"<artifactId>([^<]+)</artifactId>", text)
            deps.update(names)
            raw[gradle] = names

    return {d.lower() for d in deps if d}, raw


def walk_facts(root):
    lang_counts = {}
    test_files = []
    has_dirs = set()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in sf.IGNORE_DIRS and not d.startswith(".")]
        rel_dir = os.path.relpath(dirpath, root)
        base = os.path.basename(dirpath)
        if base in ("prisma", "migrations", "alembic", "__tests__", "tests", "test"):
            has_dirs.add(base)
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXT_LANG:
                lang_counts[EXT_LANG[ext]] = lang_counts.get(EXT_LANG[ext], 0) + 1
            rel = os.path.normpath(os.path.join(rel_dir, fn))
            low = fn.lower()
            if (any(g in low for g in TEST_GLOBS) or low.startswith("test_")
                    or "__tests__" in rel.replace(os.sep, "/")
                    or "/tests/" in ("/" + rel.replace(os.sep, "/") + "/")):
                if len(test_files) < 2000:
                    test_files.append(rel)

    languages = sorted(
        ({"lang": k, "files": v} for k, v in lang_counts.items()),
        key=lambda x: x["files"], reverse=True,
    )
    return languages, test_files, has_dirs


def detect_test(root, deps, raw, test_count):
    framework = command = None
    pkg = raw.get("package.json")
    if pkg:
        if "test" in pkg.get("scripts", {}):
            command = "npm test"
        for fw in ("jest", "vitest", "mocha", "jasmine"):
            if any(fw in d for d in deps):
                framework = fw
                break
    if framework is None and any("pytest" in d for d in deps):
        framework = "pytest"
        command = command or "pytest"
    if os.path.isfile(os.path.join(root, "Cargo.toml")):
        framework = framework or "cargo test"
        command = command or "cargo test"
    if os.path.isfile(os.path.join(root, "go.mod")):
        framework = framework or "go test"
        command = command or "go test ./..."
    if framework is None and test_count and any(
        os.path.isfile(os.path.join(root, f)) for f in ("pyproject.toml", "setup.py", "requirements.txt")
    ):
        framework = "unittest"
        command = command or "python -m unittest"
    mk = os.path.join(root, "Makefile")
    if command is None and os.path.isfile(mk) and re.search(r"(?m)^test:", "\n".join(_read_lines(mk))):
        command = "make test"
    return {"framework": framework, "command": command}


def module_tree(root, max_tree):
    roots = [d for d in SOURCE_DIR_NAMES if os.path.isdir(os.path.join(root, d))] or ["."]
    tree = {}
    for src in roots:
        base = os.path.join(root, src)
        entries = []
        try:
            for name in sorted(os.listdir(base)):
                if name in sf.IGNORE_DIRS or name.startswith("."):
                    continue
                full = os.path.join(base, name)
                if os.path.isdir(full):
                    entries.append(name + "/")
                elif os.path.splitext(name)[1].lower() in EXT_LANG:
                    entries.append(name)
        except OSError:
            continue
        if entries:
            tree[src] = entries[:max_tree]
    return tree


def classify_doc(rel_path):
    for label, rx in DOC_TYPES:
        if rx.search(rel_path):
            return label
    if "/features/" in ("/" + rel_path):
        return "feature-spec"
    return "other"


def scan_documents(root):
    """Enumerate spec documents and pull declared requirement IDs from each."""
    docs = []
    for path in sf.iter_markdown(root):
        rel = os.path.relpath(path, root).replace(os.sep, "/")
        text = sf.read_text(path)
        doc_type = classify_doc(rel)
        ids = sf.extract_ids(text)
        entry = {
            "path": rel,
            "type": doc_type,
            "title": sf.first_title(text),
            "word_count": len(text.split()),
            "declared_ids": {k: v for k, v in ids.items() if v},
        }
        if doc_type == "idea-draft":
            entry["status"] = _idea_status(path, text)
        docs.append(entry)
    return docs


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="Project root (default: auto-detect)")
    parser.add_argument("--max-tree", type=int, default=40, help="Max entries per source dir")
    parser.add_argument("--docs-only", action="store_true",
                        help="Skip code facts; only enumerate documents")
    args = parser.parse_args()

    root = os.path.abspath(args.root) if args.root else sf.find_project_root()

    documents = scan_documents(root)
    doc_index = {}
    for d in documents:
        doc_index.setdefault(d["type"], []).append(d["path"])

    result = {
        "root": root,
        "documents": documents,
        "document_index": doc_index,
        "notes": [
            "Best-effort enumeration only. Verify before relying on it.",
            "Project profile (PC.3) and architecture pattern (PC.4) are NOT inferred "
            "here — do that reasoning yourself from the facts below.",
        ],
    }

    if not args.docs_only:
        deps, raw = extract_dependencies(root)
        languages, test_files, has_dirs = walk_facts(root)
        build_files = [f for f in BUILD_FILES if os.path.isfile(os.path.join(root, f))]
        frameworks = sorted({label for key, label in FRAMEWORKS.items()
                             if any(key in d for d in deps)})
        signals = {}
        for signal, needles in SIGNAL_DEPS.items():
            signals[signal] = any(any(n in d for d in deps) for n in needles)
        if has_dirs & {"prisma", "migrations", "alembic"} or os.path.isfile(os.path.join(root, "diesel.toml")):
            signals["database"] = True

        result.update({
            "languages": languages,
            "primary_language": languages[0]["lang"] if languages else None,
            "build_files": build_files,
            "dependencies": sorted(deps)[:200],
            "frameworks": frameworks,
            "signals": signals,
            "test": {
                "file_count": len(test_files),
                "sample": test_files[:5],
                **detect_test(root, deps, raw, len(test_files)),
            },
            "source_tree": module_tree(root, args.max_tree),
        })

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
