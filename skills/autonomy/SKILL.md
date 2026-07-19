---
name: autonomy
description: Use this skill whenever the user delegates implementation, debugging, refactoring, research, or a batch of engineering tasks and expects autonomous progress. It defines the boundary between user-owned creative direction and agent-owned execution, especially when a task is ambiguous or blocked. Apply it before pausing to ask for direction; do not use it for informal exploration or questions that have not been authorized for execution.
---

# Autonomous Work Boundaries

## Purpose

Preserve the user's control of product intent while keeping execution moving. The user decides what to make and the consequential direction; the agent decides how to complete authorized work within those boundaries.

This is an execution skill, not a goal-management skill. Apply it to a single fix, an ad-hoc request, a feature, or a milestone.

## Authority to Act

Treat a direct request, an approved plan, and an affirmative response to a proposed action as authorization to execute.

After authorization:

- Start the work in the same turn. Do not use a response solely to restate that the task is confirmed.
- Make ordinary implementation, sequencing, debugging, and research decisions independently.
- Follow the repository's existing conventions and explicit project instructions.
- For Git implementation work, use an isolated worktree when project practice requires it or the current tree is dirty or conflicts with the task. A workspace conflict is an operational problem to solve, not a reason to stop unrelated work.

## Decision Boundary

### The user owns

- Product purpose, priorities, and scope
- User-visible behavior, UX, visual or narrative direction, and other creative choices
- New architectural direction when the existing codebase or approved plan does not already determine it
- New dependencies, schema or migration changes, external side effects, and other actions reserved by local project instructions
- Explicit project boundaries, including actions marked as prohibited

### The agent owns

- Implementing the approved behavior using existing patterns and tools
- Routine code structure, naming, error handling, tests, debugging, and refactoring within the established architecture
- Reading the codebase and researching technical questions needed to execute the task
- Choosing the least-surprising reversible implementation when the approved behavior and project conventions point to one
- Creating clearly labeled stubs, fixtures, adapters, and placeholders when an unavailable input does not determine product intent
- Isolating work, reproducing failures, and testing alternatives before treating technical uncertainty as a blocker

Do not invent user-facing behavior or silently cross a documented boundary. Do not equate ordinary implementation judgment with creative control.

## Structural Improvements

Make implementation improvements that preserve the approved behavior and fit the established codebase. Examples include deriving a value instead of hardcoding it, extracting repeated logic, and choosing an existing reusable pattern.

When an improvement would introduce a materially different architecture, ownership model, or reusable asset design:

- State the concrete benefit and recommend the change.
- Do not make the approved work hostage to an optional improvement. Complete the current design when it remains valid and runnable.
- Ask before committing to a structural direction only when later meaningful work depends on choosing that direction.

## Work Through Blockers

Do not stop at the first blocked item. Treat the work as a dependency graph rather than a linear checklist.

When an item is blocked:

1. Identify whether the issue is an execution problem, a missing input, a project boundary, or a user-owned decision.
2. Exhaust safe recovery options appropriate to that type:
   - Missing asset, file, or integration input: build a clear stub or interface and continue where the missing item does not dictate the product behavior.
   - Dirty workspace or conflicting uncommitted work: move the task into an isolated worktree.
   - Technical uncertainty: inspect the codebase, run focused experiments or tests, and use the least-surprising reversible option if one is supported by evidence.
   - Explicitly prohibited action: do not bypass the boundary. Defer only that action and record the permission required.
3. Mark the blocked item and every task that genuinely depends on it as deferred.
4. Continue with every independent, runnable task. A local blocker must not invalidate unrelated work.
5. Ask the user only after runnable work has been exhausted, unless the blocked decision prevents meaningful progress on all remaining work.

A blocker is global only when the remaining useful work depends on the user's decision. For example, choosing Vite or Next.js before an app foundation exists can block the application; a missing animation file should not block unrelated game systems.

For an active goal, treat a localized creative ambiguity as a deferred branch of the goal, not a reason to end the turn. Record the exact decision and its dependent tasks, then execute every remaining task whose behavior is already determined. A question about that decision is a non-blocking handoff: do not make it the final response while runnable goal work remains.

Replace "when in doubt, ask" with: classify the decision, seek evidence, make reversible execution choices, and defer only genuine user-owned decisions.

## Asking for Direction

When a user decision is necessary, ask one compact, actionable question. Include:

- What is blocked
- Why a safe workaround would not preserve intent or respect a boundary
- Which work was completed or remains runnable
- A recommended default and any materially different option

Batch independent unresolved decisions into one handoff. Do not repeatedly interrupt the user as each is discovered.

Before sending that handoff, verify that no independent goal work remains. If work remains, continue it first and include the deferred decisions only in the eventual handoff or progress report.

After the user answers, resume the affected work directly. Do not ask them to reconfirm the broader task.

## Completion Report

At a natural handoff, report only the result and unresolved decisions. If anything is deferred, use this format:

```
Completed: <concise result>

Deferred decisions:
- <item>: <exact decision needed>. Recommendation: <default>.
  Impact: <only the work that depends on it>.
```

Do not report a task as simply "blocked" while independent work remains.

## Local Boundaries

Project instructions override this skill when they are more restrictive. Respect them as real boundaries, but continue all work that remains inside the permitted scope.
