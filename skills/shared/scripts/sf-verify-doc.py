#!/usr/bin/env python3
"""Verify the structural integrity of a spec-forge document.

Covers the deterministic half of the review/audit quality gate: the document is
non-empty and has a title, recommended sections for its type are present, IDs
are well-formed and unique, and there are no leftover template placeholders.
The JUDGEMENT half (requirement quality, vague-vs-concrete specificity, semantic
consistency) stays with the model — this only reports what is mechanically
checkable.

Severity:
  ERROR  structural (file missing/empty, no title, malformed/duplicate IDs)
  WARN   cosmetic/advisory (missing recommended section, leftover placeholder)

--strict promotes every WARN to ERROR (use it for a hard quality gate). Exit
code is non-zero when any ERROR remains.

Doc type is auto-detected from the filename (prd.md / srs.md / tech-design.md /
docs/features/*.md / test-cases.md / test-plan.md); override with --type. An
unknown type is checked for the type-agnostic rules only (title, IDs,
placeholders) — spec-forge does not force its structure on arbitrary docs.

Usage:
  sf-verify-doc.py <file> [--type TYPE] [--strict] [--json]
"""

import argparse
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_common as sf

# Recommended (not mandatory) sections per doc type. Missing -> WARN, because
# the skills deliberately omit sections that do not apply to a given project
# profile. id_prefixes lists which ID grammars are expected to appear.
DOC_SCHEMAS = {
    "prd": {
        "id_prefixes": ["PRD"],
        "recommended": ["Overview", "Problem", "Goal", "User", "Requirement", "Metric"],
    },
    "srs": {
        "id_prefixes": ["FR"],
        "recommended": ["Introduction", "Overall Description", "Functional Requirement",
                        "Non-Functional", "Traceability"],
    },
    "tech-design": {
        "id_prefixes": [],
        "recommended": ["Overview", "Goal", "Solution", "Architecture",
                        "Component Overview", "Detailed Design"],
    },
    "feature": {
        "id_prefixes": [],
        "recommended": ["Overview", "Acceptance"],
    },
    "test-cases": {
        "id_prefixes": ["TC"],
        "recommended": ["Coverage", "Test Case"],
    },
    "test-plan": {
        "id_prefixes": ["TC"],
        "recommended": ["Strategy", "Traceability"],
    },
}

_TYPE_BY_NAME = [
    ("prd", re.compile(r"(^|/)prd\.md$", re.I)),
    ("srs", re.compile(r"(^|/)srs\.md$", re.I)),
    ("tech-design", re.compile(r"(^|/)tech-design\.md$", re.I)),
    ("test-cases", re.compile(r"(^|/)test-cases\.md$", re.I)),
    ("test-plan", re.compile(r"(^|/)test-plan\.md$", re.I)),
]


def detect_type(path):
    norm = path.replace(os.sep, "/")
    if "/features/" in ("/" + norm):
        return "feature"
    for label, rx in _TYPE_BY_NAME:
        if rx.search(norm):
            return label
    return "unknown"


class Report:
    def __init__(self):
        self.checks = []  # (severity, passed, message)

    def add(self, severity, passed, message):
        self.checks.append((severity, passed, message))

    def errors(self, strict):
        return [m for sev, ok, m in self.checks
                if not ok and (sev == "ERROR" or (strict and sev == "WARN"))]

    def warnings(self, strict):
        if strict:
            return []
        return [m for sev, ok, m in self.checks if not ok and sev == "WARN"]


