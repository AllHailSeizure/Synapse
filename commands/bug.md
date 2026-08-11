---
description: Capture a bug report without diagnosing or fixing it
---

# /bug

Invoke the current `bug-capture` skill with the user's command arguments as the
bug report. Follow that skill as the source of truth, including its capture-only
boundary: capture the report, but do not diagnose, investigate, plan, or fix the
bug in this command.

After capture, kick `@bug-bandaid` by default. Do not kick it when the user
explicitly opts out with language such as "capture only", "don't kick
@bug-bandaid", "no bandaid", or an equivalent unambiguous instruction.
