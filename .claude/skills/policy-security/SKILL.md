---
name: policy-security
description: Security policy of the todo app team (version 2). Rules for input handling, destructive operations, rendering user text and dependencies. Load it whenever you write or review a spec, design or code that reads files or input, deletes or overwrites data, renders user text, or adds a dependency.
version: 2
owner: Khoa (tech lead, also security owner, simulated) · backup: Mai (simulated)
---

# Security policy · v2

Sample policy for the demo. Each rule has an ID; cite it as `policy-security@2#S<n>`.

- **S1.** Treat every imported file as untrusted. Validate it against the expected schema, reject unknown fields, cap its size at
  1 MB, never evaluate its content. The expected schema is the one of the file's own `version`: a field that a later version
  allows is still unknown in an earlier one (v2, 2026-11-04: backup files gain `version: 2` with an optional `dueDate`).
- **S2.** Any operation that overwrites or deletes more than one item asks for an explicit confirmation **before** it runs, and the
  confirmation says what will be lost (for example "Thay 12 việc hiện có bằng 30 việc trong file?").
- **S3.** Render user-provided text with `textContent`, never `innerHTML`.
- **S4.** No new external dependency (CDN script, library, web service) without sign-off from the security owner.
