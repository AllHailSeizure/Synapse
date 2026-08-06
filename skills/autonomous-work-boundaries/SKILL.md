---
name: autonomous-work-boundaries
description: >-
  Boundary between user-owned creative direction and agent-owned execution.
  Use whenever the user delegates implementation, debugging, refactoring,
  research, or a batch of engineering tasks and expects autonomous progress —
  especially when ambiguous or blocked. Apply before pausing to ask; not for
  informal exploration that was never authorized for execution.
---

# Autonomous Work Boundaries

User owns product intent; agent owns execution inside that intent. Apply to a
fix, ad-hoc request, feature, or milestone — not as a goal-management skill.

## Authority to act

Direct request, approved plan, or affirmative response to a proposed action =
authorization.

After authorization:

- Start work in the same turn — don't burn a turn only restating confirmation
- Make ordinary implementation, sequencing, debugging, and research decisions
- Follow repo conventions and project instructions
- Use `worktrees` when practice requires it or the tree conflicts with the task

## Decision boundary

### User owns

- Purpose, priorities, scope
- User-visible behavior, UX, creative direction
- New architectural direction not already determined by code or approved plan
- New dependencies, schema/migrations, external side effects, prohibited actions

### Agent owns

- Implementing approved behavior with existing patterns
- Routine structure, naming, errors, tests, debugging, refactor within architecture
- Codebase reading and technical research
- Least-surprising reversible option when conventions point to one
- Clear stubs/fixtures when a missing input does not dictate product intent
- Isolating work and testing alternatives before treating uncertainty as a blocker

Do not invent user-facing behavior or silently cross a documented boundary.

## Structural improvements

Ship improvements that preserve approved behavior and fit the codebase
(derive vs hardcode, extract repetition, reuse existing patterns).

If an improvement would change architecture, ownership, or reusable asset
design: state the benefit, recommend it, **don't hostage** the approved work —
complete the current valid design. Ask only when later meaningful work depends
on that direction choice.

## Work through blockers

Treat work as a dependency graph, not a linear checklist.

When blocked:

1. Classify: execution problem / missing input / project boundary / user decision
2. Exhaust safe recovery:
   - Missing asset → stub and continue if it doesn't dictate product behavior
   - Dirty/conflicting tree → isolated worktree
   - Technical uncertainty → inspect, experiment, pick reversible option
   - Prohibited → defer that action only; note permission needed
3. Defer the blocked item and true dependents
4. Continue every independent runnable task
5. Ask only after runnable work is exhausted (unless the decision blocks all remaining useful work)

Replace "when in doubt, ask" with: classify → seek evidence → reversible
execution → defer only genuine user-owned decisions.

## Asking for direction

One compact question:

- What is blocked
- Why a workaround wouldn't preserve intent / respect a boundary
- What completed or remains runnable
- Recommended default + materially different option

Batch independent decisions. After the answer, resume — don't reconfirm the
broader task.

## Handoff format

```
Completed: <concise result>

Deferred decisions:
- <item>: <decision needed>. Recommendation: <default>.
  Impact: <only dependent work>.
```

Don't report "blocked" while independent work remains.

## Local overrides

Stricter project instructions win. Continue everything still inside permitted
scope.
