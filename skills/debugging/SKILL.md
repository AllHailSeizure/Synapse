---
name: debugging
description: >-
  Fast hypothesis-driven debugging. Trigger on any bug report, stack trace,
  error message, failing test, or "this isn't behaving right" — including when
  the user runs /debug. Cursory look first, up to four competing hypotheses,
  instrumentation that tells them apart, one repro from the user, then
  diagnose → fix → PR. Use this instead of reading the whole codebase before
  guessing, and instead of multi-agent investigation pipelines. Not for filing
  a bug to look at later (use bug-capture).
---

# Debugging

Hypotheses first, reading second. Instrument to discriminate, repro once,
diagnose from evidence.

The failure mode this replaces: an hour of tracing call paths, anchored on
whatever file you opened first, arriving at one theory you're now invested in.
Cheap hypotheses generated early cost minutes and give the reading a target.

## 1. Cursory exploration (minutes, not tens of minutes)

Read only what's needed to name plausible causes:

- The error/stack trace, top frames first
- The file(s) it points at — the failing function, not the whole module
- Recent changes to that area (`git log -n 5 --oneline -- <path>`, `git diff`)

Stop as soon as you can write hypotheses. You are not trying to understand the
system; you are trying to generate candidates worth testing.

## 2. Up to four hypotheses

State 2–4 candidate causes. Fewer than two means you anchored; more than four
means you haven't thought, you've listed.

Each one needs a **distinct predicted observation** — something that would be
true in the logs/state if this cause is the real one and false if it isn't.
That's what makes a hypothesis worth writing down:

```
H1: <cause> → expect <observable> at <location>
H2: <cause> → expect <observable> at <location>
```

Two hypotheses that predict identical evidence are one hypothesis. Merge them
or sharpen one until they diverge.

Show the list to the user. Don't ask for approval — it's a heads-up, and it
lets them kill a wrong one before you spend instrumentation on it.

## 3. Set up tooling

Instrument the points where the hypotheses disagree, so a **single** repro
splits the field. Match the tool to the surface:

| Surface | Tooling |
|---------|---------|
| Any code path | Targeted log lines at the divergence points, tagged (e.g. `[dbg]`) |
| Web / browser | Console + network capture via browser tools; log lines in the handler |
| Already-failing test | Run it yourself — skip to step 5. No user repro needed |
| Deterministic and scriptable | Write the throwaway repro script; run it yourself |
| Genuinely opaque | Attach the debugger / breakpoints |

Log the *values that discriminate*, not "here 1", "here 2". If a hypothesis has
no instrument that could kill it, say so out loud — an untestable hypothesis is
a note, not a candidate.

Never ask the user to repro something you can trigger yourself.

## 4. Prompt for repro

One round trip. Give them:

- Exact steps to run (command, URL, click path)
- What you need back (console output, log file path, screenshot, what they saw)
- What you'll do with it

Keep it to one repro. If you need a second, you instrumented badly — say what
you missed and what you added, so it's a correction, not a fishing expedition.

## 5. Diagnose

Read the evidence and go through the hypotheses explicitly:

```
H1: killed — <evidence>
H2: confirmed — <evidence>
H3: killed — <evidence>
```

State the root cause and the line of evidence that establishes it. Not "likely"
— if it's still likely, you're missing an instrument, so add it and repro again.

**All four killed** is a good outcome, not a failure: you now know four things
it isn't. Generate a fresh set informed by what the evidence *did* show, and go
around once. If a second full round dies too, stop and hand back what you've
ruled out — don't keep spinning.

## 6. Fix

Proportional to the bug. Follow `testing`: a failing repro test first when the
behavior is testable, then the fix.

**Rip out the instrumentation.** Every `[dbg]` line, every temp script. Grep
your own tag before committing — leftover debug logging in a PR is the most
common tell that this step got skipped.

Verify per `verification`: run the standard check, quote the outcome.

## 7. PR

Follow `finishing-branches` (verify → confirm base → push → PR). Because the
repro was manual, the PR body carries the confirmation back to the user:

```markdown
## Bug
<symptom as reported>

## Root cause
<cause, and the evidence that established it>

## Ruled out
- <hypothesis> — <why it died>

## Fix
<what changed, and why this addresses the cause>

## Verification
- [x] Regression test added: `<name>`
- [x] Standard suite run: `<command>` — <result>
- [ ] **Manual confirmation needed** — reproduce the original steps and confirm
      the bug is gone. Automated checks don't cover the path you hit.
```

That last box is unchecked on purpose and stays unchecked until the user says
so. Do not tick it, and do not merge on their behalf.

## Don't

- Read broadly before forming hypotheses
- Carry one hypothesis into instrumentation
- Ask for a repro you could run yourself
- Ask for repeated repros to compensate for thin instrumentation
- Spawn an investigation pipeline of subagents for this
- Claim fixed without the repro evidence
- Leave debug logging in the diff
- Tick the manual-confirmation box or merge the PR
