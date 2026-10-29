#!/usr/bin/env bash
# Runs the whole test suite N times (default 10) and lists every test whose result changed between runs.
# Usage: bash scripts/flaky.sh [N]
set -u
cd "$(dirname "$0")/.."
n="${1:-10}"; out="$(mktemp -d)"
for i in $(seq 1 "$n"); do
  node --test --test-reporter=tap 2>/dev/null | grep -E '^(not )?ok [0-9]+ - ' | sed -E 's/^(not ok|ok) [0-9]+ - (.*)$/\1\t\2/' > "$out/$i.tsv"
  printf 'run %2d: %s pass, %s fail\n' "$i" "$(grep -c '^ok' "$out/$i.tsv")" "$(grep -c '^not ok' "$out/$i.tsv")"
done
cut -f2 "$out"/*.tsv | sort -u | while IFS= read -r t; do
  r="$(grep -hF "	$t" "$out"/*.tsv | cut -f1 | sort -u | tr '\n' ' ')"
  case "$r" in *"not ok"*ok*|ok*"not ok"*) echo "FLAKY: $t";; esac
done | tee "$out/flaky.txt"
[ -s "$out/flaky.txt" ] && echo "flaky tests: $(wc -l < "$out/flaky.txt")" || echo "flaky tests: 0 in $n runs"
rm -rf "$out"
