#!/usr/bin/env bash
# run-tests.sh — Test runner for spec-forge
# Usage:
#   bash tests/run-tests.sh                  # Run all tests
#   bash tests/run-tests.sh --verbose        # Verbose output
#   bash tests/run-tests.sh --test prd       # Run only test-prd.sh
#   bash tests/run-tests.sh --timeout 60     # Set timeout per claude call (seconds)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Defaults ────────────────────────────────────────────────────────
VERBOSE=false
TARGET_TEST=""
export TEST_TIMEOUT=30

# ── Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

# ── Parse Arguments ─────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --verbose|-v)
      VERBOSE=true
      shift
      ;;
    --test|-t)
      TARGET_TEST="$2"
      shift 2
      ;;
    --timeout)
      TEST_TIMEOUT="$2"
      shift 2
      ;;
    --help|-h)
      echo "Usage: bash tests/run-tests.sh [OPTIONS]"
      echo ""
      echo "Options:"
      echo "  --verbose, -v          Verbose output"
      echo "  --test, -t <name>      Run only the specified test (e.g., 'prd' for test-prd.sh)"
      echo "  --timeout <seconds>    Timeout per claude call (default: 30)"
      echo "  --help, -h             Show this help"
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}" >&2
      exit 1
      ;;
  esac
done

export VERBOSE

# ── Banner ──────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║       spec-forge Test Runner v1.1.0          ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════╝${NC}"
echo ""

# ── Discover & Run Tests ────────────────────────────────────────────
TOTAL_PASSED=0
TOTAL_FAILED=0
TOTAL_SKIPPED=0
SUITE_COUNT=0
FAILED_SUITES=()

# Find test files
if [ -n "$TARGET_TEST" ]; then
  TEST_FILES=("$SCRIPT_DIR/test-${TARGET_TEST}.sh")
  if [ ! -f "${TEST_FILES[0]}" ]; then
    echo -e "${RED}Test file not found: test-${TARGET_TEST}.sh${NC}" >&2
    exit 1
  fi
else
  TEST_FILES=()
  while IFS= read -r f; do
    TEST_FILES+=("$f")
  done < <(find "$SCRIPT_DIR" -name 'test-*.sh' -not -name 'test-helpers.sh' | sort)
fi

if [ ${#TEST_FILES[@]} -eq 0 ]; then
  echo -e "${YELLOW}No test files found.${NC}"
  exit 0
fi

echo -e "${BLUE}Found ${#TEST_FILES[@]} test suite(s)${NC}"
echo -e "${BLUE}Timeout: ${TEST_TIMEOUT}s per claude call${NC}"
echo ""

for test_file in "${TEST_FILES[@]}"; do
  test_name="$(basename "$test_file" .sh)"
  ((SUITE_COUNT++))

  echo -e "${BOLD}── $test_name ──${NC}"

  # Run test in subshell to isolate failures
  set +e
  output=$(bash "$test_file" 2>&1)
  exit_code=$?
  set -e

  echo "$output"

  # Extract counts from output (look for summary lines)
  passed=$(echo "$output" | grep -c "PASS" || true)
  failed=$(echo "$output" | grep -c "FAIL" || true)
  skipped=$(echo "$output" | grep -c "SKIP" || true)

  TOTAL_PASSED=$((TOTAL_PASSED + passed))
  TOTAL_FAILED=$((TOTAL_FAILED + failed))
  TOTAL_SKIPPED=$((TOTAL_SKIPPED + skipped))

  if [ $exit_code -ne 0 ]; then
    FAILED_SUITES+=("$test_name")
  fi

  echo ""
done

# ── Final Summary ──────────────────────────────────────────────────
echo -e "${BOLD}══════════════════════════════════════════════${NC}"
echo -e "${BOLD}  Final Summary${NC}"
echo -e "${BOLD}══════════════════════════════════════════════${NC}"
echo -e "  Suites:  $SUITE_COUNT"
echo -e "  ${GREEN}Passed:  $TOTAL_PASSED${NC}"
echo -e "  ${RED}Failed:  $TOTAL_FAILED${NC}"
echo -e "  ${YELLOW}Skipped: $TOTAL_SKIPPED${NC}"

if [ ${#FAILED_SUITES[@]} -gt 0 ]; then
  echo ""
  echo -e "  ${RED}Failed suites:${NC}"
  for s in "${FAILED_SUITES[@]}"; do
    echo -e "    ${RED}- $s${NC}"
  done
  echo ""
  exit 1
else
  echo ""
  echo -e "  ${GREEN}All test suites passed!${NC}"
  echo ""
  exit 0
fi
