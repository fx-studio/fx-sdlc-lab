#!/usr/bin/env bash
# Spec job (Design stage, step 3 of the playbook's "by hand → slash command → triggered job").
# Called by .git/hooks/post-commit. For every intent/*.md that the last commit set to `Status: accepted` and that has no spec yet:
# run /write-spec headless, then THIS SCRIPT (not the agent) commits the draft spec on main. A person still has to accept the spec.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
LOG="${SPEC_JOB_LOG:-.spec-job.log}"

for f in $(git diff-tree --no-commit-id --name-only -r HEAD -- 'intent/*.md'); do
  [ -f "$f" ] || continue
  grep -qiE '^.*Status:[[:space:]]*accepted' "$f" || continue
  spec="spec/$(basename "$f")"
  [ -e "$spec" ] && continue
  echo "[$(date '+%F %T')] spec job: $f → $spec" >> "$LOG"
  t0=$(date +%s)
  claude -p "/write-spec $f" --output-format json \
    --allowedTools "Read,Glob,Grep,Skill,Write(spec/**),Edit(spec/**)" < /dev/null >> "$LOG" 2>&1 || true
  echo "" >> "$LOG"
  if [ -f "$spec" ]; then
    git add "$spec"
    # The hook inherits the triggering commit's identity and date (GIT_AUTHOR_*, GIT_CONFIG_PARAMETERS): drop them.
    env -u GIT_AUTHOR_NAME -u GIT_AUTHOR_EMAIL -u GIT_AUTHOR_DATE -u GIT_COMMITTER_NAME -u GIT_COMMITTER_EMAIL \
      -u GIT_COMMITTER_DATE -u GIT_CONFIG_PARAMETERS GIT_AUTHOR_NAME=spec-job GIT_AUTHOR_EMAIL=spec-job@localhost \
      GIT_COMMITTER_NAME=spec-job GIT_COMMITTER_EMAIL=spec-job@localhost git commit -q -m "spec (draft): $(basename "$spec" .md), sinh tự động khi intent được accepted" -- "$spec"
    echo "[$(date '+%F %T')] committed $spec in $(( $(date +%s) - t0 )) s (Status: draft, waiting for a person)" >> "$LOG"
  else
    echo "[$(date '+%F %T')] no spec written for $f" >> "$LOG"
  fi
done
