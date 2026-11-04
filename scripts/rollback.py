#!/usr/bin/env python3
"""Rollback is one command (playbook Stage 5, CI/CD step 6): python3 scripts/rollback.py <env>

Switches <env> back to its previous release. Rehearse it in staging: python3 scripts/rollback-drill.py staging 10
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import deploy  # noqa: E402

if len(sys.argv) != 2:
    print(__doc__)
    sys.exit(2)
import json  # noqa: E402
print(json.dumps(deploy.rollback(sys.argv[1]), ensure_ascii=False))
