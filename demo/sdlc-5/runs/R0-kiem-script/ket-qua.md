# R0 · thử script bước Deploy

Chạy 2026-11-04 09:34 trong bản clone tạm, không gọi Claude. **36/36 đạt.** Hook release-gate chậm nhất 36 ms (5 lần, gồm khởi động Python).

| Nhóm | Ca | Loại | Ra | Muốn | |
|---|---|---|---|---|---|
| production-gate.sh | deploy production, không biến | phải chặn | `exit2` | `exit2` | ✅ |
| production-gate.sh | deploy production, RELEASE_APPROVAL có trong môi trường phiên | phải qua | `allow` | `allow` | ✅ |
| production-gate.sh | agent gõ biến vào lệnh: RELEASE_APPROVAL=1 python3 … deploy production | phải chặn | `exit2` | `exit2` | ✅ |
| production-gate.sh | deploy staging | phải qua | `allow` | `allow` | ✅ |
| production-gate.sh | lệnh vô hại có cả hai chữ: grep deploy README | grep production | khác dạng: chặn nhầm (giới hạn của mẫu; lượt đầu mình ghi kỳ vọng sai là qua) | `exit2` | `exit2` | ✅ |
| production-gate.sh | đổi thẳng symlink: ln -sfn releases/x deploy/prod*/current | khác dạng: lọt (giới hạn của mẫu) | `allow` | `allow` | ✅ |
| release-gate.py | deploy production, chưa có duyệt trên main | phải hỏi | `ask` | `ask` | ✅ |
| release-gate.py | như trên, RELEASE_GATE=deny | phải chặn | `deny` | `deny` | ✅ |
| release-gate.py | agent gõ biến vào lệnh | phải hỏi | `ask` | `ask` | ✅ |
| release-gate.py | đổi thẳng symlink deploy/production/current | phải hỏi | `ask` | `ask` | ✅ |
| release-gate.py | Write vào release/approvals/ | phải chặn | `deny` | `deny` | ✅ |
| release-gate.py | Write vào deploy/production/ | phải chặn | `deny` | `deny` | ✅ |
| release-gate.py | deploy staging | phải qua | `allow` | `allow` | ✅ |
| release-gate.py | status | phải qua | `allow` | `allow` | ✅ |
| release-gate.py | Write vào app/ | phải qua | `allow` | `allow` | ✅ |
| release-gate.py | file duyệt có trên đĩa nhưng chưa commit | phải hỏi | `ask` | `ask` | ✅ |
| release-gate.py | người duyệt đúng bản này, commit trên main | phải qua | `allow` | `allow` | ✅ |
| release-gate.py | đã duyệt một bản, deploy một bản cũ hơn chưa duyệt | phải hỏi | `ask` | `ask` | ✅ |
| release-gate.py | lệnh dạng khác: deploy.py deploy prod (viết tắt) | khác dạng (phải hỏi) | `ask` | `ask` | ✅ |
| deploy.py | hai lần deploy staging → current = bản sau | phải qua | `2e7c076-20261104-093444-336488` | `2e7c076-20261104-093444-336488` | ✅ |
| rollback.py | rollback staging → về bản trước | phải qua | `b7d8f7e-20261104-093444-044633` | `b7d8f7e-20261104-093444-044633` | ✅ |
| rollback.py | rollback dev khi chưa có bản nào | khác dạng (báo, không hỏng) | `nothing to roll back to` | `nothing to roll back to` | ✅ |
| rollback-drill.py | tập 3 lần ở staging | phải qua | `0` | `0` | ✅ |
| rollback-drill.py | tập ở production | phải chặn | `1` | `1` | ✅ |
| deploy.py | người chạy (không FX_ACTOR) → actor person:… | phải qua | `person:nguoi-chay-demo` | `person:nguoi-chay-demo` | ✅ |
| deploy-mcp | tools/list có 4 công cụ | phải qua | `4` | `4` | ✅ |
| deploy-mcp | deploy production | phải chặn | `True` | `True` | ✅ |
| deploy-mcp | deploy dev | phải qua | `False` | `False` | ✅ |
| deploy-mcp | rollback production | phải chặn | `True` | `True` | ✅ |
| deploy-mcp | prepare_release (production, không chuyển) | phải qua | `False` | `False` | ✅ |
| deploy-mcp | actor của lần gọi qua MCP | phải qua | `agent:fx-sdlc-agent` | `agent:fx-sdlc-agent` | ✅ |
| deploy-mcp | production vẫn chưa có bản nào sau prepare_release | phải qua | `None` | `None` | ✅ |
| pr.py | PR chỉ sửa style.css → rủi ro low | phải qua | `low` | `low` | ✅ |
| pr.py | thêm store.js → rủi ro high | phải qua | `high` | `high` | ✅ |
| pr.py | > 400 dòng → cảnh báo | phải qua | `True` | `True` | ✅ |
| pr.py | 900 dòng ở demo/ không tính vào cỡ | khác dạng | `424` | `424` | ✅ |
