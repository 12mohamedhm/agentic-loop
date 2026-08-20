# /enter — compile and enter the current phase

Resolve the system repo:
`LOOP_REPO=$(cat .claude/loop-repo 2>/dev/null || git rev-parse --show-toplevel)`

Run:

    python3 "$LOOP_REPO/compose/enter_phase.py" --project-dir .

On COMPILED: load ONLY the files on the printed reading list — the hub's
context is an index, never a payload. On REFUSED: do what the refusal names
(grill MISSION.md, confirm, set mission_confirmed) and run again.

Completion criterion: enter_phase exited 0 and every file on the reading
list is loaded, with nothing beyond it.
