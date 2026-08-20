# Discipline: Design

One authoring mind; adversarial stress; transmission test at the consumer's
capability; append-only records. The loop's largest planned hub spend.
Regime: interrogator for the design grill = {{INTERROGATOR}},
answerer = {{ANSWERER}}, escalation set = {{ESCALATION_SET}}.

## Steps

1. Sources-of-record first: for every external dependency the mission
   touches, a doc-review worker banks the authoritative documentation
   (schemas/sources-of-record.md). Authorship waits for annex coverage.
2. Author alone from synthesis + annex: ADRs (append-only, superseding
   links), contracts (one per self-contained module, sized deep — interface,
   invariants, non-goals, exact write_set, machine-checkable acceptance
   criteria tagged [script] or [model]), and the validation checklist
   derived clause-by-clause now, each entry tracing to a contract.
3. Stress in parallel, fresh contexts:
   - Adversary (templates/mandate-critic.md): strongest case against, every
     objection citing an ADR or contract line.
   - Implementability read (templates/mandate-implementability.md): restate
     each contract's intent, draft the breakdown, list every ambiguity that
     would force a guess. Reconstruction errors measure transmission loss.
4. Grill the design: {{INTERROGATOR}} works the tree over the artifacts;
   {{ANSWERER}} answers DESIGN from mission and annex; INTENT gaps follow
   {{ESCALATION_SET}}. A contested design question with a cheap empirical
   answer becomes a throwaway prototype, not a debate.
5. Adjudicate: every objection dispositioned in an ADR; every ambiguity
   fixed by amending the contract itself.

## Done when

Gate passes: annex covers every named dependency (CITABLE), every contract
carries write_set and tagged criteria, critique and implementability exist
with zero undispositioned items, checklist traces fully.
