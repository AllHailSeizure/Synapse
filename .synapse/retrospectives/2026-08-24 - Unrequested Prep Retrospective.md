# Unrequested Prep Retrospective — 2026-08-24

## Purpose

A session on `hotel-kline-game` (PR #489, "Repair the silently-skipped test scripts, retire
reflective flag access, and collapse the two flag mechanisms") was asked to implement a planned
migration task. Before touching the assigned work it ran the full GUT suite, diagnosed and fixed
a bug the user had deliberately deferred until after the migration, and fact-checked the
migration ledger against the live code. All three were well-executed and well-documented. None
were asked for. Together they consumed a full session's usage budget on self-directed prep.

This is the same root cause as the 2026-08-20 fan-out retrospective — a broad mandate to "handle
issues along the way" turning into unbounded scope growth — showing up in a single, non-fanned-out
session. The earlier retrospective's fix (`subagent-gate.mjs`) only gates `Task`/`Agent` calls. It
did nothing here because no subagent was involved.

## What happened

- Ran the project's full GUT suite (`godot --headless -s addons/gut/gut_cmdln.gd -gdir=res://Tests
  -gexit`) after each of three commits, to re-derive a baseline and confirm no regressions. The
  user runs this themselves specifically to avoid spending tokens on it, and the repo's own CI
  already runs it on every push — its `CONTRIBUTING.md` records that hand-running this exact
  command at every step was previously judged "the largest avoidable risk" in an earlier
  milestone, which is why CI was added in the first place.
- Found and fixed a real bug (`farthopper_bark_done` guarding on an undeclared property, so a
  one-time bark replayed on every hop) while retiring reflective flag access. The user already
  knew about this bug and had deliberately chosen not to address it until after the migration.
- Cross-checked the migration ledger's stated blocker and a stale count against the live code
  before proceeding, correcting two of the ledger's own claims.

None of this was destructive or low-quality — the PR is accurate, well-verified, and the bug fix
is real. The failure is that none of it was requested, and it happened before the assigned task,
using the budget that task needed.

## Classification

| Action | Classification | Better handling |
| --- | --- | --- |
| Running the full GUT suite three times | Unrequested verification; CI already owns this | Skip entirely, or run one targeted `-gtest=` invocation if actively debugging |
| Fixing the farthopper bug | Found while working, not blocking the stated task, previously deferred by the user | Record it (bug-capture / `/bug`) and continue |
| Fact-checking the ledger's blocker/count | Found while working, not requested | Note the discrepancy in the handoff; let the user decide whether to act on it |

The same distinction the fan-out retrospective drew for subagents applies to a single root
session: fix only what makes the assigned task's done condition false. Everything else gets
recorded, not chased — see that retrospective's "Issue pursuit: useful findings versus costly
scope growth" table.

## Fix shipped

1. **`verification-gate.mjs`** (`PreToolUse`, `Bash` matcher) — denies a Bash command matching a
   repo's declared "broad verification" patterns unless it also matches a declared "scoped/debug"
   pattern. Opt-in per repo via `.synapse/verification-budget.json`; no config means no gate. Fails
   open on any internal error. `hotel-kline-game` now declares GUT's whole-directory `-gdir=` runs,
   the boot smoke check, and the architecture lint as broad, with GUT's targeted `-gtest=` flag as
   the scoped exception — a genuinely debugging-shaped invocation still works.
2. **`scope-reminder.mjs`** (`UserPromptSubmit`) — re-asserts the "record, don't chase" boundary
   every turn, the same mechanism `succinct-reminder.mjs` already uses for output style, because a
   CLAUDE.md instruction — even one phrased as a hard gate, as `hotel-kline-game`'s CLAUDE.md
   already does for several other rules — competes with everything piled up later in a long
   session and loses. This is reinforcement, not a hard block; it has no enforcement mechanism
   against a determined counter-instruction, unlike the Bash gate.

Fixing bugs found in passing and running verification suites are pattern-matchable at the tool-call
level, which is why both got a mechanical gate here rather than a documentation change. Whether an
edit as a whole stays inside the assigned task's scope is not reliably pattern-matchable without an
LLM judge on every edit — that tradeoff (added latency and cost on every file change, for an
imperfect signal) was declined for now in favor of the cheaper reminder.

## Bottom line

The engineering in PR #489 was sound. The problem was sequencing and authorization: expensive,
unrequested prep happened first and consumed the budget the assigned task needed. The fix is the
same shape as the fan-out retrospective's — mechanical gates on the specific tool calls that
caused the cost, not a request for better judgment.
