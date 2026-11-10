# R4-day038-staging_error_rate

Chạy 2026-11-10 16:02 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status,mcp__deploy__rollback,Bash(python3 scripts/collect.py traffic:*)`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `staging_error_rate` reached **level 3** (act through the gate) on simulated day 38 (2026-11-07). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): Known noise: the browser storage refuses about 1 % of writes, and every action that writes can fail from it: each save (not_saved) and each import (store.replace -> import_failed). Expect roughly 2 failures a day out of ~210 actions; a day with 6-9 happens a few times a year by chance alone.

Detection (scripts/detect.py, no model):
```json
{
 "metric": "staging_error_rate",
 "day": 38,
 "date": "2026-11-07",
 "value": 0.20465,
 "level": 3,
 "mode": "stats",
 "rules": [
  "WE1: last point 0.2046 > mean + 3 sd (0.0247)"
 ],
 "mean": 0.01011,
 "sd": 0.00486,
 "baseline_points": 14,
 "release_changes": [
  {
   "day": 38,
   "from": "b51a55e-20261110-154535-211496",
   "to": "2e2ce98-20261110-160042-934299"
  }
 ],
 "action": "act",
 "simulated_clock": true
}
```

Last points of ops/metrics/staging_error_rate.jsonl (oldest first):
```
{"day": 29, "date": "2026-10-29", "value": 0.01376, "failed": 3, "actions": 218, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 30, "date": "2026-10-30", "value": 0.00922, "failed": 2, "actions": 217, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 31, "date": "2026-10-31", "value": 0.0084, "failed": 2, "actions": 238, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 32, "date": "2026-11-01", "value": 0.00457, "failed": 1, "actions": 219, "by_kind": {"not_saved": 1, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 33, "date": "2026-11-02", "value": 0.01277, "failed": 3, "actions": 235, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 34, "date": "2026-11-03", "value": 0.01304, "failed": 3, "actions": 230, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 35, "date": "2026-11-04", "value": 0.01852, "failed": 4, "actions": 216, "by_kind": {"not_saved": 3, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 36, "date": "2026-11-05", "value": 0, "failed": 0, "actions": 205, "by_kind": {"not_saved": 0, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 37, "date": "2026-11-06", "value": 0.00935, "failed": 2, "actions": 214, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 38, "date": "2026-11-07", "value": 0.20465, "failed": 44, "actions": 215, "by_kind": {"not_saved": 8, "import_failed": 36, "exception": 0}, "release": "2e2ce98-20261110-160042-934299"}
```

Level 3 means you may act, but only through these paths: runbook, pull_request. Approved runbooks: rollback staging (MCP tool deploy.rollback, env staging), only when a release changed inside the window.

If a release went live inside the window, run the approved runbook: roll staging back with the deploy MCP tool rollback(env=staging), then confirm with python3 scripts/collect.py traffic --env staging --day <same day> --confirm that the rate is back near the baseline. Do not fix code on staging. Write the intent for the real fix.

Agent-written intents still waiting for triage (0 of max 5):
(empty)

If an open intent above is about the same problem, merge into it instead of writing a new one.

Reply in exactly this shape:
- First line: a JSON object, either {"action": "new", "slug": "<short-kebab-name>"} or {"action": "merge", "into": "intent/auto/<file>.md"}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.


## Tool call (16)

1. Skill · skill=diagnose
2. Bash · command=tail -5 deploy/staging/history.jsonl
3. Bash · command=git log --oneline b51a55e..2e2ce98
4. Bash · command=git show 2e2ce98
5. Grep · pattern=import_failed|duplicate|title
6. Grep · pattern=import_failed
7. Read · file_path=<repo>/scripts/traffic.js
8. ToolSearch · {"query": "select:mcp__deploy__rollback,mcp__deploy__status", "max_results": 2}
9. mcp__deploy__rollback · {"env": "staging"}
10. Bash · command=python3 scripts/collect.py traffic --env staging --day 38 --confirm
11. Bash · command=git show b51a55e:app/backup.js
12. Grep · pattern=confirm|state|seed
13. Write · file_path=<thư-mục-tạm>
14. Bash · command=node <thư-mục-tạm> ops/state/staging.json
15. Read · file_path=<repo>/.claude/skills/write-intent/template.md
16. Grep · pattern=^const (todo|fileOf)|function (todo|fileOf)

## Claude · 76 s

{"action": "new", "slug": "import-refuses-duplicate-titles"}

# Intent: Importing a backup fails when two todos have the same title (release 2e2ce98)

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch staging_error_rate level 3, simulated day 38 · Date: 2026-11-07

## Problem
On release 2e2ce98, people who save their list to a file and import that same file back get the message "File sao lưu này bị lỗi". That happens whenever their list has two todos with the same title, for example "Mua sữa" added on two different days. The app lets them add the same title twice, then refuses the backup it wrote itself. Their list stays as it was, but they cannot restore it (for example on a new laptop).

## Evidence
- Day 38: 44 failed out of 215 actions (20.5 %). 36 were import_failed and 8 were not_saved. The baseline is 1.0 % ± 0.49 % [ops/metrics/staging_error_rate.jsonl day 38]
- Days 29–37: import_failed was 0 or 1 per day, on release b51a55e [ops/metrics/staging_error_rate.jsonl days 29–37]
- Release 2e2ce98 went live on staging (actor `person:long-dev`), replacing b51a55e [deploy/staging/history.jsonl]
- The only commit in the change: "backup: refuse a file that lists the same todo twice". It adds a title set and refuses the file when a trimmed, lower-cased title repeats [git show 2e2ce98]
- Simulated users pick titles from 9 fixed words and import a backup of their own list (13 % of actions), so most lists hold a repeated title [scripts/traffic.js:47, :94-101]
- Noise arithmetic for import_failed: about 32 imports, and each fails from storage about 1 % of the time, so ~0.3 failures are expected. 36 means nearly every import failed. **Not noise.** [ops/bands.yaml noise model, ops/metrics day 38]
- Noise arithmetic for not_saved: about 180 writes at 1 % gives an expected 1.8. 8 is rare (Poisson P(≥8) ≈ 0.1 %), but the noise model says 6–9 "happens a few times a year", and the change does not touch save. **Probably noise**, low confidence [ops/bands.yaml, git show 2e2ce98]
- After the rollback to b51a55e, the confirm run gave 14/224 = 6.25 % (not_saved 3, import_failed 11). That is lower, but not back at the baseline [collect.py traffic --env staging --day 38 --confirm]

## Diagnosis
- **Cause:** `app/backup.js:101-102` in 2e2ce98 treats a repeated title as a corrupt file. Two todos with the same title are valid data in this app; only a repeated **id** means a bad file. The new test in `tests/backup.test.js` pins this wrong rule.
- **Confidence: high.** It is the only code change in the window, it is the import path, and the failures are almost all of that kind. A replay of day 38 on 2e2ce98 with no repeated titles in the lists would prove this wrong.
- **The 11 import failures after rollback: unexplained, medium-confidence hypothesis.** b51a55e refuses repeated **ids**. Simulated ids are `<user>-<day>-<i>` [scripts/traffic.js:82], and the confirm run replays day 38 on the state file that the first day-38 run already wrote [scripts/collect.py:65-67]. That would give ids repeated from the earlier run, so this is an artifact of the replay harness, not of b51a55e. I could not check `ops/state/staging.json`: the read script needed an approval that a headless run cannot get. If this hypothesis holds, the confirm run has also **saved** repeated-id lists into the staging state, and those users' imports will keep failing on any release.
- **Ruled out:** a bug in b51a55e (it had 0–1 import failures a day for 9 days), and storage noise as the cause of the import failures (see the arithmetic).

## Desired outcome
Anyone can import a backup the app made of their own list, including a list where two todos share a title.

## Success criteria
- staging_error_rate back inside its band (≤ mean + 3 sd ≈ 2.5 %), with import_failed at 0–1 per day.
- Exporting and then importing a list with two todos titled "Mua sữa" gives "Đã nhập n việc."

## Affected users and systems
`app/backup.js` (parseBackup), `tests/backup.test.js` (the new test), the staging environment, and production if 2e2ce98 is promoted.

## Constraints
- A file with a repeated **id** must still be refused (the existing b51a55e rule) [git show b51a55e:app/backup.js].
- An import refuses the whole file, never part of it [app/backup.js comment on parseBackup].

## Out of scope
Detecting "two backups pasted together" in some other way. If that is still wanted, it needs its own intent from the product owner.

## Impact
High. Restoring a backup is the only way to move or recover a list, and on 2e2ce98 it breaks for most real lists.

## Open questions
- What was 2e2ce98 meant to fix? Was a real complaint about pasted backups behind it? (long-dev, product owner)
- Revert 2e2ce98, or keep the id check only and drop the title check plus its test? (tech lead)
- Does `ops/state/staging.json` now hold repeated ids from the day-38 replay? Should the simulated state be reset before day 39? (on-call)
- Is 2e2ce98 queued for production anywhere? Production is on b51a55e according to commit 4b3f1b5. (release manager Khoa)

ACTIONS TAKEN: Rolled staging back from 2e2ce98-20261110-160042-934299 to b51a55e-20261110-154535-211496 with deploy.rollback(env=staging). The confirm run (`python3 scripts/collect.py traffic --env staging --day 38 --confirm`) gave 0.0625, down from 0.2046 but still above the band, possibly because the replay repeats day-38 ids (unverified). No code, tests, bands or main changed.
