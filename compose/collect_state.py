#!/usr/bin/env python3
"""
collect_state.py — Deterministic pre-fill for the context-handoff template.

Gathers all disk-recoverable state (git, files, environment, code markers) and
substitutes it into HANDOFF_TEMPLATE.md, producing a partially-filled handoff
file. The agent then fills ONLY the [AGENT] cognitive sections.

Design principle: never spend model tokens writing what a script can read from
ground truth. Machine sections are REGENERATED fresh at every handoff (never
copied forward), so they cannot accumulate transcription drift.

Usage:
    python collect_state.py [--project-dir DIR] [--handoff-dir DIR]
                            [--template PATH] [--previous PATH_OR_ID]

Output:
    <handoff-dir>/HANDOFF-<NNN>-<UTC timestamp>.md   (machine sections filled)
    Prints the output path and a checklist of agent sections still to fill.
"""

import argparse
import signal
import datetime
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_TREE_DEPTH = 3
MAX_TREE_ENTRIES = 120
MAX_ACTIVE_FILES = 25
MAX_MARKERS = 40
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
               "build", ".next", ".cache", "target", ".mypy_cache", ".pytest_cache"}


def run(cmd, cwd, timeout=15):
    """Run a shell command; return stdout or a marked failure string (never raises)."""
    try:
        r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout or "").strip()
        if r.returncode != 0 and not out:
            err = (r.stderr or "").strip().splitlines()
            return f"(unavailable: {err[0] if err else 'command failed'})"
        return out or "(none)"
    except Exception as e:  # noqa: BLE001 — collector must never crash the handoff
        return f"(unavailable: {e})"


def collect_git(cwd):
    inside = run("git rev-parse --is-inside-work-tree", cwd)
    if inside != "true":
        return "(not a git repository)", "(not a git repository)", "(not a git repository)"
    branch = run("git branch --show-current", cwd)
    status = run("git status --short --branch", cwd)
    ahead_behind = run("git rev-list --left-right --count @{upstream}...HEAD 2>/dev/null", cwd)
    stash = run("git stash list | head -5", cwd)
    git_state = (f"branch: {branch}\n"
                 f"upstream (behind/ahead): {ahead_behind}\n"
                 f"status:\n{status}\n"
                 f"stashes:\n{stash}")
    commits = run("git log --oneline --decorate -15", cwd)
    diffstat = run("git diff --stat HEAD", cwd)
    if diffstat == "(none)":
        diffstat = "(working tree clean relative to HEAD)"
    return git_state, commits, diffstat


def collect_active_files(cwd):
    """Most recently modified tracked-looking files — the working set."""
    entries = []
    root = Path(cwd)
    for p in root.rglob("*"):
        if any(part in IGNORE_DIRS or part.startswith(".") for part in p.parts):
            continue
        if p.is_file():
            try:
                entries.append((p.stat().st_mtime, p.relative_to(root)))
            except OSError:
                continue
    entries.sort(reverse=True)
    now = datetime.datetime.now().timestamp()
    lines = []
    for mtime, rel in entries[:MAX_ACTIVE_FILES]:
        age_min = (now - mtime) / 60
        age = f"{age_min:.0f}m ago" if age_min < 120 else f"{age_min/60:.1f}h ago"
        lines.append(f"{age:>10}  {rel}")
    return "\n".join(lines) or "(no files found)"


def collect_tree(cwd):
    lines = []
    root = Path(cwd)

    def walk(d, depth, prefix):
        if depth > MAX_TREE_DEPTH or len(lines) >= MAX_TREE_ENTRIES:
            return
        try:
            children = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except OSError:
            return
        children = [c for c in children
                    if c.name not in IGNORE_DIRS and not c.name.startswith(".")]
        for c in children:
            if len(lines) >= MAX_TREE_ENTRIES:
                lines.append(f"{prefix}... (truncated at {MAX_TREE_ENTRIES} entries)")
                return
            lines.append(f"{prefix}{c.name}{'/' if c.is_dir() else ''}")
            if c.is_dir():
                walk(c, depth + 1, prefix + "  ")

    walk(root, 1, "")
    return "\n".join(lines) or "(empty)"


