---
name: bug-capture
description: >-
  Capture a noticed bug as a GitHub issue for later — no investigation, no
  fix, no enrichment. Use when the user runs /bug, asks to file/capture a
  bug sticky-note style, or says not to forget something broken. Not for
  shaping goals (use goal-oriented-development) or debugging now.
---

# Bug Capture

External memory for "don't let me forget this." Capture that the issue
exists. Think about it later.

Not goal-oriented-development: GOD steers long-term project intent; this
is a sticky note with a GitHub id.

## Do

1. Take the user's words as the issue. Prefer their text after `/bug` or
   the message they are pointing at. Do not rewrite, investigate, or add
   root cause / fix / evidence passes.
2. Title = a short slice of what they said (first line or ~72 chars).
   Body = their words verbatim (or nearly so).
3. Create on the current repo with `gh issue create`, label `bug`. If the
   label is missing, create the issue without it and note that in the
   reply — do not block on labels.
4. Reply with the issue URL in one short line.
5. Stop. Resume the prior conversation topic. Do not diagnose or fix.

## Don't

- Confirm drafts or interview for repro
- Dispatch goal-writer or start debugging
- Expand scope or invent details they didn't say

## Empty capture

If they invoked capture with no description at all, ask once what to
record — then create. Do not stretch into design.
