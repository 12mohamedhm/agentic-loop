#!/usr/bin/env python3
"""
bootstrap.py — Any-device adoption. Idempotent, hermetic, loud.

Verifies the environment (announcing every absence), then either resumes an
existing loop or initializes a new one. Prints the single next command.

Usage: python bootstrap.py [--project-dir DIR] [--new-mission]
"""
import argparse
import datetime
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

TREE = ["research/briefs", "research/sources", "design/adr", "contracts",
        "implementation/reports", "implementation/deviations",
        "validation/verdicts", "debug/ledgers", "postmortems", "runtime"]


def check_env():
    notes = []
    for tool, why in [("git", "custody and state collection"),
                      ("curl", "CITABLE raw-source banking")]:
        if shutil.which(tool) is None:
            notes.append(f"MISSING TOOL: {tool} ({why}) — continuing lane-capped; "
                         f"announce this in your first reply")
    host = REPO / "hosts" / "claude-code.json"
    if host.exists():
        notes.append(f"host profile: {host}")
    return notes


def init_loop(project, loop):
    for d in TREE:
        (loop / d).mkdir(parents=True, exist_ok=True)
    state = {"phase": "research", "mission_confirmed": False,
             "created_at": datetime.datetime.now(datetime.timezone.utc)
                           .isoformat(timespec="seconds"),
             "gate_history": [],
             "telemetry": {"novel_findings_per_search": None,
                            "reconstruction_errors": None,
                            "deviations_per_contract": None,
                            "correlated_miss_rate": None,
                            "hypotheses_killed_per_wave": None,
                            "escalations_this_mission": 0}}
    (loop / "STATE.json").write_text(json.dumps(state, indent=2))
    mission = (REPO / "schemas" / "mission.md").read_text()
    mission = mission.replace("{{NAME}}", project.name)
    (loop / "MISSION.md").write_text(mission)
    (loop / "loop.json").write_text(json.dumps({"system_repo": str(REPO)}, indent=2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--new-mission", action="store_true",
                    help="archive the finished .loop and start fresh")
    args = ap.parse_args()

    project = Path(args.project_dir).resolve()
    loop = project / ".loop"

    print(f"agentic-loop bootstrap — system repo: {REPO}")
    for n in check_env():
        print(f"  {n}")

    ledger = REPO / "preferences" / "PREFERENCES.md"
    seeded = ledger.exists() and "PREF-" in ledger.read_text()

    if (loop / "STATE.json").exists() and not args.new_mission:
        state = json.loads((loop / "STATE.json").read_text())
        handoffs = sorted((project / ".handoffs").glob("HANDOFF-*.md")) \
            if (project / ".handoffs").exists() else []
        print(f"\nRESUME: existing loop found — phase '{state['phase']}', "
              f"mission_confirmed={state.get('mission_confirmed')}")
        if handoffs:
            print(f"  1. Read {handoffs[-1]} and follow its Receiver Synthesis "
                  f"Protocol (disk wins).")
            print(f"  2. Then: python {REPO}/compose/enter_phase.py "
                  f"--project-dir {project}")
        else:
            print(f"  Next: python {REPO}/compose/enter_phase.py "
                  f"--project-dir {project}")
        return 0

    if args.new_mission and loop.exists():
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        loop.rename(project / f".loop-archived-{stamp}")
        print(f"  archived previous mission to .loop-archived-{stamp}/")

    init_loop(project, loop)
    print(f"\nINIT: new loop at {loop}")
    if not seeded:
        print("  0. The preference ledger is unseeded. Run a one-time seeding "
              "grill (disciplines/grilling.md, all questions INTENT): testing "
              "philosophy, dependency appetite, error handling, formatting, "
              "risk tolerance, communication format. Write entries per "
              "schemas/preference-entry.md into preferences/PREFERENCES.md.")
    print(f"  1. Grill {loop / 'MISSION.md'} (disciplines/grilling.md) — the "
          f"ledger pre-answers; only the delta reaches the answerer. On "
          f"confirmation set mission_confirmed=true in STATE.json and set the "
          f"Modes vector.")
    print(f"  2. Then: python {REPO}/compose/enter_phase.py --project-dir {project}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
