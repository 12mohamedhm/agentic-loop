# Discipline: Validation

Checklist-driven inspection, three rings cheapest-first, fresh eyes always.
Regime: ring-3 adjudicator = {{ANSWERER}}, spot-audit rate =
{{AUDIT_RATE}}.

## Steps

1. Ring 1 — scripts: every [script] item runs as code; results land in
   verdicts untouched by any model. Includes the standing checks: write-set
   diff, budget reconciliation, gate-integrity (a change to any check in
   the same changeset it passes is an automatic deviation).
2. Ring 2 — parallel validators, one defect class each
   (templates/mandate-validator.md), fresh contexts, never shown
   implementer sessions or self-assessments. Force decorrelation by
   framing: top-down, prediction-first, adversarial-input. Every finding
   cites a checklist item and evidence.
3. Ring 3 — {{ANSWERER}} adjudicates contested findings and spot-audits
   {{AUDIT_RATE}} of unanimous passes on high-stakes criteria; unanimity
   among same-family validators is unconfirmed until sampled.

## Done when

A verdict per contract per assigned class; every checklist item PASS/FAIL
with evidence; any FAIL routes the loop to debug; correlated-miss rate
recorded.
