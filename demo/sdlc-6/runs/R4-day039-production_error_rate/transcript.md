# R4-day039-production_error_rate

Chạy 2026-11-10 16:03 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `production_error_rate` reached **level 3** (act through the gate) on simulated day 39 (2026-11-08). The clock of this demo is simulated: a "day"
is one collection run.

Noise model of this metric (ops/bands.yaml): Known noise: the browser storage refuses about 1 % of writes, and every action that writes can fail from it: each save (not_saved) and each import (store.replace -> import_failed). Expect roughly 2 failures a day out of ~210 actions; a day with 6-9 happens a few times a year by chance alone.

Detection (scripts/detect.py, no model):
```json
{
 "metric": "production_error_rate",
 "day": 39,
 "date": "2026-11-08",
 "value": 0.1267,
 "level": 3,
 "mode": "stats",
 "rules": [
  "WE1: last point 0.1267 > mean + 3 sd (0.0296)",
  "WE2: 2 of last 3 > mean + 2 sd (0.0238)"
 ],
 "mean": 0.01208,
 "sd": 0.00586,
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
{"day": 30, "date": "2026-10-30", "value": 0.01402, "failed": 3, "actions": 214, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 31, "date": "2026-10-31", "value": 0.02137, "failed": 5, "actions": 234, "by_kind": {"not_saved": 5, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 32, "date": "2026-11-01", "value": 0.00917, "failed": 2, "actions": 218, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 33, "date": "2026-11-02", "value": 0.01887, "failed": 4, "actions": 212, "by_kind": {"not_saved": 2, "import_failed": 2, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 34, "date": "2026-11-03", "value": 0.01914, "failed": 4, "actions": 209, "by_kind": {"not_saved": 4, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 35, "date": "2026-11-04", "value": 0.01478, "failed": 3, "actions": 203, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 36, "date": "2026-11-05", "value": 0.01339, "failed": 3, "actions": 224, "by_kind": {"not_saved": 2, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 37, "date": "2026-11-06", "value": 0.00926, "failed": 2, "actions": 216, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 38, "date": "2026-11-07", "value": 0.11848, "failed": 25, "actions": 211, "by_kind": {"not_saved": 0, "import_failed": 25, "exception": 0}, "release": "2e2ce98-20261110-160043-036580"}
{"day": 39, "date": "2026-11-08", "value": 0.1267, "failed": 28, "actions": 221, "by_kind": {"not_saved": 0, "import_failed": 28, "exception": 0}, "release": "2e2ce98-20261110-160043-036580"}
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
4. Grep · pattern="u0[0-4]-38-\d+"
5. Glob · pattern=ops/metrics/production*
6. Grep · pattern=u0[0-4]-3[89]-\d+

## Claude · 25 s

{"action": "merge", "into": "intent/auto/2026-11-07-import-refuses-duplicate-titles.md"}

## Update: production day 39, watch production_error_rate level 3 (2026-11-08)

**Page: on-call. This is the second page, because the day-38 page was not acted on.** Production still runs 2e2ce98. Roll it back to **`b51a55e-20261110-154535-364521`**. A person runs:

```
python3 scripts/rollback.py production
```

The command picks the previous distinct release in history, and that is the release named above [scripts/deploy.py:102-112, deploy/production/history.jsonl]. I did not run it.

### Problem (day 39)
A second day has passed on 2e2ce98. People whose list has two todos with the same title still cannot import their own backup and see "File sao lưu này bị lỗi". Nearly every import in production fails.

### Evidence
- Day 39: 28 of 221 actions failed (12.7 %). All 28 were import_failed, with not_saved 0 and exception 0. Release 2e2ce98-20261110-160043-036580 [ops/metrics/production_error_rate.jsonl day 39]
- Day 38 showed the same pattern, with 25 of 211 all import_failed [ops/metrics/production_error_rate.jsonl day 38]
- No rollback or new release has happened since day 38. The last entry in history is still 2e2ce98 (actor `person:fx-studio`) [deploy/production/history.jsonl]
- Noise arithmetic for import_failed: about 13 % of 221 actions are imports, so ~29 imports. At a 1 % storage failure rate that gives ~0.3 expected failures. 28 means nearly every import failed, so this is **not noise** [ops/bands.yaml noise model]
- Noise arithmetic for not_saved: ~1.9 expected and 0 seen. P(0) ≈ 15 %, so this is **noise** [ops/bands.yaml]
- Production has no confirm-run file (only `staging_error_rate.confirm.jsonl` exists). In a sample of users u00–u04, no day-38 or day-39 id appears twice in the production state. That means the repeated-id harness fault found on staging has not reached production [ops/metrics/, ops/state/production.json grep `u0[0-4]-3[89]-*`]

### Diagnosis
- **Cause:** unchanged from day 38. In 2e2ce98, `app/backup.js:101-102` refuses a file whose titles repeat, but repeated titles are valid data.
- **Confidence: high.** The failures are only of the import kind, they started on day 38 with the release, and they continue without a break on that same release. The staging failures that went on after its rollback came from replay ids, and that cause does not apply here (see the evidence above). This diagnosis would be proved wrong if import failures stay above 0–2 a day once production is back on b51a55e.
- **Damage:** a refused import writes nothing, so no bad data is stored. The users who failed on days 38–39 have to retry after the rollback.
- **Ruled out:** storage noise (see the arithmetic), a replay-state fault in production (no confirm run, no repeated ids in the sample), and b51a55e (0–2 import failures a day on days 29–37).

### Open questions (added)
- The day-38 page asked for a production rollback, and none was done. Was the page received? Was the rollback deliberately deferred in favour of a fix forward? (on-call, release manager Khoa)
- If you decide on a fix forward instead of the rollback, when will it ship? Every day on 2e2ce98 costs about 28 failed restores. (tech lead)

ACTIONS TAKEN: page_a_person. This update carries "Page: on-call" with the rollback target b51a55e-20261110-154535-364521 and the command `python3 scripts/rollback.py production`. I did not roll back or deploy production. I changed no code, tests, bands, state or main. I only ran read-only greps on ops/state/production.json.
