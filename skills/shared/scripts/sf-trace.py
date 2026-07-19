#!/usr/bin/env python3
"""Traceability + coverage bookkeeping for the spec chain.

Builds the deterministic half of the traceability work the skills otherwise do
by hand: extract requirement/test-case IDs, compute the requirement->downstream
coverage matrix, allocate the next free ID, and cross-check the tech-design <->
feature-spec <-> overview set membership. The JUDGEMENT half (is an uncovered
requirement acceptable, is a mismatch Critical or Minor, does an API signature
truly match) stays with the model.

Subcommands:
  ids      <file...>                          IDs per file, by prefix
  matrix   --upstream U --downstream D        requirement coverage U -> D
  next-id  --prefix P --module M [--existing F...]   next free zero-padded ID
  chain    --tech-design T --features-dir Y [--overview O]   set-membership check

Add --json for machine-readable output (ids/matrix/next-id always emit JSON).

Usage:
  sf-trace.py <subcommand> [...]
"""

import argparse
import glob
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_common as sf


def cmd_ids(args):
    out = {}
    for path in args.files:
        text = sf.read_text(path)
        ids = {k: v for k, v in sf.extract_ids(text).items() if v}
        out[path] = ids
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _declared_ids(text, prefixes=("PRD", "FR", "NFR")):
    ids = sf.extract_ids(text)
    result = []
    for p in prefixes:
        result += ids.get(p, [])
    return sorted(set(result))


def cmd_matrix(args):
    up_text = sf.read_text(args.upstream)
    down_text = sf.read_text(args.downstream)

    upstream_ids = _declared_ids(up_text)
    down_ids = sf.extract_ids(down_text)
    down_mentioned = set()
    for group in down_ids.values():
        down_mentioned.update(group)

    matrix = []
    uncovered = []
    for uid in upstream_ids:
        # Boundary-aware match: a bare substring test would let FR-AUTH-001 be
        # "covered" by FR-AUTH-0012 (trailing digits) or by NFR-AUTH-001 (the
        # FR- inside NFR-), understating real coverage gaps. Reject a neighbour
        # word char or hyphen on either side.
        covered = re.search(rf"(?<![\w-]){re.escape(uid)}(?![\w-])", down_text) is not None
        matrix.append({"upstream_id": uid, "covered": covered})
        if not covered:
            uncovered.append(uid)

    # Downstream references to upstream-shaped IDs that are not declared upstream.
    upstream_set = set(upstream_ids)
    orphan = sorted(i for i in down_mentioned
                    if i.split("-")[0] in ("PRD", "FR", "NFR") and i not in upstream_set)

    total = len(upstream_ids)
    result = {
        "upstream": args.upstream,
        "downstream": args.downstream,
        "matrix": matrix,
        "uncovered_upstream": uncovered,
        "orphan_downstream_refs": orphan,
        "stats": {
            "upstream_total": total,
            "covered": total - len(uncovered),
            "uncovered": len(uncovered),
            "coverage_pct": round(100 * (total - len(uncovered)) / total, 1) if total else None,
            "downstream_test_case_ids": len(down_ids.get("TC", [])),
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def cmd_next_id(args):
    prefix = args.prefix.upper()
    module = args.module.upper()
    pat = re.compile(rf"\b{re.escape(prefix)}-{re.escape(module)}-(\d+)\b")
    max_n = 0
    width = 3
    for path in args.existing or []:
        for m in pat.finditer(sf.read_text(path)):
            n = int(m.group(1))
            width = max(width, len(m.group(1)))
            max_n = max(max_n, n)
    nxt = max_n + 1
    result = {
        "prefix": prefix,
        "module": module,
        "next_id": f"{prefix}-{module}-{str(nxt).zfill(width)}",
        "max_existing": max_n,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


def _slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s


def _section_text(text, keyword):
    """Return the body of the first heading containing keyword, up to the next
    heading of the same or higher level."""
    lines = text.splitlines()
    start = None
    start_level = 0
    for i, line in enumerate(lines):
        m = sf._HEADING.match(line)
        if m and keyword.lower() in m.group(2).lower():
            start = i
            start_level = len(m.group(1))
            break
    if start is None:
        return ""
    body = []
    for line in lines[start + 1:]:
        m = sf._HEADING.match(line)
        if m and len(m.group(1)) <= start_level:
            break
        body.append(line)
    return "\n".join(body)


def cmd_chain(args):
    td_text = sf.read_text(args.tech_design)
    feature_files = sorted(
        os.path.splitext(os.path.basename(p))[0]
        for p in glob.glob(os.path.join(args.features_dir, "*.md"))
        if os.path.basename(p).lower() != "overview.md"
    )

    # Reliable signal: feature spec whose filename is never mentioned in the
    # tech-design at all (likely orphan).
    features_not_mentioned = [f for f in feature_files if f not in td_text]

    # Advisory signal: first-column slugs of the Component Overview table that
    # have no matching feature file. Table parse is best-effort — the model
    # confirms severity.
    section = _section_text(td_text, "Component Overview")
    td_slugs = []
    for line in section.splitlines():
        if line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if not cells or not cells[0]:
                continue
            first = cells[0].strip("*` ")
            if first.lower() in ("component", "name", "slug", "") or set(first) <= set("-: "):
                continue
            td_slugs.append(_slugify(first))
    td_slugs = sorted(set(s for s in td_slugs if s))
    slugs_without_feature = [s for s in td_slugs if s not in feature_files]

    result = {
        "tech_design": args.tech_design,
        "features_dir": args.features_dir,
        "feature_specs": feature_files,
        "features_not_mentioned_in_tech_design": features_not_mentioned,
        "component_overview_slugs": td_slugs,
        "slugs_without_feature_file": slugs_without_feature,
    }

    if args.overview:
        ov_text = sf.read_text(args.overview)
        result["overview_missing_features"] = [f for f in feature_files if f not in ov_text]

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0  # chain findings are advisory (severity is the model's call): never hard-fail


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p_ids = sub.add_parser("ids", help="Extract IDs per file")
    p_ids.add_argument("files", nargs="+")
    p_ids.set_defaults(func=cmd_ids)

    p_matrix = sub.add_parser("matrix", help="Requirement coverage upstream -> downstream")
    p_matrix.add_argument("--upstream", required=True)
    p_matrix.add_argument("--downstream", required=True)
    p_matrix.set_defaults(func=cmd_matrix)

    p_next = sub.add_parser("next-id", help="Next free zero-padded ID for a module")
    p_next.add_argument("--prefix", required=True)
    p_next.add_argument("--module", required=True)
    p_next.add_argument("--existing", nargs="*", help="Docs to scan for existing IDs")
    p_next.set_defaults(func=cmd_next_id)

    p_chain = sub.add_parser("chain", help="tech-design <-> feature-spec <-> overview membership")
    p_chain.add_argument("--tech-design", required=True, dest="tech_design")
    p_chain.add_argument("--features-dir", required=True, dest="features_dir")
    p_chain.add_argument("--overview")
    p_chain.set_defaults(func=cmd_chain)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
