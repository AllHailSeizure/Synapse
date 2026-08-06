---
name: testing
description: >-
  Red-green-refactor as the default for real feature and bug-fix work; use
  verification-first when behavior is already clear. Use when implementing
  features, fixing bugs, or changing behavior — not for throwaway probes or
  pure config edits.
---

# Testing

Prefer tests that lock behavior. Choose the loop by how clear the behavior is.

## Mode selection

| Situation | Mode |
|-----------|------|
| Exploring API/design; behavior not settled | **TDD** — red → green → refactor |
| Behavior clear; small fix; existing coverage nearby | **Verification-first** — implement, then run/extend the check that proves it |
| Bug with no repro | Write a failing repro test first, then fix |
| Throwaway prototype / generated / pure config | Skip formal cycle; don't pretend |

Do not ask permission for every mode choice. Use judgment. If you skipped a
test that later mattered, add it — don't rewrite history with ritual deletion.

## Red → Green → Refactor (default for real work)

### RED

One minimal test for one behavior. Clear name. Assert real outcomes (mocks
only when unavoidable).

### Verify RED

Run it. Confirm it fails for the right reason (missing behavior), not a typo.
Passes immediately → you're testing existing behavior; fix the test.

### GREEN

Smallest code that passes. No extra features, no drive-by refactors.

### Verify GREEN

Same test passes; related tests still pass.

### REFACTOR

Only after green: names, duplication, helpers. Stay green. No new behavior.

## Verification-first (when clear)

1. Implement the obvious change.
2. Run the standard check that covers it (`verification`).
3. If coverage is missing for the regression you care about, add a focused
   test after — still assert behavior, not internals.
4. Don't claim fixed/done without the command outcome.

## Good tests

| Do | Don't |
|----|-------|
| One behavior per test | "and" sandwiches |
| Name the behavior | `test1` / `works` |
| Assert observable results | Assert mock call choreography |
| Fail when production breaks | Pass against any implementation |

Before writing a test, name the production change that would make it fail.

## Bug fixes

Prefer a failing repro first. That test proves the fix and guards regression.

## When stuck

| Problem | Move |
|---------|------|
| Don't know how to test | Wish for the API; write assertion first |
| Test is huge | Simplify the interface |
| Everything needs mocks | Too coupled — inject dependencies |

## Align with suite philosophy

Tests verify public behavior, not private details. Coverage supports
confidence — not an arbitrary percentage.
