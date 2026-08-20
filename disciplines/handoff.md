# Discipline: Handoff

Every gate is a handoff; every handoff survives a dead session. Trigger
proactively at the 60% context check-in — seam at a lawful boundary rather
than discover the emergency later.

## Write

1. `python compose/collect_state.py` fills every machine section from disk
   (git, files, tree, markers, environment) and chains the numbering.
2. Fill agent sections highest-value first: exact stopping point (file and
   next keystroke), action list with acceptance criteria, decision log
   copied forward verbatim then appended, dead ends, contracts and
   invariants, mission (re-affirm or amend), contingencies and escalation
   triggers, open questions ("None pending" is written, never implied).
   Every figure recomputed at this seat.
3. `python compose/validate_handoff.py <file>` — fix every FAIL; structure
   is the bar, never length.

## Receive

Follow the document's own Receiver Synthesis Protocol: re-collect and diff
(disk wins), load the working set fully, honor contracts, write a readback
in your own words, then work the plan.
