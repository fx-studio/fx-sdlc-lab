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
| `.claude/skills/write-intent/` | Skill: template + checklist + rules for turning an idea into an intent |
| `.claude/agents/intent-reviewer.md` | Read-only subagent that prepares an intent for the product owner |
| `.claude/hooks/no-self-approve.py` | Hook: the agent cannot merge, rebase, push, or commit on `main` |
| `demo/sdlc-<n>/` | Evidence for each episode: personas, run script, raw transcripts, findings (Vietnamese) |
| `docs/` | The channel owner's own notes on the playbook. **Do not edit.** |

## Rules

- **The product owner approves by merging into `main`.** Agents work on branches (`intent/<slug>`) and stop there. The hook enforces it.
- **Demos record only what actually ran.** Transcripts are saved verbatim, never edited.
- All people, tickets and numbers in `tickets/` and `demo/` are **sample data**, not real users. No code, tickets or names from real
  client projects.
- Never read or print `.env`, `.secrets/`, tokens.
- Never push, create releases, or change remotes. Publishing is the repo owner's call.
