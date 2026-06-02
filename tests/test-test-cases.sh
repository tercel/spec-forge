#!/usr/bin/env bash
# test-test-cases.sh — Tests for the /test-cases skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /test-cases skill..."

# ── Static Tests ────────────────────────────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/test-cases.md" \
  "test-cases.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/test-cases-generation/SKILL.md" \
  "Test Cases SKILL.md exists"
assert_file_exists "$PROJECT_DIR/skills/test-cases-generation/references/template.md" \
  "Test Cases template exists"
assert_file_exists "$PROJECT_DIR/skills/test-cases-generation/references/checklist.md" \
  "Test Cases checklist exists"

# Verify real database testing policy
assert_file_contains "$PROJECT_DIR/commands/test-cases.md" "REAL database" \
  "test-cases.md enforces real database testing"
assert_file_contains "$PROJECT_DIR/commands/test-cases.md" "TC-" \
  "test-cases.md defines TC ID format"

# Verify data integrity testing
assert_file_contains "$PROJECT_DIR/commands/test-cases.md" "Data Integrity" \
  "test-cases.md mentions data integrity testing"

# Verify defensive prompts and next steps
assert_file_contains "$PROJECT_DIR/commands/test-cases.md" "Anti-Shortcut" \
  "test-cases.md contains Anti-Shortcut Rules"
assert_file_contains "$PROJECT_DIR/commands/test-cases.md" "Next Steps" \
  "test-cases.md contains Next Steps section"

# ── Headless Tests ──────────────────────────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /test-cases skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "test" \
    "claude recognizes test cases skill"
  assert_contains "$CLAUDE_OUTPUT" "case" \
    "claude mentions test cases"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
