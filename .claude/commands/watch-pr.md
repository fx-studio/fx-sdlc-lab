---
description: Watch your own local pull request until only a person's approval is left (playbook Stage 5, review loop)
argument-hint: <pr number>
---

You opened local pull request **#$ARGUMENTS**. Babysit it until the only thing left is a person's approval. Work in its worktree
(`.worktrees/pr-$ARGUMENTS`), on its branch.

Loop, at most **3 rounds**:

1. Read the newest `review/$ARGUMENTS/*/findings.json` (newest folder by time) and `bash scripts/check.sh` in the worktree.
2. If there is no **Important** finding left unaddressed and the check is OK: stop the loop.
3. Otherwise fix each unaddressed Important finding in the code (not by weakening a test). Nits: fix only if trivial and safe,
   otherwise leave them and say why.
4. Run `bash scripts/check.sh` in the worktree. Commit on the PR branch, one commit per finding you fixed, message
   `review: <finding title>`.
5. Request a fresh review: `python3 scripts/review.py $ARGUMENTS --label watch-<round>`. Go back to 1.

Then write `review/$ARGUMENTS/watch.md`: each finding → fixed (commit) / left (why) / disagree (why), the last check output, and one
line: "Waiting for: <who approves, from the risk label in PR.md>".

Never merge, rebase onto main, push, or approve. If a finding asks for something the spec or plan does not allow, do not do it:
write it under "Needs a person".
