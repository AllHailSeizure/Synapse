# Synapse for Codex

Synapse enforces structured coding practices through skills with explicit gates and visible outputs.

## Working Rules

- Before implementation, agree on the approach and exact behavior.
- When a project uses GitHub milestones, identify the active goal before starting work.
- Treat a new implementation idea outside the active goal as a deliberate pivot; confirm it before writing code.
- After a goal closes, review whether the next queued goal still makes sense.
- Keep one active goal at a time.

## Goal-Oriented Development

Use `goal-oriented-development` to orient work around GitHub milestones and issues. Its Codex agents are registered under `.codex/agents/synapse/`:

- `codebase-explorer` researches focused codebase questions.
- `goal-writer` turns a committed idea into an executable issue.
- `goal-surveyor` turns a broad direction into candidate goals.
- `goal-fulfiller` executes an already-written issue.

The skill source is in `skills/goal-oriented-development/SKILL.md`.
