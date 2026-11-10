#!/usr/bin/env python3
"""Count triage decisions by reason (fix 4.3 of 06-maintain.md) and say what each count suggests.

    python3 scripts/triage-stats.py [ops/triage.md]

ops/triage.md is written by the person who owns the queue this week. Each row:
    | intent | decision | reason | by | date |
decision: fix-now | schedule | dismiss.  reason (only for dismiss), from this fixed list:
    false-alarm      the metric moved within normal noise        -> widen the band (a PR on ops/bands.yaml, a person reviews)
    known            right, already being handled                -> merge into the existing intent
    accepted         right, but acceptable                       -> write why, silence this kind for a set time
    wrong-diagnosis  the agent named the wrong cause             -> improve the diagnose skill, add an eval
Many false alarms = the band is wrong. Many wrong diagnoses = the agent lacks context.
"""
import collections, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADVICE = {"false-alarm": "widen the band of that metric (PR on ops/bands.yaml)",
          "known": "the agent should have merged: check the queue rule",
          "accepted": "write the acceptance and its end date in ops/bands.yaml (silence)",
          "wrong-diagnosis": "add context to the diagnose skill and an eval for that case"}
f = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "ops" / "triage.md"
every = [[c.strip() for c in l.strip().strip("|").split("|")] for l in f.read_text().splitlines()
         if l.startswith("|") and not re.match(r"\|\s*(intent\s*\||-)", l)]
rows = list({r[0]: r for r in every}.values())  # an intent can be triaged again (after an investigation): the last row counts
dec = collections.Counter(r[1] for r in rows if len(r) > 2)
why = collections.Counter(r[2] for r in rows if len(r) > 2 and r[1] == "dismiss")
print(f"{len(rows)} intents triaged ({len(every)} decisions): " + ", ".join(f"{k} {v}" for k, v in dec.items()))
for k, v in why.most_common():
    print(f"  dismiss · {k}: {v} -> {ADVICE.get(k, 'unknown reason: use the fixed list')}")
bad = [r for r in rows if len(r) > 2 and r[1] == "dismiss" and r[2] not in ADVICE]
if bad:
    print(f"  {len(bad)} dismissals without a reason from the list: {[r[0] for r in bad]}")
