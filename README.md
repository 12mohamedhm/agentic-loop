# agentic-loop

A portable operating system for frontier-hub multi-agent work: five phases
(Research, Design, Implementation, Validation, Debug), two modes (paired,
autonomous) set per-phase, instructions compiled per regime by scripts,
deterministic gates, a preference ledger that makes elicitation incremental,
and crash-safe handoffs at every boundary.

Grounded in organizational research (hub-and-spoke saturation, hidden-profile
information pooling, mission command, Fagan inspection, I-PASS handoffs). See
`constitution/principles.md` for the invariants and their provenance.

## Quick start (60 seconds)

    git clone https://github.com/12mohamedhm/agentic-loop.git
    cd /path/to/your/project
    bash /path/to/agentic-loop/install.sh

Then, in Claude Code inside your project: `/loop` — and obey what it prints.
Human operators: read `docs/OPERATORS-GUIDE.md` — the three verbs, the mode
vector, gates, escalations, and a worked example, in plain English.

## Layout

| Layer | What it is |
|---|---|
| `SKILL.md` | sole agent entry point |
| `constitution/` | how everything else is written; the invariants |
| `disciplines/` | invariant workflow cores (the only prose you edit) |
| `regimes/` | mode x phase bindings + reversibility policy (data you tune) |
| `schemas/` | regime-invariant artifact contracts |
| `compose/` | bootstrap, phase compiler, gates (code you test) |
| `hosts/` | per-harness capability profiles |
| `preferences/` | your ledger; grows across all projects |
| `templates/` | worker mandate stubs consumed by the compiler |
| `.claude/commands/` | slash commands installed into projects by `install.sh` |
| `docs/` | human-facing operator documentation |

Generated files under a project's `.loop/runtime/` are compiler output —
edit `disciplines/` and `regimes/`, never the runtime copies.

## Tests

    python -m pytest compose/tests -q

## License and notice

MIT — see `LICENSE`. The agent-writing doctrine in
`constitution/writing-for-agents.md` is adapted from
[mattpocock/skills](https://github.com/mattpocock/skills) (MIT).
