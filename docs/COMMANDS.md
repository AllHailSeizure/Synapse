# Synapse commands

This index lives in `docs/` rather than `commands/` because Cursor publishes
only the files listed in its plugin manifest.

Cursor loads only the files listed in `.cursor-plugin/plugin.json` (`/bug`,
`/patch`). Cursor already ships `/debug`. Codex has no slash-command files;
`$debug` is the explicit debugging skill. Sticky-note capture is Cursor `/bug`
or `/patch`, or the matching `commands/*.mjs` scripts.

| Command | Purpose |
| --- | --- |
| [`/bug`](../commands/bug.md) | Run `commands/bug.mjs` with the user's arguments. Creates a GitHub issue and comments `@bug-bandaid` unless they opted out. |
| [`/patch`](../commands/patch.md) | Same capture as `/bug`, but comments `@fastpatch`. |

`/weedeat` moved to its own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).
