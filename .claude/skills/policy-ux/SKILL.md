---
name: policy-ux
description: UX standard of the todo app team (version 2). Rules for feedback on failures, confirmations, screen states, wording and accessibility. Load it whenever you write or review a spec, design or UI code for the app.
version: 2
owner: Linh (UX owner, simulated) · backup: Thảo (product owner, simulated)
---

# UX standard · v2

Sample standard for the demo. Each rule has an ID; cite it as `policy-ux@2#U<n>`.

- **U1.** Never lose the user's data silently. Any failed save is shown on the same screen, in plain words, with what the user can do
  next.
- **U2.** No confirmation dialogs for actions on a single item: they happen at once and offer **Undo** for 10 seconds instead.
  Actions that overwrite or delete more than one item follow `policy-security#S2` (confirm first). *(Changed in v2, agreed by the UX
  and security owners, 2026-10-20.)*
- **U3.** Every list or screen defines its empty, loading and error states.
- **U4.** UI text is Vietnamese, short, and free of technical words (no "localStorage", "JSON", "console").
- **U5.** Every control works with the keyboard and has an accessible label.
