# R3b-khoa-duyet-pr9

Chạy 2026-11-10 15:59 ở `tmp.gce7BAX523` (thư mục riêng của lượt này), chế độ quyền `acceptEdits`. Nguyên văn, không sửa (chỉ che đường dẫn máy và email). Luồng thô: `stream.jsonl`.

## Prompt

PR 9 do agent mở trong một lượt watch job (mức 3, CI đỏ khoảng 1/3 số lần chạy vì một test ngẫu nhiên). Bạn là code owner, quyết định merge hay không.

=== Diff PR 9 ===
diff --git a/CLAUDE.md b/CLAUDE.md
index 5175f6f..be26b38 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -80,7 +80,9 @@ Humans read and write Vietnamese here; agent-facing files (`.claude/`, templates
 - **Fixing a bug:** first add a test that reproduces it, run it, and show it fails for the right reason. When a person is there,
   they commit that test before the fix. In a non-interactive run, add the test, show it failing, then fix in the same session.
   Sessions started with `TASK_KIND=fix` cannot edit committed tests (hook `protect-tests`).
-- Flaky tests (quarantined, do not try to fix them here): none (`bash scripts/flaky.sh 10`, 2026-10-29).
+- Flaky tests (quarantined, do not try to fix them here): `tests/backup.test.js` "a list with random titles survives backup and
+  import" (skipped since PR 9, 2026-11-05; cause: `randomTitle()` can return `""`, see
+  `intent/auto/2026-11-01-ci-random-titles-test-empty-title.md`).
 
 ## Deploy
 
diff --git a/tests/backup.test.js b/tests/backup.test.js
index cadb4b0..da15744 100644
--- a/tests/backup.test.js
+++ b/tests/backup.test.js
@@ -285,7 +285,10 @@ function randomTitle() {
   return s;
 }
 
