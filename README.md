# fx-sdlc-lab

![fx-sdlc-lab: AI-Native SDLC, workspace demo của Fx Studio](docs/cover.png)

**AI-Native SDLC · workspace demo của Fx Studio.**

Workspace đi kèm loạt video **AI-Native SDLC** của [Fx Studio](https://fxstudio.dev/): đọc *The AI-native SDLC playbook*
(Anthropic, 21/8/2026) bằng lời của mình, rồi **dựng thật** từng bước trên một sản phẩm nhỏ để xem câu nào đứng được, câu nào cần sửa.

Sản phẩm là một app todo-list ở [`app/`](app/): HTML/JS thuần, dữ liệu nằm trong `localStorage` của trình duyệt, không server, không tài
khoản. Mỗi tập của loạt thêm vào repo những thứ một bước SDLC cần, nên repo lớn dần theo loạt.

**Tác giả & bản quyền:** thuộc về [Fx Studio](https://fxstudio.dev/). Dùng theo giấy phép đính kèm.

## Đã có

| Tập | Bước | Thêm gì | Bằng chứng | Blog |
|---|---|---|---|---|
| SDLC-0 | Tổng quan: code nhanh rồi, sao team vẫn chậm? | `docs/`: ghi chép đọc playbook theo sáu bước, kèm chỗ còn hở và cách vá ban đầu | không có demo (tập bản đồ) | [Code nhanh rồi, sao team vẫn chậm?](https://fxstudio.dev/ai-native-sdlc-code-nhanh-team-van-cham/) |
| SDLC-1 | Plan: ý tưởng thành `intent.md` | skill `write-intent`, subagent `intent-reviewer`, hook `no-self-approve`, thư mục `intent/` | [demo/sdlc-1/](demo/sdlc-1/README.md) | [Ý tưởng thành intent.md](https://fxstudio.dev/ai-native-sdlc-plan-y-tuong-thanh-intent/) |
| SDLC-2 | Design: `intent.md` thành `spec.md` | skill `write-spec`, ba skill `policy-*` có phiên bản, subagent `spec-reviewer`, spec job (git `post-commit`), hook `no-self-approve` bản 2, thư mục `spec/` | [demo/sdlc-2/](demo/sdlc-2/README.md) | [intent.md thành spec.md](https://fxstudio.dev/ai-native-sdlc-design-intent-thanh-spec/) |
| SDLC-3 | Build: plan trước, code sau | `CLAUDE.md` mục Build (bảng phân hạng, plan bốn mục, Things Claude gets wrong), thư mục `plan/`, ba hook build (`protect-paths`, `no-secrets`, `check-js`), subagent `verifier`, git `pre-commit` đòi plan đi cùng code, bộ thử kích hoạt skill; **tính năng sao lưu / nhập lại** trong `app/` và bộ test đầu tiên (`tests/`, 42 test) | [demo/sdlc-3/](demo/sdlc-3/README.md) | chưa đăng |

Các bài của loạt trên blog: https://fxstudio.dev/tag/ai-native-sdlc/


## Mang về repo của bạn (bước Plan)

Cần Claude Code và `python3` (cho hook).

1. Chép `.claude/skills/write-intent/` vào `.claude/skills/` của repo bạn. Sửa `template.md` cho hợp với team (giữ nguyên các heading thì
   checklist vẫn chạy).
2. Chép `.claude/agents/intent-reviewer.md` vào `.claude/agents/` nếu muốn có người đọc thứ hai cho product owner.
3. Muốn chặn agent tự duyệt: chép `.claude/hooks/no-self-approve.py` và khối `hooks` trong `.claude/settings.json`. Hook chặn agent
   `git merge` / `rebase` / `push` và commit trên `main`. Nó chỉ chặn lệnh agent chạy qua Bash; ở team, thêm branch protection phía server.
4. Tạo thư mục `intent/` rồi gõ trong Claude Code:

```
/write-intent Dạo này khách cứ email than là mất hết việc trong app, nhất là sau khi đổi điện thoại.
```

Claude kiểm trùng với các intent đã có, đọc code trước, hỏi tối đa bốn câu mỗi lượt, rồi viết `intent/<ngày>-<slug>.md` ở trạng thái
`draft`, mỗi dòng bằng chứng ghi nguồn. Thứ chưa biết thành câu hỏi mở, không bị điền bừa. Ở SDLC-1, intent nằm trên một nhánh và **product owner duyệt
bằng cách merge**. Từ SDLC-2, repo này để mọi thứ ở `main`: **product owner duyệt bằng cách tự đổi `Status: draft` thành
`Status: accepted` rồi commit**. Hook bản 2 chặn agent làm việc đó. Team của bạn quen pull request thì giữ cách merge, cả hai đều được.

## Mang về repo của bạn (bước Design)

Cần Claude Code, `python3` (cho hook) và `bash` (cho spec job).

1. Viết policy của team thành skill theo khuôn `.claude/skills/policy-*/SKILL.md`: mỗi luật một mã, có `version` và `owner`. Ba policy
   trong repo là **mẫu**, đừng dùng nguyên. Bắt đầu từ policy hay bị nhắc nhất trong các lần review gần đây.
2. Chép `.claude/skills/write-spec/` và `.claude/agents/spec-reviewer.md`. Sửa `risk-list.md` cho hợp với team: demo cho thấy danh sách
   mẫu gắn nhãn rủi ro cao cho mọi spec của một app nhỏ.
3. Có intent đã `Status: accepted`, gõ trong Claude Code:

```
/write-spec intent/2026-10-19-khach-khong-mat-viec.md
```

Claude đọc intent, code và mọi policy, viết `spec/<cùng tên>.md` ở trạng thái `draft`: dòng đầu ghi phiên bản từng policy, mục
**Assumptions** gồm các câu có/không có tên người trả lời, chỗ hai policy mâu thuẫn thành một mục Concerns có phương án nhưng không chọn.
4. Muốn chấp nhận intent là tự có spec nháp: chép `scripts/` rồi chạy `scripts/install-hooks.sh` (git `post-commit`, chỉ ở máy bạn).
5. Muốn chặn agent tự duyệt: hook `no-self-approve.py` bản 2 chặn cả việc ghi `Status: accepted` vào `intent/`, `spec/`.

## Mang về repo của bạn (bước Build)

Cần Claude Code, `python3` (cho hook), Node (cho `node --test` của app mẫu; repo của bạn dùng test runner của nó).

1. Thêm vào `CLAUDE.md` của bạn ba thứ, theo mục **Build** của `CLAUDE.md` repo này: lệnh chạy app / test / lint; **bảng phân hạng
   thay đổi** (hạng nào cần plan mode, hạng nào cần `plan/<tên>.md`, hạng nào cần tech lead duyệt trước); mục **Things Claude gets
   wrong**, chỉ thêm một dòng khi **cùng một lỗi** đã xảy ra hai lần. Có thể bắt đầu bằng `/init`, nhưng soát lại: demo thấy `/init`
   viết phần kiến trúc tốt, bỏ luật của người, và tự bịa lỗi chưa xảy ra.
2. Bắt đầu mỗi thay đổi bằng plan mode (`Shift+Tab` hai lần, hoặc `claude --permission-mode plan`). Trước khi duyệt, hỏi plan ít nhất
   câu này: *"Test nào fail nếu bước rủi ro nhất làm sai?"*. Đưa plan cho người **không xem hội thoại** đọc; người đó làm theo được thì
   lưu vào `plan/<tên>.md` ở `Status: draft`, rồi một người đổi `accepted` và commit.
3. Chép `.claude/hooks/protect-paths.py`, `no-secrets.py`, `check-js.py` (sửa danh sách đường dẫn và lệnh kiểm cho hợp repo bạn) và khối
   `hooks` trong `.claude/settings.json`. Hook ghi thời gian vào `.hook-timing.log` (đã ignore) để bạn biết nó có làm chậm không.
4. Chép `.claude/agents/verifier.md`. Nó chỉ có Bash + Read nên không tự dựng được script giả lập; nếu repo bạn cần, cho nó thêm Write
   vào một thư mục tạm, hoặc viết sẵn test để nó chạy.
5. Muốn commit code phải kèm plan: chép `scripts/pre-commit` rồi chạy `scripts/install-hooks.sh`. Thay đổi nhỏ thì
   `PLAN_SKIP="<lý do>" git commit …`.
6. Viết `triggers.md` cho từng skill policy rồi chạy `scripts/skill-triggers.sh <skill>`. Demo ra 0/5 cho `policy-security`: đừng tin
   skill tự kích hoạt ở bước Build, hãy gọi tên nó trong prompt hoặc trong plan.
7. Chạy song song: trước khi mở hai worktree, hỏi một phiên plan mode *"hai việc này đụng chung file nào?"*. Mỗi worktree một nhánh tạm,
   người commit và gộp về `main`, rồi xoá nhánh.

## Bố cục

```
app/                    sản phẩm: app todo
intent/                 intent.md, mọi thứ ở main; Status: draft hoặc accepted (người đổi, người commit)
spec/                   spec.md của bước Design, cùng tên với intent
plan/                   plan.md của bước Build, cùng tên; người đổi Status: accepted
tests/                  node --test, không package
scripts/                spec job (on-intent-accepted.sh), pre-commit, install-hooks.sh, skill-triggers.sh
tickets/                ticket mẫu
.claude/
  skills/write-intent/  SKILL.md · template.md · checklist.md
  skills/write-spec/    SKILL.md · template.md · risk-list.md · checklist.md
  skills/policy-*/      policy mẫu của team (privacy, security, ux), có phiên bản
  agents/               intent-reviewer.md · spec-reviewer.md · verifier.md (chỉ đọc, chỉ báo)
  hooks/                no-self-approve.py · protect-paths.py · no-secrets.py · check-js.py
  settings.json         gắn hook
demo/sdlc-<n>/          bằng chứng của từng tập: nhân vật giả lập, script chạy lại, transcript nguyên văn, kết luận
docs/                   ghi chép của tác giả về playbook, theo từng bước
```

Thành phần cho agent (`.claude/`, template) viết tiếng Anh. Ghi chép và kết luận viết tiếng Việt.

## Lưu ý

- Mọi người, ticket và con số trong `tickets/` và `demo/` là **dữ liệu mẫu**, không phải người dùng thật.
- Mỗi kịch bản demo chạy **một lần**. Đó là ví dụ thật, không phải thống kê.
- Playbook gốc: https://claude.com/resources/articles/the-ai-native-sdlc-playbook. Chỗ nào là nhận xét của tác giả repo, tài liệu ghi rõ.
