# Discipline: Grilling

Interview until shared understanding is structural, not felt. Map the topic
as a design tree; the frontier is every decision whose prerequisites are
settled. Regime for this session: interrogator = {{INTERROGATOR}},
answerer = {{ANSWERER}}, escalation set = {{ESCALATION_SET}},
round cap = {{BUDGET_ROUNDS}}.

## Loop

1. Build the tree from the artifact under grill (mission draft, design set,
   deviation). List branches explicitly.
2. Ask the whole frontier in one round. Number each question; give a
   recommended answer. Type every question:
   - FACT — dispatch a subagent; a running lookup is an unsettled
     prerequisite, so only its downstream waits.
   - DESIGN — {{ANSWERER}} answers, justified from mission, research, and
     banked sources; the interrogator pressure-tests against those texts.
   - INTENT — ledger lookup first (preferences/PREFERENCES.md). Hit:
     surface as a resolved default with provenance, revisitable by a word.
     Miss: escalate per {{ESCALATION_SET}}. When in doubt, type INTENT.
3. Settled answers reshape the tree; recompute the frontier; next round.
4. Disputes arbitrate in order: mission text, then ledger, then escalate.
5. Write-back: classify every settled answer — project decision to an ADR;
   durable preference to the ledger with scope and provenance.

## Done when

Frontier empty and an assumptions-surfaced list is written — every branch
visited, nothing silently assumed — or the round cap seams the session with
open branches escalated. Act only after the answerer confirms the tree.
