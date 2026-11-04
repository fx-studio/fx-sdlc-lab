#!/usr/bin/env python3
"""AI review of a local pull request: a local stand-in for claude-code-action (playbook Stage 5, "AI in the PR review loop").

    python3 scripts/review.py <n> [--label <name>] [--generic] [--model <m>]

- Checks out the PR head in a throw-away worktree and runs `claude -p` there with **read-only** tools.
- Default: the reviewer follows REVIEW.md (three passes, Important / Nit, at most 5 nits).
  `--generic`: the prompt is only "review this pull request" (to compare, demo/sdlc-5 R2–R3).
  `--no-review-md`: delete REVIEW.md from the throw-away checkout, as in a repo that has none. R2 showed why it is needed:
  with `--generic` alone the reviewer still found REVIEW.md through CLAUDE.md and followed it.
- Writes review/<n>/<label>/: findings.json, tally.json (machine-readable counts by severity, what a merge gate would read),
  comment.md (what a person reads), stream.jsonl (raw, paths masked), cost.json.
- Findings never approve or block anything. This script exits 0 whatever it finds.
"""
import getpass, json, os, re, shutil, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

READ_ONLY = "Read,Glob,Grep,Bash(git diff:*),Bash(git log:*),Bash(git show:*)"


def git(*a, cwd=None):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True, cwd=cwd).stdout


ROOT = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()).parent

SCHEMA_RV = ('{"findings": [{"pass": "Bugs|Security|Compliance", "severity": "Important|Nit", "file": "<path>", "line": <n or null>, '
             '"title": "<short>", "why": "<what goes wrong, for whom>", "fix": "<suggested fix>"}], "dropped_nits": <n>, '
             '"claude_md_outdated": <true|false>}')
SCHEMA_GEN = '{"findings": [{"file": "<path>", "line": <n or null>, "comment": "<your review comment>"}]}'


def mask(s):
    s = s.replace(str(ROOT), "<repo>").replace(str(Path.home()), "<home>")
    s = re.sub(r"/(private/)?(var/folders|tmp)/[^\s\"'`]*", "<thư-mục-tạm>", s)
    s = re.sub(rf"(?<![\w.]){re.escape(getpass.getuser())}(?![\w])", "<user>", s)  # owner column of `ls -l`
    return re.sub(r"[\w.+-]+@(?!localhost)[\w-]+\.[\w.]+", "<email>", s)


def branch_of(n):
    hits = [b.strip().lstrip("*+ ").strip() for b in git("branch", "--list", f"pr/{n}-*", cwd=ROOT).splitlines()]
    if not hits:
        sys.exit(f"no branch pr/{n}-*")
    return hits[0]


def snapshot_without_review_md(base, head, dest):
    """A throw-away repo with no history: two commits (base, head) of the real trees, minus REVIEW.md and the CLAUDE.md line
    that points to it. `git show <old commit>:REVIEW.md` is then impossible (R2: deleting the file from a worktree was not enough)."""
    import io, tarfile
    subprocess.run(["git", "init", "-q", "-b", "main", str(dest)], check=True)
    ids = []
    for ref in (base, head):
        for child in dest.iterdir():
            if child.name != ".git":
                shutil.rmtree(child) if child.is_dir() else child.unlink()
        tar = subprocess.run(["git", "archive", "--format=tar", ref], capture_output=True, check=True, cwd=ROOT).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as t:
            t.extractall(dest, filter="data")
        (dest / "REVIEW.md").unlink(missing_ok=True)
        cm = dest / "CLAUDE.md"
        if cm.exists():
            cm.write_text(re.sub(r"\n- \*\*Review\*\* follows `REVIEW.md`.*?(?=\n- )", "", cm.read_text(), flags=re.S))
        g = lambda *a: subprocess.run(["git", *a], cwd=dest, capture_output=True, text=True, check=True).stdout.strip()
        g("add", "-A")
        g("-c", "user.name=snapshot", "-c", "user.email=snapshot@example.invalid", "commit", "-qm", f"snapshot of {ref}")
        ids.append(g("rev-parse", "--short=7", "HEAD"))
    return ids[0], ids[1]


def prompt_for(n, br, base_sha, head_sha, pr_md, generic):
    head = (f"This is local pull request #{n}: branch `{br}` (head {head_sha}), base {base_sha}. "
            f"The working directory is a checkout of the head. See the change with `git diff {base_sha}...HEAD`.\n\n"
            f"PR description (review/{n}/PR.md):\n\n{pr_md}\n\n")
    if generic:
        return head + ("Review this pull request.\n\nReply with ONLY one JSON object, no prose around it, in this shape:\n" + SCHEMA_GEN)
    return head + ("Review it by following REVIEW.md at the repo root exactly (read it first, then CLAUDE.md, then the spec and plan "
                   "the description names). Findings are advisory; you do not approve or block.\n\n"
                   "Reply with ONLY one JSON object, no prose around it, in this shape:\n" + SCHEMA_RV)


