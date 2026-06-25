---
name: synapse:over-engineering-guard
description: Prevents scope expansion during implementation. Flags anything not in the current goal's spec before building it.
type: behavior
applies_to: [collaborative coding sessions]
---

# Over-Engineering Guard

**Scope:** This skill applies during implementation, after a spec has been agreed on and a goal issue is open. It is not a substitute for speccing-first or goal-tracking — it operates within a session to hold the line on what was agreed.

## Rule

Do not write code for anything not explicitly in the current goal's spec. Before writing it, classify it and act accordingly.

---

## Classification

When something surfaces that isn't clearly in the spec, classify it as one of three things:

**Implementation decision** — a small choice required to complete the spec that wasn't worth speccing (e.g. "display as table or list?"). Handle in session: state the choice you're making and why, then proceed. Do not log it.

**Ambiguous addition** — something that could be in scope but wasn't stated (e.g. "should I add input validation here?"). Flag it in session: "This wasn't in the spec — do you want it included, or should I log it for later?" Wait for an answer before proceeding.

**Out of scope** — a new feature, polish layer, or admin UI that goes beyond what was agreed (e.g. a dashboard to inspect quota data when the spec just said "enforce quota"). Do not discuss it. State: "This isn't in the current goal. Logging it." Create a new issue on the current milestone and return to the current goal.

---

## The test for "out of scope"

Ask: is this required for the feature to work as specified, or does it make it more complete, more polished, or more visible?

- Required to work → implementation decision or ambiguous addition
- More complete / polished / visible → out of scope, log it

---

## What this does NOT do

- It does not prevent good ideas from existing — it queues them
- It does not apply to spec-stage decisions — that's speccing-first
- It does not manage the goals list — that's goal-tracking
