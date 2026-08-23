---
name: subagent-team-execution
description: >-
  Execute a written plan with a fresh subagent per task in the current
  session. Use when tasks are mostly independent and you want isolated
  implementers without pausing between tasks. Prefer executing-plans for
  tightly coupled work or inline execution.
---

# Subagent Team Execution

**You read the codebase. Implementers do not.** You hold the understanding and
spend it writing briefs; they receive an edit, apply it, run one command, and
return a line. Every lane that has to work out for itself what the code does
pays the whole comprehension cost again from zero, and that — not test runs,
not prompt size — is what makes a large plan expensive.

The subagent launch hook refuses briefs over 12,000 characters and more than two
open lanes, and asks for a checkpoint every seventh launch. Workers do not spawn
subagents. Adjacent findings get recorded in the handoff, not chased.

**Narration:** at most one short line between tool calls.

**Continuous within a pattern, stop at its boundary.** Do not ask "should I
continue?" between siblings of a settled pattern. Do stop at the end of each
pattern, and for unresolved BLOCKED or genuine ambiguity.

## When to use

| Have a plan? | Tasks mostly independent? | Stay in session? | Use |
|--------------|---------------------------|------------------|-----|
| Yes | Yes | Yes | This skill |
| Yes | Yes | No / separate session | `executing-plans` |
| Yes | No — tightly coupled | — | `executing-plans` or manual |
| No | — | — | `thinking` / `writing-plans` first |

Never implement on `main`/`master` without explicit consent. Use `worktrees`
when isolation is needed.

## Pattern waves

Work one pattern at a time, not one task at a time. If the plan named its
patterns (`writing-plans`), use them; if it did not, group the tasks yourself
before dispatching anything — a forty-task plan is usually five or six
mechanical changes applied to several targets each.

Per pattern:

1. **Run the setter yourself**, or with one capable implementer you stay close
   to. This is where the code gets read and the shape gets settled. Expensive
   on purpose, once.
2. **Turn its diff into the sibling brief.** The brief is the setter's actual
   diff plus this target's files and one verify command — not prose about what
   to do. If you cannot write that brief, the pattern is not settled and the
   siblings are not ready.
3. **Fan the siblings out**, cheap model, two lanes at a time.
4. **Close the pattern**: batch every hand check to the user in one message,
   report what landed and what the next pattern will cost, and stop there.

**Never dispatch a setter alongside its own siblings.** Disjoint files make
them look parallel-safe; each one still re-derives the same pattern, which is
the single most expensive mistake available here.

**Only mechanical tasks get an implementer.** If the done-condition is a
judgment — "indistinguishable", "feels the same", "decide and record" — you do
it inline or hand it to the user. A cheap lane cannot verify what it cannot
comprehend.

**No standing reviewer lane.** You wrote the brief from a diff you understand;
reviewing the result is reading a small diff, not re-reading the subsystem.
Spawn an independent reviewer only for a high-risk change, and only when the
implementation lanes are idle.

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
| Sibling of a settled pattern, brief carries the diff | Cheap / fast |
| Multi-file integration, debugging | Standard |
| Pattern setter, design judgment, broad understanding | Most capable |

If a task needs the most capable tier, ask whether it should be a subagent at
all — that tier plus a fresh context means it is re-deriving what you already
know.

## Per-task loop

**One implementer at a time** for implementation (avoid file conflicts).
Research-only agents may parallelize via `parallel-agents`.

### 1. Dispatch implementer

Give:

1. One line on where this task fits
2. The setter's diff, or the exact edit — the brief carries the change itself,
   not a description of it
3. This target's files, and anything from earlier tasks the diff can't show
4. Your resolution of any ambiguity you already noticed
5. One verify command, and what to return: status, commit, one-line result

Do not paste accumulated prior-task histories, and do not send them to read the
plan file or the subsystem. Compress each return to a line before continuing —
your context holds understanding, not transcript.

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

Pattern complete → batched hand checks to the user → report cost and what the
next pattern needs → stop. All patterns complete → `verification` on the
relevant suite → `finishing-branches`.

## Anti-patterns

| Don't | Do |
|-------|-----|
| Mandatory task-reviewer every task | Light controller check |
| 5-round fix loops | One fix pass, then escalate |
| Progress ledger ceremony | Todos + git |
| Final whole-branch reviewer always | Finish when green; review if user asks |
| Parallel implementers on same tree | One implementer at a time |
| Setter and siblings dispatched together | Setter lands, then siblings |
| Prose briefs that make a lane re-read the code | The setter's diff as the brief |
| Running the whole plan in one sitting | Stop at every pattern boundary |
| Controller silently rewriting code | Keep coordination context clean; re-dispatch |
