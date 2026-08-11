# Synapse for Codex

Synapse is a personal workflow system for Codex. Its skills are concise,
executable directives with visible outputs and proportional gates.

## Working rules

- Start clearly authorized work in the same turn.
- Use the smallest workflow that gives the change reliable evidence.
- Keep user-owned product intent and creative direction separate from routine
  implementation decisions.
- Protect the selected scope. If a new implementation idea is outside it,
  surface the pivot before writing code.
- Verify the exact claim before saying work is complete.

## Skills

The active suite lives in `skills/`:

- `thinking` — proportional design before risky or ambiguous changes.
- `verification` — claim only what was checked.
- `worktrees` — isolate work when the checkout or project workflow requires it.
- `parallel-agents` and `subagent-team-execution` — bounded delegation.
- `writing-plans` and `executing-plans` — plans for multi-step work.
- `testing` — TDD when behavior is unsettled; verification-first when clear.
- `debugging` — hypotheses, instrumentation, one repro, fix, and PR.
- `code-review` — verify review feedback before implementing it.
- `finishing-branches` — verify, push, and open a PR; merging stays user-owned.
- `goal-oriented-development` — user-directed GitHub issues; no automatic goal
  selection and no goal-fulfiller dispatch.
- `bug-capture` — record bugs for later without investigating them in-session.
- `autonomous-work-boundaries` — user intent versus agent execution.

Use the skill instructions as the source of truth for when a workflow applies.
They intentionally avoid ceremony for trivial, reversible work.

## Goal-oriented development

When the user names an issue or asks to work from issues, inspect the relevant
issue and milestone context. Do not infer the next goal from the repository.
The Codex research agents are registered under `.codex/agents/synapse/`:

- `codebase-explorer` answers focused repository questions.
- `goal-writer` drafts an evidence-based issue after the user commits to the
  outcome.
- `goal-surveyor` assesses a broad direction when the user explicitly asks for
  milestone discovery.

The primary Codex session remains responsible for user confirmation and GitHub
mutations. The current suite does not dispatch a goal-fulfiller agent.

## Repository layout

```text
skills/                         shared Synapse skills
.codex-plugin/plugin.json       Codex plugin manifest
.codex/agents/synapse/          Codex agent registrations
agents/                         Claude-compatible agent adapters
commands/                       Claude-compatible commands
automations/                    Bandaid automations (claude/ live, cursor/ frozen)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
CLAUDE.md                       Claude-compatible root guidance
```
