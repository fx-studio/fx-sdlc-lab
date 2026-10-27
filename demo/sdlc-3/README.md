# Demo SDLC-3 · Build: plan trước, code sau

Demo cho tập **SDLC-3** của loạt "AI-Native SDLC". Chạy thật ngày **2026-10-27**, Claude Code 2.1.289 headless (`claude -p`). Phiên
code, plan, review và verifier dùng `claude-opus-5-5`; phiên đóng vai dùng `sonnet`. 53 lượt `run.py` + 2 lượt bộ thử kích hoạt skill +
một lượt máy chạy T0 trên Chromium. Tổng khoảng **27,2 USD**: 24,06 USD ghi trong `runs/*/so-do.jsonl`, 1,44 USD lượt R6 lần 2, khoảng
1,4 USD lượt R6 lần 1 (script lúc đó cộng tiền sai nên không ghi được, số này là ước) và 0,29 USD một lượt gỡ lỗi script.

## Demo này để làm gì

Playbook của Anthropic nói bước Build làm thế này: bắt đầu bằng **plan mode**, Claude đọc `intent.md`, `spec.md` và code rồi đề xuất
plan (file nào đổi, thứ tự, rủi ro, test chứng minh); người chất vấn plan trước khi duyệt; duyệt xong mới cho code (auto-accept);
`CLAUDE.md` giữ thứ cả team cùng giữ; policy phải luôn đúng thì cần thứ tất định (hook); một verifier chỉ đọc và chạy, báo "đã chạy
gì, thấy gì"; việc độc lập chạy song song trong worktree. Demo dựng **đúng bộ đồ đó** trên app todo của SDLC-2 và chạy từng câu.

**Bộ đồ của bước Build** (tiếng Anh, vì đây là thứ agent đọc; commit `9af318d`):

| Thành phần | Vai trò | Ứng với playbook |
|---|---|---|
| `CLAUDE.md` mục **Build** | Lệnh chạy app/test/lint, bảng phân hạng thay đổi (Trivial · Small · Medium · Large), plan bốn mục, mục **Things Claude gets wrong** | "a CLAUDE.md the whole team maintains" |
| `plan/` | Plan được duyệt nằm ở đây, `Status: draft` → người đổi `accepted` | "plan.md": plan có người chấp nhận |
| `.claude/hooks/protect-paths.py` · `no-secrets.py` · `check-js.py` | Chặn sửa `docs/`, `tickets/` và file `intent/` · `spec/` · `plan/` đã accepted; chặn chữ trông như khoá bí mật; `node --check` sau mỗi lần sửa `.js`. Mỗi hook ghi thời gian chạy vào `.hook-timing.log` | "Hooks: deterministic" |
| `.claude/hooks/no-self-approve.py` bản 3 | Thêm `plan/` vào danh sách agent không được ghi `Status: accepted` | "A human always makes that call" |
| `.claude/agents/verifier.md` | Subagent chỉ có Bash + Read: chạy test, thử thay đổi và hai luồng gần nhất, so diff với plan, **không sửa gì** | Mẫu verifier của playbook |
| `scripts/pre-commit` | Commit đổi `app/` mà không đổi `plan/` thì chặn, trừ khi đặt `PLAN_SKIP="<lý do>"` | "When implementation departs from the plan, update plan.md in the same commit" |
| `.claude/skills/policy-security/triggers.md` + `scripts/skill-triggers.sh` | Năm câu người ta hay hỏi; mỗi câu chạy một phiên plan mode, xem skill có được gọi không | "Test that the skill triggers on different phrasings" |

**Nhân vật giả lập** ở `personas/`: Thảo (product owner), Khoa (tech lead, kiêm bảo mật), Linh (UX owner, duyệt chữ trên app), Mai
(privacy owner). Mỗi người một phiên `sonnet` chạy trong thư mục trống, chỉ biết hồ sơ của mình và đúng phần được đưa.

**Việc được làm:** spec `khach-khong-mat-viec` của SDLC-2 (sao lưu ra file, nhập lại, báo khi không lưu được). Ở SDLC-2 spec này còn
`draft`, ghi `policy-ux@1`, nên **bước 0** là đưa nó tới `accepted`.

## Các lượt chạy

