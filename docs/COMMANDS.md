# Synapse commands

This index lives in `docs/` rather than `commands/` on purpose: every extra
`.md` file in `commands/` is published as a Claude slash command.

Cursor loads only the files listed in `.cursor-plugin/plugin.json` (`/bug`).
Cursor already ships `/debug`. Codex has no slash-command files; use the
explicit skills `$bug` and `$debug`.

| Command | Purpose |
| --- | --- |
| [`/bug`](../commands/bug.md) | Capture a bug report with the `bug-capture` skill; kicks `@bug-bandaid` by default unless the user explicitly opts out. |
| [`/debug`](../commands/debug.md) | Hypothesis-driven debug session. Claude command file; Codex `$debug` skill; skip on Cursor. |

`/weedeat` moved to its own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).
