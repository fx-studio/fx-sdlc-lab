#!/usr/bin/env bash
# One command for "is the work done": every test, then a syntax check of every script. Exit code is non-zero on any failure.
# Run as `bash scripts/check.sh` (do not rely on the executable bit: uploads can drop it).
set -u
cd "$(dirname "$0")/.."
fail=0
echo "== test: node --test"
node --test 2>&1 | grep -E '^(not ok|ℹ (tests|pass|fail))' || true
node --test >/dev/null 2>&1 || fail=1
echo "== lint: node --check app/*.js tests/*.js"
for f in app/*.js tests/*.js; do node --check "$f" || { echo "lint failed: $f"; fail=1; }; done
[ "$fail" = 0 ] && echo "== check: OK" || echo "== check: FAILED"
exit "$fail"
