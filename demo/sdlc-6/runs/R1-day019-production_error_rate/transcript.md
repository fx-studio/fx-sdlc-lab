# R1-day019-production_error_rate

Chạy 2026-11-10 15:47 bởi scripts/watch.py (không người khởi động phiên), quyền: `Read,Glob,Grep,Skill,Bash(python3 scripts/ci_log.py:*),Bash(git log:*),Bash(git show:*),Bash(git diff:*),mcp__deploy__status`. Nguyên văn, chỉ che đường dẫn máy và email. Luồng thô: `stream.jsonl`.

## Prompt

You were invoked by the watch job (scripts/watch.py), non-interactive. No person started this session and nobody is
watching it. Use the `diagnose` skill.

Metric `production_error_rate` reached **level 3** (act through the gate) on simulated day 19 (2026-10-19). The clock of this demo is simulated: a "day"
is one collection run.

Detection (scripts/detect.py, no model):
```json
{
 "metric": "production_error_rate",
 "day": 19,
 "date": "2026-10-19",
 "value": 0.04265,
 "level": 3,
 "mode": "stats",
 "rules": [
  "WE1: last point 0.0427 > mean + 3 sd (0.0285)"
 ],
 "mean": 0.01288,
 "sd": 0.00519,
 "baseline_points": 14,
 "release_changes": [],
 "action": "act",
 "simulated_clock": true
}
```

Last points of ops/metrics/production_error_rate.jsonl (oldest first):
```
{"day": 10, "date": "2026-10-10", "value": 0.00897, "failed": 2, "actions": 223, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 11, "date": "2026-10-11", "value": 0.01802, "failed": 4, "actions": 222, "by_kind": {"not_saved": 3, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 12, "date": "2026-10-12", "value": 0.00922, "failed": 2, "actions": 217, "by_kind": {"not_saved": 1, "import_failed": 1, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 13, "date": "2026-10-13", "value": 0.01429, "failed": 3, "actions": 210, "by_kind": {"not_saved": 3, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 14, "date": "2026-10-14", "value": 0.0045, "failed": 1, "actions": 222, "by_kind": {"not_saved": 1, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 15, "date": "2026-10-15", "value": 0.00976, "failed": 2, "actions": 205, "by_kind": {"not_saved": 0, "import_failed": 2, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 16, "date": "2026-10-16", "value": 0.02041, "failed": 4, "actions": 196, "by_kind": {"not_saved": 4, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 17, "date": "2026-10-17", "value": 0.0199, "failed": 4, "actions": 201, "by_kind": {"not_saved": 4, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 18, "date": "2026-10-18", "value": 0.00905, "failed": 2, "actions": 221, "by_kind": {"not_saved": 2, "import_failed": 0, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
{"day": 19, "date": "2026-10-19", "value": 0.04265, "failed": 9, "actions": 211, "by_kind": {"not_saved": 4, "import_failed": 5, "exception": 0}, "release": "b51a55e-20261110-154535-364521"}
```

Level 3 means you may act, but only through these paths: page_a_person.

Production rollback is a person's call in this repo. Diagnose, name the release to roll back to (from deploy/production/history.jsonl) and the exact command a person runs, and stop. Put it at the top of the intent as "Page: on-call".

Agent-written intents still waiting for triage (0 of max 5):
(empty)

If an open intent above is about the same problem, merge into it instead of writing a new one.

Reply in exactly this shape:
- First line: a JSON object, either {"action": "new", "slug": "<short-kebab-name>"} or {"action": "merge", "into": "intent/auto/<file>.md"}.
- Then the intent in Markdown (for "merge": only what is new, it is appended as an update).
- Last line: `ACTIONS TAKEN: <none, or what you did through the level 3 paths>`.


## Tool call (16)

1. Skill · skill=diagnose
2. Bash · command=cat deploy/production/history.jsonl
3. Bash · command=cat ops/metrics/production_error_rate.jsonl
4. Read · file_path=<repo>/scripts/collect.py
5. Read · file_path=<repo>/deploy/production/history.jsonl
6. Read · file_path=<repo>/scripts/traffic.js
7. Read · file_path=<repo>/deploy/production/current/backup.js
8. Bash · command=git log --oneline -8 -- app/ deploy/
9. Read · file_path=<repo>/deploy/production/current/store.js
10. Bash · command=cat deploy/production/current/RELEASE.json
11. Bash · command=ls -la ops/metrics/ ops/state/
12. Read · file_path=<repo>/ops/watch.jsonl
13. Write · file_path=<thư-mục-tạm>
14. Bash · command=node <thư-mục-tạm> ops/state/production.json
15. Bash · command=git diff --stat 20b4e8f b51a55e -- app/
16. Read · file_path=<repo>/.claude/skills/write-intent/template.md

## Claude · 72 s

{"action": "new", "slug": "production-import-failed-spike-day19"}

# Intent: Lượng "nhập lại file sao lưu thất bại" tăng vọt trên production, ngày 19

Page: on-call. **Rollback không giúp gì ở đây, khuyên không chạy.** Production chưa đổi release trong cả khoảng theo dõi. Bản trước trong `deploy/production/history.jsonl` là `20b4e8f-20261104-102454-306665`, nhưng `app/` của nó giống hệt bản đang chạy (`git diff --stat 20b4e8f b51a55e -- app/` không ra gì). Nếu on-call vẫn muốn quay về bản đó thì chạy `python3 scripts/rollback.py production`. Chạy hay không là quyết định của một người.

