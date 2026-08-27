# Synapse

Synapse is a personal workflow system for Cursor, Codex, and Claude Code. It
keeps software work deliberate with concise skills, visible evidence, and gates
that scale with risk instead of ceremony.

## Current skill suite

The shared skills live in `skills/` and cover:

- read-only collaborative thinking, feature specifications, and implementation plans;
- testing, verification, debugging, and code review;
- worktree isolation and bounded subagent delegation;
- finishing branches with verification, push, and pull request creation;
- user-directed GitHub issues and sticky-note bug capture;
- autonomous-work boundaries between user intent and agent execution; and
- report-only surveys of what a repo accumulates on its own — asset churn in a
  branch, worktree and branch sprawl.

See [`skills/README.md`](skills/README.md) for the complete inventory and the
skills that were intentionally dropped or replaced.

## Cursor installation

The Cursor plugin manifest is
[`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json). It ships `skills/`,
`/bug` and `/weedeat` (not `/debug` — Cursor already has one), and hooks from
[`hooks/cursor.json`](hooks/cursor.json).

Install from a local checkout or a marketplace that points at this repo. After
install, start a new agent chat so skills, commands, and hooks load.

## Codex plugin installation

The Codex package manifest is [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json)
and Codex root guidance is in [`AGENTS.md`](AGENTS.md). Registered Codex agents
live under `.codex/agents/synapse/`. Hooks use the Claude-compatible
[`hooks/hooks.json`](hooks/hooks.json) (Codex sets `CLAUDE_PLUGIN_ROOT` for
compatibility). Codex custom prompts are gone; `/bug`, `/weedeat`, and `/debug`
are explicit skills (`$bug`, `$weedeat`, `$debug`).

Use the registered `spec-writer` for a named feature when you want a grounded
`PENDING` spec plus terminal-interview questions. It stops after drafting; the
operator completes approval separately with `TODO`.

For a personal local checkout, place the repository at
`C:\Users\nateb\plugins\synapse`, then refresh and install it from the personal
marketplace:

```powershell
python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py C:\Users\nateb\plugins\synapse
codex plugin add synapse@personal
```

Start a new Codex task after reinstalling so the updated skills, commands, and
agent registrations are loaded.

## Claude installation

Synapse still publishes a Claude marketplace via
[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json):

```bash
claude plugin marketplace add AllHailSeizure/Synapse
```

```bash
claude plugin install synapse@synapse
```

Root `skills/` and `commands/` are discovered by convention. Claude also loads
`/debug` from `commands/debug.md`. The Claude root guidance is in
[`CLAUDE.md`](CLAUDE.md), and the Claude agent adapters are in `agents/`.

The command index is in [`docs/COMMANDS.md`](docs/COMMANDS.md) — kept out of
`commands/`, since every extra `.md` in that directory would ship as a slash
command.

## Session briefing and other hooks

[`hooks/session-briefing.mjs`](hooks/session-briefing.mjs) injects the Synapse
operating briefing — skill routing, standing rules, and the `.synapse/` layout —
plus the scope reminder. Edit [`hooks/synapse-briefing.md`](hooks/synapse-briefing.md),
not the script.

The same scripts serve every host; JSON output includes both Cursor fields
(`additional_context`, `permission`) and Claude/Codex `hookSpecificOutput`.

| Host | Config |
|------|--------|
| Cursor | [`hooks/cursor.json`](hooks/cursor.json) — `sessionStart`, `subagentStart`/`Stop`, `beforeShellExecution` |
| Codex / Claude | [`hooks/hooks.json`](hooks/hooks.json) — `SessionStart`, `UserPromptSubmit`, `PreToolUse`/`PostToolUse` |

Fan-out state lives under `~/.synapse/fanout/`. Verification gating still
requires `.synapse/verification-budget.json` in the target repo.

## Per-repo configuration and artifacts

A repo that Synapse operates on stores configuration in one `.synapse/`
directory — no skills or scripts. Artifacts live beside that configuration:
feature specifications in `.synapse/specs/`, implementation plans in
`.synapse/plans/`. Each tool reads only the files it needs:

```text
.synapse/identity.md    repo, base, stack          every tool
.synapse/bandaids.md    Secrets, Verify, Repro,    the bandaids
                        Protected, Ignore
.synapse/verification.md commands, scope mapping,  verification
                         environment, completion
.synapse/weedeat.md     Assets, Worktrees          the /weedeat surveys
.synapse/weedeat-tags.json                       weedeat CLI overrides
```

Pending feature specs can have a sibling `.questions.json` file produced by
the `writing-specs` skill or registered Codex `spec-writer`. The interviewer
is a separate package (`D:/libraries/TODO`). Install it with
`pip install -e D:/libraries/TODO`, then run `TODO` from the target
repository. It lists only `PENDING` specs as `SPEC:` rows; selecting one asks
the recorded questions plus a required approval closer, appends the answers,
and changes the spec to `APPROVED`. Use `TODO --list` for a non-interactive
inventory. The CLI makes no model calls.

The bandaids stop at Gate 0 on a missing section. Verification uses its local
file for the claims it covers and falls back to repository discovery when the
file or a relevant entry is absent. The `/weedeat` surveys degrade to documented
defaults instead and say so in their own output.

There is **no fallback** to the old root `SYNAPSE.md`. That single file was a
contention point — every workstream edited it, and an uncommitted edit was once
reset away by another before it was committed. Reading it as a fallback would
also mean silently serving standards from a file nobody remembers, so a tool
that can't find `.synapse/` fails loudly or uses defaults you can read here. If
a root `SYNAPSE.md` is still lying around, delete it.

Schema: [`docs/TEMPLATES/synapse/`](docs/TEMPLATES/synapse/). Worked example:
[`docs/EXAMPLES/synapse.hotel-kline-game.md`](docs/EXAMPLES/synapse.hotel-kline-game.md).

## Weedeat

The `/weedeat` (or `$weedeat`) command in this plugin is report-only: it runs
`asset-churn-audit` and `worktree-cleanup`. The interactive trim CLI is a
separate repository; agents never launch `weedeat run` on the user's behalf.

If that CLI is installed, a human in an interactive terminal may run it
directly. Nothing is removed on launch; `trim N` previews levels `1..N` and
requires confirmation. Level `0` is never deletable.

## Repository structure

```text
skills/                         shared skills (including $bug/$debug/$weedeat)
hooks/                          briefing, scope, fan-out, verification gates
.cursor-plugin/plugin.json      Cursor plugin manifest
.codex-plugin/plugin.json       Codex plugin manifest
.claude-plugin/                 Claude marketplace + plugin
.codex/agents/synapse/          Codex agent registrations
agents/                         Claude-compatible agent adapters
commands/                       /bug, /weedeat; /debug for Claude only
automations/                    Bandaid automations (special case)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
CLAUDE.md                       Claude-compatible root guidance
```