Transcript ở `runs/<run>/transcript.md` (prompt, **từng tool call**, câu trả lời cuối), luồng thô nguyên văn ở `stream.jsonl`, số đo ở
`so-do.jsonl`. Chạy lại bằng `run.py` (docstring đầu file). `run.py` che đường dẫn máy, email và tên người dùng **ngay lúc ghi**.

### Bước 0 · đưa spec tới accepted (B0a–B0l, khoảng 5 USD)

`/write-spec` viết lại spec theo `policy-ux@2`, rồi bốn nhân vật trả lời mục giả định. Mỗi vòng trả lời lại đẻ ra giả định mới:
**12 → 4 → 3 → 1 → 0**. Linh trả lời A3 "Có" rồi rút lại sau khi đọc lời Khoa. Hai lần Claude không ghi được vào `spec/` dù đã cho
`Write(spec/**)` ở chế độ quyền `default` (B0f, B0i): nó ghi bản nháp ra thư mục tạm, người chạy demo lấy nội dung từ `stream.jsonl` đặt
vào spec; B0k dùng `acceptEdits`. Bảng câu trả lời: [tra-loi-gia-dinh.md](tra-loi-gia-dinh.md). Spec accepted ở commit `fdf3791`.

### Plan và code (R0–R3f)

| Run | Làm gì | Kết quả chính |
|---|---|---|
| **R0** · làm luôn | "Implement spec/…" ở worktree riêng, **không plan mode** | 225 s, 1,14 USD, 4 file (+200/−5). Chạy được. Thử `npm install jsdom`, bị chặn; viết script kiểm ở thư mục tạm nên **repo không có test nào**. Tự quyết 3 chỗ spec không nói (câu chữ tự viết, chặn file không có việc nào, tiêu đề chỉ có dấu cách) và **có ghi ra** để người xác nhận |
| **R1** · plan mode | Cùng yêu cầu, `--permission-mode plan` | 135 s. Plan v1 ~1.900 từ, tự chọn hạng **Medium**. Hỏi **6 câu** trước khi code (hạng, thêm `backup.js`, 1 MB là bao nhiêu byte, file `todos: []`, `"null"`, kiểm tay). Đề xuất tách logic ra `backup.js` để Node test được. Plan nằm ở `~/.claude/plans/`, không nằm trong tool call `ExitPlanMode`: người chạy demo chép ra `plan-v1.md` |
| **R2a** · chất vấn plan | Năm câu chất vấn, tiếp đúng session R1 | Câu 4, "test nào fail nếu bước rủi ro nhất làm sai?" → *"Before the revision, none did."* Thêm test vòng sao lưu → nhập, tách `persist` / `importBackup`, thêm mục "cách đơn giản hơn đã cân nhắc và bỏ". Plan v2 ~2.500 từ |
| **R2b** · Khoa đọc plan | Khoa **chỉ có plan**, không có hội thoại | Một engineer khác làm theo được, nhưng thiếu **8 chỗ** (thứ tự commit mâu thuẫn, câu chữ, lỗi `file.text()`, `revokeObjectURL`, static test, grep nơi gọi `store`, rollback, kiểm tay). Chốt hạng **Large**, 1 MB = 1.048.576 byte, duyệt **có điều kiện** |
| **R2c–R2e** | Thảo, Linh trả lời Q4; Claude sửa plan; Linh duyệt câu chữ | R2d (2,43 USD) tìm thêm: thử trên điện thoại cần HTTPS (`crypto.randomUUID`), spec hạn chót sẽ đá với spec này ở dạng dữ liệu. Linh thay M11 và **M12**. Plan accepted ở commit `948e1ce` dưới tên Khoa (giả lập) |
| **R3** · code theo plan | Tiếp session R2, plan đã accepted | 440 s, **4,93 USD**, 35 test. Claude **báo chứ không tự sửa** 5 chỗ code phải lệch plan, đáng kể nhất: câu M12 Linh sửa làm **trượt tiêu chí 23** của spec đã accepted. 9 lệnh Bash bị từ chối (script nháp dựng trong Bash: heredoc, `sed -i`, vòng lặp) |
| **R3b** · verifier | Subagent `verifier` | 0 lỗi code, 35/35 test, **5 chỗ lệch plan** (thứ tự commit, một dòng Proof không thể xảy ra, chỗ đặt M12, banner không có test tự động, plan chưa cập nhật). **Không chạy được phần nối với trang**: chỉ có Bash + Read nên không ghi được file script, đi đường heredoc thì bị chặn 4 lần. Nó nói rõ điều đó và không lách |
| **R3c** · Khoa review diff | Điều kiện 4 của plan: người khác review diff commit B | Cho commit **kèm ba điều kiện**. Nêu một lỗi *có thể* thật: validator nhập chặt hơn chỗ tạo việc (người chạy demo đọc code: `add()` đã trim và sinh `id` chuỗi từ bản đầu, nên Khoa đòi một test ghim). Một race "đáng sửa, không chặn". Mai: phải giữ ý "xoá dữ liệu" (P4); Linh chốt "dữ liệu trang web"; Mai xác nhận đạt |
| **R3d** · sửa trước commit B | Session mới, hai việc | M12 theo câu Linh chốt; `tests/app.test.js` chạy **nguyên `app.js`** trong `node:vm` để ghim `add()`: đúng phần verifier bó tay. 38 test |
| **R3e** · T0 bằng máy | `t0-chromium.py`, Chromium headless | Dữ liệu do **bản cũ** ghi (3 việc thêm bằng tay; 2.000 việc), mở bằng bản mới: đủ việc, không dải báo, không ghi lại; sao lưu rồi nhập lại ra y danh sách cũ (2.001 việc: 0,46 s); dữ liệu hỏng giữ nguyên. **Lần chạy đầu trượt 2 mục vì lỗi script của người chạy demo**, không phải lỗi app. Thấy thêm: hộp xác nhận viết "2001", không "2.001" |
| **R3f** · so R0 với R3 | Phiên chỉ đọc, chấm từng tiêu chí của spec | **R0 đạt 25/26, R3 đạt 25/26** (cùng một tiêu chí "chưa biết": bàn phím + trình đọc màn hình). R0 có spec accepted trong tay, chỉ không có plan. R0 làm **tốt hơn** ở câu từ chối: spec F2 bước 4 đòi nói "vì sao + làm gì tiếp", năm câu của R3 thiếu (lọt qua plan, Linh, verifier, Khoa). R3 hơn ở iOS Safari (`revokeObjectURL`) và để lại test trong repo. Prompt của lượt này **mô tả sai R0** ("coded straight from the intent"); Claude đọc `diff.patch` và tự sửa lại |

