---
name: executing-plans
description: >-
  Execute a written implementation plan in this session with review
  checkpoints. Use when a plan file exists and work will proceed inline
  rather than via subagent-team-execution.
---

# Executing Plans

Load the plan, review it once, execute tasks, stop when blocked. Use
`subagent-team-execution` instead when tasks are independent and you want a
fresh subagent per task.

## Process

### 1. Load and review

1. Isolate if needed (`worktrees`).
2. Read the plan.
3. Surface real concerns once (gaps, contradictions, unsafe steps).
4. If concerns block start → ask before coding.
5. If clean → create todos and proceed.

Never start implementation on `main`/`master` without explicit consent.

### 2. Execute

For each task:

1. Mark in progress
2. Follow the steps
3. Run the verifications the plan names (`verification`)
4. Mark complete
5. Continue

Batch related micro-steps; don't pause for permission between routine tasks.

### 3. Checkpoints (not endless loops)

Pause for human review when:

- A natural batch finishes (e.g. 2–3 tasks or a subsystem boundary)
- Behavior choice appears that the plan didn't settle
- Tests fail in a way that suggests the plan is wrong

Do **not** invent multi-round review ceremonies, ledgers, or fixed "N of 5
fix loops." Fix failures, re-verify, move on — or stop and ask.

### 4. Finish

When all tasks are done and verified → `finishing-branches`.

## Stop and ask

Stop immediately when:

- Blocker you can't resolve (missing dependency, unclear instruction)
- Plan has a critical gap that prevents starting
- Same verification fails repeatedly without a new theory
- You would have to guess at user-owned intent

Don't force through blockers. Don't silently rewrite the plan to match
failing reality — raise the conflict.

## Remember

- Critical review once at the start
- Follow plan steps; skip nothing that verifies behavior
- Isolation via `worktrees` when appropriate
- `verification` before claiming a task done
- Finish via `finishing-branches`
