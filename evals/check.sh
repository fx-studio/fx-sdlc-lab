#!/usr/bin/env bash
# Playbook-style name for the grader: bash evals/check.sh <task.json> <worktree> <stream.jsonl>
exec python3 "$(dirname "$0")/check.py" "$@"
