# Operator's Guide

You point an agent at a project; the agent runs a mission through five
phases — Research, Design, Implementation, Validation, Debug — and this
system decides what the agent reads, when a phase is truly done, and when
you get asked. This guide is everything you, the human, need. No Python
required.

## The three verbs

Everything the agent does cycles through three commands:

1. **Bootstrap** (`/loop`) — adopt or resume the loop in a project. It
   detects whether a mission is in flight and prints the one next step.
2. **Enter** (`/enter`) — compile the instructions for the current phase
   and hand the agent an exact reading list. The agent loads only that.
3. **Gate** (`/gate`) — a program, not the agent's opinion, checks whether
   the phase's required artifacts exist and are complete. Only a passing
   gate advances the mission.

**What you actually type:** `/loop` once per project, then let the agent
drive; `/gate` any time you want to know whether the current phase would
pass right now.

## The mode vector and how to flip it

Every mission file (`.loop/MISSION.md`) carries one line like:

    Modes: {"research": "auto", "design": "paired", ...}

`auto` means the agent advances through that phase's gate on its own.
`paired` means the gate can pass, but the mission does not advance until
you say so. Flip any phase at any time — mid-mission flips take effect at
the next gate.

**What you actually type:** `/pair design` (or `/auto research`, or bare
`/pair` for every phase). The agent echoes the new vector back to you.

## What each gate asks of you

Gates are automated checks; your part is small and specific:

- **Mission confirmation** (before anything runs): the agent interviews
  you about the mission draft and you confirm it. Nothing proceeds without
  your confirmed mission.
- **Paired-phase gates**: you see the PASS output and give the word to
  advance. That is the whole ritual — approve or send it back.
- **Auto-phase gates**: nothing; you can read the gate history in
  `.loop/STATE.json` whenever you like.

**What you actually type:** "confirmed" (or your amendments) at mission
grilling; "advance" (or objections) at paired gates.

## Where escalations surface

Two kinds of questions reach you, and only these:

- **Intent questions** the preference ledger cannot answer — taste, risk,
  scope. They arrive numbered, with a recommended answer attached.
- **Hard-deny verbs** — secrets, spending, tags, releases, deletions,
  publication. The agent announces and queues these for you; it never
  performs them (see `regimes/policy.json`).

Everything else the agent resolves from the mission text, its research, or
your ledger, and logs where you can audit it.

**What you actually type:** an answer to each numbered question, or "take
your recommendations".

## How the preference ledger grows

Every intent answer you give is written to `preferences/PREFERENCES.md` as
a numbered PREF entry with a scope (global, per-stack, or per-repo) and
provenance (when and why you said it). The next mission reads the ledger
before asking, so a question you have answered once surfaces as "resolved
default, say the word to revisit" instead of a question. Over time,
missions ask you less and less. Change your mind any time — a new entry
supersedes the old one; nothing is silently edited.

**What you actually type:** nothing extra — answering questions is the
maintenance.

## One mission, ten lines

1. You: `bash <repo>/install.sh` inside your project, then `/loop`.
2. Agent interviews you on the mission draft; you answer, say "confirmed".
3. Agent enters Research, spawns readers, banks sources, writes synthesis.
4. `/gate` passes research (auto mode) — mission advances, handoff written.
5. Agent enters Design; asks you two intent questions the ledger missed.
6. You answer; ADRs and contracts are written; the design gate passes.
7. Design was `paired`, so the agent shows you PASS; you say "advance".
8. Implementation and Validation run in auto; you watch or walk away.
9. A validation check fails; the mission routes to Debug, fixes ship
   through a new contract, validation re-passes.
10. Mission complete — your two answers are now ledger entries, and the
    next mission will not ask them again.

**What you actually type:** two commands, one confirmation, a handful of
answers.
