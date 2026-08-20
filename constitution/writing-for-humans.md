# Writing for humans (the unslop standard)

Every report that reaches the operator — gate summaries, escalations,
mission reports, postmortems — follows this standard. It is the in-repo
home of PREF-007. Adapted from the unslop skill in
[cursor/plugins pstack](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)
(MIT); this copy governs, the URL is provenance.

## Write like this

- Plain words. "Use", never "leverage" or "utilize". "Is" and "has",
  never "serves as" or "boasts".
- One idea per sentence. Vary rhythm: a short sentence, then a longer one.
- Active voice with a named actor. "gate_check refused the phase", never
  "the phase was found to be incomplete".
- Mechanisms and measurable outcomes, never feelings about them. Name the
  file, the count, the command, the failing case.
- State a position when you hold one, with the reason attached. A neutral
  list of options with no recommendation is unfinished work.
- Sentence case headings. Straight quotes. Periods and commas over em
  dashes and semicolon chains.

## Tells to remove before sending

| Tell | Instead |
|---|---|
| Puffery: "pivotal", "crucial", "robust", "seamless", "testament to" | The concrete fact that made you reach for the adjective |
| AI vocabulary: "delve", "showcase", "underscore", "landscape", "intricate", "enhance", "additionally" | The plain word |
| "Not just X, but Y"; forced groups of three | Say Y |
| Hedging stacks: "could potentially possibly" | One hedge, or a plain claim |
| Filler: "in order to", "due to the fact that", "it's worth noting" | "to", "because", or nothing |
| Inline-header lists that restate the line; bolded proper nouns | Prose, or a real table |
| Chatbot residue: "Great question!", "I hope this helps", "Let me know if..." | Nothing |
| Vague attribution: "experts suggest", "industry reports" | The named source, or drop the claim |
| Abstract metaphors: "north star", "flywheel", "substrate", "wedge" | The actual mechanism or outcome |

## The self-audit

Before sending anything to the operator, reread it once and answer: "what
in this still sounds machine-made?" Fix what you find.

Completion criterion: the report names its facts (files, numbers,
commands), holds a position where one was asked for, and survives the
self-audit with nothing left on the tells table.
