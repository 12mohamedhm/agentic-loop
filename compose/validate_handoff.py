#!/usr/bin/env python3
"""
validate_handoff.py — Structural completeness check for a handoff document.

Replaces a raw length minimum with the checks that actually predict handoff
quality (structure prevents omission; length does not):

  1. No unfilled {{PLACEHOLDER}} tokens remain.
  2. No leftover template instruction comments (<!-- AGENT: ... -->) in
     required sections — their presence means the section wasn't filled.
  3. Every required section is present and non-trivially filled.
  4. Every Action List item has an acceptance criterion.
  5. "In progress" names at least one concrete file path.
  6. Decision Log has at least one real row (and warns if the chain has
     more than one session but only one decision — likely a lost copy-forward).
  7. Section 9 is explicit: either content or the literal "None pending".

Exit code 0 = PASS (warnings allowed), 1 = FAIL.

Usage: python validate_handoff.py <handoff-file.md> [--strict]
       (--strict promotes warnings to failures)
"""

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "## 1. Mission",
    "## 2. State of the World",
    "## 3. Progress Ledger",
    "## 4. Decision Log",
    "## 5. Dead Ends & Gotchas",
    "## 6. Contracts & Invariants",
    "## 7. Action List",
    "## 8. Contingencies",
    "## 9. Open Questions",
    "## 10. Receiver Synthesis Protocol",
]

# Sections where a lingering AGENT comment means "not filled".
AGENT_SECTIONS = ["## 1.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8.", "## 9."]

MIN_SECTION_CONTENT_CHARS = {
    "## 1. Mission": 120,
    "## 3. Progress Ledger": 120,
    "## 7. Action List": 80,
}


def split_sections(text):
    """Return {header_line: body_text} for all ## sections."""
    sections = {}
    current, buf = None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                sections[current] = "\n".join(buf)
            current, buf = line.strip(), []
        else:
            buf.append(line)
    if current:
        sections[current] = "\n".join(buf)
    return sections


def find_section(sections, prefix):
    for header, body in sections.items():
        if header.startswith(prefix):
            return header, body
    return None, None


def strip_noise(body):
    """Remove comments, code fences content markers, and blank/bullet-only lines."""
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL)
    lines = [l.strip() for l in body.splitlines()]
    lines = [l for l in lines if l and l not in {"-", "*", "1.", "```"}]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("handoff")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()

    text = Path(args.handoff).read_text()
    failures, warnings = [], []

    # 1. Placeholders
    leftovers = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))
    if leftovers:
        failures.append(f"Unfilled placeholders: {', '.join(leftovers)}")

    sections = split_sections(text)

    # 3. Required sections present + minimally filled
    for req in REQUIRED_SECTIONS:
        header, body = find_section(sections, req.split("`")[0].strip())
        if header is None:
            failures.append(f"Missing section: {req}")
            continue
        min_chars = MIN_SECTION_CONTENT_CHARS.get(req)
        if min_chars and len(strip_noise(body)) < min_chars:
            failures.append(f"Section under-filled (<{min_chars} chars of content): {req}")

    # 2. Agent sections that contain nothing but the template's instruction comment
    for prefix in AGENT_SECTIONS:
        header, body = find_section(sections, prefix)
        if body is None:
            continue
        content = strip_noise(body)
        # Drop table-header/divider scaffolding rows from consideration
        content = "\n".join(l for l in content.splitlines()
                            if not re.match(r"^\|\s*#|^\|[-\s|]+\|?$", l)
                            and not re.match(r"^\*\*(Purpose|Method|End state)[^*]*\*\*\s*$", l)
                            and not l.startswith("###"))
        if len(content) < 30:
            failures.append(f"Section not filled (template scaffolding only): {header}")

    # 4. Action items have acceptance criteria
    _, actions = find_section(sections, "## 7.")
    if actions:
        action_count = len(re.findall(r"^\s*\d+\.\s+\*\*Action", actions, re.M))
        criteria_count = len([l for l in actions.splitlines()
                              if re.search(r"acceptance criterion:\s*\S", l, re.I)])
        if action_count == 0:
            failures.append("Action List has no actions in the required format")
        elif criteria_count < action_count:
            failures.append(f"Action List: {action_count} actions but only "
                            f"{criteria_count} filled acceptance criteria")

    # 5. In-progress stopping point names a file
    _, ledger = find_section(sections, "## 3.")
    if ledger:
        m = re.search(r"### In progress.*?(?=###|\Z)", ledger, re.DOTALL)
        chunk = strip_noise(m.group(0)) if m else ""
        has_path = bool(re.search(r"[\w./-]+\.(py|js|ts|tsx|jsx|go|rs|java|rb|md|c|cpp|h|json|yaml|yml|toml|sql|sh)\b", chunk))
        if len(chunk) > 40 and not has_path:
            warnings.append("'In progress' names no concrete file path — the stopping "
                            "point may not be actionable for the receiver")

    # 6. Decision log rows
    _, dlog = find_section(sections, "## 4.")
    session_m = re.search(r"Session number in chain \|\s*(\d+)", text)
    session_num = int(session_m.group(1)) if session_m else 1
    if dlog:
        rows = [l for l in dlog.splitlines()
                if l.strip().startswith("|") and not re.match(r"^\|\s*#|^\|[-\s|]+\|?$", l.strip())]
        real_rows = [r for r in rows if len(strip_noise(r.replace("|", " "))) > 10]
        if not real_rows:
            failures.append("Decision Log has no filled rows — every session makes at least "
                            "one decision worth recording; if truly none, record that explicitly")
        elif session_num > 1 and len(real_rows) < 2:
            warnings.append(f"Session {session_num} in chain but only {len(real_rows)} decision "
                            "row(s) — prior entries may not have been copied forward (append-only rule)")

    # 7. Open questions explicit
    _, oq = find_section(sections, "## 9.")
    if oq is not None:
        content = strip_noise(oq)
        if not content:
            failures.append("Section 9 is blank — write questions or the literal 'None pending'")

    # Report
    print(f"Validating: {args.handoff}\n")
    for f in failures:
        print(f"  FAIL  {f}")
    for w in warnings:
        print(f"  WARN  {w}")
    if not failures and not warnings:
        print("  All checks passed.")

    if failures or (args.strict and warnings):
        print(f"\nRESULT: FAIL ({len(failures)} failure(s), {len(warnings)} warning(s))")
        return 1
    print(f"\nRESULT: PASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
