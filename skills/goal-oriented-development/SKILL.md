---
name: goal-oriented-development
description: >-
  User-directed GitHub issue workflow. Use when the user wants to create,
  select, inspect, prioritize, or address an issue; when work must stay inside
  an approved issue; or when a high-level direction needs evidence before the
  user decides what to track. Do not infer the next goal from the codebase.
---

# Goal-Oriented Development

Keep work anchored to user-owned intent. Issues preserve problem, evidence,
desired outcome, and boundaries — not a prescribed implementation. The user
decides what becomes an issue and when it is addressed. The implementation
session owns technical investigation and planning after the user invokes it.

## Issue orientation

When the user asks to work from issues, inspect relevant open issues and
milestones. Do **not** select a next issue or require a milestone before useful
work can begin. Ask which issue to address when they have not named one.

## Exploring ideas

1. Explore conversationally
2. Do not implement yet
3. Queue only if the user commits to tracking it — then investigate and draft

## Scope protection

When implementation is about to start on work outside the selected issue, name
the change and ask whether to switch or expand scope. Exploring is welcome;
silently starting is not.

## Writing issues

When the user has chosen an outcome to track, spawn a `goal-writer` agent
(Task tool / subagent) with the stated intent and repository path. It returns
an evidence-based draft. Present it for confirmation before creating the
GitHub issue.

When spawning, create a compact task artifact (scripts/agent-utils.py create-task) that includes `spawn_budget_tokens` and `spawn_limit`. Spawned agents must not themselves spawn workers unless they are explicitly the leader recorded on the artifact and validate/reserve budget via the helper.

A useful issue carries:

- **User intent** — outcome or problem they chose to track
- **Relevant evidence** — files, methods, flows, current behavior
- **Desired outcome** — specific, observable acceptance criteria
- **Scope boundaries** — exclusions and open user-owned decisions

Do not turn investigation into a solution: no architecture, algorithm, refactor
plan, or ordered implementation checklist unless the user explicitly asked for
it.

## Addressing issues

When the user says to address an issue, the primary session takes it on. Read
the issue as an approved problem statement, then use the normal implementation
skills (`thinking`, `testing`, plans as needed) to inspect live code, confirm
behavior, and implement.

Do **not** dispatch a goal-fulfiller. Do not treat issue evidence as a mandated
solution. Surface material conflict between the issue and live code or user
intent before proceeding. Use `worktrees` when the project workflow requires
isolation.

## Reflection gate

When an issue closes:

1. Show what was completed
2. If useful, show remaining issues as options
3. Ask whether another issue still makes sense, or whether completed work
   changed what they want next

Do not start another issue until the user selects it.

## Milestone discovery

When the user explicitly asks for a broad assessment, spawn `goal-surveyor`
with the repository path and their direction. It returns evidence plus
questions or potential issue prompts. It does **not** create goals, set
priorities, or auto-draft issues.

The user selects any outcome to track. Only then may `goal-writer` investigate
and draft that single issue for approval.
