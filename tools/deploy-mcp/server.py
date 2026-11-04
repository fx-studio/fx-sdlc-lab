#!/usr/bin/env python3
"""MCP server `deploy` (stdio, Python stdlib only): deploy, status and rollback as tools scoped per environment.

Playbook Stage 5, CI/CD step 4: "the agent's deploy permission is an allowlist, not a script holding credentials".
Scope, enforced here and not by the agent's good will:

| tool              | dev | staging | production                                   |
|-------------------|-----|---------|----------------------------------------------|
| deploy            | yes | yes     | **no**: returns an error that says who can   |
| prepare_release   |  -  |  -      | yes: builds a candidate, does not switch     |
| status            | yes | yes     | yes                                          |
| rollback          | yes | yes     | **no**: production rollback is a person's call in this repo |

Registered in .mcp.json. Speaks JSON-RPC 2.0, one message per line (MCP stdio transport).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "scripts"))
import deploy as d  # noqa: E402

AGENT_ENVS = ("dev", "staging")
ENV = {"type": "string", "enum": ["dev", "staging", "production"]}
TOOLS = [
    {"name": "deploy", "description": "Build app/ at a git ref and make it live in dev or staging. Production is not allowed here: "
     "use prepare_release, then a named release manager authorizes the switch.",
     "inputSchema": {"type": "object", "properties": {"env": ENV, "ref": {"type": "string", "default": "HEAD"}}, "required": ["env"]}},
    {"name": "prepare_release", "description": "Build a production release candidate from a git ref without switching production.",
     "inputSchema": {"type": "object", "properties": {"ref": {"type": "string", "default": "HEAD"}}}},
    {"name": "status", "description": "Live release of every environment (or one).",
     "inputSchema": {"type": "object", "properties": {"env": ENV}}},
    {"name": "rollback", "description": "Switch dev or staging back to its previous release. One call, rehearsed in staging.",
     "inputSchema": {"type": "object", "properties": {"env": ENV}, "required": ["env"]}},
]


def call(name, a):
    env = a.get("env")
    if name == "deploy":
        if env not in AGENT_ENVS:
            raise PermissionError(f"deploy to {env!r} is outside this tool's scope (dev, staging). For production: call "
                                  "prepare_release, then ask the release manager to approve it on main.")
        return d.deploy(env, a.get("ref") or "HEAD")
    if name == "prepare_release":
        return d.prepare(a.get("ref") or "HEAD")
    if name == "status":
        return d.status(env)
    if name == "rollback":
        if env not in AGENT_ENVS:
            raise PermissionError("production rollback is a person's call in this repo: say what is broken and stop.")
        return d.rollback(env)
    raise KeyError(name)


def reply(i, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": i}
    msg["error" if error else "result"] = error or result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


os.environ.setdefault("FX_ACTOR", "agent:fx-sdlc-agent")  # every call through this server is the agent's
for line in sys.stdin:
    try:
        msg = json.loads(line)
    except json.JSONDecodeError:
        continue
    i, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if i is None:
        continue  # notifications (initialized, cancelled)
    if method == "initialize":
        reply(i, {"protocolVersion": params.get("protocolVersion", "2025-06-18"), "capabilities": {"tools": {}},
                  "serverInfo": {"name": "deploy", "version": "1.0.0"}})
    elif method == "tools/list":
        reply(i, {"tools": TOOLS})
    elif method == "tools/call":
        try:
            out = call(params.get("name"), params.get("arguments") or {})
            reply(i, {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]})
        except Exception as e:  # tool errors go back to the model, not as protocol errors
            reply(i, {"content": [{"type": "text", "text": f"{type(e).__name__}: {e}"}], "isError": True})
    elif method == "ping":
        reply(i, {})
    else:
        reply(i, error={"code": -32601, "message": f"method not found: {method}"})
