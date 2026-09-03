# Synapse commands

This index lives in `docs/` rather than `commands/` because Cursor publishes
only the files listed in its plugin manifest.

Cursor loads only the files listed in `.cursor-plugin/plugin.json` (`/bug`).
Cursor already ships `/debug`. Codex has no slash-command files; use the
explicit skills `$bug` and `$debug`.

| Command | Purpose |
| --- | --- |
| [`/bug`](../commands/bug.md) | Capture a bug report with the `bug-capture` skill; kicks `@bug-bandaid` by default unless the user explicitly opts out. |

`/weedeat` moved to its own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).
