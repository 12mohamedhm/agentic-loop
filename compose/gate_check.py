#!/usr/bin/env python3
"""
gate_check.py — Deterministic phase gates. The hub does not decide a phase
is done; this program does. Structure is the bar, never length.

Usage:
  python gate_check.py --status [--project-dir DIR]
  python gate_check.py --phase P [--advance] [--to NEXT] [--project-dir DIR]
Exit: 0 PASS, 1 FAIL, 2 state/usage error.
"""
import argparse
import datetime
import json
import re
import signal
import subprocess
import sys
from pathlib import Path

ORDER = ["research", "design", "implementation", "validation", "debug", "complete"]


def unfilled(text):
    return sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", text)))


def has_content(path, min_chars=60):
    if not path.exists():
        return False
    body = re.sub(r"<!--.*?-->", "", path.read_text(), flags=re.DOTALL)
    return len(body.strip()) >= min_chars


def check_research(loop, f, w):
    proto = loop / "research" / "protocol.md"
    synth = loop / "research" / "synthesis.md"
    briefs = list((loop / "research" / "briefs").glob("*.md"))
    if not has_content(proto):
        f.append("research/protocol.md missing or empty"); return
    if unfilled(proto.read_text()):
        f.append("protocol.md has unfilled placeholders")
    questions = re.findall(r"^\s*-\s*(Q-\d+)", proto.read_text(), re.M)
    if not questions:
        f.append("protocol.md defines no questions (Q-N)")
    if not briefs:
        f.append("no research briefs")
    for b in briefs:
        t = b.read_text()
        if "CITABLE" in t and not re.search(r"sha|[0-9a-f]{16}", t):
            w.append(f"{b.name}: CITABLE findings without visible sha evidence")
    if not has_content(synth):
        f.append("research/synthesis.md missing or empty"); return
    stext = synth.read_text()
    for q in questions:
        if not re.search(rf"{q}\b(.|\n){{0,400}}?\b(ANSWERED|UNANSWERABLE)\b",
                         stext, re.I):
            f.append(f"synthesis does not mark {q} ANSWERED/UNANSWERABLE")
    for line in stext.splitlines():
        if "LOAD-BEARING" in line.upper() and "NOMINATED" in line.upper():
            f.append("synthesis has a load-bearing claim resting on a "
                     "NOMINATED finding — bank the source or demote the claim")


def check_design(loop, f, w):
    adrs = list((loop / "design" / "adr").glob("*.md"))
    contracts = list((loop / "contracts").glob("C-*.md"))
    critique = loop / "design" / "critique.md"
    impl_read = loop / "design" / "implementability.md"
    checklist = loop / "validation" / "checklist.md"
    annex = loop / "design" / "sources-of-record.md"
    if not adrs:
        f.append("no ADRs")
    for a in adrs:
        t = a.read_text()
        for sec in ("## Context", "## Decision", "## Consequences"):
            if sec not in t:
                f.append(f"{a.name}: missing {sec}")
        if unfilled(t):
            f.append(f"{a.name}: unfilled placeholders")
    if not contracts:
        f.append("no contracts")
    named_deps = set()
    for c in contracts:
        t = c.read_text()
        if not re.search(r"^- AC-\d+ \[(script|model)\]:\s*\S", t, re.M):
            f.append(f"{c.name}: no filled tagged acceptance criterion")
        ws = re.search(r"## write_set.*?\n(.*?)(?=\n## )", t, re.DOTALL)
        if not ws or not re.search(r"^\s*-\s*\S", ws.group(1), re.M):
            f.append(f"{c.name}: write_set empty — enumerate lawful surfaces exactly")
        if unfilled(t):
            f.append(f"{c.name}: unfilled placeholders")
        m = re.search(r"Sources of record:\s*(.+)", t)
        if m and m.group(1).strip() not in ("", "(none)", "{{ANNEX_ENTRIES}}"):
            named_deps.update(x.strip() for x in m.group(1).split(",") if x.strip())
    if named_deps:
        atext = annex.read_text() if annex.exists() else ""
        for d in named_deps:
            if d not in atext:
                f.append(f"dependency '{d}' named in a contract has no "
                         f"sources-of-record entry")
    if not has_content(critique):
        f.append("design/critique.md missing (adversary pass not run)")
    if not has_content(impl_read):
        f.append("design/implementability.md missing")
    elif re.search(r"unresolved", impl_read.read_text(), re.I) and \
            not re.search(r"(zero|no)\s+unresolved", impl_read.read_text(), re.I):
        w.append("implementability read mentions unresolved items — confirm "
                 "every ambiguity was fixed in its contract")
    if not has_content(checklist):
        f.append("validation/checklist.md missing — derive at design time")
    else:
        rows = [l for l in checklist.read_text().splitlines()
                if l.strip().startswith("| CHK")]
        if not rows:
            f.append("checklist has no CHK rows")
        for r in rows:
            if not re.search(r"C-\d+", r):
                f.append(f"checklist row lacks contract traceability: {r[:50]}")


def _git_changed_files(loop):
    try:
        out = subprocess.run(["git", "diff", "--name-only", "HEAD"],
                             cwd=loop.parent, capture_output=True, text=True,
                             timeout=10)
        if out.returncode == 0:
            return [l for l in out.stdout.splitlines()
                    if l and not l.startswith((".loop", ".handoffs"))]
    except Exception:
        pass
    return None


