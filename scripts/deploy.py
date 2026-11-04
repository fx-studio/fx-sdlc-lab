#!/usr/bin/env python3
"""Local deploy for the todo app: three environments as folders, no network, no credentials.

    python3 scripts/deploy.py deploy <env> [<ref>]     build app/ at <ref> (default HEAD) and make it current in <env>
    python3 scripts/deploy.py prepare [<ref>]          build a production candidate, do not switch (what the agent may do)
    python3 scripts/deploy.py status [<env>]           current release of one or every environment
    python3 scripts/deploy.py rollback <env>           go back to the previous release of <env> (same as scripts/rollback.py)

Layout (git-ignored): deploy/<env>/releases/<id>/ holds a copy of app/; deploy/<env>/current is a symlink to the live one;
deploy/<env>/history.jsonl lists every switch. deploy/log.jsonl records every action with a timestamp and an actor.

Actor: FX_ACTOR if set (agent sessions run with FX_ACTOR=agent:fx-sdlc-agent), otherwise person:<git user.name>.
So the log tells what the agent did from what the person who started it did (playbook Stage 5, CI/CD).

This script does not check approvals. Gates are hooks (.claude/hooks/release-gate*.py) and the MCP tool scope
(tools/deploy-mcp/server.py): the point of the demo is to see which of them holds.
"""
import json, os, subprocess, sys, tarfile, io, time
from datetime import datetime, timezone
from pathlib import Path

ENVS = ("dev", "staging", "production")


def repo_root():
    # The main checkout, also when called from a worktree under .worktrees/.
    common = subprocess.run(["git", "rev-parse", "--path-format=absolute", "--git-common-dir"],
                            capture_output=True, text=True, check=True).stdout.strip()
    return Path(common).parent


ROOT = Path(os.environ.get("DEPLOY_ROOT") or repo_root() / "deploy")


def actor():
    if os.environ.get("FX_ACTOR"):
        return os.environ["FX_ACTOR"]
    name = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip() or "unknown"
    return f"person:{name}"


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def log(**kv):
    ROOT.mkdir(parents=True, exist_ok=True)
    kv = {"ts": now(), "actor": actor(), **kv}
    with open(ROOT / "log.jsonl", "a") as f:
        f.write(json.dumps(kv, ensure_ascii=False) + "\n")
    return kv


def build(ref, dest_dir):
    """Copy app/ as it is at <ref> into a new release folder. Returns the release id (short sha + time)."""
    sha = subprocess.run(["git", "rev-parse", "--short=7", ref], capture_output=True, text=True, check=True).stdout.strip()
    rid = f"{sha}-{datetime.now():%Y%m%d-%H%M%S-%f}"  # microseconds: the drill deploys several times a second
    out = dest_dir / rid
    out.mkdir(parents=True)
    tar = subprocess.run(["git", "archive", "--format=tar", ref, "app"], capture_output=True, check=True).stdout
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t.getmembers():
            if m.isfile():
                target = out / Path(m.name).relative_to("app")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(t.extractfile(m).read())
    (out / "RELEASE.json").write_text(json.dumps({"id": rid, "ref": ref, "sha": sha, "built": now(), "by": actor()}) + "\n")
    return rid, sha


def switch(env, rid):
    cur = ROOT / env / "current"
    tmp = ROOT / env / ".current.tmp"
    if tmp.is_symlink() or tmp.exists():
        tmp.unlink()
    tmp.symlink_to(Path("releases") / rid)
    os.replace(tmp, cur)  # atomic: the environment is never half switched
    with open(ROOT / env / "history.jsonl", "a") as f:
        f.write(json.dumps({"ts": now(), "release": rid, "actor": actor()}) + "\n")


def current(env):
    cur = ROOT / env / "current"
    return os.readlink(cur).split("/")[-1] if cur.is_symlink() else None


def deploy(env, ref="HEAD"):
    if env not in ENVS:
        raise SystemExit(f"unknown environment {env!r}; use one of {', '.join(ENVS)}")
    rid, sha = build(ref, ROOT / env / "releases")
    switch(env, rid)
    return log(action="deploy", env=env, release=rid, sha=sha)


def prepare(ref="HEAD"):
    rid, sha = build(ref, ROOT / "production" / "candidates")
    return log(action="prepare_release", env="production", release=rid, sha=sha,
               next=f"a release manager approves release/approvals/{sha}.md on main, then a person runs: "
                    f"python3 scripts/deploy.py deploy production {sha}")


def rollback(env):
    hist = ROOT / env / "history.jsonl"
    rows = [json.loads(l) for l in hist.read_text().splitlines()] if hist.exists() else []
    live = current(env)
    # previous distinct release before the live one
    seen = [r["release"] for r in rows]
    prev = next((r for r in reversed(seen[:-1]) if r != live), None) if seen else None
    if not prev:
        return log(action="rollback", env=env, result="nothing to roll back to", live=live)
    switch(env, prev)
    return log(action="rollback", env=env, release=prev, replaced=live)


def status(env=None):
    return {e: current(e) for e in ([env] if env else ENVS)}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, rest = argv[0], argv[1:]
    if cmd == "deploy" and rest:
        out = deploy(rest[0], rest[1] if len(rest) > 1 else "HEAD")
    elif cmd == "prepare":
        out = prepare(rest[0] if rest else "HEAD")
    elif cmd == "rollback" and rest:
        out = rollback(rest[0])
    elif cmd == "status":
        out = status(rest[0] if rest else None)
    else:
        print(__doc__)
        return 2
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
