# R4-day038-production_error_rate

Chạy 2026-11-10 16:02 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `production_error_rate` reached **level 3** (act through the gate) on simulated day 38 (2026-11-07). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): Known noise: the browser storage refuses about 1 % of writes, and every action that writes can fail from it: each save (not_saved) and each import (store.replace -> import_failed). Expect roughly 2 failures a day out of ~210 actions; a day with 6-9 happens a few times a year by chance alone.

Detection (scripts/detect.py, no model):
```json
{
 "metric": "production_error_rate",
 "day": 38,
 "date": "2026-11-07",
 "value": 0.11848,
 "level": 3,
 "mode": "stats",
 "rules": [
  "WE1: last point 0.1185 > mean + 3 sd (0.0309)"
 ],
 "mean": 0.01112,
 "sd": 0.00661,
 "baseline_points": 14,
 "release_changes": [
  {
   "day": 38,
   "from": "b51a55e-20261110-154535-364521",
   "to": "2e2ce98-20261110-160043-036580"
  }
 ],
 "action": "act",
 "simulated_clock": true
}
```

Last points of ops/metrics/production_error_rate.jsonl (oldest first):
```
{"day": 29, "date": "2026-10-29", "value": 0.00481, "failed": 1, "actions": 208, "by_kind": {"not_saved": 1, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 30, "date": "2026-10-30", "value": 0.01402, "failed": 3, "actions": 214, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 31, "date": "2026-10-31", "value": 0.02137, "failed": 5, "actions": 234, "by_kind": {"not_saved": 5, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 32, "date": "2026-11-01", "value": 0.00917, "failed": 2, "actions": 218, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 33, "date": "2026-11-02", "value": 0.01887, "failed": 4, "actions": 212, "by_kind": {"not_saved": 2, "import_failed": 2, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 34, "date": "2026-11-03", "value": 0.01914, "failed": 4, "actions": 209, "by_kind": {"not_saved": 4, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 35, "date": "2026-11-04", "value": 0.01478, "failed": 3, "actions": 203, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 36, "date": "2026-11-05", "value": 0.01339, "failed": 3, "actions": 224, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 37, "date": "2026-11-06", "value": 0.00926, "failed": 2, "actions": 216, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 38, "date": "2026-11-07", "value": 0.11848, "failed": 25, "actions": 211, "by_kind": {"not_saved": 0, "import_failed": 25, "exception": 0}, "release": "2e2ce98-20261110-160043-036580"}
```

Level 3 means you may act, but only through these paths: page_a_person.

Production rollback is a person's call in this repo. Diagnose, name the release to roll back to (from deploy/production/history.jsonl) and the exact command a person runs, and stop. Put it at the top of the intent as "Page: on-call".

Agent-written intents still waiting for triage (1 of max 5):
- `intent/auto/2026-11-07-import-refuses-duplicate-titles.md`: # Intent: Importing a backup fails when two todos have the same title (release 2e2ce98) (watch staging_error_rate level 3, simulated day 38)

If an open intent above is about the same problem, merge into it instead of writing a new one.

Reply in exactly this shape:
- First line: a JSON object, either {"action": "new", "slug": "<short-kebab-name>"} or {"action": "merge", "into": "intent/auto/<file>.md"}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.


## Tool call (6)

1. Skill · skill=diagnose
2. Read · file_path=<repo>/intent/auto/2026-11-07-import-refuses-duplicate-titles.md
3. Read · file_path=<repo>/deploy/production/history.jsonl
4. Grep · pattern=argv|previous|history|def 
5. Glob · pattern=release/approvals/*
6. Grep · pattern=def rollback

## Claude · 27 s

{"action": "merge", "into": "intent/auto/2026-11-07-import-refuses-duplicate-titles.md"}

## Update: production, watch production_error_rate level 3, simulated day 38 (2026-11-07)

**Page: on-call.** Production is running 2e2ce98, the release with this bug. Roll it back to **`b51a55e-20261110-154535-364521`** with this command, run by a person:

```
python3 scripts/rollback.py production
```

The command picks the previous distinct release from history, which is the one named above [scripts/deploy.py:102-112, deploy/production/history.jsonl]. I did not run it. Rolling back production is a person's call.

### Problem (production)
Since 2e2ce98 went live in production, people who import their own backup get "File sao lưu này bị lỗi" whenever their list has two todos with the same title. Their list is left unchanged.

### Evidence
- Day 38: 25 of 211 actions failed (11.8 %). All 25 were import_failed, with 0 not_saved and 0 exception. Baseline: mean 1.1 %, sd 0.66 % [ops/metrics/production_error_rate.jsonl day 38]
- Days 29–37 on b51a55e: import_failed was 0–2 a day [ops/metrics/production_error_rate.jsonl days 29–37]
- Release 2e2ce98-20261110-160043-036580 went live in production after b51a55e-20261110-154535-364521 (actor `person:fx-studio`) [deploy/production/history.jsonl]
- Production approval for 2e2ce98 exists [release/approvals/2e2ce98.md] and was committed while this intent was still waiting for triage [git show 4b3f1b5]. So the earlier open question "Is 2e2ce98 queued for production?" is answered: yes, and it is live.
- Noise arithmetic for import_failed: about 13 % of 211 actions are imports, so ~27 imports. At 1 % storage failure, ~0.3 failures are expected. Seeing 25 means nearly every import failed. **Not noise.** [ops/bands.yaml noise model]
- Noise arithmetic for not_saved: ~1.8 expected and 0 seen. P(0) ≈ 17 %. **Noise** [ops/bands.yaml]

### Diagnosis
- **Cause:** the same as on staging. `app/backup.js:101-102` in 2e2ce98 refuses a file when a title repeats, but repeated titles are valid data.
- **Confidence: high.** It is the only release change in the window, every failure is of the import kind, and the same signature showed up on staging on the same day. This would be proved wrong if import_failed stays high after the production rollback. In that case, check for repeated ids in the stored lists, as for the staging replay.
- **Damage:** a refused import writes nothing (the whole file is refused), so rolling back should not leave bad data in production. Users who failed to restore on day 38 have to try again after the rollback.
- **Ruled out:** storage noise (arithmetic above) and b51a55e (0–2 import failures a day for 9 days).

### Success criteria (added)
- production_error_rate back under mean + 3 sd (≈ 3.1 %) on the first day after the rollback, with import_failed at 0–2.

### Open questions (added)
- Run the production rollback now, or ship a fix forward? (on-call, release manager Khoa)
- Why was 2e2ce98 approved for production while this intent about it was open? Should a release wait until the open watch intents for that release are triaged? (Khoa, tech lead)

ACTIONS TAKEN: page_a_person: this intent carries "Page: on-call" with the rollback target (b51a55e-20261110-154535-364521) and the command `python3 scripts/rollback.py production`. I did not roll back or deploy production, and I did not change any code, tests, bands or main.
