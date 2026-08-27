# Synapse commands

This index lives in `docs/` rather than `commands/` on purpose: every extra
`.md` file in `commands/` is published as a Claude slash command.

Cursor loads only the files listed in `.cursor-plugin/plugin.json` (`/bug`,
`/weedeat`). Cursor already ships `/debug`. Codex has no slash-command files;
use the explicit skills `$bug`, `$weedeat`, and `$debug`.

| Command | Purpose |
| --- | --- |
| [`/bug`](../commands/bug.md) | Capture a bug report with the `bug-capture` skill; kicks `@bug-bandaid` by default unless the user explicitly opts out. |
| [`/weedeat`](../commands/weedeat.md) | Survey what accumulated on its own — asset churn in the branch, worktree and branch sprawl — with `asset-churn-audit` and `worktree-cleanup`. Report-only. |
| [`/debug`](../commands/debug.md) | Hypothesis-driven debug session. Claude command file; Codex `$debug` skill; skip on Cursor. |
