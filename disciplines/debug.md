# Discipline: Debug

Model first, then hypothesis discipline, parallelized; the fix ships through
the pipeline; the learning ships upstream. Regime: wave ceiling =
{{BUDGET_WORKERS}}, escalation set = {{ESCALATION_SET}}.

## Steps

1. Orientation (one worker, bounded): a feedback loop that goes red on this
   bug — deterministic repro — plus the expected-behavior model around the
   fault. Hypotheses wait until the loop is red.
2. Waves: the hub owns the ledger (schemas/hypothesis-ledger.md). Each
   wave spawns one experimenter per live hypothesis
   (templates/mandate-experimenter.md): one prediction, one experiment,
   predicted-vs-observed, verdict. Update append-only; prune; respawn.
3. Resolve: the confirmed cause becomes a fix contract that re-enters
   Implementation and Validation under the same gates.
4. Kill the class: the micro-postmortem (schemas/postmortem.md) lands every
   contributing factor in a typed home — a checklist entry, a handoff
   dead-end, a superseding ADR — and anything unhomeable stays project law.

## Done when

Ledger CLOSED with confirmed cause(s); fix contract PASSED validation;
postmortem written with at least one upstream write; hypotheses-killed-
per-wave recorded.
