#!/bin/bash

# synapse-init: Set up or tear down Synapse skill symlinks in a project
# Usage: ./synapse-init.sh <project-directory> [enable|disable]

PROJECT_DIR="${1:-.}"
COMMAND="${2:-enable}"
SYNAPSE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_LINK="$PROJECT_DIR/.claude/skills/synapse"
SKILLS_SOURCE="$SYNAPSE_ROOT/.claude/skills/synapse"

case "$COMMAND" in
  enable)
    mkdir -p "$PROJECT_DIR/.claude/skills"
    if [ -e "$SKILLS_LINK" ]; then
      echo "Synapse skills already linked at $SKILLS_LINK"
    else
      ln -s "$SKILLS_SOURCE" "$SKILLS_LINK"
      echo "✓ Synapse skills enabled at $PROJECT_DIR"
    fi
    ;;
  disable)
    if [ -L "$SKILLS_LINK" ]; then
      rm "$SKILLS_LINK"
      echo "✓ Synapse skills disabled at $PROJECT_DIR"
    else
      echo "Synapse skills not linked at $PROJECT_DIR"
    fi
    ;;
  status)
    if [ -L "$SKILLS_LINK" ]; then
      echo "✓ Synapse skills enabled"
      ls -l "$SKILLS_LINK"
    else
      echo "✗ Synapse skills not linked"
    fi
    ;;
  *)
    echo "Usage: synapse-init.sh <project-directory> [enable|disable|status]"
    exit 1
    ;;
esac
