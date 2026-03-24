#!/usr/bin/env bash
# test-audit.sh — Tests for the /audit skill
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

echo "Testing /audit skill..."

# ── Static Tests (no claude CLI needed) ─────────────────────────────

echo ""
echo "Static validation:"

# Verify command file exists
assert_file_exists "$PROJECT_DIR/commands/audit.md" \
  "audit.md command file exists"

# Verify skill files exist
assert_file_exists "$PROJECT_DIR/skills/audit/SKILL.md" \
  "Audit SKILL.md exists"

# Verify command file contains key elements
assert_file_contains "$PROJECT_DIR/commands/audit.md" "audit" \
  "audit.md references audit skill"
assert_file_contains "$PROJECT_DIR/commands/audit.md" "ARGUMENTS" \
  "audit.md passes arguments"
assert_file_contains "$PROJECT_DIR/commands/audit.md" "documentation quality" \
  "audit.md sets documentation quality persona"

# Verify SKILL.md contains core workflow steps
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Audit Scope" \
  "SKILL.md defines Audit Scope step"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Document Inventory" \
  "SKILL.md defines Document Inventory step"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Code Alignment" \
  "SKILL.md defines Code Alignment check"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Internal Consistency" \
  "SKILL.md defines Internal Consistency check"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Quality Assessment" \
  "SKILL.md defines Quality Assessment step"

# Verify severity levels
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Critical" \
  "SKILL.md defines Critical severity"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Major" \
  "SKILL.md defines Major severity"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Minor" \
  "SKILL.md defines Minor severity"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Info" \
  "SKILL.md defines Info severity"

# Verify core principles
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Evidence-based" \
  "SKILL.md includes evidence-based principle"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Code-grounded" \
  "SKILL.md includes code-grounded principle"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Read-only by default" \
  "SKILL.md includes read-only by default principle"

# Verify code alignment sub-checks
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "API Surface" \
  "SKILL.md checks API Surface alignment"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Feature Coverage" \
  "SKILL.md checks Feature Coverage"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Architecture Alignment" \
  "SKILL.md checks Architecture Alignment"

# Verify report output
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "audit-report.md" \
  "SKILL.md specifies audit-report.md output"
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Document Health Matrix" \
  "SKILL.md includes Document Health Matrix in report"

# Verify optional fix mode
assert_file_contains "$PROJECT_DIR/skills/audit/SKILL.md" "Apply Fixes" \
  "SKILL.md has Apply Fixes step"

# Verify orchestrator routes to audit
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "spec-forge:audit" \
  "Orchestrator routes to spec-forge:audit"
assert_file_contains "$PROJECT_DIR/commands/spec-forge.md" "Route F" \
  "Orchestrator has Route F for audit"

# ── Headless Tests (require claude CLI) ─────────────────────────────

echo ""
echo "Headless tests:"

if check_claude_available; then
  run_claude "Load the /audit skill and describe what it does. Do not execute it, just summarize its purpose and key sections." || true

  assert_contains "$CLAUDE_OUTPUT" "audit" \
    "claude recognizes audit skill"
  assert_contains "$CLAUDE_OUTPUT" "documentation" \
    "claude mentions documentation auditing"
else
  skip_test "claude CLI not available — skipping headless tests"
fi

# ── Summary ─────────────────────────────────────────────────────────
print_summary
