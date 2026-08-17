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
- Store feature specs in `.synapse/specs/` with `PENDING`, `APPROVED`, or
  `IMPLEMENTED` in both the filename and title.
- When implementation is governed by an approved spec, mark it `IMPLEMENTED`
  only after verifying its success criteria.

## Skills

The active suite lives in `skills/`:

- `thinking` — read-only collaborative exploration of intent and tradeoffs.
- `writing-specs` — capture feature intent in an approved document.
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

## Weeds (`/weedeat` equivalent)

Two more agents under `.codex/agents/synapse/` survey what a repo accumulates
on its own - Claude's `/weedeat` command triggers these by name; Codex has no
slash commands, so dispatch on the same signals directly:

- `asset-churn-audit` - dispatch before opening or merging a PR that touches
  assets, when `git status` shows dirty art nobody remembers editing, or when
  a PR diff looks larger than the work done.
- `worktree-cleanup` - dispatch when the user mentions worktree sprawl, stale
  or dead branches, running out of disk, or asks what is safe to delete.

Both ship a script at `agents/scripts/<name>.py` in this Synapse install.
Resolve its absolute path before dispatching (the agent's own instructions
expect it as an input, not something it discovers itself) and pass it along
with the repository path. Both read repo-specific configuration from
`.synapse/weedeat.md` - `## Assets` and `## Worktrees` - plus
`.synapse/identity.md` for the baseline branch; a missing section degrades to
generic defaults rather than stopping.

Both are report-only. Present findings and the exact commands, then stop - do
not run a removal, revert, or stage anything yourself. If the user authorizes
one tier ("drop the churn", "remove the safe ones"), that authorizes only that
tier for that run, not REVIEW or HOLD, and it does not carry to the next
invocation.

That boundary applies to the agent-dispatched report path. If the standalone
`weedeat` CLI is installed, a human in an interactive terminal may run
`weedeat run` directly to review numeric risk levels in a command prompt.
Nothing is removed on launch; `trim N` previews levels `1..N` and requires
confirmation, while level `0` is never deletable. Agents do not launch that
human-invoked path on the user's behalf.

## Response style

Tone and verbosity do not belong in this file. AGENTS.md is context layered on
top of Codex's built-in instructions, so directives about how to respond
compete with them and lose over a long session — the same reason Claude's
CLAUDE.md is the wrong channel for it.

Codex's system-prompt-level lever is `model_instructions_file` in
`config.toml`. Unlike Claude's output styles, which append and can retain the
built-in coding instructions via `keep-coding-instructions: true`, this key
**replaces** Codex's built-in instructions outright. Adopting it means owning
that baseline. Synapse does not set it; enabling it is a deliberate,
user-approved change, not a default.

Claude's equivalent, which Synapse does ship, is `output-styles/succinct.md`.

## Repository layout

```text
output-styles/                  Claude output styles (Succinct)
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
