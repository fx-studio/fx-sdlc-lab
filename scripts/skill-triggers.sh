#!/usr/bin/env bash
# Skill trigger test (Build stage, "test that the skill triggers on different phrasings").
# Runs every numbered line of .claude/skills/<skill>/triggers.md as a fresh headless session in plan mode (read-only),
# and reports whether the session loaded the skill. Usage: scripts/skill-triggers.sh <skill> [model] [dir to keep each stream in]
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
skill="$1"; model="${2:-}"; keep="${3:-}"; hit=0; n=0; usd=0
while IFS= read -r line; do
  q="${line#*. }"; n=$((n+1))
  out=$(claude -p "$q" --permission-mode plan --max-turns 6 --output-format stream-json --verbose ${model:+--model "$model"} < /dev/null 2>/dev/null || true)
  [ -n "$keep" ] && mkdir -p "$keep" && printf '%s\n' "$out" > "$keep/$n.jsonl"
  # LOADED = the Skill tool loaded it. READ = the session only opened its SKILL.md as a file (the policy was seen, the skill did not trigger).
  got=$(printf '%s' "$out" | python3 -c "
import json, sys
s = sys.argv[1]; got = 'MISSED'
for l in sys.stdin:
    if not l.startswith('{'): continue
    e = json.loads(l)
    if e.get('type') != 'assistant': continue
    for c in e['message']['content']:
        if c.get('type') != 'tool_use': continue
        i = c.get('input', {})
        if c['name'] == 'Skill' and i.get('skill') == s: got = 'LOADED'
        elif got == 'MISSED' and f'skills/{s}/SKILL.md' in (i.get('file_path', '') + i.get('command', '')): got = 'READ'
print(got)" "$skill")
  [ "$got" = LOADED ] && hit=$((hit+1))
  printf '%-8s %s. %s\n' "$got" "$n" "$q"
  usd=$(printf '%s' "$out" | python3 -c "import json,sys; print(round(float(sys.argv[1]) + sum(e.get('total_cost_usd') or 0 for l in sys.stdin if l.startswith('{') for e in [json.loads(l)] if e.get('type') == 'result'), 4))" "$usd")
done < <(grep -E '^[0-9]+\. ' ".claude/skills/$skill/triggers.md")
echo "$skill: $hit/$n loaded by the Skill tool · $usd USD"
