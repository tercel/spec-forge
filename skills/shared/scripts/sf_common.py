"""Shared helpers for the spec-forge script layer.

Used by sf-config.py, sf-scan.py, sf-verify-doc.py, and sf-trace.py. Pure
Python 3 standard library only — no third-party dependencies, no pip installs.
Sibling scripts import this module directly because they live in the same
directory.

The division of labour mirrors code-forge: these scripts own the deterministic
record-keeping (enumeration, ID extraction, cross-reference, structure checks);
the model keeps the reasoning (requirement quality, architecture trade-offs,
conflict judgement). Everything here is a FACTS/STRUCTURE layer, never an
analyst.
"""

import json
import os
import re
from datetime import datetime, timezone

# Project-root markers, highest-priority first. The walk stops at the first
# directory containing any of these.
ROOT_MARKERS = [
    ".spec-forge.json",
    ".git",
    "pyproject.toml",
    "package.json",
    "Cargo.toml",
    "go.mod",
    "build.gradle",
    "pom.xml",
    "Makefile",
]

# Layer 1 of the config merge. _tool is read-only and is always forced back to
# these values after merging (callers must not override it).
SYSTEM_DEFAULTS = {
    "_tool": {
        "name": "spec-forge",
        "description": "Professional specification system: idea -> decompose -> tech-design + feature specs, with optional PRD/SRS/test-cases/audit/analyze/propagate",
        "url": "https://github.com/tercel/spec-forge",
    },
    # Directory conventions. All relative to <base>, which is relative to root.
    "directories": {
        "base": "",
        "docs": "docs/",
        "ideas": "ideas/",
        "features": "docs/features/",
    },
    # Generation posture. adapt_to_profile=true means "omit sections that do not
    # apply to this project rather than filling them with placeholders" — the
    # profile-adaptive discipline the skills enforce.
    "generation": {
        "adapt_to_profile": True,
    },
}

# Requirement / test-case ID grammars used across the spec chain. Word-boundary
# anchored so NFR- never matches inside FR- extraction and vice versa.
ID_PATTERNS = {
    "PRD": r"\bPRD-[A-Z][A-Z0-9]*-\d{3,}\b",
    "NFR": r"\bNFR-[A-Z][A-Z0-9]*-\d{3,}\b",
    "FR": r"\bFR-[A-Z][A-Z0-9]*-\d{3,}\b",
    "TC": r"\bTC-[A-Z][A-Z0-9]*-\d{3,}\b",
    "AC": r"\bAC-\d{1,}\b",
}
# Each pattern is \b-anchored, so the FR- inside "NFR-AUTH-001" is never matched
# as an FR (the 'N' before 'F' leaves no word boundary). No post-hoc de-dup step
# is needed — the boundaries keep the prefixes disjoint.
_ID_COMPILED = {k: re.compile(v) for k, v in ID_PATTERNS.items()}

# Directories never worth walking for docs or source facts.
IGNORE_DIRS = {
    ".git", "node_modules", "dist", "build", "target", ".venv", "venv", "env",
    "__pycache__", ".worktrees", "worktrees", "planning", ".code-forge",
    ".spec-forge", ".next", ".nuxt", "coverage", "vendor", ".mypy_cache",
    ".pytest_cache", ".idea", ".vscode", ".tox", ".gradle", "out", "bin", "obj",
}

# Curly template vars ({placeholder}) and prose stop-words that signal an
# unfinished document. Bracket template tokens ([Feature Name]) are handled
# separately so markdown checkboxes and links are not misflagged.
_CURLY_PLACEHOLDER = re.compile(r"\{[a-z][a-z0-9_]*\}")
_PROSE_PLACEHOLDER = re.compile(r"(?<![A-Za-z])(TBD|TODO|FIXME|XXX)(?![A-Za-z])")
_BRACKET_TOKEN = re.compile(r"\[[A-Z][^\]\n]{0,70}\]")
_MD_CHECKBOX = re.compile(r"^\s*[-*+]\s+\[[ xX]\]")
_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


