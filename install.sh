#!/usr/bin/env bash
# install.sh — register agentic-loop for agent access in the current project.
# Idempotent: safe to run repeatedly. Run from the project you want to adopt
# the loop in; running from inside this repo installs into the repo itself.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$(pwd)"

# Environment check — reuse bootstrap's check_env, never duplicate it.
if ! command -v python3 >/dev/null 2>&1; then
  echo "MISSING TOOL: python3 (runs every compose script) — install it, then rerun." >&2
  exit 1
fi
python3 - "$REPO" <<'PY'
import sys
sys.path.insert(0, sys.argv[1] + "/compose")
import bootstrap
for note in bootstrap.check_env():
    print(f"  {note}")
PY

# Register the slash commands in the project.
mkdir -p "$PROJECT/.claude/commands"
for cmd in "$REPO"/.claude/commands/*.md; do
  ln -sf "$cmd" "$PROJECT/.claude/commands/$(basename "$cmd")"
done
printf '%s\n' "$REPO" > "$PROJECT/.claude/loop-repo"

echo "Installed: $(ls "$REPO"/.claude/commands/*.md | wc -l | tr -d ' ') commands -> $PROJECT/.claude/commands (system repo: $REPO)"
echo
echo "Adopt (from SKILL.md):"
echo "  1. Run: python $REPO/compose/bootstrap.py --project-dir $PROJECT"
echo "  2. Obey what it prints."
echo "Or, in Claude Code here: /mission (optionally: /mission <context to seed the interview>)"
