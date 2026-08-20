# /pair — set phase mode(s) to paired

Arguments: zero or more phase names (research, design, implementation,
validation, debug). No argument means every phase.

Edit the `Modes:` JSON vector in `.loop/MISSION.md`: set each named phase
(or all phases) to `"paired"`. Change nothing else in the file.

Echo the full new vector back to the human.

Completion criterion: MISSION.md holds the new vector and the human has
seen it echoed.
