---
name: bug-capture
description: >-
  Capture a noticed bug as a GitHub issue and kick the bug-bandaid
  automation — no investigation, no fix, no enrichment in this chat. Use
  when the user runs /bug, asks to file/capture a bug sticky-note style,
  or says not to forget something broken. Not for shaping goals (use
  goal-oriented-development) or debugging now in-session.
---

# Bug Capture

External memory for "don't let me forget this," plus a kick so the
repo's bug-bandaid automation can try a one-shot fix. Capture that the
issue exists; do not think about it here.

Not goal-oriented-development: GOD steers long-term project intent; this
is a sticky note with a GitHub id and a trigger comment.

## Do

1. Take the user's words as the issue. Prefer their text after `/bug` or
   the message they are pointing at. Do not rewrite, investigate, or add
   root cause / fix / evidence passes.
2. Title = a short slice of what they said (first line or ~72 chars).
   Body = their words verbatim (or nearly so).
3. Create on the current repo with `gh issue create`, labels `bug` and a
   priority (see below). If a label is missing, create the issue without
   it and note that in the reply — do not block on labels.
4. Kick the bandaid unless they opted out (see below). Comment on the
   issue just created with a body that starts with `@bug-bandaid` and
   carries the bug text so the automation does not need Issues API:

   ```
   @bug-bandaid

   Title: <same title as the issue>

   <same body as the issue>
   ```

   Use that exact shape (trigger token on its own first line, then title,
   then body). Do not invent or enrich. If the comment fails, note that
   in the reply; still return the issue URL.
5. Reply with the issue URL in one short line.
6. Stop. Resume the prior conversation topic. Do not diagnose or fix.

## Priority

Default `p3`. Capture usually happens mid-playthrough, where most of what
you notice is minor — so the default should cost nothing to accept.

They can override by leading with the level: `/bug p0 hard crash on chapter
load`. Take it verbatim, strip it from the title and body, apply that label
instead. Don't infer priority from how the bug sounds — a default they can
override beats a guess they have to correct.

| Label | Means |
|-------|-------|
| `p0` | Blocker. Unplayable, broken build, data loss. No workaround. |
| `p1` | Major. Core flow broken, workaround exists. |
| `p2` | Normal. Real defect, doesn't block. |
| `p3` | Minor. Polish, cosmetic, low impact. |

Priority is severity, not difficulty. Nothing downstream rewrites it. A
bandaid that can't handle a bug simply leaves the issue open, which is
already the signal that it's yours — no label needed to say so.

## Skip the kick

If they say not to kick / start / run the bandaid (e.g. "don't kick",
"capture only", "no bandaid", "don't trigger"), create the issue and
skip step 4. Do not comment `@bug-bandaid`. Default is kick.

## Don't

- Confirm drafts or interview for repro
- Dispatch goal-writer or start debugging in this chat
- Expand scope or invent details they didn't say
- Drop the `@bug-bandaid` first line or omit title/body from the kick
  (cloud agents often cannot `gh issue view`)

## Empty capture

If they invoked capture with no description at all, ask once what to
record — then create (and kick unless they opted out). Do not stretch
into design.
