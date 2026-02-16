#!/usr/bin/env bash
# test-decompose.sh — Tests for the /decompose skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /decompose skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/decompose.md" \
  "decompose.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/decompose/SKILL.md" \
  "Decompose SKILL.md exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/decompose.md" "decompose" \
  "decompose.md references decompose skill"
assert_file_contains "$PROJECT_DIR/commands/decompose.md" "sub-features" \
  "decompose.md mentions sub-features"

# Verify SKILL.md contains core workflow steps
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Scope Interview" \
  "SKILL.md defines Scope Interview step"
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Split Decision" \
  "SKILL.md defines Split Decision step"
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "FEATURE_MANIFEST" \
  "SKILL.md defines FEATURE_MANIFEST format"

# Verify SKILL.md contains core principles
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Lightweight" \
  "SKILL.md states lightweight principle"
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Boundary-focused" \
  "SKILL.md states boundary-focused principle"

# Verify manifest structure requirements
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "kebab-case" \
  "SKILL.md requires kebab-case naming for sub-features"
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Execution Order" \
  "SKILL.md includes Execution Order section in manifest"
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "Cross-Cutting" \
  "SKILL.md includes Cross-Cutting Concerns in manifest"

# Verify the new directory convention is documented
assert_file_contains "$PROJECT_DIR/skills/decompose/SKILL.md" "docs/" \
  "SKILL.md references docs/ directory for output"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /decompose skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "decompose" \
    "claude recognizes decompose skill"
  assert_contains "$CLAUDE_OUTPUT" "feature" \
    "claude mentions feature splitting"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