Commit A (`eae2c2c`, `backup.js` + test, 21 test trên đúng cây đó) và commit B (`8300aaa`, 38 test) do người chạy demo commit, kèm mục
**Tiến độ** của plan. Commit B đi **trước** bảng kiểm tay T0–T13: lệch plan, ghi rõ trong plan, tính năng **chưa nghiệm thu**.

### Hook, CLAUDE.md, skill, song song (R4–R8)

| Run | Làm gì | Kết quả chính |
|---|---|---|
| **R4** · hook chặn | Ba việc trong một phiên, worktree riêng: sửa tiêu chí 23 của spec accepted (đúng gợi ý của Mai), dán một khoá giả, dán một hàm JS thiếu `}` | `protect-paths` **chặn** sửa spec (0,5 ms). `no-secrets` **chặn** khoá (0,1 ms). `check-js` **bắt** JS hỏng ngay sau khi ghi (133 ms) và báo lại cho Claude. Với cả ba, Claude nói bước tiếp theo đúng: người sửa spec; khoá coi như lộ, sync cần intent riêng; thêm `}` hoặc trả file |
| **R5a** · `/init` | `/init` trên bản repo đã xoá `CLAUDE.md` | 72 dòng (bản của repo: 64). **Hơn** bản của repo ở phần kiến trúc app (thứ tự nạp script, chỉ `store.js` chạm bộ nhớ). **Thiếu** luật của người (demo chỉ ghi thứ đã chạy, dữ liệu mẫu, không đọc `.env`, không push). **Tự bịa** hai dòng "Things Claude gets wrong" chưa từng xảy ra. Phần kiến trúc đã ghép vào `CLAUDE.md` sau khi người soát |
| **R5b / R5c** · vòng "sai → ghi → vẫn sai → hook" | Lỗi lặp nhất qua R0, R3, R3b, R3d: dựng script nháp trong Bash, **20 lần bị từ chối**. Cùng một việc kiểm biên 1 MB, chạy 2 lần không có dòng nào, 2 lần có một dòng trong `CLAUDE.md` | Không có dòng: **2 + 2 lần bị từ chối**, 8–9 tool call, 0,30–0,33 USD. Có dòng: **0 + 0**, 5 tool call, 0,23–0,27 USD. **Ghi một dòng là hết sai, không cần làm hook.** Dòng đó đã vào `CLAUDE.md` |
| **R6** · bộ thử kích hoạt skill | 5 câu × `policy-security`, mỗi câu một phiên plan mode, chạy 2 lần | Cả hai lần **0/5** câu gọi skill qua công cụ Skill. Lần 2 tách kỹ hơn: 2/5 câu **mở file** `SKILL.md` bằng `cat` (policy có được đọc, skill không kích hoạt), 3/5 không đụng policy nào. Câu 1 (nhập JSON) còn phát hiện tính năng đã có và khuyên không viết plan mới. Phiên thử nạp cả skill riêng của máy người chạy, nên môi trường không sạch |
| **R7a** · hỏi trước khi chạy song song | Ba việc chờ: A câu từ chối (R3f tìm ra), B race khi nhập (Khoa nêu), C hạn chót (spec còn draft). Hỏi từng cặp đụng file nào | A+B **chạy song song được**; A+C, B+C không nên (đụng `backup.js`, cùng mở rộng bộ giả lập test); **C chưa bắt đầu được** (spec draft, chưa có plan). Và: **ca lỗi Khoa tả không xảy ra** (`add()` dùng `push`, cùng mảng); ca thật là hai lần nhập chồng nhau hoặc xoá việc lúc đang đọc file. Người chạy demo kiểm code: đúng |
| **R7b** · hai session, hai worktree | Nhánh tạm `wt/cau-tu-choi` (A) và `wt/nhap-chong` (B), chạy cùng lúc | A: hạng Trivial, 38 test; tự nhắc M8 từng do Thảo duyệt nên cần Thảo (R7c: đồng ý). B: hạng Small, viết test **fail trước** (38/39) rồi sửa (39/39). Người commit từng nhánh kèm plan, gộp về `main`: **không xung đột**, 39 test. Xoá nhánh |
| **R8** · phân hạng | 4 yêu cầu cỡ khác nhau, chỉ hỏi hạng | **4/4 khớp** đáp án người chạy demo chốt trước ([dap-an-truoc.md](runs/R8-phan-hang/dap-an-truoc.md)). Câu 2 là lỗi giả định, Claude đọc code và nói hai dòng đếm trông đúng, sẽ đổi hạng nếu nguyên nhân ở ngoài |
| **R9** · làm nốt ba việc treo | Sửa spec đã accepted theo đúng đường: Thảo, Khoa, Mai, Linh (giả lập) quyết; **người** sửa spec và commit dưới tên Thảo (`65fae52`); Claude code; người cập nhật plan và commit (`028b8c0`) | Tiêu chí 23 đổi theo chữ "dữ liệu trang web". Câu riêng M17 khi nhập lỗi lúc lưu: Khoa chỉ ra ca **đã có phần chưa lưu** thì câu Linh đề xuất ban đầu nói sai, Linh viết lại một câu đúng cho cả hai ca thay vì thêm nhánh code. Số từ 1.000 có dấu chấm ở mọi câu, kể cả dòng đếm (Claude hỏi lại chỗ này thay vì tự làm). Hạng Small, 42 test, 1,81 USD |

