# Review instructions

How Claude reviews a pull request in this repo (playbook Stage 5, "AI in the PR review loop"). Written by the tech lead (sample data:
Khoa). Findings are advisory: they never approve or block a pull request. A person approves.

Read first: the diff, `CLAUDE.md`, and the spec and plan the pull request names in `PR.md` (`spec/`, `plan/`). Read the policies in
`.claude/skills/policy-*/SKILL.md` when a change touches what they cover.

## Passes

Run three passes, in this order. Each finding belongs to exactly one pass.

1. **Bugs**: logic errors, wrong edge cases (empty list, filter active, one item, many items), state that is saved but not shown or shown
   but not saved, broken keyboard use.
2. **Security**: `policy-security`. User text reaches the page only through `textContent` (S3). Imported files are validated (S1). No new
   network request, script, CDN or dependency (S4). Nothing destructive without a confirm (S2).
3. **Compliance**: the change does what its accepted spec and plan say, and nothing the spec puts out of scope. UI text follows
   `policy-ux` (Vietnamese, short, no technical words). `CLAUDE.md` rules (size of change, tests with the fix).

## What Important means here

A finding is **Important** if it would break behaviour a user relies on, lose or leak data, or breach a policy or an accepted spec.
Everything else is a **Nit**: naming, formatting, comments, style, a cleaner way to write the same thing.

If you are not sure a problem is real, say what you would check, and mark it Nit.

## Cap the nits

At most **5 nits** per review. Pick the ones most worth a person's time. Say how many you dropped.

## Do not report

- Anything `bash scripts/check.sh` already checks (tests pass, syntax).
- `demo/`, `evals/results/`, `review/`: evidence and generated output.
- Wording inside `tickets/` and `docs/`: not working files.
- Praise, summaries of what the diff does, or restating the PR description.

## Also say

- If the change makes `CLAUDE.md` out of date (a command, a rule, a file it names), report it as a Compliance finding.
- If the same mistake is already listed under "Things Claude gets wrong" in `CLAUDE.md`, say so: the line is not working.
