# /mission — adopt or resume the agentic loop here

Optional argument: free-text mission context from the operator. It seeds
the mission draft and steers the grill; it never replaces confirmation.

Operator context for this run: $ARGUMENTS

Resolve the system repo first:
`LOOP_REPO=$(cat .claude/loop-repo 2>/dev/null || git rev-parse --show-toplevel)`

Run one of these:

    # no operator context given
    python3 "$LOOP_REPO/compose/bootstrap.py" --project-dir .

    # operator context given — pass it verbatim, quoted safely
    python3 "$LOOP_REPO/compose/bootstrap.py" --project-dir . --seed "<the context>"

Obey its printed output exactly — it detects init vs resume, announces any
missing tool, and names the single next command. Announce any MISSING TOOL
or SEED IGNORED line in your first reply. When a seed was written, the
grill (disciplines/grilling.md) builds its tree from the whole draft
including the Operator seed section: questions the seed already answers
surface as recommended answers with the seed as provenance, and only the
remaining frontier reaches the operator.

Completion criterion: bootstrap exited 0 and you have executed (or surfaced
to the human) every numbered step it printed.