Thời gian hook trong các lượt code (`runs/hook-timing-main.jsonl`, đo bên trong script, **chưa tính** khởi động Python): `protect-paths`
23 lần, trung bình 0,2 ms; `no-secrets` 23 lần, trung bình 0,5 ms, tối đa 1,2 ms; `check-js` 12 lần, trung bình 77 ms, tối đa 138 ms.

## Đối chiếu với tài liệu Build

| Tài liệu nói | Demo cho thấy | Kết luận |
|---|---|---|
| Bắt đầu bằng plan mode, plan nêu file, thứ tự, rủi ro, test | R1 hỏi 6 câu đúng những chỗ R0 lặng lẽ tự quyết | **Đúng.** Giá trị lớn nhất của plan ở đây là **câu hỏi**, không phải danh sách file |
| Người chất vấn plan trước khi duyệt | R2a: một câu "test nào fail?" làm plan có test. R2b: người không xem hội thoại tìm ra 8 chỗ thiếu | **Đúng, có bằng chứng.** Người duyệt nên đọc plan **không kèm hội thoại**, như người sẽ làm theo nó |
| Plan trước thì code ra đúng hơn (ý ngầm của "plan sai thì sửa một tài liệu") | R0 và R3 cùng đạt 25/26 tiêu chí khi **cả hai có spec tốt** | **Chưa thấy hơn ở độ đúng.** Hơn ở chỗ khác: test nằm lại repo (0 → 38), quyết định có tên người, lỗi Safari iOS được chặn trước. Plan còn **thêm người đụng vào chữ** và sinh ra một lỗi (M12), rồi chính quy trình bắt lại |
| `CLAUDE.md`: lỗi lặp thì ghi một dòng | R5: một dòng, 2 lần chạy đều hết sai | **Đúng** ở lỗi này. Bước "vẫn sai thì thành hook" không xảy ra |
| Hook cho thứ phải luôn đúng | R4: ba lần chặn, hook nhanh nhất 0,1 ms, chậm nhất 138 ms | **Đúng.** `check-js` chạy **sau** khi ghi: file hỏng đã nằm trên đĩa, hook chỉ báo |
| `/init` làm điểm xuất phát | R5a: kiến trúc tốt, luật của người không có, tự bịa lỗi | **Đúng là điểm xuất phát**, không hơn. Đừng chép nguyên mục "Things Claude gets wrong" của nó |
| Verifier chỉ đọc và chạy, báo "đã chạy gì, thấy gì" | R3b: báo trung thực, nói rõ không chạy được gì | **Đúng, kèm giá:** Bash + Read không đủ để dựng giả lập trang; R3d (có Write) làm được trong một lượt |
| Thử skill kích hoạt với nhiều cách hỏi | R6: 0/5, hai lần | **Đúng là phải thử**: không thử thì không biết skill policy gần như không tự kích hoạt ở bước Build |
| Việc độc lập chạy song song trong worktree | R7a hỏi trước, R7b chạy, gộp không xung đột | **Chạy được.** Phần đáng giá là câu hỏi **trước** khi chạy: nó loại C và sửa lại mô tả lỗi của B |
| Phân hạng thay đổi | R8: 4/4 | **Đúng** ở bốn câu rõ ràng. Chưa thử ca lưng chừng |
| Cổng cuối là người | Commit A/B, merge, bảng kiểm tay do người; commit B đi trước kiểm tay và ghi là lệch | **Đúng.** Demo không có người cầm ba thiết bị, nên tính năng **chưa nghiệm thu** |

