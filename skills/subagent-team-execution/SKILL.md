---
name: subagent-team-execution
description: >-
  Execute a written plan with a fresh subagent per task in the current
  session. Use when tasks are mostly independent and you want isolated
  implementers without pausing between tasks. Prefer executing-plans for
  tightly coupled work or inline execution.
---

# Subagent Team Execution

Dispatch a fresh implementer per plan task. You coordinate; they implement.
Keep your context clean — hand requirements as files or tight prompts, not
session history dumps.

Use scripts/agent-utils.py to record a task artifact and enforce leader-only spawning and spawn budgets. Workers must not spawn subagents; they should write results under `.synapse/tasks/<task-id>/workers/` and append cost entries via the helper.

**Narration:** at most one short line between tool calls.

**Continuous execution:** do not ask "should I continue?" between tasks.
Stop only for unresolved BLOCKED, genuine ambiguity, or completion.

## When to use

| Have a plan? | Tasks mostly independent? | Stay in session? | Use |
|--------------|---------------------------|------------------|-----|
| Yes | Yes | Yes | This skill |
| Yes | Yes | No / separate session | `executing-plans` |
| Yes | No — tightly coupled | — | `executing-plans` or manual |
| No | — | — | `thinking` / `writing-plans` first |

Never implement on `main`/`master` without explicit consent. Use `worktrees`
when isolation is needed.

## Setup

1. Read the plan once; note Global Constraints.
2. Todo per task.
3. Pre-flight: scan for contradictions or impossible mandates. Batch any
   conflicts into one question before Task 1. If clean, start silently.
4. Track progress with todos (and git log). No heavyweight ledger files.

## Model selection

Pick the weakest model that can do the job; always set model explicitly.

| Task shape | Model tier |
|------------|------------|
| 1–2 files, complete code in plan | Cheap / fast |
| Multi-file integration, debugging | Standard |
| Design judgment, broad understanding | Most capable |

## Per-task loop

**One implementer at a time** for implementation (avoid file conflicts).
Research-only agents may parallelize via `parallel-agents`.

### 1. Dispatch implementer

Give:

1. One line on where this task fits
2. Full task text (or path to a task brief) — exact values live here
3. Interfaces/decisions from earlier tasks the brief can't know
4. Your resolution of any ambiguity you already noticed
5. What to return: status, commits, one-line test summary, concerns

Do not paste accumulated prior-task histories. Do not make them read the
whole plan file if a task extract exists.

### 2. Handle status

| Status | Action |
|--------|--------|
| DONE | Spot-check summary; run focused verify if risk warrants; next task |
| DONE_WITH_CONCERNS | Read concerns; fix correctness/scope before continuing |
| NEEDS_CONTEXT | Answer and re-dispatch |
| BLOCKED | Add context, bump model, split task, or escalate — never blind retry |

Answer clarifying questions fully before forcing implementation.

### 3. Controller review (lightweight)

You are the gate — not a mandatory reviewer subagent after every task.

After each DONE:

- Spec: did the task deliver what the plan asked?
- Smoke: did reported tests actually address the change?
- Conflicts: any plan contradiction?

If something's wrong, send findings back to a fresh or resumed implementer
**once**. If still broken and load-bearing → stop and escalate. No 5-round
fix loops, no parked-finding bureaucracy, no final whole-branch reviewer
dispatch by default.

Optional targeted review is fine for high-risk diffs — discretionary, not
ritual.

### 4. Next task

Mark complete and continue until the plan is done or blocked.

## Finish

All tasks complete → `verification` on the relevant suite → `finishing-branches`.

## Anti-patterns

| Don't | Do |
|-------|-----|
| Mandatory task-reviewer every task | Light controller check |
| 5-round fix loops | One fix pass, then escalate |
| Progress ledger ceremony | Todos + git |
| Final whole-branch reviewer always | Finish when green; review if user asks |
| Parallel implementers on same tree | One implementer at a time |
| Controller silently rewriting code | Keep coordination context clean; re-dispatch |
