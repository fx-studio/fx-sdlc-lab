#!/usr/bin/env bash
# PreToolUse hook (Bash): the playbook's production gate, ported as written (Stage 5, "Hooks as approval gates").
# Kept unchanged on purpose: demo/sdlc-5 run R8 measures what this exact shape catches and what it lets through.
# The repo's own gate is release-gate.py (approval tied to one release, written by a person on main).
cmd=$(jq -r '.tool_input.command' < /dev/stdin)
if [[ "$cmd" == *"deploy"* && "$cmd" == *"production"* ]]; then
  if [ -z "$RELEASE_APPROVAL" ]; then
    echo "Production deploys need a release authorization." >&2
    exit 2 # exit 2 blocks the action; the message goes to Claude
  fi
fi
exit 0
