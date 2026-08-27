---
name: debug
description: >-
  Start a hypothesis-driven debugging session. Use when the user invokes
  /debug or $debug, or names this skill explicitly. Cursor already ships a
  /debug command; this skill is the Codex (and explicit-skill) entry point.
disable-model-invocation: true
---

Follow the `debugging` skill. If the user gave no description, take the most
recent error, failing test, or reported misbehavior from this conversation —
and only ask what's broken if there's nothing to go on.

Start now with the cursory exploration. Do not read broadly before you have
hypotheses.
