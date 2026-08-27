---
name: bug
description: >-
  Capture a bug report without diagnosing or fixing it. Use when the user
  invokes /bug or $bug, or asks to file a bug sticky-note style.
disable-model-invocation: true
---

Follow the `bug-capture` skill. Treat the user's arguments as the bug report.
Do not diagnose, investigate, plan, or fix the bug in this invocation.

After capture, kick `@bug-bandaid` by default unless the user explicitly opts
out (capture only, no bandaid, or equivalent).
