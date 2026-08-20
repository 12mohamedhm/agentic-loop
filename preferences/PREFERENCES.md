# Preference Ledger

Standing answers to INTENT questions, written by grilling write-backs and
escalation resolutions. Grilling reads this before asking; a covered
question surfaces as a resolved default with provenance, never as a
question. Entries follow schemas/preference-entry.md; supersede with links,
never edit.

## PREF-001: Testing philosophy — TDD, test-first
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q1
Preference: Tests come before implementation for every contract;
red-green-refactor is the law. A contract's acceptance criteria translate
into failing tests before any production code is written.

## PREF-002: Dependency appetite — stdlib-first
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q2
Preference: Prefer the standard library and dependencies already in the
project. A new dependency needs a stated justification covering size,
maintenance health, and security surface — written where the dependency is
introduced (contract or ADR).

## PREF-003: Error handling — fail fast, loud
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q3
Preference: Validate at boundaries and raise early with context-rich
messages. Silent catches and defensive fallbacks that mask bugs are
defects, not robustness.

## PREF-004: Formatting — tool-enforced, zero debate
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q4
Preference: The repo's formatter/linter config is law; absent one, install
the ecosystem standard (black/ruff, prettier). Match surrounding code.
Style is never argued in prose or review.

## PREF-005: Risk tolerance — bold within the write-set
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q5
Preference: Any change inside a contract's declared write_set proceeds
without asking, however large. Any change outside it stops and surfaces as
a deviation. The write_set is the risk boundary.

## PREF-006: Review strictness — block on correctness only
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q6
Preference: Validator and critic seats FAIL only on bugs, contract
violations, and missing acceptance criteria. Style and taste observations
are logged as warnings, never blockers.

## PREF-007: Communication format — unslop
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q7 (escalated twice to
pin the exact source: the unslop skill in cursor/plugins pstack,
https://github.com/cursor/plugins/tree/main/pstack/skills/unslop).
2026-08-19: standard vendored into this repo at
constitution/writing-for-humans.md, which is now the governing copy.
Preference: Every report to the human (gate summaries, escalations,
mission reports) follows constitution/writing-for-humans.md — plain words,
active voice, concrete facts over vibes, the tells table cleared, and the
self-audit pass before sending.

## PREF-008: Default mode vector — pair design only
Scope: GLOBAL   Status: ACTIVE
Provenance: founder seeding session, 2026-08-19, Q8
Preference: New missions default to
{"research": "auto", "design": "paired", "implementation": "auto",
"validation": "auto", "debug": "auto"} — the human approves the design
gate; every other gate advances on PASS. Flip per-mission at any gate.