Author: fx-sdlc-agent (watch job) · Status: draft · Source: watch production_error_rate level 3, simulated day 19 · Date: 2026-10-19

## Problem
Ngày 19, nhiều người dùng (giả lập) sao lưu danh sách ra file rồi nhập lại chính file đó thì bị app từ chối: 5 lần, trong khi các ngày trước chỉ 0–2 lần. Lỗi "chưa lưu" (not_saved) vẫn ở mức bình thường. Đây là traffic giả lập, không có người dùng thật.

## Evidence
- Ngày 19 tỉ lệ lỗi là 0.0427 (9/211). Trung bình nền 0.0129, sd 0.0052, vượt mức mean + 3 sd (0.0285) [ops/metrics/production_error_rate.jsonl day 19]
- Ngày 19 tách theo loại: import_failed 5, not_saved 4, exception 0 [ops/metrics/production_error_rate.jsonl day 19]
- Ngày 1–18 có tổng cộng 8 import_failed, khoảng 0.44/ngày, chưa ngày nào quá 2. not_saved dao động 0–5/ngày [ops/metrics/production_error_rate.jsonl day 1–18]
- Cả 19 ngày chạy cùng một release `b51a55e-20261110-154535-364521`, detect báo `release_changes: []` [ops/metrics/production_error_rate.jsonl] [deploy/production/history.jsonl]
- Bản trước `20b4e8f` có app giống hệt bản đang chạy [git diff --stat 20b4e8f b51a55e -- app/]
- Staging ngày 19 vẫn bình thường: 0.0182, level 0 [ops/watch.jsonl line 56]
- Một import chỉ bị tính import_failed trong hai trường hợp: `parseBackup` từ chối file, hoặc `store.replace` không ghi được vì storage giả lập ném lỗi quota với xác suất 1% [scripts/traffic.js:95-101] [deploy/production/current/backup.js:130-134] [deploy/production/current/store.js:30-44]

## Diagnosis
- Không có thay đổi code hay release nào trong khoảng theo dõi, nên nguyên nhân không nằm ở một bản deploy.
- Giả thuyết 1 (nhiễu): `store.replace` gặp lỗi quota 1% của traffic.js:55. Mỗi ngày có khoảng 32 lần nhập, nên trung bình khoảng 0.3–0.44 lần lỗi/ngày. Theo Poisson, xác suất có từ 5 lần trở lên trong một ngày vào khoảng 1e-4, quá thấp để coi là nhiễu thông thường.
- Giả thuyết 2: dữ liệu trong `ops/state/production.json` khiến `parseBackup` từ chối, ví dụ id trùng (backup.js:100). Trường hợp này xảy ra khi cùng một simulated day chạy hai lần trên cùng state, vì id có dạng `user-day-i` (traffic.js:82). Chưa kiểm chứng được: tôi không chạy được script đọc state trong phiên này (cần duyệt) và không có file `.confirm` nào.
- **Confidence: low.** Muốn chắc hơn thì quét `ops/state/production.json` tìm id trùng hoặc todo sai. Nếu có thì giả thuyết 2 đúng. Một cách khác là chạy lại ngày 19 trên một bản sao của state rồi in message của từng import thất bại.
- Đã loại trừ: release mới (không có), lỗi code app (exception = 0, code giống bản trước), lỗi chung của môi trường (not_saved và staging đều bình thường).

## Desired outcome
Người dùng nhập lại được file sao lưu do chính app tạo ra, trừ khi lỗi đúng là do bộ nhớ trình duyệt đầy.

## Success criteria
- production_error_rate quay về dưới mean + 3 sd trong 3 ngày giả lập liền nhau.
- import_failed ≤ 2/ngày.
- Biết nguyên nhân của 5 lần import_failed ngày 19: quota hay parseBackup.

## Affected users and systems
Người dùng giả lập trên production, luồng sao lưu rồi nhập lại (`backup.importBackup`).

## Constraints
- Rollback production do một người quyết định [CLAUDE.md#Deploy].
- Watch run không được sửa ops/bands.yaml hay test [CLAUDE.md#Maintain].

## Out of scope
Sửa code, đổi bands, rollback.

## Impact
Low: chỉ có một ngày tăng, không có exception, và traffic là giả lập. Nếu giả thuyết 2 đúng thì lỗi nằm ở bộ sinh traffic chứ không ở app.

## Open questions
- Ngày 19 có bị chạy `collect.py traffic --env production` hai lần, hoặc có ai sửa `ops/state/production.json` không? (on-call)
- Có nên ghi lý do của mỗi lần import thất bại vào by_kind (quota hay parse) để lần sau tự phân biệt được không? (tech lead)
- Hook release-gate đang chặn cả lệnh chỉ đọc (`cat`) trong `deploy/production/`. Có đúng ý đồ không? (tech lead)

ACTIONS TAKEN: page_a_person: dòng "Page: on-call" ở đầu intent này. Không rollback, không deploy, không sửa file nào trong repo. Chỉ ghi một script đọc ở scratchpad, nhưng không chạy được vì cần duyệt.
