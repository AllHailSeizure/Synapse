---
name: goal-oriented-development
description: >-
  User-directed GitHub issue workflow. Use when the user wants to create,
  select, inspect, prioritize, or address an issue; when work must stay inside
  an approved issue; or when a high-level direction needs evidence before the
  user decides what to track. When the user says to address, work through, or
  unblock a selected feature issue without explicitly requesting
  implementation, route to writing-specs rather than goal-writer. Do not infer
  the next goal from the codebase.
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

Use `goal-writer` only when the user wants to create a GitHub issue or
explicitly rewrite an existing issue. Do not dispatch it merely because a
selected feature issue is incomplete or needs product decisions; route that
work through `writing-specs` instead.

When the user has chosen a new outcome to track, spawn a `goal-writer` agent
(Task tool / subagent) with the stated intent and repository path. It returns
an evidence-based draft. Present it for confirmation before creating the
GitHub issue.

A useful issue carries:

- **User intent** — outcome or problem they chose to track
- **Relevant evidence** — files, methods, flows, current behavior
- **Desired outcome** — specific, observable acceptance criteria
- **Scope boundaries** — exclusions and open user-owned decisions

Do not turn investigation into a solution: no architecture, algorithm, refactor
plan, or ordered implementation checklist unless the user explicitly asked for
it.

## Addressing issues

When the user says to address, work through, or unblock a selected issue,
inspect the issue, milestone context, and relevant repository evidence, then
route by intent:

- **Feature issue, implementation not explicitly requested** — invoke
  `writing-specs`. It invokes `thinking`, develops shared understanding, and
  captures an approved spec before any implementation.
- **Explicit request to create or rewrite the GitHub issue** — use
  `goal-writer`, present its draft, and mutate GitHub only after confirmation.
- **Explicit request to implement or fix now** — treat the issue as the scope
  boundary and use the normal implementation skills.
- **Bug, verification, or refactor with settled behavior** — do not force a
  feature spec; follow the appropriate workflow for the user's requested
  outcome.

Do not interpret “address this feature issue” as permission to implement, and
do not use `goal-writer` as a substitute for developing the feature's meaning.

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
