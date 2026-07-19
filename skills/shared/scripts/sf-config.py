#!/usr/bin/env python3
"""spec-forge configuration resolver (read-only).

Implements config Step 0: project-root detection, the three-layer merge
(system defaults -> ~/.spec-forge.json -> <root>/.spec-forge.json), validation,
and directory resolution. Prints one JSON object:

  project_root, config, base_dir, docs_dir, ideas_dir, features_dir,
  sources, errors

On a validation error it reports the error and falls back to system defaults.
Never writes files.

Usage:
  sf-config.py [--root PATH]
Output: JSON on stdout.
"""

import argparse
import json
import os
import sys

sys.dont_write_bytecode = True  # never write .pyc into a possibly read-only install dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sf_common as sf


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", help="Project root (default: auto-detect)")
    args = parser.parse_args()

    root = os.path.abspath(args.root) if args.root else sf.find_project_root()
    config, sources, load_errors = sf.load_config(root)

    validation_errors = sf.validate_config(config)
    if validation_errors:
        # Fall back to system defaults so downstream never runs on a bad config.
        config = sf.copy_defaults()
        sources = ["system defaults (fell back after validation error)"]

    dirs = sf.resolve_dirs(root, config)

    result = {
        "project_root": root,
        "config": config,
        "base_dir": dirs["base_dir"],
        "docs_dir": dirs["docs_dir"],
        "ideas_dir": dirs["ideas_dir"],
        "features_dir": dirs["features_dir"],
        "sources": sources,
        "errors": load_errors + validation_errors,
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
