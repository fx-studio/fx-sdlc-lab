#!/usr/bin/env python3
"""Local pull requests (this repo has no remote): a branch pr/<n>-<slug>, a worktree, and review/<n>/PR.md.

    python3 scripts/pr.py new <slug> [--title "<title>"] [--base main]   open PR <n>: branch + worktree .worktrees/pr-<n>
    python3 scripts/pr.py show <n>                                       size, risk label, files (JSON), and updates PR.md
    python3 scripts/pr.py list

Size and risk are computed by this script from the diff, never chosen by the agent (fix 4.1 and 4.3 of 05-deploy.md):
  - size: lines added + removed, not counting generated or evidence paths (demo/, review/, evals/results/). Over 400: warning.
  - risk: the highest level among the paths the PR touches (RISK below). high = 2 reviewers, one of them the tech lead.
Merging stays a person's act: `git merge pr/<n>-<slug>` on main, run by a person.
"""
import json, re, subprocess, sys
from pathlib import Path

MAX_LINES = 400
GENERATED = re.compile(r"^(demo/|review/|evals/results/)")
RISK = [  # first match wins
    ("high", re.compile(r"^(app/store\.js|app/backup\.js|\.claude/|scripts/deploy\.py|scripts/rollback|tools/deploy-mcp/|release/|"
                        r"\.github/|\.mcp\.json|CLAUDE\.md|REVIEW\.md)")),
    ("medium", re.compile(r"^(app/app\.js|app/index\.html|scripts/|evals/)")),
    ("low", re.compile(r".*")),  # app/style.css, tests/, docs, text
]
REVIEWERS = {"low": "1 code owner", "medium": "1 code owner, who reads the plan", "high": "2 people, one of them the tech lead"}


def git(*a, cwd=None):
    return subprocess.run(["git", *a], capture_output=True, text=True, check=True, cwd=cwd).stdout


ROOT = Path(git("rev-parse", "--path-format=absolute", "--git-common-dir").strip()).parent
REVIEW = ROOT / "review"


def branch_of(n):
    hits = [b.strip().lstrip("*+ ").strip() for b in git("branch", "--list", f"pr/{n}-*", cwd=ROOT).splitlines()]
    if not hits:
        sys.exit(f"no branch pr/{n}-*")
    return hits[0]


def new(slug, title=None, base="main"):
    nums = [int(p.name) for p in REVIEW.glob("*") if p.name.isdigit()]
    n = max(nums, default=0) + 1
    br = f"pr/{n}-{slug}"
    wt = ROOT / ".worktrees" / f"pr-{n}"
    git("worktree", "add", "-b", br, str(wt), base, cwd=ROOT)
    d = REVIEW / str(n)
    d.mkdir(parents=True)
    (d / "base").write_text(base + "\n")  # stacked PRs are measured against their own base, not main
    (d / "PR.md").write_text(f"# PR {n} · {title or slug}\n\nBranch: `{br}` · Base: `{base}` "
                             f"({git('rev-parse', '--short=7', base, cwd=ROOT).strip()})\n\n"
                             "Spec: (none) · Plan: (none)\n\n## What changes\n\n(author fills this in)\n\n## How it was checked\n\n"
                             "(author: paste the end of `bash scripts/check.sh`)\n")
    print(json.dumps({"pr": n, "branch": br, "worktree": str(wt.relative_to(ROOT))}))


def stats(n, base=None):
    br = branch_of(n)
    bf = REVIEW / str(n) / "base"
    base = base or (bf.read_text().strip() if bf.exists() else "main")
    rows = []
    for line in git("diff", "--numstat", f"{base}...{br}", cwd=ROOT).splitlines():
        a, r, path = line.split("\t", 2)
        a, r = (int(a), int(r)) if a != "-" else (0, 0)
        rows.append({"path": path, "added": a, "removed": r, "generated": bool(GENERATED.match(path))})
    counted = [x for x in rows if not x["generated"]]
    lines = sum(x["added"] + x["removed"] for x in counted)
    levels = [next(lvl for lvl, rx in RISK if rx.match(x["path"])) for x in counted]
    risk = "high" if "high" in levels else "medium" if "medium" in levels else "low"
    return {"pr": n, "branch": br, "base": base, "files": len(counted), "lines": lines, "max_lines": MAX_LINES,
            "size_warning": lines > MAX_LINES, "risk": risk, "reviewers": REVIEWERS[risk],
            "by_file": [{**x, "risk": lvl} for x, lvl in zip(counted, levels)]}


def show(n):
    s = stats(n)
    pr = REVIEW / str(n) / "PR.md"
    if pr.exists():
        text = re.sub(r"\n<!-- pr\.py -->.*", "", pr.read_text(), flags=re.S)
        warn = f" · ⚠ over {MAX_LINES} lines: split it in the order of the plan" if s["size_warning"] else ""
        pr.write_text(text.rstrip() + f"\n\n<!-- pr.py -->\n## Size and risk (computed by scripts/pr.py)\n\n"
                      f"{s['lines']} lines in {s['files']} files{warn} · risk **{s['risk']}** → {s['reviewers']}\n")
    print(json.dumps(s, ensure_ascii=False, indent=1))


def main(a):
    if a[:1] == ["new"] and len(a) > 1:
        title = a[a.index("--title") + 1] if "--title" in a else None
        base = a[a.index("--base") + 1] if "--base" in a else "main"
        new(a[1], title, base)
    elif a[:1] == ["show"] and len(a) > 1:
        show(a[1])
    elif a[:1] == ["list"]:
        for b in git("branch", "--list", "pr/*", cwd=ROOT).splitlines():
            print(b.strip())
    else:
        print(__doc__)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
