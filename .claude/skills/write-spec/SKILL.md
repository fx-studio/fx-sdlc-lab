---
name: write-spec
description: Turn an accepted intent/<file>.md into spec/<same-name>.md, one requirements-and-design spec that follows the team's policy skills (policy-*). Records the policy versions it applied, lists every assumption as a yes/no question, flags concerns and policy conflicts without picking a side, labels risk, and writes a draft only. Use when someone runs /write-spec or asks for a spec from an intent.
---

# write-spec

You write the spec for the **Design** stage. A product owner reviews it later; you never approve, commit or set it to accepted.

Write the spec in the language of the intent. Keep the template headings as they are.

## Hard rules

1. **Accepted intents only.** If the intent's header does not say `Status: accepted`, stop and say so. Do not write anything.
2. **Every statement has a source.** After each statement in the body, put its source in brackets: `[intent]`, `[app/store.js]`,
   `[policy-ux@1#U2]`. A statement you cannot source is an **assumption**: move it to `## Assumptions`. Do not leave it in the body.
3. **Assumptions are yes/no questions** with the person who can answer: `- Users keep fewer than 500 todos, right? → tech lead`.
   The reviewer reads this section first.
4. **Never resolve a policy conflict yourself.** When two rules cannot both be satisfied, write a concern that quotes both rule IDs and
   names both owners. You may list options with their cost; you do not choose.
5. **Do not widen the scope.** Anything the intent marks out of scope stays out, even if it looks like the right solution.
6. **Draft only.** Write the file with `Status: draft` and stop. Committing and accepting belong to people.

## Steps

### 1 · Read

- The intent file, fully. Note its open questions and what the product owner already answered.
- Every policy skill: read `.claude/skills/policy-*/SKILL.md`, note each `version` and `owner`. These versions go on line 2 of the spec.
- The code the change touches (`app/`), so the spec fits the codebase as it is.
- [risk-list.md](risk-list.md).

### 2 · Apply the policies

For every rule in every policy, decide: applies / does not apply. Every rule that applies appears under `## Policy constraints` with
how the spec satisfies it, or under `## Concerns` if it cannot.

### 3 · Draft

Follow [template.md](template.md). Acceptance criteria must be checkable by a test or by a person following steps; no "fast", "easy",
"intuitive".

### 4 · Label risk

Apply [risk-list.md](risk-list.md). Write `Risk: high (<which line>)` or `Risk: normal`. High risk means a tech lead must review too.

### 5 · Self-check and write

Run [checklist.md](checklist.md), print the result, then save as `spec/<same file name as the intent>`. Tell the user the path and the
number of assumptions and concerns, then stop.
