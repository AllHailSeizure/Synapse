# Synapse

Synapse is a personal workflow system for Claude Code and Codex. It keeps
software work deliberate with concise skills, visible evidence, and gates that
scale with risk instead of ceremony.

## Current skill suite

The shared skills live in `skills/` and cover:

- proportional thinking and implementation plans;
- testing, verification, debugging, and code review;
- worktree isolation and bounded subagent delegation;
- finishing branches with verification, push, and pull request creation;
- user-directed GitHub issues and sticky-note bug capture;
- autonomous-work boundaries between user intent and agent execution; and
- report-only surveys of what a repo accumulates on its own — asset churn in a
  branch, worktree and branch sprawl.

See [`skills/README.md`](skills/README.md) for the complete inventory and the
skills that were intentionally dropped or replaced.

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

Skills and commands can still be copied into the local configuration
directories instead, for a checkout you're actively editing:

```powershell
powershell -Command "'.claude','.cursor' | % { Copy-Item 'D:\Libraries\Synapse\skills\*' \"$env:USERPROFILE\$_\skills\" -Recurse -Force; Copy-Item 'D:\Libraries\Synapse\commands\*.md' \"$env:USERPROFILE\$_\commands\" -Force }"
```

The Claude root guidance is in [`CLAUDE.md`](CLAUDE.md), and the Claude agent
adapters are in `agents/`.

The `/bug` command is defined in [`commands/bug.md`](commands/bug.md) and
delegates to the capture-only `bug-capture` skill. The command index is in
[`docs/COMMANDS.md`](docs/COMMANDS.md) — kept out of `commands/`, since every
`.md` in that directory ships as a slash command.

## Per-repo configuration

A repo that Synapse operates on carries exactly one Synapse file: `SYNAPSE.md`
at its root. Nothing else — no skills, no scripts, no config directory. The
bandaids read it at Gate 0 and stop on a missing section; the `/weedeat` survey
skills read `## Assets` and `## Worktrees` and degrade to generic defaults
instead, saying so in their own output.

Schema and examples: [`docs/TEMPLATES/SYNAPSE.md`](docs/TEMPLATES/SYNAPSE.md).

## Codex plugin installation

The repository also contains the Codex package manifest at
`.codex-plugin/plugin.json` and Codex root guidance in `AGENTS.md`. The
registered Codex agents live under `.codex/agents/synapse/`.

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
.codex-plugin/plugin.json       Codex plugin manifest
.codex/agents/synapse/          Codex agent registrations
agents/                         Claude-compatible agent adapters
commands/                       Claude-compatible commands
automations/                    Bandaid automations (claude/ live, cursor/ frozen)
docs/                           templates and design history
AGENTS.md                       Codex root guidance
CLAUDE.md                       Claude-compatible root guidance
```