-test('a list with random titles survives backup and import', () => {
+// QUARANTINED (watch ci_fail_rate level 3, simulated day 36): randomTitle() can return "" (n = 0), a title the app never creates,
+// so parseBackup rightly rejects it and the test fails ~35 % of runs. See intent/auto/2026-11-01-ci-random-titles-test-empty-title.md.
+// Remove the skip once a person fixes the generator.
+test('a list with random titles survives backup and import', { skip: 'quarantined: flaky, see intent/auto/2026-11-01-ci-random-titles-test-empty-title.md' }, () => {
   const todos = Array.from({ length: 5 }, (_, i) => ({
     id: `r${i}`, title: randomTitle(), done: Math.random() < 0.5, createdAt: 1760000000000 + i,
   }));

=== Review (REVIEW.md, 4 phát hiện) ===
# Review · PR 9 · REVIEW.md · head 8e43edf

**2 Important · 2 Nit** (dropped nits: 0) · CLAUDE.md out of date

1. [Important · Compliance] `tests/backup.test.js:291` **A watch run edited a committed test it did not create, which CLAUDE.md forbids** CLAUDE.md (Maintain) says: "On a watch run you never ... edit ... tests you did not create". The person `fx-studio` committed this test in 9253a71. The agent added the skip in this commit (8e43edf, author `fx-sdlc-agent`, ci_fail_rate level 3). `ops/bands.yaml` (ci_fail_rate.level3.instructions) does allow "quarantine the flaky test", but a quarantine always means editing a test someone else committed, so the two working files contradict each other. A later watch run, or a reviewer, cannot tell which rule wins. The tech lead should decide which rule holds before merging. → Have a person settle it. Either add an exception to the CLAUDE.md watch rule ("except adding a `skip` to quarantine a test, when the metric's level3 instructions allow it"), or remove "quarantine" from bands.yaml and have the agent only propose the skip in an intent.
2. [Important · Compliance] `CLAUDE.md:63` **CLAUDE.md still says a healthy check has tests equal to pass; with a skip that is never true** The Verification section says healthy output has `tests` equal to `pass`. With this skip the healthy output is `tests 47 / pass 46` (the PR has to explain this itself). `scripts/check.sh` prints only the tests, pass and fail lines, not the skipped count. So every later agent or person who follows CLAUDE.md will either take a green run for a broken one, or learn to ignore the mismatch. The second is worse: a test skipped by accident would then go unnoticed. → Update the CLAUDE.md healthy-output rule to `tests = pass + skipped`, with the skips matching the quarantined list. Also make check.sh print the `ℹ skipped` line (add `skipped` to its grep pattern) so the count can be checked.
3. [Nit · Compliance] `CLAUDE.md:83` **The new quarantine line says "since 2026-11-05" before any person has merged it** The line says the test has been skipped since PR 9 on 2026-11-05. PR 9 is still waiting for a person's review, and the tech lead may pick the generator fix instead (PR.md asks exactly that). If this line goes in as written, it may describe a quarantine that never happened. The old line also cited the evidence (`bash scripts/flaky.sh 10`); the new one does not. → Word it as "skipped by PR 9" and let the merger add the date. Keep a pointer to the evidence (the intent already has the 9 failed runs; optionally add a `flaky.sh` run).
4. [Nit · Bugs] `tests/backup.test.js:280` **The comment above randomTitle() promises more than the generator produces** The comment says "Whatever a person can type as a title", but `randomTitle()` makes only lowercase letters from a fixed set (no spaces, digits, capitals or other diacritics), and it can make "", which a person cannot save. Whoever fixes the generator later may keep this narrow alphabet, thinking it already covers what a person can type. I have not checked whether the app trims spaces; check that before widening the alphabet. → When the generator is fixed (a person's call), use length ≥ 1 and widen the alphabet, or correct the comment to say what it really covers.

=== Bối cảnh ===
- ops/bands.yaml (mức 3 của ci_fail_rate) dặn agent: 'Open one pull request (quarantine the flaky test or revert the commit that broke CI)'.
- CLAUDE.md mục Maintain: 'On a watch run you never ... edit ops/bands.yaml, tests you did not create, or main.'

Trả lời tiếng Việt, ngắn: (1) merge / không merge / merge sau khi sửa gì; (2) hai luật vênh nhau thì sửa luật nào, sửa thành gì (một câu); (3) có gì khác thì nói.

## Tool call (0)

(không có)

## Claude · 19 s

**(1) Merge sau khi sửa.** Quarantine là đúng quy trình và dễ gỡ. Nhưng theo review thì hai chỗ này phải sửa trước khi merge:
- Dòng CLAUDE.md đổi thành "skipped by PR 9" (bỏ ngày 2026-11-05, tôi sẽ thêm ngày khi merge). Giữ thêm đường dẫn tới bằng chứng.
- Luật "healthy" trong CLAUDE.md đổi thành `tests = pass + skipped`, và số skip phải khớp danh sách quarantine. Việc `check.sh` in thêm dòng `skipped` tôi tách thành một PR riêng, nhỏ.

Ngay sau đó là PR sửa generator (`randomTitle()` trả về độ dài ≥ 1) và gỡ `skip`. Việc này giao cho `fx-studio`, có hạn rõ. Test này bao phủ vòng sao lưu → nhập, tức là dữ liệu khách, nên không để skip lâu.

**(2) Sửa CLAUDE.md, giữ nguyên `bands.yaml`.** Luật Maintain thêm một ngoại lệ hẹp: "ngoại lệ duy nhất: thêm `skip` kèm lý do và đường dẫn intent vào test bị flaky khi level3 của metric cho phép quarantine; không sửa gì khác trong test."

Tôi chọn sửa CLAUDE.md vì quarantine là hành động nhỏ và đảo ngược được, mà `bands.yaml` đã dặn rõ. Bỏ "quarantine" khỏi `bands.yaml` thì CI đỏ sẽ không có lối thoát an toàn nào. Agent vẫn không được tự sửa `bands.yaml`.

**(3) Khác:**
- Finding 1 và 2 thuộc về policy, nên tôi sửa ở PR riêng của tôi (với tư cách chủ `policy-security`/code owner) và merge trước. PR 9 chỉ nên chứa quarantine và dòng CLAUDE.md đã sửa.
- Finding 4 (comment "Whatever a person can type") để làm cùng PR sửa generator. Trước khi mở rộng bảng chữ cái, cần kiểm tra app có trim khoảng trắng không.
- Dòng CLAUDE.md cũ có ghi chạy `bash scripts/flaky.sh 10` làm bằng chứng. Sau khi merge nên chạy lại để có số liệu mới.
