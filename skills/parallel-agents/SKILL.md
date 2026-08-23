---
name: parallel-agents
description: >-
  Parallel subagent dispatch for independent work. Use when facing 2+ tasks
  that share no state and have no sequential dependencies — different test
  files, subsystems, or bugs that can be investigated concurrently.
---

# Parallel Agents

Dispatch one focused subagent per independent problem domain. They must not
inherit session history — give each exactly the context it needs.

A subagent launch hook enforces this mechanically: briefs over 12,000 characters
are refused as context forwarding, and more than two open lanes are refused
until one closes. Every seventh launch in a session asks you for a checkpoint.
Send a task packet — task text, base commit, allowed files, done condition, one
verify command — not session history. Workers are single-purpose and do not
spawn further subagents; only you open lanes.

Tune the caps per repo in `.synapse/fanout.json`
(`maxConcurrent`, `maxPromptChars`, `waveSize`).

## Decision tree

1. Multiple distinct problems?
   - No → stay in this session.
2. Independent (fixing one won't likely fix the others)?
   - No → one agent (or you) investigates the related set.
3. Can they run without shared mutable state (same files, same resources)?
   - No → sequential agents or single session.
   - Yes → **parallel dispatch** (multiple Task calls in one response).

## Use when

- 3+ failing test files with different root causes
- Independent subsystems broken separately
- Each problem understandable without the others

## Don't use when

- Failures are related
- Full-system context is required
- Exploratory debugging — you don't know what's broken yet
- Agents would edit the same files or fight over resources

## Dispatch pattern

1. **Group by domain** — one agent per domain.
2. **Write self-contained prompts** — scope, goal, constraints, expected return.
3. **Fire in one response** — multiple Task/subagent calls together = parallel.
4. **Integrate** — read summaries, check conflicts, run the suite that covers
   the combined change.

### Prompt checklist

- Focused: one file/subsystem, not "fix everything"
- Context: error messages, test names, relevant paths
- Constraints: what not to change
- Output: root cause + what changed

### Good vs bad

| Bad | Good |
|-----|------|
| "Fix all the tests" | "Fix `agent-tool-abort.test.ts`" |
| "Fix the race" (no where) | Paste failures + file path |
| No constraints | "Do not change production code" / "tests only" |
| "Fix it" | "Return root cause and diff summary" |

## After return

1. Review each summary
2. Check overlapping edits
3. Run verification covering the union of changes (`verification` skill)
