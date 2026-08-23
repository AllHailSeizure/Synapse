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
return a line. Every agent that has to work out for itself what the code does
pays the whole comprehension cost again from zero, and that — not test runs,
not prompt size — is what makes a large plan expensive.

The subagent launch hook refuses briefs over 12,000 characters and more than
two agents at once, and asks for a checkpoint every seventh launch. Workers do
not spawn subagents. Adjacent findings get recorded in the handoff, not chased.

**Narration:** at most one short line between tool calls.

**Continuous execution:** do not ask "should I continue?" between tasks. Stop
only for unresolved BLOCKED, genuine ambiguity, or completion.

## When to use

| Have a plan? | Tasks mostly independent? | Stay in session? | Use |
|--------------|---------------------------|------------------|-----|
| Yes | Yes | Yes | This skill |
| Yes | Yes | No / separate session | `executing-plans` |
| Yes | No — tightly coupled | — | `executing-plans` or manual |
| No | — | — | `thinking` / `writing-plans` first |

Never implement on `main`/`master` without explicit consent. Use `worktrees`
when isolation is needed.

**Only mechanical tasks get an implementer.** If the done-condition is an open
design question rather than a command, settle it yourself first — a cheap agent
cannot verify what it cannot comprehend.

**No standing reviewer agent.** You wrote the brief from a diff you understand;
reviewing the result is reading a small diff, not re-reading the subsystem.
Spawn an independent reviewer only for a high-risk change, and only when the
implementers are idle.

## When tasks repeat

Some plans contain one change applied to several targets — the same conversion
per module, per endpoint, per file. Those tasks are not independent even though
their files are: dispatched cold, each agent re-derives the same change from
the codebase and you pay for that reading once per target.

Run the first one yourself, then hand its diff to the rest. A brief carrying
the actual diff plus this target's files and one verify command costs a cheap
agent almost nothing; if you cannot write that brief, the change is not settled
and the repeats are not ready. Never dispatch the first one alongside its own
repeats — disjoint files make them look parallel-safe, and it is the most
expensive mistake available here.

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
| 1–2 files, brief carries the exact edit | Cheap / fast |
| Multi-file integration, debugging | Standard |
| Design judgment, broad understanding | Most capable |

If a task needs the most capable tier, ask whether it should be a subagent at
all — that tier plus a fresh context means it is re-deriving what you already
know.

## Per-task loop

**One implementer at a time** for implementation (avoid file conflicts).
Research-only agents may parallelize via `parallel-agents`.

### 1. Dispatch implementer

Give:

1. One line on where this task fits
2. The exact edit — a diff where one exists; the brief carries the change
   itself, not a description of it
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

### 3. Your review (lightweight)

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
| Mandatory task-reviewer every task | A light check by you |
| 5-round fix loops | One fix pass, then escalate |
| Progress ledger ceremony | Todos + git |
| Final whole-branch reviewer always | Finish when green; review if user asks |
| Parallel implementers on same tree | One implementer at a time |
| Repeated work dispatched all at once | First one lands, then the repeats |
| Prose briefs that make an agent re-read the code | The diff as the brief |
| Manual checks in a plan or a brief | Only what the agent can run |
| Silently rewriting code yourself | Keep coordination context clean; re-dispatch |
