#!/usr/bin/env bash
# test-prd.sh — Tests for the /prd skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /prd skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/prd.md" \
  "prd.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/prd-generation/SKILL.md" \
  "PRD SKILL.md exists"
assert_file_exists "$PROJECT_DIR/skills/prd-generation/references/template.md" \
  "PRD template exists"
assert_file_exists "$PROJECT_DIR/skills/prd-generation/references/checklist.md" \
  "PRD checklist exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/prd.md" "market" \
  "prd.md mentions market analysis"
assert_file_contains "$PROJECT_DIR/commands/prd.md" "feasibility" \
  "prd.md mentions feasibility assessment"
assert_file_contains "$PROJECT_DIR/commands/prd.md" "anti-pseudo-requirement" \
  "prd.md mentions anti-pseudo-requirement principle"
assert_file_contains "$PROJECT_DIR/commands/prd.md" "Anti-Shortcut" \
  "prd.md contains Anti-Shortcut Rules"
assert_file_contains "$PROJECT_DIR/commands/prd.md" "Next Steps" \
  "prd.md contains Next Steps section"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /prd skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "PRD" \
    "claude recognizes PRD skill"
  assert_contains "$CLAUDE_OUTPUT" "product" \
    "claude mentions product requirements"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
