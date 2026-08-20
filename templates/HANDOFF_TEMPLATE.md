# CONVERSATION HANDOFF — {{PROJECT_NAME}}

> **Protocol note for the receiving agent:** Do not begin work from this document alone.
> Follow the Receiver Synthesis Protocol in Section 10 before taking any action.
> Machine sections (marked `[MACHINE]`) were collected from disk at {{COLLECTED_AT}} and are
> ground truth *as of that moment only* — re-verify before trusting.

| Field | Value |
|---|---|
| Handoff ID | {{HANDOFF_ID}} |
| Previous handoff | {{PREVIOUS_HANDOFF}} |
| Session number in chain | {{SESSION_NUMBER}} |
| Collected at | {{COLLECTED_AT}} |
| Working directory | {{WORKING_DIRECTORY}} |
| Session status | <!-- AGENT: ON_TRACK / BLOCKED / DEGRADED / EXPLORATORY — one word plus one sentence --> |

---

## 1. Mission `[AGENT — carried forward each handoff, re-affirmed or amended]`

<!-- AGENT: Purpose–Method–End-State format. This is the commander's intent for the whole
     effort, not this session. If unchanged from the previous handoff, copy it forward and
     write "UNCHANGED since handoff N". If amended, state what changed and why. -->

**Purpose (why this work exists):**

**Method (the chosen approach, at design level):**

**End state (what "done" looks like, with observable acceptance criteria):**

---

## 2. State of the World `[MACHINE — do not hand-write; regenerated fresh each handoff]`

### Git
```
{{GIT_STATE}}
```

### Recent commits
```
{{RECENT_COMMITS}}
```

### Working tree changes (diffstat)
```
{{DIFFSTAT}}
```

### Recently active files (by modification time)
```
{{ACTIVE_FILES}}
```

### Project structure
```
{{PROJECT_TREE}}
```

### Markers found in code (TODO / FIXME / HACK / XXX)
```
{{CODE_MARKERS}}
```

### Environment
```
{{ENVIRONMENT}}
```

---

## 3. Progress Ledger `[AGENT]`

<!-- AGENT: Every claim of completion needs evidence a stranger can check: a commit hash,
     a file path, a passing test command. "Implemented X" without evidence is not complete. -->

### Completed this session (with evidence)
-

### In progress — exact stopping point
<!-- AGENT: This is the highest-value field in the document. File and line/function,
     what was mid-flight, what the very next keystroke would have been. Be surgical. -->
-

### Not started (from current plan)
-

---

## 4. Decision Log `[AGENT — append-only across the chain; never delete prior entries]`

<!-- AGENT: Copy forward all prior entries verbatim, then append this session's.
     Rationale and rejected alternatives are the point — the decision itself is
     usually visible in the code; WHY it was made is not. -->

| # | Session | Decision | Rationale | Alternatives rejected & why | Reversible? |
|---|---------|----------|-----------|------------------------------|-------------|
| 1 | | | | | |

---

## 5. Dead Ends & Gotchas `[AGENT — append-only across the chain]`

<!-- AGENT: Everything tried that failed, and the failure mode. This section is what
     prevents the next session from burning half its context re-discovering the same
     walls. Include environmental surprises (flaky test, misleading docs, weird API
     behavior) even if they feel minor. -->

-

---

## 6. Contracts & Invariants `[AGENT — the design-authority section]`

<!-- AGENT: Interfaces that are frozen, constraints that must not be violated, and
     assumptions the current code depends on. The receiving agent treats these as
     binding unless the human amends them. If subagents/workers are in play, their
     task contracts live here too. -->

-

---

## 7. Action List `[AGENT — forward plan]`

<!-- AGENT: Priority-ordered. Every action gets: the files involved, and an acceptance
     criterion (how the receiver knows it's done). An action without an acceptance
     criterion is a wish, not a plan. -->

1. **Action:**
   - Files:
   - Acceptance criterion:

---

## 8. Contingencies & Situational Awareness `[AGENT]`

<!-- AGENT: "If X happens, do Y." Known risks in the current approach, and explicit
     escalation triggers — the conditions under which the receiving agent should STOP
     and ask the human rather than proceed. -->

### If/then contingencies
-

### Escalation triggers (stop and ask the human when...)
-

---

## 9. Open Questions for the Human `[AGENT]`

<!-- AGENT: Decisions deferred to the human, ambiguities in requirements, tradeoffs
     that need a judgment call. Empty is acceptable ONLY if truly nothing is pending —
     write "None pending" explicitly rather than leaving blank. -->

-

---

## 10. Receiver Synthesis Protocol `[FIXED — instructions to the incoming agent]`

You are a fresh session receiving this handoff. Before doing ANY work:

1. **Re-verify ground truth.** Run the state collector (`scripts/collect_state.py`) or the
   equivalent git/file commands, and diff reality against Section 2. Where they disagree,
   **disk wins** — the handoff is stale, not the repo. Note any drift explicitly.
2. **Load the working set.** Read every file listed under "In progress" in Section 3 and
   any file named in the top 2 items of Section 7. Do not skim — the stopping point in
   Section 3 only makes sense with the surrounding code in context.
3. **Honor the contracts.** Section 6 is binding. If an action in Section 7 appears to
   conflict with an invariant in Section 6, that conflict is an escalation (Section 8),
   not a judgment call.
4. **Write your readback.** Produce a short synthesis IN YOUR OWN WORDS: current state as
   you verified it, the next 1–3 actions you intend to take, and any drift or conflicts
   found in steps 1–3. This is your plan; present it before executing.
5. **Then begin.** Work the action list. When your own context approaches its limit,
   generate the next handoff in this chain using the same skill.
