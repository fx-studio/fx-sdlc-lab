# PR 1 · Nút Huỷ hiện viền khi hộp xác nhận mở

Branch: `pr/1-huy-hien-vien` · Base: `main` (04ee584)

Spec: (none) · Plan: (none)

## What changes

Size: Small (one CSS rule + one test). Commit `4ec1f73`.

- `app/style.css`: new rule `dialog button:focus { outline: 2px solid #1a5fd0; outline-offset: 2px; }`, the same ring
  `#import-label:focus-within` already uses. Both dialog buttons ("Thay", "Huỷ") now show a ring whenever they have focus.
- Cause (probable, not confirmed in a browser): the default ring is drawn only on `:focus-visible`. The dialog opens after the
  OS file picker closes, and Firefox does not count the `autofocus` focus at that moment as keyboard focus, so "Huỷ" has focus
  but no ring. A rule on plain `:focus` does not depend on that heuristic. Side effect: a mouse click on a dialog button also
  shows the ring (the dialog closes right after, so it is barely visible).
- `tests/static.test.js`: new test "confirm dialog buttons show a focus ring on any focus, not only :focus-visible (U5, PR 1)".
  It pins the CSS rule; it cannot reproduce Firefox's focus heuristic. Fails before the fix (no matching rule in
  `style.css`), passes after.
- No change to `index.html`, JS, or behaviour; test count 44 → 45.

**Still needs a person:** repeat T12 by keyboard in Firefox on macOS (`demo/sdlc-4/kiem-tay.md`) and confirm the ring is
visible on "Huỷ" when the dialog opens. Not tried in a browser here.

## How it was checked

New test before the fix (`node --test tests/static.test.js`):

```
✖ confirm dialog buttons show a focus ring on any focus, not only :focus-visible (U5, PR 1)
ℹ tests 6
ℹ pass 5
ℹ fail 1
  AssertionError [ERR_ASSERTION]: The input did not match the regular expression /dialog button:focus\s*\{[^}]*outline:\s*2px solid/.
```

After the fix, `bash scripts/check.sh`:

```
== test: node --test
ℹ tests 45
ℹ pass 45
ℹ fail 0
== lint: node --check app/*.js tests/*.js
== check: OK
```

<!-- pr.py -->
## Size and risk (computed by scripts/pr.py)

9 lines in 2 files · risk **low** → 1 code owner