## Giới hạn

- Người trả lời và người review là **nhân vật giả lập**, mỗi người một phiên Claude chỉ biết hồ sơ của mình. Một lần (R3c Linh, lượt
  đầu) prompt của người chạy demo **gán nhầm** một ghi chú kỹ thuật cho Khoa; lượt đó đã xoá và chạy lại với ghi chú đúng người nói.
- Phần lớn kịch bản chạy **một lần**; R5 và R6 chạy hai lần. Đây là ví dụ thật, không phải thống kê.
- Bảng kiểm tay T0–T13 **chưa người nào chạy**. R3e là máy chạy một phần T0 và T9 trên Chromium headless, không thay ô nào trong bảng;
  Safari iOS, Chrome Android, bàn phím, trình đọc màn hình chưa thử.
- R3f, verifier và Claude viết code cùng họ model. Các chỗ R3f nói (25/26, năm câu từ chối) người chạy demo đã đối chiếu với file.
- Phiên thử của R6 chạy trên máy có skill riêng của người chạy demo; ở máy sạch kết quả có thể khác.
- Trong `runs/` đã che đường dẫn máy (`<repo>`, `<home>`, `<thư-mục-tạm>`), email (`<email>`) và tên người dùng trong kết quả `ls -l`
  (`<user>`, sửa sau ở commit `c094063` cho B0f, R0, R1). Ngoài mấy chỗ đó, transcript giữ nguyên văn.
- Không chạy: auto mode (tài liệu nói tới, demo dùng `acceptEdits`), GitHub Actions, review tự động trên pull request, nhiều người thật.

## Việc còn mở

- Bảng kiểm tay T0–T13 trên ba trình duyệt: để trống, chuyển sang các tập sau nếu có liên quan.
- Spec hạn chót vẫn `draft`, phải đi lại bước 0 trước khi có plan; R7a đã chỉ ra nó đụng `backup.js`.
