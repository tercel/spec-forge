#!/usr/bin/env bash
# test-srs.sh — Tests for the /srs skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /srs skill..."

# ── Static Tests ────────────────────────────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/srs.md" \
  "srs.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/srs-generation/SKILL.md" \
  "SRS SKILL.md exists"
assert_file_exists "$PROJECT_DIR/skills/srs-generation/references/template.md" \
  "SRS template exists"
assert_file_exists "$PROJECT_DIR/skills/srs-generation/references/checklist.md" \
  "SRS checklist exists"

# Verify IEEE 830 compliance markers
assert_file_contains "$PROJECT_DIR/commands/srs.md" "IEEE 830" \
  "srs.md references IEEE 830"
assert_file_contains "$PROJECT_DIR/commands/srs.md" "FR-" \
  "srs.md defines FR ID format"
assert_file_contains "$PROJECT_DIR/commands/srs.md" "NFR-" \
  "srs.md defines NFR ID format"

# Verify upstream PRD traceability
assert_file_contains "$PROJECT_DIR/commands/srs.md" "PRD" \
  "srs.md mentions upstream PRD traceability"

# Verify defensive prompts and next steps
assert_file_contains "$PROJECT_DIR/commands/srs.md" "Anti-Shortcut" \
  "srs.md contains Anti-Shortcut Rules"
assert_file_contains "$PROJECT_DIR/commands/srs.md" "Next Steps" \
  "srs.md contains Next Steps section"

# ── Headless Tests ──────────────────────────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /srs skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "SRS" \
    "claude recognizes SRS skill"
  assert_contains "$CLAUDE_OUTPUT" "requirement" \
    "claude mentions requirements"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
