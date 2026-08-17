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

1. **Subagent team** (`subagent-team-execution`) — fresh agent per task, continuous
2. **This session** (`executing-plans`) — inline with checkpoints

If the user already named a mode, start it. Don't force planning when the
change is trivial — use `thinking` first.
