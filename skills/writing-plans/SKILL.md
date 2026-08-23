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

## When tasks repeat

If the plan contains one change applied to several targets — the same
conversion per chapter, per module, per endpoint — say so, and name which
instance runs first. Pick the hardest or best-documented target; its diff is
what every other instance gets handed, so understanding is paid once instead of
once per target. State that the rest run only after it lands, and never
alongside it.

**"Parallel-safe" is a claim about file conflicts, not about cost.** Two
repeats of an unsettled change touch disjoint files and still cost three times
what they should, because each re-derives the same change from the codebase.

## Executable by whom

Mark every task **mechanical** or **judgment**.

| | Done-condition | Runs as |
|---|---|---|
| Mechanical | A command — a test, a lint, a grep | A cheap subagent, from a brief carrying the diff |
| Judgment | An open design question — "decide and record", "check whether X, else file the gap" | Inline, by you |

A task is mechanical only if its done-condition is checkable by running
something. If you cannot name that command, the task is carrying an unsettled
design question — answer it in the plan rather than passing it down.

**Never defer a design question into a task marked mechanical.** "Check whether
X supports arguments; if not, file the gap" and "settle the fade inside this
task" are judgment. Left in a mechanical task they silently turn a cheap agent
into a design agent at design cost — either answer them in the plan or mark
the task judgment.

## No manual steps

**A plan is written for an agent to execute. Never put a manual check in one.**
No hand replays, no "play the chapter and confirm the timing", no "verify it
feels the same", batched or otherwise. Every step in a plan is something the
agent runs.

Verification is whatever command would catch a wrong result — run it where it
is cheap and once where it matters, not after every task. Anything a command
cannot catch is left to surface in use and get fixed then; that is cheaper than
a gate, and planning around it is not your call to make on the user's behalf.

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

1. **Subagent team** (`subagent-team-execution`) — fresh agent per task,
   continuous
2. **This session** (`executing-plans`) — inline with checkpoints

If the user already named a mode, start it. Don't force planning when the
change is trivial — use `thinking` first.