def collect_markers(cwd):
    cmd = ("grep -rn --binary-files=without-match -E '(TODO|FIXME|HACK|XXX)[:( ]' . "
           "--include='*.py' --include='*.js' --include='*.ts' --include='*.tsx' "
           "--include='*.jsx' --include='*.go' --include='*.rs' --include='*.java' "
           "--include='*.rb' --include='*.md' --include='*.c' --include='*.cpp' "
           "--include='*.h' 2>/dev/null "
           + " ".join(f"--exclude-dir={d}" for d in IGNORE_DIRS)
           + f" | head -{MAX_MARKERS}")
    return run(cmd, cwd, timeout=20)


def collect_environment(cwd):
    parts = [f"cwd: {cwd}",
             f"python: {run('python3 --version 2>&1', cwd)}",
             f"node: {run('node --version 2>/dev/null', cwd)}"]
    for manifest in ("package.json", "pyproject.toml", "requirements.txt",
                     "Cargo.toml", "go.mod", "Makefile"):
        if (Path(cwd) / manifest).exists():
            parts.append(f"manifest present: {manifest}")
    return "\n".join(parts)


def next_handoff_number(handoff_dir):
    existing = sorted(handoff_dir.glob("HANDOFF-*.md"))
    nums = []
    for p in existing:
        m = re.match(r"HANDOFF-(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1 if nums else 1), (existing[-1].name if existing else "(none — first handoff in chain)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--handoff-dir", default=None,
                    help="default: <project-dir>/.handoffs")
    ap.add_argument("--template", default=None,
                    help="default: HANDOFF_TEMPLATE.md next to this script's assets dir")
    ap.add_argument("--previous", default=None,
                    help="override previous-handoff reference")
    args = ap.parse_args()

    cwd = str(Path(args.project_dir).resolve())
    handoff_dir = Path(args.handoff_dir) if args.handoff_dir else Path(cwd) / ".handoffs"
    handoff_dir.mkdir(parents=True, exist_ok=True)

    template_path = (Path(args.template) if args.template
                     else Path(__file__).resolve().parent.parent / "templates" / "HANDOFF_TEMPLATE.md")
    template = template_path.read_text()

    num, prev = next_handoff_number(handoff_dir)
    if args.previous:
        prev = args.previous
    now = datetime.datetime.now(datetime.timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    handoff_id = f"HANDOFF-{num:03d}-{stamp}"

    git_state, commits, diffstat = collect_git(cwd)
    values = {
        "PROJECT_NAME": Path(cwd).name,
        "HANDOFF_ID": handoff_id,
        "PREVIOUS_HANDOFF": prev,
        "SESSION_NUMBER": str(num),
        "COLLECTED_AT": now.isoformat(timespec="seconds"),
        "WORKING_DIRECTORY": cwd,
        "GIT_STATE": git_state,
        "RECENT_COMMITS": commits,
        "DIFFSTAT": diffstat,
        "ACTIVE_FILES": collect_active_files(cwd),
        "PROJECT_TREE": collect_tree(cwd),
        "CODE_MARKERS": collect_markers(cwd),
        "ENVIRONMENT": collect_environment(cwd),
    }

    filled = template
    for key, val in values.items():
        filled = filled.replace("{{" + key + "}}", val)

    out_path = handoff_dir / f"{handoff_id}.md"
    out_path.write_text(filled)

    print(f"WROTE: {out_path}")
    print(f"PREVIOUS: {prev}")
    print("\nMachine sections filled deterministically. AGENT must now fill:")
    for section in ("Session status (header table)", "1. Mission",
                    "3. Progress Ledger", "4. Decision Log (copy forward + append)",
                    "5. Dead Ends & Gotchas (copy forward + append)",
                    "6. Contracts & Invariants", "7. Action List",
                    "8. Contingencies", "9. Open Questions"):
        print(f"  [ ] {section}")
    print("\nThen run validate_handoff.py before ending the session.")


if __name__ == "__main__":
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (AttributeError, ValueError):
        pass
    sys.exit(main())
