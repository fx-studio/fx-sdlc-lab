# Lessons after incidents

Version-controlled lessons file (playbook Stage 6: "writes the post-mortem to a version-controlled lessons file"; format from 4.5
of 06-maintain.md). One entry per incident, newest first, five lines. The watch job's `diagnose` skill reads this file.
When the same lesson appears twice, it becomes a line in `CLAUDE.md` ("Things Claude gets wrong"); if it still recurs, a hook.

```
## <date> · <one line: what users saw>
Signal: <metric, level, day>
Cause: <file:line, what was wrong>
Fix: <PR / commit>
Eval: <evals/tasks/...>
Lesson: <one line a future session can apply>
```

## Ngày 38 (giả lập) · Khách không nhập lại được file sao lưu của chính mình khi có hai việc trùng tên
Signal: staging_error_rate 20,5 % và production_error_rate 11,8 %, mức 3, ngày 38 (nền ~1 %)
Cause: app/backup.js parseBackup của 2e2ce98 coi trùng tên là file hỏng; spec đã duyệt chỉ cấm trùng id (A7)
Fix: rollback staging (agent, runbook) + production (Huy, theo page); 2e2ce98 không lên main
Eval: evals/tasks/E10-nhap-trung-ten.json
Lesson: một thay đổi đi ngược luật trong spec đã duyệt phải sửa spec trước; production chờ staging ít nhất một ngày có số

## Ngày 31–37 (giả lập) · CI đỏ khoảng 1/3 số lần chạy vì một test ngẫu nhiên
Signal: ci_fail_rate mức 2 ngày 32, mức 3 ngày 36 (nền 0, không có mức thống kê, dùng ngưỡng cố định)
Cause: tests/backup.test.js randomTitle() có thể ra tên rỗng, thứ app không bao giờ tạo; parseBackup từ chối đúng luật
Fix: PR 9 (agent cách ly, mức 3) · PR 10 (sửa bộ sinh, gỡ cách ly)
Eval: không (lỗi nằm ở test; flaky.sh 30 lượt là phép kiểm)
Lesson: test ngẫu nhiên chỉ sinh dữ liệu app tạo được, và chạy flaky.sh trước khi merge

People, metrics and incidents in this repo are sample data.
