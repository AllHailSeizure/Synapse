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
- Store feature specs in `.synapse/specs/` with `PENDING`, `APPROVED`,
  `IMPLEMENTED`, or `CLOSED` in both the filename and title.
- When implementation is governed by an approved spec, mark it `IMPLEMENTED`
  only after verifying its success criteria.

## Skills

The active suite lives in `skills/`:

- `thinking` — read-only collaborative exploration of intent and tradeoffs.
- `writing-specs` — draft a grounded `PENDING` spec and terminal questions.
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
- `autonomous-work-boundaries` — user intent versus agent execution.

Explicit command skill (invoke with `$name`; do not auto-fire): `debug`.
Cursor `/bug` / `/patch` and `commands/bug.mjs` / `commands/patch.mjs` capture
a sticky-note issue (`@bug-bandaid` vs `@fastpatch`); Codex has no slash
command for that.

Use the skill instructions as the source of truth for when a workflow applies.
They intentionally avoid ceremony for trivial, reversible work.

## Goal-oriented development

When the user names an issue or asks to work from issues, inspect the relevant
issue and milestone context. Do not infer the next goal from the repository.
The Codex agents are registered under `.codex/agents/synapse/`:

- `codebase-explorer` answers focused repository questions.
- `spec-writer` drafts one named feature as a `PENDING` spec and questions
  file, then stops for the operator's `TODO` interview.
- `goal-writer` drafts an evidence-based issue after the user commits to the
  outcome.
- `goal-surveyor` assesses a broad direction when the user explicitly asks for
  milestone discovery.

The primary Codex session remains responsible for user confirmation and GitHub
mutations. The current suite does not dispatch a goal-fulfiller agent.

## Weeds

Asset-churn and worktree/branch-sprawl surveys moved out of this repo into
their own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).
Install it separately if you want those agents available under Codex.

## Response style

Tone and verbosity do not belong in this file. AGENTS.md is context layered on
top of Codex's built-in instructions, so directives about how to respond
compete with them and lose over a long session.

Codex's system-prompt-level lever is `model_instructions_file` in
`config.toml`. That key **replaces** Codex's built-in instructions outright.
Synapse does not set it.

## Repository layout

```text
skills/                         shared Synapse skills
hooks/                          plugin hooks for Codex and Cursor
.cursor-plugin/plugin.json      Cursor plugin manifest
.codex-plugin/plugin.json       Codex plugin manifest
.codex/agents/synapse/          Codex agent registrations
commands/                       Cursor /bug and /patch plus capture scripts
automations/                    Bandaid automations (special case)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
```
