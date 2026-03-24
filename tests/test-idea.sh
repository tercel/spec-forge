#!/usr/bin/env bash
# test-idea.sh — Tests for the /idea skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /idea skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/idea.md" \
  "idea.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/idea/SKILL.md" \
  "Idea SKILL.md exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/idea.md" "spec-forge:idea" \
  "idea.md invokes spec-forge:idea skill"
assert_file_contains "$PROJECT_DIR/commands/idea.md" "ARGUMENTS" \
  "idea.md passes arguments to skill"

# Verify SKILL.md contains core workflow phases
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Explore" \
  "SKILL.md defines Explore phase"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Research" \
  "SKILL.md defines Research phase"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Validate" \
  "SKILL.md defines Validate phase"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Refine" \
  "SKILL.md defines Refine phase"

# Verify core principles
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Anti-pseudo-requirement" \
  "SKILL.md includes anti-pseudo-requirement principle"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "What if we don't build this" \
  "SKILL.md includes 'What if we don't build this' check"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "Demand Validation" \
  "SKILL.md includes Demand Validation section"

# Verify storage structure
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "ideas/" \
  "SKILL.md uses ideas/ directory for storage"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "state.json" \
  "SKILL.md defines state.json for status tracking"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "draft.md" \
  "SKILL.md defines draft.md for evolving summary"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "sessions/" \
  "SKILL.md uses sessions/ subdirectory"

# Verify session naming convention
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "kebab-case" \
  "SKILL.md requires kebab-case for idea names"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "overview.md" \
  "SKILL.md tracks session order in overview.md"

# Verify status lifecycle
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "exploring" \
  "SKILL.md defines exploring status"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "researching" \
  "SKILL.md defines researching status"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "refining" \
  "SKILL.md defines refining status"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "ready" \
  "SKILL.md defines ready status"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "graduated" \
  "SKILL.md defines graduated status"
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "parked" \
  "SKILL.md defines parked status"

# Verify graduation gate
assert_file_contains "$PROJECT_DIR/skills/idea/SKILL.md" "validated" \
  "SKILL.md requires validation before graduation"

# Verify orchestrator routes to idea
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "spec-forge:idea" \
  "Orchestrator routes to spec-forge:idea skill"
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "Route B" \
  "Orchestrator has Route B for idea"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /idea skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "idea" \
    "claude recognizes idea skill"
  assert_contains "$CLAUDE_OUTPUT" "valid" \
    "claude mentions validation"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
