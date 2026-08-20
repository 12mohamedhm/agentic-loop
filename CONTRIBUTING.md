# Contributing

The whole repo follows one law: every fact lives in exactly one file, and
everything else points at it. Before changing anything, find that file.

## Where changes go

| You want to change | Edit | Never edit |
|---|---|---|
| How a phase works | the discipline in [disciplines/](disciplines) | any `.loop/runtime/` output |
| When a mode applies, what's reversible | [regimes/regimes.json](regimes/regimes.json), [regimes/policy.json](regimes/policy.json) | |
| What a gate demands of an artifact | the contract in [schemas/](schemas) | the gate script, unless the check itself is wrong |
| Compiler or gate behavior | [compose/](compose), with a test | |
| The invariants themselves | [constitution/principles.md](constitution/principles.md), sparingly | |

If a generated file looks wrong, the bug is upstream in a discipline or a
regime. Fix it there and recompile; a hand-edited runtime file will be
overwritten and deserves to be.

## Before you open a PR

1. Run the tests. They take under a second, so there is no excuse:

   ```bash
   python3 -m pytest compose/tests -q
   ```

2. Compiler changes need a test in
   [compose/tests](compose/tests). Prose changes need every pointer they
   touch to still resolve to a real file.

3. Write prose the way the constitution demands. Instructions for agents
   follow
   [writing-for-agents.md](constitution/writing-for-agents.md): positive
   phrasing, a completion criterion on every step, one meaning one home.
   Anything a human reads follows
   [writing-for-humans.md](constitution/writing-for-humans.md): plain
   words, named facts, no AI tells.

## Constraints that will not move

- `compose/` stays stdlib-only Python 3.9+. A dependency needs a reason
  the standard library cannot answer.
- `SKILL.md` stays the sole agent entry point. New capability is reached
  by a pointer from it or from a script it names, never by a second door.
- Commit messages are conventional (`feat:`, `fix:`, `docs:`, `chore:`)
  with the change's reason in the body when it isn't obvious.
