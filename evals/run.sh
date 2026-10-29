#!/usr/bin/env bash
# Run the whole eval suite (see evals/run.py for options). Uses your Claude Code login or ANTHROPIC_API_KEY; every run costs money.
exec python3 "$(dirname "$0")/run.py" "$@"
