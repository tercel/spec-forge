#!/usr/bin/env bash
# test-helpers.sh — Common test utilities for spec-forge tests
# Inspired by superpowers/tests/claude-code/test-helpers.sh

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ── Counters ────────────────────────────────────────────────────────
TESTS_PASSED=0
TESTS_FAILED=0
TESTS_SKIPPED=0

# ── Paths ───────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Core Functions ──────────────────────────────────────────────────

# Run claude in headless mode with a prompt
# Usage: run_claude "prompt text" [extra_args...]
# Output is stored in $CLAUDE_OUTPUT
run_claude() {
  local prompt="$1"
  shift
  local max_timeout="${TEST_TIMEOUT:-30}"

  # Use gtimeout (coreutils) on macOS, timeout on Linux
  local timeout_cmd=""
  if command -v gtimeout &>/dev/null; then
    timeout_cmd="gtimeout"
  elif command -v timeout &>/dev/null; then
    timeout_cmd="timeout"
  fi

  if [ -n "$timeout_cmd" ]; then
    CLAUDE_OUTPUT=$($timeout_cmd "$max_timeout" claude -p "$prompt" --plugin-dir "$PROJECT_DIR/.." "$@" 2>&1) || {
      local exit_code=$?
      if [ $exit_code -eq 124 ]; then
        echo -e "${YELLOW}TIMEOUT: claude command timed out after ${max_timeout}s${NC}" >&2
      fi
      return $exit_code
    }
  else
    # Fallback: run without timeout
    CLAUDE_OUTPUT=$(claude -p "$prompt" --plugin-dir "$PROJECT_DIR/.." "$@" 2>&1) || {
      return $?
    }
  fi
}

# Assert that a string contains a substring
# Usage: assert_contains "$haystack" "needle" "description"
assert_contains() {
  local haystack="$1"
  local needle="$2"
  local description="${3:-assert_contains}"

  if echo "$haystack" | grep -qi "$needle"; then
    echo -e "  ${GREEN}PASS${NC}: $description"
    ((TESTS_PASSED++))
    return 0
  else
    echo -e "  ${RED}FAIL${NC}: $description"
    echo -e "    Expected to contain: ${YELLOW}$needle${NC}"
    echo -e "    Actual output (first 200 chars): ${YELLOW}${haystack:0:200}${NC}"
    ((TESTS_FAILED++))
    return 1
  fi
}

# Assert that a string does NOT contain a substring
# Usage: assert_not_contains "$haystack" "needle" "description"
assert_not_contains() {
  local haystack="$1"
  local needle="$2"
  local description="${3:-assert_not_contains}"

  if echo "$haystack" | grep -qi "$needle"; then
    echo -e "  ${RED}FAIL${NC}: $description"
    echo -e "    Expected NOT to contain: ${YELLOW}$needle${NC}"
    ((TESTS_FAILED++))
    return 1
  else
    echo -e "  ${GREEN}PASS${NC}: $description"
    ((TESTS_PASSED++))
    return 0
  fi
}

# Assert that a file exists
# Usage: assert_file_exists "path/to/file" "description"
assert_file_exists() {
  local file_path="$1"
  local description="${2:-File exists: $file_path}"

  if [ -f "$file_path" ]; then
    echo -e "  ${GREEN}PASS${NC}: $description"
    ((TESTS_PASSED++))
    return 0
  else
    echo -e "  ${RED}FAIL${NC}: $description"
    echo -e "    File not found: ${YELLOW}$file_path${NC}"
    ((TESTS_FAILED++))
    return 1
  fi
}

# Assert that a file contains a specific string
# Usage: assert_file_contains "path/to/file" "needle" "description"
assert_file_contains() {
  local file_path="$1"
  local needle="$2"
  local description="${3:-File contains: $needle}"

  if [ ! -f "$file_path" ]; then
    echo -e "  ${RED}FAIL${NC}: $description"
    echo -e "    File not found: ${YELLOW}$file_path${NC}"
    ((TESTS_FAILED++))
    return 1
  fi

  if grep -qi "$needle" "$file_path"; then
    echo -e "  ${GREEN}PASS${NC}: $description"
    ((TESTS_PASSED++))
    return 0
  else
    echo -e "  ${RED}FAIL${NC}: $description"
    echo -e "    File ${YELLOW}$file_path${NC} does not contain: ${YELLOW}$needle${NC}"
    ((TESTS_FAILED++))
    return 1
  fi
}

# Skip a test with a reason
# Usage: skip_test "reason"
skip_test() {
  local reason="${1:-no reason given}"
  echo -e "  ${YELLOW}SKIP${NC}: $reason"
  ((TESTS_SKIPPED++))
}

# Print test suite summary
print_summary() {
  local total=$((TESTS_PASSED + TESTS_FAILED + TESTS_SKIPPED))
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo -e "  Total:   $total"
  echo -e "  ${GREEN}Passed:  $TESTS_PASSED${NC}"
  echo -e "  ${RED}Failed:  $TESTS_FAILED${NC}"
  echo -e "  ${YELLOW}Skipped: $TESTS_SKIPPED${NC}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

  if [ "$TESTS_FAILED" -gt 0 ]; then
    return 1
  fi
  return 0
}

# Check if claude CLI is available
check_claude_available() {
  if ! command -v claude &>/dev/null; then
    echo -e "${YELLOW}WARNING: 'claude' CLI not found. Skipping headless tests.${NC}" >&2
    return 1
  fi
  return 0
}
