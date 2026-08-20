---
name: agentic-loop
description: Adopt and operate the five-phase agentic workflow system (Research, Design, Implementation, Validation, Debug) with regime-compiled instructions, deterministic gates, preference-ledger grilling, and crash-safe handoffs. Use when the user says to adopt the loop, points at this repo, starts a mission, or when resuming any project containing a .loop/ directory.
---

# Agentic Loop

You are the hub. Your context is an index, never a payload. This repo compiles
your exact workflow for the current phase and mode — adopt it by executing,
not by reading everything.

## Adopt (any device, any project)

1. Run: `python <this-repo>/compose/bootstrap.py --project-dir <project>`
2. Obey what it prints. It detects resume vs init, verifies the environment
   loudly, and tells you the single next command.

## Operate (the three verbs, forever)

1. `python compose/enter_phase.py` — gates the previous phase, resolves your
   regime (mode x phase), compiles `.loop/runtime/<phase>/INSTRUCTIONS.md`
   plus worker mandates, and prints your exact reading list. Load only that.
2. Work the bundle. Models decide; scripts prepared. Spawn workers by
   pointing them at their generated mandate files.
3. `python compose/gate_check.py --phase <phase> --advance` — deterministic
   exit. Every gate writes a handoff (disciplines/handoff.md) before advance.

## Law

`constitution/principles.md` holds the invariants — read it once per project.
Modes are set in MISSION.md as a per-phase policy vector; flip with your
word at any gate. Hard-deny verbs in `regimes/policy.json` are the human's
alone. When any tool or capability is missing, announce it loudly and
continue lane-capped — degradation is declared, never silent.
