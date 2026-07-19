#!/usr/bin/env python3
"""Standard-library unittest for the spec-forge script layer.

Run: python3 skills/shared/scripts/test_scripts.py
Covers sf_common plus every CLI end-to-end (subprocess), stdlib only.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sf_common as sf


def run(script, *cli_args):
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, script), *cli_args],
        capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


class TestSfCommon(unittest.TestCase):
    def test_extract_ids_word_boundary(self):
        text = "FR-AUTH-001 and NFR-PERF-002 plus TC-LOGIN-010 and AC-3."
        ids = sf.extract_ids(text)
        self.assertEqual(ids["FR"], ["FR-AUTH-001"])
        self.assertEqual(ids["NFR"], ["NFR-PERF-002"])
        self.assertEqual(ids["TC"], ["TC-LOGIN-010"])
        self.assertEqual(ids["AC"], ["AC-3"])
        # NFR must not leak into FR extraction.
        self.assertNotIn("FR-PERF-002", ids["FR"])

    def test_headings_and_title(self):
        text = "# Title\n## Section A\ntext\n### Sub\n"
        self.assertEqual(sf.first_title(text), "Title")
        self.assertTrue(sf.has_section(text, "section a"))
        self.assertFalse(sf.has_section(text, "nonexistent"))

    def test_placeholders(self):
        text = "\n".join([
            "# [Feature Name]",
            "- [ ] a real checkbox",
            "See [the docs](http://x) here",
            "value: {placeholder}",
            "status: TBD",
            "- [x] done",
        ])
        found = sf.find_placeholders(text)
        kinds = {k for _, _, k in found}
        toks = {t for _, t, _ in found}
        self.assertIn("bracket", kinds)      # [Feature Name]
        self.assertIn("curly", kinds)        # {placeholder}
        self.assertIn("prose", kinds)        # TBD
        self.assertIn("[Feature Name]", toks)
        self.assertNotIn("[ ]", toks)        # checkbox excluded
        self.assertNotIn("[the docs]", toks)  # link excluded

    def test_topo_order(self):
        order = sf.topo_order(["a", "b", "c"], {"b": ["a"], "c": ["b"]})
        self.assertEqual(order, ["a", "b", "c"])
        with self.assertRaises(ValueError):
            sf.topo_order(["a", "b"], {"a": ["b"], "b": ["a"]})

    def test_config_merge_tool_readonly(self):
        with tempfile.TemporaryDirectory() as d:
            write(os.path.join(d, ".spec-forge.json"),
                  json.dumps({"_tool": {"name": "hacked"}, "directories": {"docs": "spec/"}}))
            config, sources, errors = sf.load_config(d, home=d)
            self.assertEqual(config["_tool"]["name"], "spec-forge")  # forced back
            self.assertEqual(config["directories"]["docs"], "spec/")
            self.assertEqual(errors, [])

    def test_validate_config_rejects_traversal(self):
        cfg = sf.copy_defaults()
        cfg["directories"]["docs"] = "../evil"
        self.assertTrue(sf.validate_config(cfg))


class TestConfigCli(unittest.TestCase):
    def test_config_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            code, out, _ = run("sf-config.py", "--root", d)
            self.assertEqual(code, 0)
            data = json.loads(out)
            self.assertEqual(data["config"]["_tool"]["name"], "spec-forge")
            self.assertTrue(data["docs_dir"].endswith("docs"))

    def test_config_bad_falls_back(self):
        with tempfile.TemporaryDirectory() as d:
            write(os.path.join(d, ".spec-forge.json"),
                  json.dumps({"directories": {"docs": "/abs"}}))
            code, out, _ = run("sf-config.py", "--root", d)
            data = json.loads(out)
            self.assertTrue(data["errors"])
            self.assertEqual(data["config"]["directories"]["docs"], "docs/")  # default


class TestScanCli(unittest.TestCase):
    def _project(self, d):
        write(os.path.join(d, "package.json"),
              json.dumps({"dependencies": {"express": "^4"}, "scripts": {"test": "jest"}}))
        write(os.path.join(d, "src", "index.js"), "console.log(1)\n")
        write(os.path.join(d, "docs", "auth", "prd.md"),
              "# Auth PRD\nRequirement PRD-AUTH-001 here.\n")
        write(os.path.join(d, "docs", "auth", "srs.md"),
              "# Auth SRS\n#### FR-AUTH-001\nThe system shall log in.\n")
        write(os.path.join(d, "ideas", "auth", "draft.md"),
              "# Auth idea\nStatus: ready\n")

    def test_scan_project_and_docs(self):
        with tempfile.TemporaryDirectory() as d:
            self._project(d)
            code, out, _ = run("sf-scan.py", "--root", d)
            self.assertEqual(code, 0)
            data = json.loads(out)
            self.assertEqual(data["primary_language"], "JavaScript")
            self.assertIn("Express", data["frameworks"])
            types = {doc["type"] for doc in data["documents"]}
            self.assertIn("prd", types)
            self.assertIn("srs", types)
            self.assertIn("idea-draft", types)
            idea = next(x for x in data["documents"] if x["type"] == "idea-draft")
            self.assertEqual(idea["status"], "ready")
            srs = next(x for x in data["documents"] if x["type"] == "srs")
            self.assertEqual(srs["declared_ids"]["FR"], ["FR-AUTH-001"])

    def test_scan_docs_only(self):
        with tempfile.TemporaryDirectory() as d:
            self._project(d)
            code, out, _ = run("sf-scan.py", "--root", d, "--docs-only")
            data = json.loads(out)
            self.assertNotIn("languages", data)
            self.assertIn("documents", data)

    def test_idea_status_prefers_state_json(self):
        with tempfile.TemporaryDirectory() as d:
            # draft.md uses a blockquote "> Status:" and says exploring; the
            # authoritative state.json says ready — state.json must win.
            write(os.path.join(d, "ideas", "pay", "draft.md"),
                  "# Pay idea\n> Status: Exploring | Draft v1 | 2026-01-01\n")
            write(os.path.join(d, "ideas", "pay", "state.json"),
                  json.dumps({"status": "ready"}))
            code, out, _ = run("sf-scan.py", "--root", d, "--docs-only")
            idea = next(x for x in json.loads(out)["documents"] if x["type"] == "idea-draft")
            self.assertEqual(idea["status"], "ready")

    def test_idea_status_blockquote_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            # No state.json → fall back to the draft's "> Status:" blockquote line.
            write(os.path.join(d, "ideas", "pay", "draft.md"),
                  "# Pay idea\n> Status: refining | Draft v2 | 2026-01-02\n")
            code, out, _ = run("sf-scan.py", "--root", d, "--docs-only")
            idea = next(x for x in json.loads(out)["documents"] if x["type"] == "idea-draft")
            self.assertEqual(idea["status"], "refining")


class TestVerifyDocCli(unittest.TestCase):
    def test_good_srs_passes(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "srs.md")
            write(p, "\n".join([
                "# Software Requirements Specification",
                "## 3. Introduction",
                "## 4. Overall Description",
                "## 5. Functional Requirements",
                "#### FR-AUTH-001",
                "The system shall authenticate.",
                "## 6. Non-Functional Requirements",
                "## 9. Requirements Traceability Matrix",
            ]))
            code, out, _ = run("sf-verify-doc.py", p, "--json")
            data = json.loads(out)
            self.assertEqual(code, 0)
            self.assertEqual(data["type"], "srs")
            self.assertEqual(data["errors"], [])

    def test_duplicate_id_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "srs.md")
            write(p, "# SRS\n#### FR-AUTH-001\nx\n#### FR-AUTH-001\ny\n")
            code, out, _ = run("sf-verify-doc.py", p, "--json")
            data = json.loads(out)
            self.assertEqual(code, 1)
            self.assertTrue(any("duplicate" in e.lower() for e in data["errors"]))

    def test_placeholder_warns_then_strict_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "prd.md")
            write(p, "# [Feature Name]\n## Overview\nvalue {placeholder}\n")
            code, out, _ = run("sf-verify-doc.py", p, "--json")
            data = json.loads(out)
            self.assertEqual(code, 0)
            self.assertTrue(data["warnings"])
            code2, out2, _ = run("sf-verify-doc.py", p, "--json", "--strict")
            self.assertEqual(code2, 1)

    def test_missing_title_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "tech-design.md")
            write(p, "no heading here\n## Overview\n")
            code, out, _ = run("sf-verify-doc.py", p, "--json")
            self.assertEqual(code, 1)


class TestTraceCli(unittest.TestCase):
    def test_ids(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "srs.md")
            write(p, "#### FR-AUTH-001\n#### NFR-PERF-001\n")
            code, out, _ = run("sf-trace.py", "ids", p)
            data = json.loads(out)
            self.assertEqual(data[p]["FR"], ["FR-AUTH-001"])
            self.assertEqual(data[p]["NFR"], ["NFR-PERF-001"])

    def test_matrix_coverage(self):
        with tempfile.TemporaryDirectory() as d:
            up = os.path.join(d, "srs.md")
            down = os.path.join(d, "test-cases.md")
            write(up, "#### FR-AUTH-001\n#### FR-AUTH-002\n")
            write(down, "TC-AUTH-001 traces to FR-AUTH-001. Also FR-BOGUS-999.\n")
            code, out, _ = run("sf-trace.py", "matrix", "--upstream", up, "--downstream", down)
            data = json.loads(out)
            self.assertEqual(data["stats"]["upstream_total"], 2)
            self.assertIn("FR-AUTH-002", data["uncovered_upstream"])
            self.assertIn("FR-BOGUS-999", data["orphan_downstream_refs"])

    def test_matrix_coverage_is_boundary_aware(self):
        with tempfile.TemporaryDirectory() as d:
            up = os.path.join(d, "srs.md")
            down = os.path.join(d, "test-cases.md")
            write(up, "#### FR-AUTH-001\n")
            # Downstream mentions FR-AUTH-0012 (trailing digits) and NFR-AUTH-001
            # (FR- inside NFR-), but never FR-AUTH-001 itself → must be uncovered.
            write(down, "Covers FR-AUTH-0012 and NFR-AUTH-001, but not the target.\n")
            code, out, _ = run("sf-trace.py", "matrix", "--upstream", up, "--downstream", down)
            data = json.loads(out)
            self.assertIn("FR-AUTH-001", data["uncovered_upstream"])
            self.assertEqual(data["stats"]["coverage_pct"], 0.0)

    def test_next_id(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "srs.md")
            write(p, "#### FR-AUTH-001\n#### FR-AUTH-003\n")
            code, out, _ = run("sf-trace.py", "next-id", "--prefix", "FR",
                               "--module", "AUTH", "--existing", p)
            data = json.loads(out)
            self.assertEqual(data["next_id"], "FR-AUTH-004")

    def test_chain(self):
        with tempfile.TemporaryDirectory() as d:
            td = os.path.join(d, "tech-design.md")
            fdir = os.path.join(d, "features")
            write(td, "\n".join([
                "# TD",
                "### 8.1 Component Overview",
                "| Component | Description |",
                "|---|---|",
                "| login | handles login |",
                "| orphan-comp | not built |",
            ]))
            write(os.path.join(fdir, "login.md"), "# login\n")
            write(os.path.join(fdir, "extra.md"), "# extra feature\n")
            code, out, _ = run("sf-trace.py", "chain", "--tech-design", td, "--features-dir", fdir)
            data = json.loads(out)
            self.assertIn("extra", data["features_not_mentioned_in_tech_design"])
            self.assertIn("orphan-comp", data["slugs_without_feature_file"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