def check_implementation(loop, f, w):
    contracts = list((loop / "contracts").glob("C-*.md"))
    write_sets = []
    for c in contracts:
        cid = re.match(r"(C-\d+)", c.name).group(1)
        ws = re.search(r"## write_set.*?\n(.*?)(?=\n## )", c.read_text(), re.DOTALL)
        if ws:
            write_sets += [l.strip().lstrip("- ").strip() for l in
                           ws.group(1).splitlines() if l.strip().startswith("-")]
        rep = list((loop / "implementation" / "reports").glob(f"{cid}*.md"))
        if not rep:
            f.append(f"{cid}: no completion report"); continue
        t = rep[0].read_text()
        if unfilled(t):
            f.append(f"{rep[0].name}: unfilled placeholders")
        if not re.search(r"Declared budget:\s*\S+.*Actual:\s*\S+", t):
            f.append(f"{rep[0].name}: declared/actual spend not reconciled")
        if not re.search(r"\|\s*AC-?\d", t):
            w.append(f"{cid}: self-assessment table looks unfilled")
    changed = _git_changed_files(loop)
    if changed is not None and write_sets:
        for path in changed:
            if not any(path == wsp or path.startswith(wsp.rstrip("*").rstrip("/") )
                       for wsp in write_sets):
                f.append(f"write-set violation: '{path}' changed but is in no "
                         f"contract's write_set")
    elif changed is None:
        w.append("git unavailable — write-set diff skipped; announce this")
    for d in (loop / "implementation" / "deviations").glob("*.md"):
        if not re.search(r"Resolution:\s*(CONTRACT_AMENDED|SUPERSEDING_ADR|ESCALATED)",
                         d.read_text()):
            f.append(f"unresolved deviation: {d.name}")


def check_validation(loop, f, w):
    contracts = list((loop / "contracts").glob("C-*.md"))
    verdicts = list((loop / "validation" / "verdicts").glob("*.md"))
    if not verdicts:
        f.append("no verdicts")
    fails = []
    for v in verdicts:
        t = v.read_text()
        if unfilled(t):
            f.append(f"{v.name}: unfilled placeholders")
        fails += re.findall(r"\|\s*(CHK-\d+)\s*\|\s*FAIL", t)
    for c in contracts:
        cid = re.match(r"(C-\d+)", c.name).group(1)
        if not any(v.name.startswith(cid) for v in verdicts):
            f.append(f"{cid}: no verdict")
    if fails:
        w.append(f"FAILed checks {sorted(set(fails))} — structural PASS, but "
                 f"advance must be --to debug, never complete")


def check_debug(loop, f, w):
    ledgers = list((loop / "debug" / "ledgers").glob("L-*.md"))
    pms = list((loop / "postmortems").glob("PM-*.md"))
    if not ledgers:
        f.append("no hypothesis ledgers")
    for l in ledgers:
        t = l.read_text()
        if "Status: CLOSED" not in t:
            f.append(f"{l.name}: not CLOSED")
        if "## Confirmed contributing cause" not in t:
            f.append(f"{l.name}: no confirmed-cause section")
    if not pms:
        f.append("no postmortem")
    for p in pms:
        t = p.read_text()
        if "## Kill the class" not in t:
            f.append(f"{p.name}: missing Kill-the-class section")
        if unfilled(t):
            f.append(f"{p.name}: unfilled placeholders")


CHECKS = {"research": check_research, "design": check_design,
          "implementation": check_implementation,
          "validation": check_validation, "debug": check_debug}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--phase", choices=list(CHECKS))
    ap.add_argument("--advance", action="store_true")
    ap.add_argument("--to", choices=ORDER)
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    loop = Path(args.project_dir).resolve() / ".loop"
    state_p = loop / "STATE.json"
    if not state_p.exists():
        print("No .loop/STATE.json — run bootstrap.py first.")
        return 2
    state = json.loads(state_p.read_text())

    if args.status:
        print(json.dumps({"phase": state["phase"],
                          "mission_confirmed": state.get("mission_confirmed"),
                          "gates_passed": [g["phase"] for g in
                                           state.get("gate_history", [])],
                          "telemetry": state.get("telemetry", {})}, indent=2))
        return 0
    if not args.phase:
        print("Provide --phase or --status."); return 2
    if state["phase"] != args.phase:
        print(f"STATE says phase is '{state['phase']}', not '{args.phase}'.")
        return 2
    if not state.get("mission_confirmed"):
        print("FAIL  MISSION.md not confirmed"); return 1

    failures, warnings = [], []
    CHECKS[args.phase](loop, failures, warnings)
    for x in failures:
        print(f"  FAIL  {x}")
    for x in warnings:
        print(f"  WARN  {x}")
    if failures:
        print(f"\nGATE: FAIL ({len(failures)})"); return 1
    print(f"\nGATE: PASS ({len(warnings)} warning(s))")

    if args.advance:
        nxt = args.to or ORDER[ORDER.index(args.phase) + 1]
        state.setdefault("gate_history", []).append(
            {"phase": args.phase, "to": nxt,
             "at": datetime.datetime.now(datetime.timezone.utc)
                   .isoformat(timespec="seconds"),
             "warnings": warnings})
        state["phase"] = nxt
        state_p.write_text(json.dumps(state, indent=2))
        print(f"ADVANCED: {args.phase} -> {nxt}")
        print("Every gate is a handoff — write it now (disciplines/handoff.md), "
              "then enter_phase.py.")
    return 0


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
