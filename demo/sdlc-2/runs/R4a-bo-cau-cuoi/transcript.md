# R4a-bo-cau-cuoi

Chạy 2026-10-20 16:56 ở `sdlc2-baseline-R4a` (thư mục riêng của lượt này). Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team.

Attached: intent/2026-10-19-khach-khong-mat-viec.md

## Tool call (8)

1. Bash · command=find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -100 && cat intent/2026-10-19-khach-khong-mat-viec.md
2. Bash · command=for f in app/store.js app/app.js app/index.html app/style.css .claude/skills/*/SKILL.md tickets/T-012-due-dates.md intent/2026-10-19-khach-doanh-nghiep-sao-luu.md intent/2026-10-19-han-chot-cho-viec.md; do echo "=== $f"; cat -n "$f"; done
3. Bash · command=cat -n app/store.js app/app.js app/index.html app/style.css
4. Bash · command=cat .claude/skills/policy-privacy/SKILL.md .claude/skills/policy-security/SKILL.md .claude/skills/policy-ux/SKILL.md tickets/T-012-due-dates.md intent/2026-10-19-khach-doanh-nghiep-sao-luu.md intent/2026-10-19-han-chot-cho-viec.md
5. Skill · skill=policy-privacy
6. Skill · skill=policy-security
7. Skill · skill=policy-ux
8. Write · file_path=<thư-mục-tạm>/sdlc2-baseline-R4a/spec.md

## Claude · 204 s

I've written the spec to `spec.md`. It's ready to hand to engineering, but five decisions from named owners are still open (listed in §2 of the spec).

**What gets built** (fits the PO's budget of one developer for two weeks; there's a day-by-day plan in §12):
- **Back up to a file:** a plain, readable file holding only the user's tasks, created on the device with nothing sent anywhere.
- **Restore from a file:** the file is checked fully before anything changes. Restoring only adds tasks and never changes or removes existing ones, and there's a 10-second Undo.
- **Failed saves are shown:** if storage is full or blocked, a message appears on the same screen with a button to back up to a file right away, so nothing is lost.
- **Two smaller items:** text in the app saying where the list is kept, and an empty-list hint ("Mới đổi máy? Nhập từ file…"). A reminder when it's been a while since the last backup is proposed but can be cut.

**Problems I found that you should know about:**
1. **Two of your policies contradict each other.** The security policy requires a confirmation before overwriting several items; the UX standard bans confirmation dialogs and wants Undo instead. A "replace my list with this file" restore can't meet both. The spec avoids the clash by making restore add-only, but Khoa and Linh need to agree to that (D-1, D-2).
2. **One success criterion can't be met.** "Add a task on one device, the other sees it" is sync, which the PO put out of scope. I've asked the PO to drop or move it (D-5).
3. **The current code can wipe data silently.** If the saved list can't be read, `store.load()` returns an empty list and the next save overwrites the old data. Also, when browser storage is blocked, the app quietly works in memory only and loses everything on reload. Both are fixed in the spec (§3, §6.2).
4. **Backups only help people who make them.** Users who never back up will keep losing their lists, which puts the target of under 5 complaint emails per 2 weeks at risk. That's why I proposed the reminder (PO decides, D-4). I also suggest Lan note in each new complaint whether the customer had a backup.
5. **Other points:**
   - The backup file includes a format version and an export date; Mai needs to confirm that's allowed under the privacy policy (D-3).
   - Lists over about 8,000 tasks would exceed the 1 MB limit on backup files, so the app warns when a backup is too big to restore.
   - Deleting a single task already has no Undo, which breaks the UX standard. It's logged as a follow-up, not in this scope.

**Brand guidelines:** the repo has none. I applied the privacy, security and UX policies (each rule is cited by ID in the spec) and reused the app's current look.
