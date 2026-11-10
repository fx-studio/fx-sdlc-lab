# R4-day039-staging_error_rate

Chạy 2026-11-10 16:03 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status,mcp__deploy__rollback,Bash(python3 scripts/collect.py traffic:*)`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `staging_error_rate` reached **level 3** (act through the gate) on simulated day 39 (2026-11-08). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): Known noise: the browser storage refuses about 1 % of writes, and every action that writes can fail from it: each save (not_saved) and each import (store.replace -> import_failed). Expect roughly 2 failures a day out of ~210 actions; a day with 6-9 happens a few times a year by chance alone.

Detection (scripts/detect.py, no model):
```json
{
 "metric": "staging_error_rate",
 "day": 39,
 "date": "2026-11-08",
 "value": 0.07292,
 "level": 3,
 "mode": "stats",
 "rules": [
  "WE1: last point 0.0729 > mean + 3 sd (0.0237)",
  "WE2: 2 of last 3 > mean + 2 sd (0.0187)"
 ],
 "mean": 0.00881,
 "sd": 0.00496,
 "baseline_points": 14,
 "release_changes": [
  {
   "day": 38,
   "from": "b51a55e-20261110-154535-211496",
   "to": "2e2ce98-20261110-160042-934299"
  },
  {
   "day": 39,
   "from": "2e2ce98-20261110-160042-934299",
   "to": "b51a55e-20261110-154535-211496"
  }
 ],
 "action": "act",
 "simulated_clock": true
}
```

Last points of ops/metrics/staging_error_rate.jsonl (oldest first):
```
{"day": 30, "date": "2026-10-30", "value": 0.00922, "failed": 2, "actions": 217, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 31, "date": "2026-10-31", "value": 0.0084, "failed": 2, "actions": 238, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 32, "date": "2026-11-01", "value": 0.00457, "failed": 1, "actions": 219, "by_kind": {"not_saved": 1, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 33, "date": "2026-11-02", "value": 0.01277, "failed": 3, "actions": 235, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 34, "date": "2026-11-03", "value": 0.01304, "failed": 3, "actions": 230, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 35, "date": "2026-11-04", "value": 0.01852, "failed": 4, "actions": 216, "by_kind": {"not_saved": 3, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 36, "date": "2026-11-05", "value": 0, "failed": 0, "actions": 205, "by_kind": {"not_saved": 0, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 37, "date": "2026-11-06", "value": 0.00935, "failed": 2, "actions": 214, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
{"day": 38, "date": "2026-11-07", "value": 0.20465, "failed": 44, "actions": 215, "by_kind": {"not_saved": 8, "import_failed": 36, "exception": 0}, "release": "2e2ce98-20261110-160042-934299"}
{"day": 39, "date": "2026-11-08", "value": 0.07292, "failed": 14, "actions": 192, "by_kind": {"not_saved": 3, "import_failed": 11, "exception": 0}, "release": "b51a55e-20261110-154535-211496"}
```

Level 3 means you may act, but only through these paths: runbook, pull_request. Approved runbooks: rollback staging (MCP tool deploy.rollback, env staging), only when a release changed inside the window.

If a release went live inside the window, run the approved runbook: roll staging back with the deploy MCP tool rollback(env=staging), then confirm with python3 scripts/collect.py traffic --env staging --day <same day> --confirm that the rate is back near the baseline. Do not fix code on staging. Write the intent for the real fix.

Agent-written intents still waiting for triage (1 of max 5):
- `intent/auto/2026-11-07-import-refuses-duplicate-titles.md`: # Intent: Importing a backup fails when two todos have the same title (release 2e2ce98) (watch staging_error_rate level 3, simulated day 38)

If an open intent above is about the same problem, merge into it instead of writing a new one.

Reply in exactly this shape:
- First line: a JSON object, either {"action": "new", "slug": "<short-kebab-name>"} or {"action": "merge", "into": "intent/auto/<file>.md"}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.


## Tool call (12)

1. Skill · skill=diagnose
2. Bash · command=tail -5 deploy/staging/history.jsonl
3. Read · file_path=<repo>/intent/auto/2026-11-07-import-refuses-duplicate-titles.md
4. Bash · command=tail -5 ops/metrics/staging_error_rate.confirm.jsonl
5. Glob · pattern=ops/state/*
6. Read · file_path=<repo>/scripts/traffic.js
7. Read · file_path=<repo>/scripts/collect.py
8. Write · file_path=<thư-mục-tạm>
9. Bash · command=node <thư-mục-tạm> ops/state/staging.json
10. Grep · pattern=u0[0-4]-38-[0-9]+
11. Grep · pattern=u0[0-4]-39-[0-9]+
12. Grep · pattern=u0[0-4]-37-[0-9]+

## Claude · 50 s

{"action": "merge", "into": "intent/auto/2026-11-07-import-refuses-duplicate-titles.md"}

## Update: staging day 39, watch staging_error_rate level 3 (2026-11-08)

### Problem (day 39)
Staging is back on the good release b51a55e, but imports still fail on day 39: 11 of about 25 imports. 2e2ce98 is no longer the cause. Most simulated users now have a stored list where the same todo **id** appears twice. b51a55e correctly refuses such a file, so these users cannot restore their own backup on any release. The damaged data is in the simulated staging state, not in the app code.

### Evidence
- Day 39: 14 of 192 actions failed (7.3 %): import_failed 11, not_saved 3, exception 0. Release b51a55e [ops/metrics/staging_error_rate.jsonl day 39]
- The only release change on day 39 is the rollback from day 38 (2e2ce98 → b51a55e, actor `agent:fx-sdlc-watch`). No new release went live [deploy/staging/history.jsonl, detection release_changes]
- The day-38 confirm run on b51a55e already showed the same pattern: import_failed 11 out of 224 actions [ops/metrics/staging_error_rate.confirm.jsonl day 38]
- Noise arithmetic for import_failed: about 13 % of 192 actions are imports, so ~25. At 1 % storage failure, ~0.25 failures are expected. 11 is **not noise**. not_saved: ~1.7 expected and 3 seen, which is **noise** [ops/bands.yaml noise model]
- I sampled the stored lists of users u00–u04. Four of the five hold repeated day-38 ids: `u00-38-4`, `u02-38-1`, `u02-38-2`, `u03-38-4` and `u04-38-2` each appear twice. Day-37 and day-39 ids never repeat [ops/state/staging.json, grep of `u0[0-4]-3[789]-*`]
- Simulated ids are `<user>-<day>-<i>` [scripts/traffic.js:82]. The confirm run uses the same `--day` and the same state file as the first run, and only the seed differs [scripts/collect.py:65-67]. Users who added todos in both day-38 runs got the same ids twice, and traffic.js saves the state at the end [scripts/traffic.js:112]

### Diagnosis
- **Cause:** the `--confirm` replay in `scripts/collect.py:65-67` re-runs the same day on the live state file. `scripts/traffic.js:82` builds ids from (user, day, i), so the replay writes repeated ids into users' stored lists. Every later import of those lists is refused by b51a55e's repeated-id rule, which is the correct rule. This confirms the medium-confidence hypothesis of day 38.
- **Confidence: high.** Repeated ids occur only for day 38, the only day that ran twice. The failures continue on a release that had 0–1 import failures a day for 9 days. Two things would prove this wrong: import failures on day 39 from users whose lists have no repeated ids, or failures that remain after the state is repaired.
- **Not an app bug.** It is a fault in the simulation harness. A real user's list cannot be written twice by a replay. The app's id generation was not checked in this run.
- **Rollback runbook not run, on purpose.** No release went live in the window apart from the rollback itself, and staging already runs the good release. A second `rollback(env=staging)` would pick the previous distinct release, which is the faulty 2e2ce98 [scripts/deploy.py:102-112].
- **Ruled out:** 2e2ce98 (no longer live), storage noise (arithmetic above), and b51a55e (refusing repeated ids is its intended rule).

### Desired outcome (added)
A confirm run checks the release without changing the stored data of the series it confirms.

### Success criteria (added)
- staging_error_rate under mean + 3 sd (≈ 2.4 %) with import_failed at 0–1, on the first day after the staging state is repaired.
- A `--confirm` run leaves `ops/state/<env>.json` unchanged, or writes ids that cannot collide with the main run.

### Open questions (added)
- Should the repeated day-38 entries be removed from `ops/state/staging.json` (keep the first copy of each id), or should the staging state be reset? It is simulated data, so this is the on-call engineer's call. I did not touch it.
- Fix the harness: should `--confirm` run on a copy of the state, or use a different id prefix? (tech lead)
- Was a `--confirm` run also made on production for day 38? If so, `ops/state/production.json` has the same problem, and import failures there will continue after the production rollback. (on-call)
- Should the detector leave out the day after a rollback, or mark it, when the confirm run shares state with the series? (tech lead; `ops/bands.yaml` is changed only by a person)

ACTIONS TAKEN: none. I did not run the staging rollback runbook: no release went live in the window apart from the earlier rollback to the good release b51a55e, and rolling back again would put 2e2ce98 back. I opened no pull request: the fix belongs in the harness (`scripts/collect.py` / `scripts/traffic.js`) and the simulated state, which need a person's decision. No code, tests, bands, state or main were changed. My one script (a read-only count of repeated ids) was refused because it needed approval, so I used grep on the state file instead.
