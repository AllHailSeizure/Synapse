---
description: Capture a patch request without diagnosing or fixing it
---

# /patch

Do not diagnose, investigate, plan, or fix. Run the capture script with the
user's arguments unchanged:

```
node "${CURSOR_PLUGIN_ROOT}/commands/patch.mjs" <arguments>
```

If `CURSOR_PLUGIN_ROOT` is unset, run `commands/patch.mjs` relative to this
Synapse checkout.

Reply with the script's stdout (the issue URL) in one short line. If the script
fails, report its stderr. Stop. Do not create the issue or comment
`@fastpatch` yourself — the script does that unless the user opted out
(`--no-kick`, "capture only", "no bandaid", or equivalent).
