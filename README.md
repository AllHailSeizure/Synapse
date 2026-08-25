# Synapse

Synapse is a personal workflow system for Claude Code and Codex. It keeps
software work deliberate with concise skills, visible evidence, and gates that
scale with risk instead of ceremony.

## Current skill suite

The shared skills live in `skills/` and cover:

- read-only collaborative thinking, feature specifications, and implementation plans;
- testing, verification, debugging, and code review;
- worktree isolation and bounded subagent delegation;
- finishing branches with verification, push, and pull request creation;
- user-directed GitHub issues and sticky-note bug capture; and
- autonomous-work boundaries between user intent and agent execution.

See [`skills/README.md`](skills/README.md) for the complete inventory and the
skills that were intentionally dropped or replaced.

Report-only surveys of what a repo accumulates on its own — asset churn in a
branch, worktree and branch sprawl — moved out to their own plugin:
[`weedeat`](https://github.com/AllHailSeizure/weedeat).

## Claude installation

Synapse publishes itself as a marketplace via
[`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json), so the
skills, commands, and bandaids install as one plugin rather than being copied:

```bash
claude plugin marketplace add AllHailSeizure/Synapse
```

```bash
claude plugin install synapse@synapse
```

Root `skills/` and `commands/` are discovered by convention, so a new skill
directory or command file ships with the next release — no manifest edit.
Publishing means landing it on the branch the marketplace tracks.

The plugin is the only supported install path. There is no copy step.

Output styles ship the same way, from `output-styles/`. Installing the plugin
makes `Succinct` available; activate it with `"outputStyle": "Succinct"` in a
settings file. It is read once at session start, so it applies after `/clear`
or a new session.

The Claude root guidance is in [`CLAUDE.md`](CLAUDE.md), and the Claude agent
adapters are in `agents/`.

The `/bug` command is defined in [`commands/bug.md`](commands/bug.md) and
delegates to the capture-only `bug-capture` skill. The command index is in
[`docs/COMMANDS.md`](docs/COMMANDS.md) — kept out of `commands/`, since every
`.md` in that directory ships as a slash command.

## Session briefing hook

[`hooks/hooks.json`](hooks/hooks.json) registers a `SessionStart` hook that
injects the Synapse operating briefing — skill routing, standing rules, and the
`.synapse/` layout — into every session, so a session knows how to use the suite
without being told. The prose lives in
[`hooks/synapse-briefing.md`](hooks/synapse-briefing.md); edit that file, not
the script. [`hooks/session-briefing.mjs`](hooks/session-briefing.mjs) reads it,
appends which of the target repo's `.synapse/` files actually exist, and prints
the `additionalContext` payload.

Like the skills and output styles, the hook ships with the plugin — landing it
on the branch the marketplace tracks is what publishes it. It is read at session
start, so it applies to the next session after the plugin updates.

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
```

Pending feature specs can have a sibling `.questions.json` file produced by
the `writing-specs` skill or registered Codex `spec-writer`. Install the
script-only interviewer with `pip install -e apps/todo`, then run `TODO` from
the target repository. It lists only `PENDING` specs as `SPEC:` rows; selecting
one asks the recorded questions plus a required approval closer, appends the
answers, and changes the spec to `APPROVED`. Use `TODO --list` for a
non-interactive inventory. The CLI makes no model calls.

The bandaids stop at Gate 0 on a missing section. Verification uses its local
file for the claims it covers and falls back to repository discovery when the
file or a relevant entry is absent.

There is **no fallback** to the old root `SYNAPSE.md`. That single file was a
contention point — every workstream edited it, and an uncommitted edit was once
reset away by another before it was committed. Reading it as a fallback would
also mean silently serving standards from a file nobody remembers, so a tool
that can't find `.synapse/` fails loudly or uses defaults you can read here. If
a root `SYNAPSE.md` is still lying around, delete it.

Schema: [`docs/TEMPLATES/synapse/`](docs/TEMPLATES/synapse/). Worked example:
[`docs/EXAMPLES/synapse.hotel-kline-game.md`](docs/EXAMPLES/synapse.hotel-kline-game.md).

## Codex plugin installation

The repository also contains the Codex package manifest at
`.codex-plugin/plugin.json` and Codex root guidance in `AGENTS.md`. The
registered Codex agents live under `.codex/agents/synapse/`.

Use the registered `spec-writer` for a named feature when you want a grounded
`PENDING` spec plus terminal-interview questions. It stops after drafting; the
operator completes approval separately with `TODO`.

Codex plugin manifests expose skills rather than Claude-style slash-command
files, so use the `bug-capture` skill for the same bug-report workflow in
Codex.

For a personal local checkout, place the repository at
`C:\Users\nateb\plugins\synapse`, then refresh and install it from the personal
marketplace:

```powershell
python C:\Users\nateb\.codex\skills\.system\plugin-creator\scripts\update_plugin_cachebuster.py C:\Users\nateb\plugins\synapse
codex plugin add synapse@personal
```

Start a new Codex task after reinstalling so the updated skills and agent
registrations are loaded.

## Repository structure

```text
skills/                         shared skills
hooks/                          SessionStart briefing hook
.codex-plugin/plugin.json       Codex plugin manifest
.codex/agents/synapse/          Codex agent registrations
agents/                         Claude-compatible agent adapters
commands/                       Claude-compatible commands
automations/                    Bandaid automations (claude/ live, cursor/ frozen)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
CLAUDE.md                       Claude-compatible root guidance
```
