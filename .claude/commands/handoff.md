# /handoff — write a crash-safe handoff now

Resolve the system repo:
`LOOP_REPO=$(cat .claude/loop-repo 2>/dev/null || git rev-parse --show-toplevel)`

Execute the WRITE flow of `$LOOP_REPO/disciplines/handoff.md`:

1. `python3 "$LOOP_REPO/compose/collect_state.py" --project-dir .` — machine
   sections fill from disk; note the output path it prints.
2. Fill the [AGENT] sections highest-value first: exact stopping point (file
   and next keystroke), action list with acceptance criteria, decision log
   copied forward verbatim then appended, dead ends, contracts and
   invariants, mission, contingencies, open questions ("None pending" is
   written, never implied). Recompute every figure at this seat.
3. `python3 "$LOOP_REPO/compose/validate_handoff.py" <file>` — fix every
   FAIL and run again until PASS.

Completion criterion: validate_handoff prints PASS on the new handoff file.
