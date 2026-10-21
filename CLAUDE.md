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
| `.claude/skills/write-intent/` | Skill: template + checklist + rules for turning an idea into an intent |
| `.claude/agents/intent-reviewer.md` | Read-only subagent that prepares an intent for the product owner |
| `.claude/skills/write-spec/` | Skill: intent → spec, template + risk list + checklist |
| `.claude/skills/policy-*/` | The team's policies (privacy, security, UX) as versioned skills (sample data) |
| `.claude/agents/spec-reviewer.md` | Read-only subagent that prepares a spec for the product owner and tech lead |
| `.claude/hooks/no-self-approve.py` | Hook: the agent cannot merge, rebase, push, commit on `main`, or set `Status: accepted` |
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