def verify(path, doc_type=None, root=None):
    rep = Report()
    doc_type = doc_type or detect_type(path)

    exists = os.path.isfile(path)
    rep.add("ERROR", exists, f"file exists: {path}")
    if not exists:
        return rep, doc_type
    text = sf.read_text(path)
    rep.add("ERROR", bool(text.strip()), "file is non-empty")

    rep.add("ERROR", sf.first_title(text) is not None, "document has an H1 title")

    schema = DOC_SCHEMAS.get(doc_type, {})
    for section in schema.get("recommended", []):
        rep.add("WARN", sf.has_section(text, section),
                f"has recommended section: {section}")

    # ID format + uniqueness. Malformed near-misses (e.g. FR-1 without module or
    # zero-padding) are flagged; exact duplicates of a well-formed ID are errors.
    ids = sf.extract_ids(text)
    line_map = sf.id_line_map(text)
    all_ids = [i for group in ids.values() for i in group]

    # Duplicate *definitions*. A single requirement is usually defined by BOTH a
    # heading ("#### FR-AUTH-001") and an ID table row ("| **ID** | FR-AUTH-001 |")
    # — that is one definition, not two. So count heading-defs and idrow-defs
    # separately and flag an ID only when EITHER kind repeats (the block itself
    # appears twice).
    heading_counts = {}
    idrow_counts = {}
    for line in text.splitlines():
        stripped = line.strip()
        for i in all_ids:
            if stripped.startswith("#") and i in stripped:
                heading_counts[i] = heading_counts.get(i, 0) + 1
            elif re.match(rf"^\|\s*\*\*ID\*\*\s*\|\s*{re.escape(i)}\b", stripped):
                idrow_counts[i] = idrow_counts.get(i, 0) + 1
            elif stripped.startswith(i + ":"):
                heading_counts[i] = heading_counts.get(i, 0) + 1
    dupes = sorted({i for i in all_ids
                    if heading_counts.get(i, 0) > 1 or idrow_counts.get(i, 0) > 1})
    rep.add("ERROR", not dupes,
            f"no duplicate ID definitions{'; dupes: ' + ', '.join(dupes) if dupes else ''}")

    # Malformed IDs for the expected prefixes: catch e.g. FR-001 (no module) or
    # FR-AUTH-1 (short number) that the strict grammar would reject.
    malformed = []
    for prefix in schema.get("id_prefixes", []):
        loose = re.compile(rf"\b{prefix}-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?\b")
        strict_rx = sf._ID_COMPILED[prefix]
        for m in loose.finditer(text):
            tok = m.group(0)
            if not strict_rx.match(tok) and tok not in malformed:
                malformed.append(tok)
    rep.add("WARN", not malformed,
            f"expected IDs are well-formed{'; malformed: ' + ', '.join(sorted(malformed)) if malformed else ''}")

    # Leftover template placeholders (cosmetic by default).
    placeholders = sf.find_placeholders(text)
    sample = ", ".join(f"L{ln}:{tok}" for ln, tok, _ in placeholders[:8])
    rep.add("WARN", not placeholders,
            f"no leftover template placeholders{'; found ' + str(len(placeholders)) + ': ' + sample if placeholders else ''}")

    return rep, doc_type


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", help="Path to the document to verify")
    parser.add_argument("--type", choices=sorted(DOC_SCHEMAS) + ["unknown"],
                        help="Document type (default: auto-detect from filename)")
    parser.add_argument("--strict", action="store_true", help="Promote warnings to errors")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    rep, doc_type = verify(os.path.abspath(args.file), doc_type=args.type)
    errors = rep.errors(args.strict)
    warnings = rep.warnings(args.strict)

    if args.json:
        print(json.dumps({
            "file": os.path.abspath(args.file),
            "type": doc_type,
            "errors": errors,
            "warnings": warnings,
            "checks": [{"severity": s, "passed": p, "message": m} for s, p, m in rep.checks],
        }, indent=2, ensure_ascii=False))
    else:
        print(f"Document verification: {os.path.abspath(args.file)}  (type: {doc_type})")
        for severity, passed, message in rep.checks:
            tag = "PASS" if passed else ("FAIL" if severity == "ERROR" or (args.strict and severity == "WARN") else "WARN")
            print(f"  [{tag}] {message}")
        print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s)")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
