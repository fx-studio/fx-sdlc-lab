# CLAUDE.md — fx-sdlc-lab (demo workspace)

Demo workspace for the Fx Studio video series **"AI-Native SDLC"**. The product is a tiny todo app in `app/`. Each episode adds the
pieces one SDLC stage needs, so the repo grows stage by stage.

Humans read and write Vietnamese here; agent-facing files (`.claude/`, templates) are in English.

## Layout

| Path | What |
|---|---|
| `app/` | The product: static HTML/JS todo app, data in `localStorage` only (no server, no account) |
| `tickets/` | Incoming tickets (sample data) |
| `intent/` | Plan stage output: one `intent.md` per change, `<YYYY-MM-DD>-<slug>.md` |
| `spec/` | Design stage output: one spec per accepted intent, same file name as the intent |
| `plan/` | Build stage output: one plan per accepted spec, same file name |
| `tests/` | `node --test` tests (no packages) |
| `.claude/skills/write-intent/` | Skill: template + checklist + rules for turning an idea into an intent |
| `.claude/agents/intent-reviewer.md` | Read-only subagent that prepares an intent for the product owner |
| `.claude/skills/write-spec/` | Skill: intent → spec, template + risk list + checklist |
| `.claude/skills/policy-*/` | The team's policies (privacy, security, UX) as versioned skills (sample data) |
| `.claude/agents/spec-reviewer.md` | Read-only subagent that prepares a spec for the product owner and tech lead |
| `.claude/hooks/no-self-approve.py` | Hook: the agent cannot merge, rebase, push, commit on `main`, or set `Status: accepted` |
| `.claude/hooks/protect-paths.py` · `no-secrets.py` · `check-js.py` | Build hooks: read-only paths, no credentials, `node --check` after each edit |
| `.claude/agents/verifier.md` | Subagent: runs tests, checks the change against its plan, reports only |
| `scripts/` | Spec job: `install-hooks.sh` adds a git post-commit hook; accepting an intent runs `/write-spec` headless |
| `demo/sdlc-<n>/` | Evidence for each episode: personas, run script, raw transcripts, findings (Vietnamese) |
| `docs/` | The channel owner's own notes on the playbook. **Do not edit.** |

## Rules

- **Everything lives on `main`.** Intents and specs start as `Status: draft`. **A person approves by changing it to
  `Status: accepted` and committing.** The agent writes drafts and stops: it never commits, merges, or sets `accepted`. The hook enforces it.
  (Until SDLC-1, approval was a merge from an `intent/<slug>` branch; those branches are merged as drafts.)
- **Demos record only what actually ran.** Transcripts are saved verbatim, never edited.
- All people, tickets and numbers in `tickets/` and `demo/` are **sample data**, not real users. No code, tickets or names from real
  client projects.
- Never read or print `.env`, `.secrets/`, tokens.
- Never push, create releases, or change remotes. Publishing is the repo owner's call.

## Build

- **Run the app:** `python3 -m http.server -d app 8000`, open http://localhost:8000. **Tests:** `node --test` (Node ≥ 18, no
  packages; tests live in `tests/`). **Lint:** `node --check <file>`, run by a hook after every edit.
- Plain HTML/JS, no build step, no npm dependency (`policy-security#S4`). User text via `textContent` (`#S3`). UI text Vietnamese.
- **App architecture** (taken from a `/init` run, `demo/sdlc-3/runs/R5a-init/`, checked by a person): plain scripts sharing globals,
  loaded `store.js` → `backup.js` → `app.js` (pinned by `tests/static.test.js`). `store.js` is the only file that touches
  `localStorage` (key `todo.v1`); after a read error `save()` returns `'skipped'` and only `replace()` (import) may write. `backup.js`
  is DOM-free logic and takes `store` as a parameter. `app.js` only wires the DOM; `tests/app.test.js` runs it unchanged in a `vm`.
- **Size the change first** and say which size you picked:

  | Size | Example | Plan |
  |---|---|---|
  | Trivial | wording, a colour, a constant | no plan mode |
  | Small | one well-located bug, one file | plan mode, plan not committed |
  | Medium | a small feature, a few files | plan mode, `plan/<name>.md` committed |
  | Large | many modules, architecture | `plan/<name>.md` + tech lead approves before code |

- A plan has four sections: **Files that change · Order of work · Risks · Proof** (which test proves each step). Write it as
  `Status: draft`; a person accepts it. Implement only an accepted plan. If the code has to depart from it, stop and say how: a person
  updates the plan in the same commit (a git pre-commit hook checks this).

## Things Claude gets wrong

One line per mistake, with the month it was added. Added after the **same** mistake happens twice. If it still happens after the line
is here, the line becomes a hook and is removed from this list.

- 2026-10: Building throwaway scripts in Bash (heredocs, `sed -i`, `for` loops, `&&` chains, `echo $?`). Those need approval and get
  refused in a headless run (R0, R3, R3b, R3d: 20 refusals). Write the script with the Write tool, then run it with one plain
  `node <file>`. One command per Bash call.
