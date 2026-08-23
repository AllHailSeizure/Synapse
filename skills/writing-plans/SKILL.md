---
name: writing-plans
description: >-
  Bite-sized implementation plans for multi-step work. Use when you have an
  agreed approach or requirements and need a task breakdown before touching
  code — not for trivial single-edit changes.
---

# Writing Plans

Turn an agreed approach into executable tasks an agent (or you) can follow
without guessing. DRY. YAGNI. Prefer TDD steps when behavior is being designed;
prefer verification-first when behavior is already clear (`testing` skill).

Save plans where the project prefers them. Default if none: `./.synapse/plans/YYYY-MM-DD-<feature>.md`.

## Scope

One plan = one coherent deliverable that can ship and be tested on its own.
Independent subsystems → separate plans.

## Patterns before tasks

A plan with more than a handful of tasks is rarely that many distinct problems.
Most large plans are a few mechanical changes applied to several targets — the
same conversion done per chapter, per module, per endpoint. Group the tasks that
way before ordering them, because it decides what execution costs: understanding
is paid once per pattern, not once per task.

Per pattern, name three things:

- **The pattern** — one line on what the change actually is.
- **The setter** — the instance that runs first. Pick the hardest or the
  best-documented target; it produces the worked example the rest consume.
- **The siblings** — the remaining instances.

Then state, per group: *siblings run only after the setter has landed, and a
setter never runs concurrently with its own siblings.*

**"Parallel-safe" is a claim about file conflicts, not about cost.** Say which
you mean. Two siblings of an unsettled pattern touch disjoint files and still
cost three times what they should, because each re-derives the same pattern from
the codebase.

## Executable by whom

Mark every task **mechanical** or **judgment**.

| | Done-condition | Runs as |
|---|---|---|
| Mechanical | A command — a test, a lint, a grep | A cheap subagent, from a diff-grade brief |
| Judgment | "indistinguishable", "feels the same", "decide and record" | Inline, or handed to the user |

A task is mechanical only if its done-condition is checkable by running
something. "Replay the chapter and confirm the timing is unchanged" is never
mechanical, however precise the steps are.

**Never defer a design question into a task marked mechanical.** "Check whether
X supports arguments; if not, file the gap" and "settle the fade inside this
task" are judgment. Left in a mechanical task they silently turn a cheap lane
into a design lane at design-lane cost — either answer them in the plan or mark
the task judgment.

## Before tasks: file map

List files to create/modify and each one's responsibility. Prefer focused
files; follow existing codebase patterns; don't unilaterally restructure unless
a file is already unwieldy and the plan includes the split.

## Task sizing

Smallest unit with its own test/verify cycle. Fold setup and docs into the
task that needs them. Split only where one task could fail review while its
neighbor still stands.

Each task ends in an independently testable deliverable.

## Plan header

```markdown
# [Feature] Implementation Plan

**Goal:** [one sentence]

**Architecture:** [2–3 sentences]

**Tech Stack:** [key pieces]

## Global Constraints

[version floors, naming, platform rules — verbatim from the agreed approach]

---
```

## Task shape

```markdown
### Task N: [Name]

**Files:**
- Create: `path`
- Modify: `path`
- Test: `path`

**Interfaces:**
- Consumes: [signatures from earlier tasks]
- Produces: [signatures later tasks need]

- [ ] Step: write failing test (or verification check if verification-first)
- [ ] Step: run it — expect [specific failure]
- [ ] Step: minimal implementation
- [ ] Step: run it — expect pass
- [ ] Step: commit
```

Include real code, commands, and expected outcomes in steps. No placeholders
("TBD", "add validation", "similar to Task N", "write tests for the above").

## Self-review (you, not a subagent)

1. Every requirement maps to a task?
2. No placeholder language?
3. Types/names consistent across tasks?

Fix inline, then hand off.

## Handoff

Plan saved. Offer execution:

1. **Subagent team** (`subagent-team-execution`) — pattern setter inline, then
   siblings fan out
2. **This session** (`executing-plans`) — inline with checkpoints

For a plan with more than one pattern, say what the first pattern will cost
before anything starts, and stop at each pattern boundary.

If the user already named a mode, start it. Don't force planning when the
change is trivial — use `thinking` first.
