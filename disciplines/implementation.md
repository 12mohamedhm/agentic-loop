# Discipline: Implementation

Contracts specify what and why; workers own how, inside an exact write-set.
Regime: worker ceiling = {{BUDGET_WORKERS}}, escalation set =
{{ESCALATION_SET}}.

## Steps

0. Freshness: re-check sources-of-record pins against banked bytes (the
   composer ran this at entry); a drifted upstream is a deviation before
   any build starts.
1. One worker per contract (templates/mandate-implementer.md), parallel
   where write-sets are disjoint. Mandates bind: interface and invariants
   frozen, write_set exact, TDD red-first (a failing test precedes the code
   it proves; commit shapes prove the order), evidence from execution.
2. Contracts marked HIGH complexity get a navigator: a second worker holding
   only the contract and the diff-so-far, reviewing at the contract's named
   checkpoints. ROUTINE contracts run solo.
3. The hub reads completion reports, deviation reports, and integration
   surfaces — the diffs belong to validation. Deviations resolve as
   contract amendment or superseding ADR; mission conflicts follow
   {{ESCALATION_SET}}.
4. Merge is a hub verb on gate pass; workers stay on their branches. Any
   irreversible operation echoes its preconditions inside the command
   itself before firing.

## Done when

Every contract has a completion report with per-criterion execution
evidence and declared-vs-actual spend; zero unresolved deviations; every
touched file inside a contract's write_set.
