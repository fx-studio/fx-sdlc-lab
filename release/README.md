# release/

Production releases are approved here, **by people only** (playbook Stage 5: "the agent may act up to the production gate and cannot
pass it"). The agent can build a candidate (`prepare_release`); it cannot write in this folder (hook `release-gate`) and cannot
commit on `main` (hook `no-self-approve`).

To approve a release, the release manager commits on `main` a file `release/approvals/<sha7>.md`:

```markdown
# Release <sha7>

Approved-by: <name> (release manager)
Date: <YYYY-MM-DD>
Checked: <one line: what you checked yourself, e.g. "ran the backup flow on staging with the keyboard">
```

Then a person runs `python3 scripts/deploy.py deploy production <sha7>`. One approval covers one release, not a session.

`gate-log.jsonl` (git-ignored) records every decision of the gate with a timestamp.
All names in this repo's demo are sample data (release manager: Khoa, simulated).
