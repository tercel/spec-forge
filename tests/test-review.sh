#!/usr/bin/env bash
# test-review.sh — Tests for the /review skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /review skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/review.md" \
  "review.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/review/SKILL.md" \
  "Review SKILL.md exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/review.md" "quality" \
  "review.md mentions quality"
assert_file_contains "$PROJECT_DIR/commands/review.md" "consistency" \
  "review.md mentions consistency"
assert_file_contains "$PROJECT_DIR/commands/review.md" "auto-fix" \
  "review.md mentions auto-fix"
assert_file_contains "$PROJECT_DIR/commands/review.md" "SKILL.md" \
  "review.md references SKILL.md"

# Verify SKILL.md contains key sections
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Completeness" \
  "SKILL.md has Completeness check"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Internal Consistency" \
  "SKILL.md has Internal Consistency check"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Specificity" \
  "SKILL.md has Specificity check"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Traceability" \
  "SKILL.md has Traceability check"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Actionability" \
  "SKILL.md has Actionability check"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Auto-Fix" \
  "SKILL.md has Auto-Fix section"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "Maximum iterations" \
  "SKILL.md defines max iterations"
assert_file_contains "$PROJECT_DIR/skills/review/SKILL.md" "REVIEW" \
  "SKILL.md uses REVIEW comment marker for unknowns"

# Verify orchestrator includes review route
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "review cool-feature" \
  "Orchestrator has review in argument table"
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "spec-forge:review" \
  "Orchestrator routes to spec-forge:review skill"
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "Stage 4 — Review" \
  "Orchestrator has Review as Stage 4 in chain"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /review skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "review" \
    "claude recognizes review skill"
  assert_contains "$CLAUDE_OUTPUT" "quality" \
    "claude mentions quality review"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