def now_iso():
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path, data):
    """Write JSON with stable 2-space indentation and a trailing newline."""
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def copy_defaults():
    """Return a deep copy of SYSTEM_DEFAULTS so callers never mutate the template."""
    return json.loads(json.dumps(SYSTEM_DEFAULTS))


def find_project_root(start=None):
    """Walk upward from `start` (or cwd) until a ROOT_MARKER is found.

    Falls back to the starting directory if no marker exists anywhere above.
    """
    start_abs = os.path.abspath(start or os.getcwd())
    cur = start_abs
    while True:
        for marker in ROOT_MARKERS:
            if os.path.exists(os.path.join(cur, marker)):
                return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start_abs
        cur = parent


def deep_merge(base, override):
    """Recursively merge `override` into `base`, returning a new dict."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(root, home=None):
    """Load the three-layer merged config.

    Returns (config, sources, load_errors). load_errors holds messages for
    config files that exist but could not be parsed.
    """
    sources = ["system defaults"]
    config = copy_defaults()
    load_errors = []

    home = home or os.path.expanduser("~")
    user_path = os.path.join(home, ".spec-forge.json")
    project_path = os.path.join(root, ".spec-forge.json")

    for path, label in (
        (user_path, "user config (~/.spec-forge.json)"),
        (project_path, "project config (.spec-forge.json)"),
    ):
        if os.path.isfile(path):
            try:
                config = deep_merge(config, read_json(path))
                sources.append(label)
            except (OSError, ValueError) as exc:
                load_errors.append(f"Failed to read {path}: {exc}")

    # _tool is read-only — restore it regardless of what the layers contained.
    config["_tool"] = copy_defaults()["_tool"]
    return config, sources, load_errors


def validate_config(config):
    """Return a list of validation error strings (empty when valid)."""
    errors = []
    dirs = config.get("directories", {})

    for key in ("base", "docs", "ideas", "features"):
        val = dirs.get(key, "") or ""
        if ".." in val:
            errors.append(f"directories.{key} must not contain '..' (path traversal risk)")
        if val.startswith("/"):
            errors.append(f"directories.{key} must be a relative path (must not start with '/')")

    base = (dirs.get("base", "") or "").strip("/")
    base_head = base.split("/")[0] if base else ""
    if base_head in {"src", "node_modules", "build", ".git"}:
        errors.append(f"directories.base must not be a system/source directory ('{base_head}')")

    adapt = config.get("generation", {}).get("adapt_to_profile")
    if adapt is not None and not isinstance(adapt, bool):
        errors.append("generation.adapt_to_profile must be a boolean")

    return errors


def resolve_dirs(root, config):
    """Resolve base/docs/ideas/features absolute directories from the config."""
    dirs = config.get("directories", {})
    base_dir = os.path.normpath(os.path.join(root, dirs.get("base", "") or ""))
    docs_dir = os.path.normpath(os.path.join(base_dir, dirs.get("docs", "") or ""))
    ideas_dir = os.path.normpath(os.path.join(base_dir, dirs.get("ideas", "") or ""))
    features_dir = os.path.normpath(os.path.join(base_dir, dirs.get("features", "") or ""))
    return {
        "base_dir": base_dir,
        "docs_dir": docs_dir,
        "ideas_dir": ideas_dir,
        "features_dir": features_dir,
    }


# --------------------------------------------------------------------------- #
# Markdown / document helpers
# --------------------------------------------------------------------------- #

def iter_markdown(root, extra_dirs=None):
    """Yield markdown file paths under the common spec directories + root.

    Walks docs/, specs/, design/, architecture/, ideas/ plus any extra_dirs, and
    the top level of root. Skips IGNORE_DIRS. Deterministic (sorted) order.
    """
    seen = set()
    search = ["docs", "specs", "design", "architecture", "ideas"]
    if extra_dirs:
        search += list(extra_dirs)
    results = []

    # Top-level markdown at the root.
    try:
        for name in sorted(os.listdir(root)):
            if name.lower().endswith(".md"):
                full = os.path.join(root, name)
                if os.path.isfile(full):
                    results.append(full)
    except OSError:
        pass

    for rel in search:
        base = os.path.join(root, rel)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if d not in IGNORE_DIRS and not d.startswith("."))
            for fn in sorted(filenames):
                if fn.lower().endswith(".md"):
                    results.append(os.path.join(dirpath, fn))

    for path in results:
        norm = os.path.normpath(path)
        if norm not in seen:
            seen.add(norm)
            yield norm


def iter_headings(text):
    """Yield (level, title, lineno) for every ATX markdown heading."""
    for i, line in enumerate(text.splitlines(), start=1):
        m = _HEADING.match(line)
        if m:
            yield len(m.group(1)), m.group(2).strip(), i


def first_title(text):
    """Return the first H1 heading text, or None."""
    for level, title, _ in iter_headings(text):
        if level == 1:
            return title
    return None


def has_section(text, keyword):
    """True if any heading line contains `keyword` (case-insensitive)."""
    kw = keyword.lower()
    for _, title, _ in iter_headings(text):
        if kw in title.lower():
            return True
    return False


def extract_ids(text):
    """Extract requirement / test-case IDs by prefix.

    Returns {prefix: sorted unique list}. Patterns are word-boundary anchored,
    so the FR- inside an NFR- ID is never counted as an FR.
    """
    found = {k: set() for k in ID_PATTERNS}
    for prefix, rx in _ID_COMPILED.items():
        for m in rx.finditer(text):
            found[prefix].add(m.group(0))
    return {k: sorted(v) for k, v in found.items()}


def id_line_map(text):
    """Return {id: [line numbers]} for every requirement/test-case ID mention."""
    hits = {}
    for i, line in enumerate(text.splitlines(), start=1):
        for rx in _ID_COMPILED.values():
            for m in rx.finditer(line):
                hits.setdefault(m.group(0), []).append(i)
    return hits


def find_placeholders(text):
    """Return [(lineno, token, kind)] for unfinished-template markers.

    kind: 'curly' ({placeholder}), 'prose' (TBD/TODO/...), 'bracket'
    ([Feature Name]). Markdown checkboxes and links are excluded from bracket
    detection. Placeholders are cosmetic by default (warnings) — a generated doc
    should have none, but the caller decides severity.
    """
    out = []
    for i, line in enumerate(text.splitlines(), start=1):
        for m in _CURLY_PLACEHOLDER.finditer(line):
            out.append((i, m.group(0), "curly"))
        for m in _PROSE_PLACEHOLDER.finditer(line):
            out.append((i, m.group(0), "prose"))
        if _MD_CHECKBOX.match(line):
            continue
        for m in _BRACKET_TOKEN.finditer(line):
            token = m.group(0)
            end = m.end()
            # Skip markdown links [text](url) and reference links [text][ref].
            if end < len(line) and line[end] in "([":
                continue
            # Skip anything that is plainly a checkbox residue.
            if token in ("[ ]", "[x]", "[X]"):
                continue
            out.append((i, token, "bracket"))
    return out


# --------------------------------------------------------------------------- #
# Graph helpers
# --------------------------------------------------------------------------- #

def topo_order(node_ids, deps):
    """Return a dependency-respecting order (Kahn's algorithm).

    node_ids: ordered list of node identifiers.
    deps: {node: [dependency nodes]}. Unknown deps are ignored.
    Ties break by original input order. Raises ValueError on a cycle.
    """
    id_set = set(node_ids)
    index = {n: i for i, n in enumerate(node_ids)}
    dep_map = {n: [d for d in deps.get(n, []) if d in id_set] for n in node_ids}

    indegree = {n: len(dep_map[n]) for n in node_ids}
    available = sorted([n for n in node_ids if indegree[n] == 0], key=lambda x: index[x])
    order = []
    while available:
        node = available.pop(0)
        order.append(node)
        for n in node_ids:
            if node in dep_map[n]:
                indegree[n] -= 1
                if indegree[n] == 0:
                    available.append(n)
        available.sort(key=lambda x: index[x])

    if len(order) != len(node_ids):
        remaining = [n for n in node_ids if n not in order]
        raise ValueError(f"Dependency cycle detected among: {remaining}")
    return order
