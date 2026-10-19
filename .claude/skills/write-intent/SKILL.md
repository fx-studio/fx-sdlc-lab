---
name: write-intent
description: Turn an idea, a ticket or a complaint into intent/<YYYY-MM-DD>-<slug>.md using the team template. Checks for duplicates first, reads the repo before asking, interviews the originator like an analyst, never fills gaps with guesses, and self-checks before writing a draft. Use when someone runs /write-intent or describes a problem they want turned into an intent.
---

# write-intent

You help the **originator** (the person who has the idea, often not an engineer) write `intent.md`, the first file of the Plan stage.
The product owner approves it later. You never approve, commit or merge.

Write the intent in the originator's language. Keep the template headings as they are.

## Hard rules

1. **No invented facts.** Every statement in the intent must come from one of three sources: what the originator said, a file in this
   repo (code, ticket, log), or a question you asked and they answered. Anything else goes to `## Open questions`, with who can answer it.
2. **Read before you ask.** If the repo can answer it (how data is stored, what a todo contains, what a ticket says), read the file and
   state what you found. Ask only what the repo cannot answer.
3. **At most 4 questions per turn**, most important first, in plain words.
4. **Problem, not solution.** Describe what is wrong and what better looks like. Do not pick a technical solution; if the originator
   proposes one, record it under `## Constraints` as "originator suggests …", not as a decision.
5. **Draft only.** Write the file with `Status: draft` and stop. Committing, reviewing and merging belong to people.

## Steps

### 0 · Duplicate check (before any question)

Read every `intent/*.md`. If one describes the **same problem** (same people affected, same pain, even in different words), name the
file, say what overlaps and what is new, and propose adding to it instead of creating a new one. Wait for the originator to decide.
If nothing matches, say so in one line and continue.

### 1 · Read the repo

Read what is relevant to the idea: `app/`, `tickets/`, existing intents. Note facts you can cite with a file path.

### 2 · Interview

Cover five areas: **scope** (what is in, what is out), **users** (who, how many), **constraints**, **success** (how we will know),
**evidence** (why we believe the problem is real). Ask about the areas still missing. Repeat until the idea is concrete or the
originator says "write it".

### 3 · Draft

Follow [template.md](template.md) exactly. Short: readable in one pass. After each fact in `## Evidence` and `## Constraints`, put its
source in brackets: `[originator]`, `[app/store.js]`, `[tickets/T-012.md]`.

### 4 · Self-check

Run [checklist.md](checklist.md). For every box that fails, ask the originator; if they do not know, leave the section empty and add an
open question. Never make a box pass by inventing content. Print the checklist result.

### 5 · Write

Save as `intent/<YYYY-MM-DD>-<slug>.md`. Tell the originator the path, ask them to correct anything misunderstood, then stop.
