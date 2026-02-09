#!/usr/bin/env bash
# test-tech-design.sh — Tests for the /tech-design skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /tech-design skill..."

# ── Static Tests ────────────────────────────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/tech-design.md" \
  "tech-design.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/tech-design-generation/SKILL.md" \
  "Tech Design SKILL.md exists"
assert_file_exists "$PROJECT_DIR/skills/tech-design-generation/references/template.md" \
  "Tech Design template exists"
assert_file_exists "$PROJECT_DIR/skills/tech-design-generation/references/checklist.md" \
  "Tech Design checklist exists"

# Verify C4 architecture diagram references
assert_file_contains "$PROJECT_DIR/commands/tech-design.md" "C4" \
  "tech-design.md references C4 architecture diagrams"

# Verify alternative solution comparison
assert_file_contains "$PROJECT_DIR/commands/tech-design.md" "alternative" \
  "tech-design.md requires alternative solutions"

# Verify parameter validation matrix
assert_file_contains "$PROJECT_DIR/commands/tech-design.md" "Parameter Validation" \
  "tech-design.md mentions parameter validation matrix"

# Verify defensive prompts and next steps
assert_file_contains "$PROJECT_DIR/commands/tech-design.md" "Anti-Shortcut" \
  "tech-design.md contains Anti-Shortcut Rules"
assert_file_contains "$PROJECT_DIR/commands/tech-design.md" "Next Steps" \
  "tech-design.md contains Next Steps section"

# ── Headless Tests ──────────────────────────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /tech-design skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "design" \
    "claude recognizes tech design skill"
  assert_contains "$CLAUDE_OUTPUT" "architecture" \
    "claude mentions architecture"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
