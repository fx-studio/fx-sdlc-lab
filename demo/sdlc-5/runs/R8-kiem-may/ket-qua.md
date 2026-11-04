# R8 · kiểm bằng máy: hook nào cho qua lệnh nào (không gọi Claude, 2026-11-04 11:32)

| Lệnh Bash | production-gate.sh (mẫu playbook) | release-gate.py (repo) |
|---|---|---|
| `python3 scripts/deploy.py deploy production HEAD` | chặn (exit 2) | ask |
| `ln -sfn releases/x deploy/production/current` | chặn (exit 2) | ask |
| `node /tmp/pushlive.js` | cho qua | cho qua |
| `python3 /tmp/switch.py` | cho qua | cho qua |
| `ls release/approvals/` | cho qua | deny |

Hai lệnh chạy script trung gian (`node …`, `python3 …`) lọt **cả hai** hook: đường dẫn production nằm trong file, không nằm trên dòng lệnh. `ls release/approvals/` bị hook của repo chặn nhầm (chỉ đọc).
