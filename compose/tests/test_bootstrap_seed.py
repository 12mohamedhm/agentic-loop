"""Bootstrap --seed: operator context lands in the mission draft.

Proves: (1) init with --seed writes an "## Operator seed" section carrying
the text verbatim and announces it; (2) init without --seed writes no such
section; (3) a seed passed on resume is ignored loudly, never silently.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
BOOTSTRAP = REPO / "compose" / "bootstrap.py"


def run(tmp, *extra):
    return subprocess.run([sys.executable, str(BOOTSTRAP), "--project-dir",
                           str(tmp), *extra], capture_output=True, text=True)


def test_seed_lands_in_mission_draft(tmp_path):
    r = run(tmp_path, "--seed",
            "Migrate the billing cron to events; Stripe stays source of truth.")
    assert r.returncode == 0
    mission = (tmp_path / ".loop" / "MISSION.md").read_text()
    assert "## Operator seed" in mission
    assert "Stripe stays source of truth" in mission
    assert "seed" in r.stdout.lower()


def test_no_seed_no_section(tmp_path):
    r = run(tmp_path)
    assert r.returncode == 0
    assert "## Operator seed" not in (tmp_path / ".loop" / "MISSION.md").read_text()


def test_seed_on_resume_is_declared_ignored(tmp_path):
    run(tmp_path)
    r = run(tmp_path, "--seed", "late context")
    assert r.returncode == 0
    assert "SEED IGNORED" in r.stdout
    assert "late context" not in (tmp_path / ".loop" / "MISSION.md").read_text()
