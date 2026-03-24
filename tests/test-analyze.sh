#!/usr/bin/env bash
# test-analyze.sh — Tests for the /analyze skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /analyze skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/analyze.md" \
  "analyze.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/analyze/SKILL.md" \
  "Analyze SKILL.md exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/analyze.md" "analyze" \
  "analyze.md references analyze skill"
assert_file_contains "$PROJECT_DIR/commands/analyze.md" "ARGUMENTS" \
  "analyze.md passes arguments"
assert_file_contains "$PROJECT_DIR/commands/analyze.md" "knowledge management" \
  "analyze.md sets knowledge management persona"

# Verify SKILL.md contains core workflow steps
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Document Discovery" \
  "SKILL.md defines Document Discovery step"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Theme" \
  "SKILL.md defines Theme analysis"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Conflict" \
  "SKILL.md defines Conflict detection"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Gap Analysis" \
  "SKILL.md defines Gap Analysis step"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Redundancy" \
  "SKILL.md defines Redundancy detection"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Staleness" \
  "SKILL.md defines Staleness assessment"

# Verify core principles
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Landscape-first" \
  "SKILL.md includes landscape-first principle"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Non-destructive" \
  "SKILL.md includes non-destructive principle"

# Verify document type classification
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "vision" \
  "SKILL.md classifies vision documents"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "architecture" \
  "SKILL.md classifies architecture documents"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "decision" \
  "SKILL.md classifies decision documents"

# Verify analyze vs audit distinction
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Analyze vs. Audit" \
  "SKILL.md documents Analyze vs Audit distinction"

# Verify report output
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "analysis-report.md" \
  "SKILL.md specifies analysis-report.md output"
assert_file_contains "$PROJECT_DIR/skills/analyze/SKILL.md" "Mermaid" \
  "SKILL.md includes Mermaid graph for relationships"

# Verify orchestrator routes to analyze
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "spec-forge:analyze" \
  "Orchestrator routes to spec-forge:analyze"
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "Route G" \
  "Orchestrator has Route G for analyze"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /analyze skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "analyze" \
    "claude recognizes analyze skill"
  assert_contains "$CLAUDE_OUTPUT" "document" \
    "claude mentions document analysis"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
