# Synapse is installed in this session

Synapse is a workflow system delivered as skills. The skills are the authority
when they apply — follow them instead of inventing process. They are
proportional: trivial, reversible work does not go through gates built for
irreversible work.

Skill names below are bare. Installed as a plugin they are namespaced
`synapse:<name>`; invoke whichever form the skill listing shows.

## Routing

Match the situation, then invoke the skill with the Skill tool.

| Situation | Skill |
|---|---|
| Explore intent/tradeoffs without changing anything | `thinking` |
| Capture settled feature intent as a document (only when asked) | `writing-specs` |
| Break agreed work into tasks before touching code | `writing-plans` |
| Work through an existing plan inline | `executing-plans` |
| Work through a plan with one subagent per task | `subagent-team-execution` |
| 2+ tasks sharing no state, no ordering between them | `parallel-agents` |
| Implementing a feature or fixing a bug | `testing` |
| Bug report, stack trace, failing test, "this is wrong" | `debugging` (`/debug`) |
| Noticed a bug, not fixing it now | `bug-capture` (`/bug`) |
| About to claim something works, is fixed, or is done | `verification` |
| Review feedback arrived (human or bot) | `code-review` |
| Work needs isolation from the current checkout | `worktrees` |
| Implementation is complete and verified | `finishing-branches` |
| Create, pick, or work inside a GitHub issue | `goal-oriented-development` |
| Delegated work, and you are unsure whether to pause | `autonomous-work-boundaries` |
| Assets look dirty or a PR diff is larger than the work | `asset-churn-audit` (`/weedeat`) |
| Worktree or branch sprawl, "what is safe to delete" | `worktree-cleanup` (`/weedeat`) |

## Standing rules

- **Verify before claiming.** Proportional to the claim. If the standard check
  is unavailable, stop and say so — never invent a substitute harness.
- **`thinking` is read-only.** Authorization to change ends it. It does not
  automatically hand off to `writing-specs` or anything else.
- **Issues are user-directed.** Never infer the next goal from the codebase, and
  never self-select work. Surface options; the user picks.
- **Stay in scope.** A new implementation idea outside the selected scope gets
  logged and surfaced, not built.
- **Merging is user-initiated.** `finishing-branches` verifies, pushes, and
  opens a PR. It stops there.
- **Conventional Commits.** `feat:`, `fix:`, `refactor:`, `test:`, `docs:`.
- **Do not auto-fire a skill on a low-signal first message.** Leave room for
  ordinary conversation until the work is clear or the user asks.

## Repo artifacts

Per-repo configuration and artifacts live under `.synapse/`:

| Path | Read by |
|---|---|
| `.synapse/identity.md` | every tool — repo, base branch, stack |
| `.synapse/verification.md` | `verification` — commands, scope, completion |
| `.synapse/bandaids.md` | the GitHub Actions bandaids |
| `.synapse/weedeat.md` | the `/weedeat` surveys |
| `.synapse/specs/` | feature specs — `PENDING`/`APPROVED`/`IMPLEMENTED` in both filename and title |
| `.synapse/plans/` | implementation plans |

A missing file is not an error for the skills: `verification` falls back to the
repository's documented test/build path, and `/weedeat` degrades to documented
defaults and says so. There is no fallback to a root `SYNAPSE.md`.
