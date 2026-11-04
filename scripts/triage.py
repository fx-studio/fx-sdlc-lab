#!/usr/bin/env python3
"""Read-only pipeline step (playbook Stage 5, CI/CD step 1): Claude reads a failed build log and writes what broke.

    bash scripts/check.sh > build.log 2>&1 || python3 scripts/triage.py build.log [--out review/<n>/triage.md]

Claude gets the log and read-only tools (it may open the files the log names, and git log/diff). It changes nothing.
The note says: what failed, the most likely cause (file:line), the evidence from the log, a suggested fix, and how sure it is.
"""
import json, os, re, subprocess, sys
from pathlib import Path

READ_ONLY = "Read,Glob,Grep,Bash(git diff:*),Bash(git log:*),Bash(git show:*)"
PROMPT = """A build in this repo failed. The log is below. Find out why, without changing anything.

Write a short note for the pull request, in this shape (Markdown, English):

## Build failed: <one line>
- **Failed:** which check, which test(s)
- **Likely cause:** file:line and what is wrong there
- **Evidence:** the lines of the log (quote them) and what you read in the code
- **Suggested fix:** one or two sentences; say if the test or the code looks wrong
- **Confidence:** high / medium / low, and what would make you surer

Log:

```
{log}
```
"""


def main(a):
    if not a:
        print(__doc__)
        return 2
    log = Path(a[0]).read_text()[-20000:]
    out = Path(a[a.index("--out") + 1]) if "--out" in a else None
    env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
    env["FX_ACTOR"] = "agent:fx-sdlc-triage"
    p = subprocess.run(["claude", "-p", PROMPT.format(log=log), "--output-format", "json", "--allowedTools", READ_ONLY,
                        "--permission-mode", "default", "--setting-sources", "project,local"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
    res = json.loads(p.stdout) if p.stdout.strip().startswith("{") else {"result": p.stdout + p.stderr}
    note = res.get("result", "")
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(note + "\n")
    print(note)
    print(json.dumps({"usd": res.get("total_cost_usd"), "turns": res.get("num_turns"),
                      "denied": [x.get("tool_name") for x in res.get("permission_denials", [])]}), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
