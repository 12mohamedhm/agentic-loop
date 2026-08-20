# agentic-loop

A portable operating system for frontier-hub multi-agent work: five phases
(Research, Design, Implementation, Validation, Debug), two modes (paired,
autonomous) set per-phase, instructions compiled per regime by scripts,
deterministic gates, a preference ledger that makes elicitation incremental,
and crash-safe handoffs at every boundary.

Grounded in organizational research (hub-and-spoke saturation, hidden-profile
information pooling, mission command, Fagan inspection, I-PASS handoffs) and
in agent-writing doctrine adapted from Matt Pocock's skills (MIT). See
`constitution/principles.md` for the invariants and their provenance.

## Layout
- `SKILL.md` — sole agent entry point
- `constitution/` — how everything else is written; the invariants
- `disciplines/` — invariant workflow cores (the only prose you edit)
- `regimes/` — mode x phase bindings + reversibility policy (data you tune)
- `schemas/` — regime-invariant artifact contracts
- `compose/` — bootstrap, phase compiler, gates (code you test)
- `hosts/` — per-harness capability profiles (discovery vs citation tools)
- `preferences/` — your ledger; grows across all projects
- `templates/` — worker mandate stubs consumed by the compiler

## Quick start
    python compose/bootstrap.py --project-dir /path/to/project

## Tests
    python -m pytest compose/tests -q

## Publish (from this directory)
    git remote add origin git@github.com:<you>/agentic-loop.git
    git push -u origin main
