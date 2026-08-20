# /loop — adopt or resume the agentic loop here

Resolve the system repo first:
`LOOP_REPO=$(cat .claude/loop-repo 2>/dev/null || git rev-parse --show-toplevel)`

Run:

    python3 "$LOOP_REPO/compose/bootstrap.py" --project-dir .

Obey its printed output exactly — it detects init vs resume, announces any
missing tool, and names the single next command. Announce any MISSING TOOL
line in your first reply.

Completion criterion: bootstrap exited 0 and you have executed (or surfaced
to the human) every numbered step it printed.
