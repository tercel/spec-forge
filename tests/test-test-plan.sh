#!/usr/bin/env bash
# test-test-plan.sh — Tests for the /test-plan skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /test-plan skill..."

# ── Static Tests ────────────────────────────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/test-plan.md" \
  "test-plan.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/test-plan-generation/SKILL.md" \
  "Test Plan SKILL.md exists"
assert_file_exists "$PROJECT_DIR/skills/test-plan-generation/references/template.md" \
  "Test Plan template exists"
assert_file_exists "$PROJECT_DIR/skills/test-plan-generation/references/checklist.md" \
  "Test Plan checklist exists"

# Verify real database testing policy
assert_file_contains "$PROJECT_DIR/commands/test-plan.md" "REAL database" \
  "test-plan.md enforces real database testing"
assert_file_contains "$PROJECT_DIR/commands/test-plan.md" "TC-" \
  "test-plan.md defines TC ID format"

# Verify data integrity testing
assert_file_contains "$PROJECT_DIR/commands/test-plan.md" "Data Integrity" \
  "test-plan.md mentions data integrity testing"

# Verify defensive prompts and next steps
assert_file_contains "$PROJECT_DIR/commands/test-plan.md" "Anti-Shortcut" \
  "test-plan.md contains Anti-Shortcut Rules"
assert_file_contains "$PROJECT_DIR/commands/test-plan.md" "Next Steps" \
  "test-plan.md contains Next Steps section"

# ── Headless Tests ──────────────────────────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /test-plan skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "test" \
    "claude recognizes test plan skill"
  assert_contains "$CLAUDE_OUTPUT" "database" \
    "claude mentions database testing"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
