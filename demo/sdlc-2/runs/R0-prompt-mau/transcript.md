# R0-prompt-mau

Chạy 2026-10-20 17:00 ở `sdlc2-baseline-R0` (thư mục riêng của lượt này). Nguyên văn, không sửa. Luồng thô: `stream.jsonl`.

## Prompt

Read the attached intent.md and produce a requirements and design spec for integrating it into our existing codebase. Apply the skills available to you so the plan conforms to our brand guidelines, security policies and UX standards. Document the spec fully as spec.md, ready to hand to the engineering team. Describe clearly any areas of concern, especially where you cannot satisfy contradicting policies.

Attached: intent/2026-10-19-khach-khong-mat-viec.md

## Tool call (9)

1. Bash · command=find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | head -100 && cat intent/2026-10-19-khach-khong-mat-viec.md
2. Bash · command=for f in app/index.html app/store.js app/app.js app/style.css tickets/T-012-due-dates.md intent/2026-10-19-han-chot-cho-viec.md intent/2026-10-19-khach-doanh-nghiep-sao-luu.md; do echo "=== $f"; cat -n "$f"; done
3. Skill · skill=policy-privacy
4. Skill · skill=policy-security
5. Skill · skill=policy-ux
6. Bash · command=cat -n app/index.html app/store.js app/app.js app/style.css && echo ==== && cat tickets/T-012-due-dates.md intent/2026-10-19-han-chot-cho-viec.md intent/2026-10-19-khach-doanh-nghiep-sao-luu.md
7. Bash · command=cat tickets/T-012-due-dates.md; echo; echo -----; cat intent/2026-10-19-han-chot-cho-viec.md; echo; echo -----; cat intent/2026-10-19-khach-doanh-nghiep-sao-luu.md; ls -la . .claude .claude/skills
8. Write · file_path=<thư-mục-tạm>/sdlc2-baseline-R0/spec.md
9. Edit · file_path=<thư-mục-tạm>/sdlc2-baseline-R0/spec.md

## Claude · 225 s

I've written the spec to `spec.md` in the project root. It applies the three policies in the repo: privacy, security and UX. It is ready for engineering except for one blocking policy decision.

**What it specifies.** This follows the scope the product owner set in the intent.
- **Export:** the user downloads the whole list as a plain, readable text file. It contains only the four task fields and a format marker, nothing about the device.
- **Import:** the file is checked strictly before anything is loaded: 1 MB size limit, no unknown fields, and one bad entry rejects the whole file. Imported tasks are added next to the existing ones, never replacing them, and the user gets 10 seconds to undo.
- **Save failures:** every failed save shows a banner that stays until the next save works, with "download backup" and "try again" buttons. The download works even when browser storage is full.
- **Also covered:** an in-app note on where the data is kept, a backup reminder worked out on the device, empty/loading/error screens, accessibility, acceptance tests, and a 10-day plan.

**Problems I found in the current code:**
- If the saved list can't be read at startup, the app starts with an empty list and overwrites the old data on the next save, with no notice. The spec now keeps the old data and shows an error screen.
- Deleting a task has no Undo, which breaks the UX standard. I added Undo as a recommended item for the product owner to confirm.
- Two open tabs silently overwrite each other's saves. This is outside the intent; I've noted it with a rough half-day fix.

**Areas of concern (§9 of the spec):**
1. **Security and UX policies contradict each other (blocking).** Security rule S2 says to ask for confirmation before overwriting or deleting more than one item. UX rule U2 says never use confirmation dialogs and offer Undo instead. No design can satisfy both.
   - I worked around it for import: tasks are only added, so nothing is overwritten or deleted. The cost is that deletes and "done" marks can't be moved between devices by file.
   - One case can't be worked around: starting a new list when the old data is unreadable and couldn't be set aside. Undo isn't possible there.
   - The security and UX owners need to agree which rule wins.
2. **The release doesn't meet three of the intent's five success criteria.** Two-device sync is out of scope. Recovery after a new phone or cleared browser data only works if the user made a backup first. And the goal of fewer than 5 complaint emails can't be tracked in the app, because the privacy policy forbids analytics. The product owner should confirm these are deferred.
3. **The 1 MB import limit can lock users out of their own backup.** Browser storage holds about 5 MB, so a very large list can be exported but not imported again. The security owner should decide whether to keep the limit.
4. **Smaller readings that need an owner to confirm:**
   - whether the format marker counts as "only user data" under the privacy rule;
   - whether the `.json` file name breaks the "no technical words" rule;
   - whether the browser's "leave page?" prompt counts as a confirmation dialog when there are unsaved changes.
5. **No brand guidelines exist** in the repo or the available skills, so I couldn't check brand compliance. The new UI follows the current `style.css`. Someone needs to supply the guidelines or confirm that style is the brand.

The intent's own open questions are still open: how the 23 emails split between a new phone and cleared browser data, and copying those emails into `tickets/`.