def parse(result):
    m = re.search(r"\{.*\}", result, re.S)
    try:
        return json.loads(m.group(0)) if m else {"findings": [], "parse_error": result[:500]}
    except json.JSONDecodeError as e:
        return {"findings": [], "parse_error": f"{e}: {result[:500]}"}


def main(a):
    if not a or a[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    n = a[0]
    generic = "--generic" in a
    no_review_md = "--no-review-md" in a
    label = a[a.index("--label") + 1] if "--label" in a else ("generic" if generic else "review") + f"-{datetime.now():%H%M%S}"
    model = a[a.index("--model") + 1] if "--model" in a else None
    br = branch_of(n)
    bf = ROOT / "review" / n / "base"  # stacked PRs: review only this PR's own commits
    base_ref = bf.read_text().strip() if bf.exists() else "main"
    base_sha = git("merge-base", base_ref, br, cwd=ROOT).strip()[:7]
    head_sha = git("rev-parse", "--short=7", br, cwd=ROOT).strip()
    pr_md = (ROOT / "review" / n / "PR.md").read_text() if (ROOT / "review" / n / "PR.md").exists() else "(no description)"
    out = ROOT / "review" / n / label
    out.mkdir(parents=True, exist_ok=True)

    wt = Path(tempfile.mkdtemp(prefix=f"review-{n}-"))
    if no_review_md:
        base_sha, head_sha = snapshot_without_review_md(base_sha, head_sha, wt)
        cleanup = lambda: shutil.rmtree(wt, ignore_errors=True)
    else:
        shutil.rmtree(wt)
        git("worktree", "add", "--detach", str(wt), br, cwd=ROOT)
        cleanup = lambda: git("worktree", "remove", "--force", str(wt), cwd=ROOT)
    try:
        cmd = ["claude", "-p", prompt_for(n, br, base_sha, head_sha, pr_md, generic), "--output-format", "stream-json", "--verbose",
               "--allowedTools", READ_ONLY, "--permission-mode", "default", "--setting-sources", "project,local"]
        if model:
            cmd += ["--model", model]
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}  # may run from inside a session (/watch-pr)
        env["FX_ACTOR"] = "agent:fx-sdlc-reviewer"
        t0 = time.time()
        p = subprocess.run(cmd, cwd=wt, capture_output=True, text=True, stdin=subprocess.DEVNULL, env=env)
        dt = time.time() - t0
    finally:
        cleanup()

    (out / "stream.jsonl").write_text(mask(p.stdout))
    final = {}
    for line in p.stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            final = ev
    data = parse(final.get("result", ""))
    data.update({"pr": int(n), "base": base_sha, "head": head_sha, "mode": ("generic" if generic else "REVIEW.md") + (", no REVIEW.md in repo" if no_review_md else "")})
    (out / "findings.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n")

    f = data.get("findings", [])
    tally = {"pr": int(n), "head": head_sha, "mode": data["mode"], "total": len(f),
             "Important": sum(x.get("severity") == "Important" for x in f), "Nit": sum(x.get("severity") == "Nit" for x in f),
             "by_pass": {k: sum(x.get("pass") == k for x in f) for k in ("Bugs", "Security", "Compliance")}}
    (out / "tally.json").write_text(json.dumps(tally) + "\n")
    cost = {"seconds": round(dt, 1), "usd": final.get("total_cost_usd"), "turns": final.get("num_turns"),
            "model": list(final.get("modelUsage", {})), "denied": [x.get("tool_name") for x in final.get("permission_denials", [])]}
    (out / "cost.json").write_text(json.dumps(cost) + "\n")

    lines = [f"# Review · PR {n} · {data['mode']} · head {head_sha}", ""]
    if data["mode"].startswith("REVIEW.md"):
        lines.append(f"**{tally['Important']} Important · {tally['Nit']} Nit** (dropped nits: {data.get('dropped_nits', '?')})"
                     f"{' · CLAUDE.md out of date' if data.get('claude_md_outdated') else ''}\n")
    for i, x in enumerate(f, 1):
        tag = f"[{x.get('severity')} · {x.get('pass')}] " if x.get("severity") else ""
        lines.append(f"{i}. {tag}`{x.get('file')}:{x.get('line')}` **{x.get('title', '')}** {x.get('why', x.get('comment', ''))}"
                     + (f" → {x['fix']}" if x.get("fix") else ""))
    if data.get("parse_error"):
        lines.append(f"\n⚠ could not parse the reviewer's reply: {data['parse_error'][:300]}")
    (out / "comment.md").write_text(mask("\n".join(lines)) + "\n")
    print(json.dumps({"out": str(out.relative_to(ROOT)), **tally, **cost}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
