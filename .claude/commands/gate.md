# /gate — run the deterministic gate for the current phase

Resolve the system repo:
`LOOP_REPO=$(cat .claude/loop-repo 2>/dev/null || git rev-parse --show-toplevel)`

Read the current phase from `.loop/STATE.json`, then run:

    python3 "$LOOP_REPO/compose/gate_check.py" --project-dir . --phase <current>

On FAIL: fix every listed failure at its source and run again — the gate
decides, never you.

On PASS: read this phase's mode from the Modes vector in `.loop/MISSION.md`.
- Mode `paired`: show the human the PASS output and ask for their word
  before re-running with `--advance`.
- Mode `auto`: re-run with `--advance` directly.

After ADVANCED, run /handoff — every gate is a handoff.

Completion criterion: gate printed ADVANCED (with human approval first in
paired mode) and the handoff is written and validated.
