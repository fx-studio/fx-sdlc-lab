# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

fx-sdlc-lab is the demo workspace for Fx Studio's "AI-Native SDLC" series. The product is a small todo app in `app/`; everything
else is the SDLC tooling built around it, one stage per episode. Agent-facing files (`.claude/`, templates, this file) are in English;
notes, plans and conclusions are in Vietnamese. People, tickets and numbers in `tickets/` and `demo/` are sample data.

## Commands

No build step, no npm packages, no dependencies. Needs Node (built-in test runner) and `python3` (hooks).

```
node --test                                   # whole suite (tests/*.test.js)
node --test tests/store.test.js               # one file
node --test --test-name-pattern "read error"  # tests whose name matches
node --check app/backup.js                    # syntax check (the check-js hook runs this after every edit)
scripts/install-hooks.sh                      # local git hooks: post-commit spec job, pre-commit plan sync
scripts/skill-triggers.sh <skill> [model]     # does .claude/skills/<skill>/triggers.md load the skill?
```

Run the app by opening `app/index.html` in a browser. Anything needing a real browser (file picker, download, `<dialog>`, layout) is
checked by hand and recorded in the plan's manual-check table.

## App architecture

Plain scripts sharing globals, loaded in this order (pinned by `tests/static.test.js`): `store.js` → `backup.js` → `app.js`.
- `store.js` is the **only** file that touches `localStorage` (key `todo.v1`, an array of `{ id, title, done, createdAt }`).
  `load()` tells "nothing saved" from "unreadable"; on a read error `store.readError` is set and `save()` returns `'skipped'` so bad
  data is never overwritten; only `replace()` (import) may write then. `save`/`replace` return `'saved' | 'failed' | 'skipped'`.
- `backup.js` is DOM-free logic (backup file text, import validation, confirm text, `MESSAGES`, `persist`, `importBackup`). It takes
  `store` as a parameter and must not contain the word `localStorage`, not even in a comment (static test).
- `app.js` only wires the DOM and has no exports; `tests/app.test.js` runs it unchanged in a `vm` context with a fake page.
- `store.js` and `backup.js` end with `if (typeof module !== 'undefined') module.exports = ...` so Node tests can `require` them.
- `index.html` loads nothing from outside, and its visible text has no technical words (static tests).

## SDLC workflow

Every change flows `intent/<date>-<slug>.md` → `spec/<same name>.md` → `plan/<same name>.md` → code, all on `main`.
- Skills `/write-intent` and `/write-spec` write drafts; `intent-reviewer`, `spec-reviewer` and `verifier` agents only report.
  Specs must follow the `policy-*` skills and record their versions; codes such as `AC3`, `P2`, `S1`, `U5`, `Q4`, `M8` in code
  comments and tests point back to the spec, the policies and the plan.
- **Approval is a person's act**: a person changes `Status: draft` to `Status: accepted` and commits. Never write that line yourself.
- With the git hooks installed, accepting an intent makes `scripts/on-intent-accepted.sh` run `/write-spec` headless and commit a
  draft spec as `spec-job`.

Guardrails (`.claude/settings.json`), all deny rather than ask:
- `no-self-approve`: no `git merge`/`rebase`/`push`, no `git commit` on `main`, no `Status: accepted` in `intent/`, `spec/`, `plan/`.
- `protect-paths`: `docs/` and `tickets/` are read-only; so is any accepted file in `intent/`, `spec/`, `plan/`. If an accepted plan
  needs to change, describe the change and stop.
- `no-secrets`: blocks text that looks like a key or credential. `check-js`: `node --check` on each edited `.js` file.
- git `pre-commit`: a commit touching `app/` must also touch `plan/`, unless `PLAN_SKIP="<reason>"` is set (tiny changes).

## Change size

Propose a size before starting:

| Size | Example | Plan |
|---|---|---|
| Tiny | wording, a colour, a constant | no plan mode (`PLAN_SKIP` at commit) |
| Small | a well-bounded bug in one file | plan mode, no `plan/` file |
| Medium | a small feature over a few files | plan mode, commit `plan/<name>.md` |
| Large | several modules, architecture change | `plan/<name>.md` approved by the tech lead before any code |

A plan covers files that change, order of work, risks and proof (tests). When the code departs from the plan, update the plan in the
same commit.

## Things Claude gets wrong

- User-facing Vietnamese text comes verbatim from the spec or plan (`M<n>` wording). Do not invent or rephrase it; new wording needs
  the UX owner.
- `demo/sdlc-*/runs/` are recorded evidence from one-off runs: do not edit them. `demo/*/run.py` writes them.
