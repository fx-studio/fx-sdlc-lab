#!/usr/bin/env bash
# Install the git post-commit hook that runs the spec job. Local only; remove .git/hooks/post-commit to turn it off.
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"
cat > .git/hooks/post-commit <<'H'
#!/usr/bin/env bash
# Skip when the commit was made by the spec job itself.
[ "$(git log -1 --format=%an)" = "spec-job" ] && exit 0
exec "$(git rev-parse --show-toplevel)/scripts/on-intent-accepted.sh"
H
chmod +x .git/hooks/post-commit scripts/on-intent-accepted.sh
echo "post-commit hook installed"
